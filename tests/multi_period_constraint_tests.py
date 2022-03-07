# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/constraint_tests.py

SPDX-License-Identifier: MIT
"""

import logging
import re
from difflib import unified_diff
from os import path as ospath

import pandas as pd
import pytest
from nose.tools import eq_
from oemof.network.network import Node

from oemof import solph

logging.disable(logging.INFO)


class TestsMultiPeriodConstraint:
    @classmethod
    def setup_class(cls):
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        timeindex1 = pd.date_range("1/1/2012", periods=2, freq="H")
        timeindex2 = pd.date_range("1/1/2013", periods=2, freq="H")
        timeindex3 = pd.date_range("1/1/2014", periods=2, freq="H")
        cls.date_time_index = timeindex1.append(timeindex2).append(timeindex3)

        cls.tmppath = solph.helpers.extend_basic_path("tmp")
        logging.info(cls.tmppath)

    def setup(self):
        self.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeindex=self.date_time_index,
            timeincrement=[1] * len(self.date_time_index),
            multi_period=True,
        )
        Node.registry = self.energysystem

    def get_om(self):
        return solph.Model(
            self.energysystem, timeindex=self.energysystem.timeindex
        )

    def compare_lp_files(self, filename, ignored=None, my_om=None):
        r"""Compare lp-files to check constraints generated within solph.

        An lp-file is being generated automatically when the tests are
        executed. Make sure that you create an empty file first and
        transfer the content from the one that has been created automatically
        into this one afterwards. Please ensure that the content is being
        checked carefully. Otherwise, errors are included within the code base.
        """
        if my_om is None:
            om = self.get_om()
        else:
            om = my_om
        tmp_filename = filename.replace(".lp", "") + "_tmp.lp"
        new_filename = ospath.join(self.tmppath, tmp_filename)
        om.write(new_filename, io_options={"symbolic_solver_labels": True})
        logging.info("Comparing with file: {0}".format(filename))
        with open(ospath.join(self.tmppath, tmp_filename)) as generated_file:
            with open(
                ospath.join(
                    ospath.dirname(ospath.realpath(__file__)),
                    "lp_files",
                    filename,
                )
            ) as expected_file:

                def chop_trailing_whitespace(lines):
                    return [re.sub(r"\s*$", "", ln) for ln in lines]

                def remove(pattern, lines):
                    if not pattern:
                        return lines
                    return re.subn(pattern, "", "\n".join(lines))[0].split(
                        "\n"
                    )

                expected = remove(
                    ignored,
                    chop_trailing_whitespace(expected_file.readlines()),
                )
                generated = remove(
                    ignored,
                    chop_trailing_whitespace(generated_file.readlines()),
                )

                def normalize_to_positive_results(lines):
                    negative_result_indices = [
                        n
                        for n, line in enumerate(lines)
                        if re.match("^= -", line)
                    ]
                    equation_start_indices = [
                        [
                            n
                            for n in reversed(range(0, nri))
                            if re.match(".*:$", lines[n])
                        ][0]
                        + 1
                        for nri in negative_result_indices
                    ]
                    for (start, end) in zip(
                        equation_start_indices, negative_result_indices
                    ):
                        for n in range(start, end):
                            lines[n] = (
                                "-"
                                if lines[n] and lines[n][0] == "+"
                                else "+"
                                if lines[n]
                                else lines[n]
                            ) + lines[n][1:]
                        lines[end] = "= " + lines[end][3:]
                    return lines

                expected = normalize_to_positive_results(expected)
                generated = normalize_to_positive_results(generated)

                eq_(
                    generated,
                    expected,
                    "Failed matching expected with generated lp file:\n"
                    + "\n".join(
                        unified_diff(
                            expected,
                            generated,
                            fromfile=ospath.relpath(expected_file.name),
                            tofile=ospath.basename(generated_file.name),
                            lineterm="",
                        )
                    ),
                )

    def test_emission_budget_limit(self):
        """Test emissions budget limit constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    emission_factor=[0.5, -1.0, 2.0, 1.0, 0.5, 0.5],
                )
            },
        )
        solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(nominal_value=100, emission_factor=3.5)
            },
        )

        # Should be ignored because the emission attribute is not defined.
        solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )

        om = self.get_om()

        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_budget_limit.lp", my_om=om)

    def test_periodical_emission_limit(self):
        """Test periodical emissions constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    emission_factor=[0.5, -1.0, 2.0, 1.0, 0.5, 0.5],
                )
            },
        )
        solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(nominal_value=100, emission_factor=3.5)
            },
        )

        # Should be ignored because the emission attribute is not defined.
        solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )

        om = self.get_om()

        solph.constraints.emission_limit_per_period(om, limit=222)

        self.compare_lp_files("periodical_emission_limit.lp", my_om=om)

    def test_periodical_emission_limit_missing_limit(self):
        """Test error for periodical emissions constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    emission_factor=[0.5, -1.0, 2.0, 1.0, 0.5, 0.5],
                )
            },
        )
        solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(nominal_value=100, emission_factor=3.5)
            },
        )

        # Should be ignored because the emission attribute is not defined.
        solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )

        om = self.get_om()

        msg = (
            "You have to provide a limit for each period!\n"
            "If you provide a scalar value, this will be applied as a "
            "limit for each period."
        )
        with pytest.raises(ValueError, match=msg):
            solph.constraints.emission_limit_per_period(om, limit=None)

    def test_linear_transformer(self):
        """Constraint test of a Transformer without Investment."""
        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        solph.components.Transformer(
            label="powerplantGas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(nominal_value=10e10, variable_costs=50)
            },
            conversion_factors={bel: 0.58},
        )

        self.compare_lp_files("linear_transformer_multi_period.lp")

    def test_linear_transformer_invest(self):
        """Constraint test of a Transformer with Investment."""

        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        solph.components.Transformer(
            label="powerplant_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    investment=solph.Investment(
                        existing=50,
                        maximum=1000,
                        overall_maximum=10000,
                        overall_minimum=200,
                        ep_costs=20,
                        age=5,
                        lifetime=40,
                    ),
                )
            },
            conversion_factors={bel: 0.58},
        )

        self.compare_lp_files("linear_transformer_invest_multi_period.lp")

    def test_linear_transformer_invest_old_capacity(self):
        """Constraint test of a Transformer with Investment."""

        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        solph.components.Transformer(
            label="powerplant_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    investment=solph.Investment(
                        existing=50,
                        maximum=1000,
                        overall_maximum=10000,
                        overall_minimum=200,
                        ep_costs=20,
                        age=1,
                        lifetime=2,
                    ),
                )
            },
            conversion_factors={bel: 0.58},
        )

        self.compare_lp_files("linear_transformer_invest_multi_period_old.lp")

    def test_max_source_min_sink(self):
        """Test source with max, sink with min"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=54, max=(0.85, 0.95, 0.61, 0.72, 0.99, 0.1)
                )
            },
        )

        solph.components.Sink(
            label="minDemand",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=54,
                    min=(0.84, 0.94, 0.59, 0.7, 0.97, 0.09),
                    variable_costs=14,
                )
            },
        )

        self.compare_lp_files("max_source_min_sink_multi_period.lp")

    def test_fixed_source_variable_sink(self):
        """Constraint test with a fixed source and a variable sink."""

        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=[0.43, 0.72, 0.29, 0.33, 0.33, 0.33], nominal_value=1e6
                )
            },
        )

        solph.components.Sink(
            label="excess", inputs={bel: solph.flows.Flow(variable_costs=40)}
        )

        self.compare_lp_files("fixed_source_variable_sink_multi_period.lp")

    def test_nominal_value_to_zero(self):
        """If the nominal value is set to zero nothing should happen."""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="s1", outputs={bel: solph.flows.Flow(nominal_value=0)}
        )
        self.compare_lp_files("nominal_value_to_zero_multi_period.lp")

    def test_fixed_source_invest_sink(self):
        """Constraints test for fixed source + invest sink w. `summed_max`"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=[12, 16, 14, 18, 18, 18], nominal_value=1e6
                )
            },
        )

        solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    summed_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    investment=solph.Investment(
                        ep_costs=500, maximum=1e6, existing=50, lifetime=20
                    ),
                )
            },
        )

        self.compare_lp_files("fixed_source_invest_sink_multi_period.lp")

    def test_investment_lifetime_missing(self):
        """Test error raised if lifetime attribute is missing"""
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    max=0.8,
                    investment=solph.Investment(
                        ep_costs=500, maximum=1e6, existing=50
                    ),
                )
            },
        )

        msg = (
            "You have to specify a lifetime "
            "for an InvestmentFlow in a multi-period model!"
        )
        with pytest.raises(ValueError, match=msg):
            self.get_om()

    def test_invest_source_fixed_sink(self):
        """Constraint test with a fixed sink and a dispatch invest source."""

        bel = solph.buses.Bus(label="electricityBus")

        solph.components.Source(
            label="pv",
            outputs={
                bel: solph.flows.Flow(
                    max=[45, 83, 65, 67, 33, 96],
                    variable_costs=13,
                    investment=solph.Investment(ep_costs=123, lifetime=25),
                )
            },
        )

        solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    fix=[0.5, 0.8, 0.3, 0.6, 0.7, 0.2], nominal_value=1e5
                )
            },
        )

        self.compare_lp_files("invest_source_fixed_sink_multi_period.lp")

    def test_storage(self):
        """ """
        bel = solph.buses.Bus(label="electricityBus")

        solph.components.GenericStorage(
            label="storage_no_invest",
            inputs={
                bel: solph.flows.Flow(nominal_value=16667, variable_costs=56)
            },
            outputs={
                bel: solph.flows.Flow(nominal_value=16667, variable_costs=24)
            },
            nominal_storage_capacity=1e5,
            loss_rate=0.13,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            initial_storage_level=0.4,
        )

        self.compare_lp_files("storage_multi_period.lp")
