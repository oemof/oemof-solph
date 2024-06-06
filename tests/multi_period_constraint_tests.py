# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/constraint_tests.py

SPDX-License-Identifier: MIT
"""

import logging
import re
from os import path as ospath

import pandas as pd
import pytest
from pyomo.repn.tests.lp_diff import lp_diff

from oemof import solph
from oemof.solph.components._offset_converter import (
    slope_offset_from_nonconvex_output,
)

logging.disable(logging.INFO)


# Warnings about the fature being experimental:
@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'periods' attribute:UserWarning"
)
# Warnings about default parameters beaing used:
@pytest.mark.filterwarnings(
    "ignore:You did not specify an interest rate.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:By default, a discount_rate of 0.02 is used for a multi-period"
    " model.:UserWarning"
)
class TestsMultiPeriodConstraint:
    @classmethod
    def setup_class(cls):
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        timeindex1 = pd.date_range("1/1/2012", periods=2, freq="h")
        timeindex2 = pd.date_range("1/1/2013", periods=2, freq="h")
        timeindex3 = pd.date_range("1/1/2014", periods=2, freq="h")
        cls.date_time_index = timeindex1.append(timeindex2).append(timeindex3)
        cls.periods = [timeindex1, timeindex2, timeindex3]

        cls.tmppath = solph.helpers.extend_basic_path("tmp")
        logging.info(cls.tmppath)

    def setup_method(self):
        self.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeindex=self.date_time_index,
            timeincrement=[1] * len(self.date_time_index),
            infer_last_interval=False,
            periods=self.periods,
        )

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
                exp = expected_file.read()
                gen = generated_file.read()

                # lp_diff returns two arrays of strings with cleaned lp syntax
                # It automatically prints the diff
                exp_diff, gen_diff = lp_diff(exp, gen)

                # sometimes, 0.0 is printed, sometimes 0, harmonise that
                exp_diff = [
                    (line + " ").replace(" 0.0 ", " 0 ") for line in exp_diff
                ]
                gen_diff = [
                    (line + " ").replace(" 0.0 ", " 0 ") for line in gen_diff
                ]

                assert len(exp_diff) == len(gen_diff)

                # Created the LP files do not have a reproducable
                # order of the lines. Thus, we sort the lines.
                for exp, gen in zip(sorted(exp_diff), sorted(gen_diff)):
                    assert (
                        exp == gen
                    ), "Failed matching expected with generated lp file."

    def test_linear_converter(self):
        """Constraint test of a Converter without Investment."""
        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        converter = solph.components.Converter(
            label="powerplantGas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(nominal_value=10e10, variable_costs=50)
            },
            conversion_factors={bel: 0.58},
        )
        self.energysystem.add(bgas, bel, converter)
        self.compare_lp_files("linear_converter_multi_period.lp")

    def test_linear_converter_invest(self):
        """Constraint test of a Converter with Investment."""

        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        converter = solph.components.Converter(
            label="powerplant_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
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
        self.energysystem.add(bgas, bel, converter)
        self.compare_lp_files("linear_converter_invest_multi_period.lp")

    def test_linear_converter_invest_remaining_value(self):
        """Constraint test of a Converter with Investment."""

        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        converter = solph.components.Converter(
            label="powerplant_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
                        existing=50,
                        maximum=1000,
                        overall_maximum=10000,
                        overall_minimum=200,
                        ep_costs=[20, 19, 18],
                        age=5,
                        lifetime=40,
                    ),
                )
            },
            conversion_factors={bel: 0.58},
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bgas, bel, converter)
        self.compare_lp_files(
            "linear_converter_invest_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_linear_converter_invest_old_capacity(self):
        """Constraint test of a Converter with Investment."""

        bgas = solph.buses.Bus(label="gas")

        bel = solph.buses.Bus(label="electricity")

        converter = solph.components.Converter(
            label="powerplant_gas",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
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
        self.energysystem.add(bgas, bel, converter)
        self.compare_lp_files("linear_converter_invest_multi_period_old.lp")

    def test_max_source_min_sink(self):
        """Test source with max, sink with min"""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=54, max=(0.85, 0.95, 0.61, 0.72, 0.99, 0.1)
                )
            },
        )

        sink = solph.components.Sink(
            label="minDemand",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=54,
                    min=(0.84, 0.94, 0.59, 0.7, 0.97, 0.09),
                    variable_costs=14,
                )
            },
        )
        self.energysystem.add(bel, source, sink)
        self.compare_lp_files("max_source_min_sink_multi_period.lp")

    def test_fixed_source_variable_sink(self):
        """Constraint test with a fixed source and a variable sink."""

        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=[0.43, 0.72, 0.29, 0.33, 0.33, 0.33], nominal_value=1e6
                )
            },
        )

        sink = solph.components.Sink(
            label="excess", inputs={bel: solph.flows.Flow(variable_costs=40)}
        )
        self.energysystem.add(bel, source, sink)
        self.compare_lp_files("fixed_source_variable_sink_multi_period.lp")

    def test_nominal_value_to_zero(self):
        """If the nominal value is set to zero nothing should happen."""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="s1", outputs={bel: solph.flows.Flow(nominal_value=0)}
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("nominal_value_to_zero_multi_period.lp")

    def test_fixed_source_invest_sink(self):
        """Constraints test for fixed source + invest sink w.
        `full_load_time_max`"""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=[12, 16, 14, 18, 18, 18], nominal_value=1e6
                )
            },
        )

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500, maximum=1e6, existing=50, lifetime=20
                    ),
                )
            },
        )
        self.energysystem.add(bel, source, sink)
        self.compare_lp_files("fixed_source_invest_sink_multi_period.lp")

    def test_investment_lifetime_missing(self):
        """Test error raised if lifetime attribute is missing"""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500, maximum=1e6, existing=50
                    ),
                )
            },
        )
        self.energysystem.add(bel, sink)
        msg = (
            "You have to specify a lifetime "
            "for a Flow with an associated investment "
            "object in a multi-period model!"
        )
        with pytest.raises(ValueError, match=msg):
            self.get_om()

    def test_invest_source_fixed_sink(self):
        """Constraint test with a fixed sink and a dispatch invest source."""

        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="pv",
            outputs={
                bel: solph.flows.Flow(
                    max=[45, 83, 65, 67, 33, 96],
                    variable_costs=13,
                    nominal_value=solph.Investment(ep_costs=123, lifetime=25),
                )
            },
        )

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    fix=[0.5, 0.8, 0.3, 0.6, 0.7, 0.2], nominal_value=1e5
                )
            },
        )
        self.energysystem.add(bel, source, sink)
        self.compare_lp_files("invest_source_fixed_sink_multi_period.lp")

    def test_storage(self):
        """ """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
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
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_multi_period.lp")

    def test_storage_invest_1(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            lifetime_inflow=20,
            lifetime_outflow=20,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                maximum=234,
                lifetime=20,
                interest_rate=0.05,
                overall_maximum=1000,
                overall_minimum=2,
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_1_multi_period.lp")

    def test_storage_invest_1_remaining_value(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            lifetime_inflow=20,
            lifetime_outflow=20,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            nominal_storage_capacity=solph.Investment(
                ep_costs=[145, 130, 115],
                maximum=234,
                lifetime=20,
                interest_rate=0.05,
                overall_maximum=1000,
                overall_minimum=2,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bel, storage)
        self.compare_lp_files(
            "storage_invest_1_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_storage_invest_2(self):
        """All can be free extended to their own cost."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage2",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=99, lifetime=20)
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=9, lifetime=20)
                )
            },
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, lifetime=20, existing=20, age=19
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_2_multi_period.lp")

    def test_storage_invest_3(self):
        """The storage capacity is fixed, but the Flows can be extended.
        e.g. PHES with a fixed basin but the pump and the turbine can be
        adapted
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage3",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        ep_costs=99,
                        lifetime=2,
                        age=1,
                        existing=10,
                    )
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=9, lifetime=20)
                )
            },
            nominal_storage_capacity=5000,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_3_multi_period.lp")

    def test_storage_invest_4(self):
        """Only the storage capacity can be extended."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage4",
            inputs={bel: solph.flows.Flow(nominal_value=80)},
            outputs={bel: solph.flows.Flow(nominal_value=100)},
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, maximum=500, lifetime=2, age=1, existing=100
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_4_multi_period.lp")

    def test_storage_invest_5(self):
        """The storage capacity is fixed, but the Flows can be extended.
        e.g. PHES with a fixed basin but the pump and the turbine can be
        adapted. The installed capacity of the pump is 10 % bigger than the
        the capacity of the turbine due to 'invest_relation_input_output=1.1'.
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage5",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        ep_costs=99, existing=110, lifetime=20
                    )
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(existing=100, lifetime=20)
                )
            },
            invest_relation_input_output=1.1,
            nominal_storage_capacity=10000,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_5_multi_period.lp")

    def test_storage_invest_6(self):
        """Like test_storage_invest_5 but there can also be an investment in
        the basin.
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage6",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        ep_costs=99, existing=110, lifetime=20
                    )
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(existing=100, lifetime=20)
                )
            },
            invest_relation_input_output=1.1,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, existing=1000, lifetime=20, age=17
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_6_multi_period.lp")

    def test_storage_minimum_invest(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, minimum=100, maximum=200, lifetime=40
            ),
            lifetime_inflow=40,
            lifetime_outflow=40,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_minimum_multi_period.lp")

    def test_storage_invest_multi_period(self):
        """Test multi-period attributes such as age, fixed_costs, ..."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                minimum=100,
                maximum=200,
                lifetime=40,
                existing=50,
                age=39,
                overall_minimum=10,
                overall_maximum=500,
                fixed_costs=5,
            ),
            lifetime_inflow=40,
            lifetime_outflow=40,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_multi_period.lp")

    def test_storage_unbalanced(self):
        """Testing a unbalanced storage (e.g. battery)."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow()},
            nominal_storage_capacity=1111,
            initial_storage_level=None,
            balanced=False,
            invest_relation_input_capacity=1,
            invest_relation_output_capacity=1,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_unbalanced_multi_period.lp")

    def test_storage_fixed_losses(self):
        """ """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage_no_invest",
            inputs={
                bel: solph.flows.Flow(nominal_value=16667, variable_costs=56)
            },
            outputs={
                bel: solph.flows.Flow(nominal_value=16667, variable_costs=24)
            },
            nominal_storage_capacity=1e5,
            loss_rate=0.13,
            fixed_losses_relative=0.01,
            fixed_losses_absolute=3,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            initial_storage_level=0.4,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_fixed_losses_multi_period.lp")

    def test_storage_invest_1_fixed_losses(self):
        """Test error for fixed losses"""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            fixed_losses_relative=0.01,
            fixed_losses_absolute=3,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=40,
            lifetime_outflow=40,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                minimum=1,
                maximum=234,
                lifetime=20,
                interest_rate=0.05,
                overall_maximum=1000,
                overall_minimum=2,
            ),
        )
        self.energysystem.add(bel, storage)
        msg = (
            "For a multi-period investment model, fixed absolute"
            " losses are not supported. Please remove parameter."
        )
        with pytest.raises(ValueError, match=msg):
            self.get_om()

    def test_storage_invest_1_initial_storage_level(self):
        """Test error for initial storage level
        with multi-period investments"""
        bel = solph.buses.Bus(label="electricityBus")
        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=40,
            lifetime_outflow=40,
            initial_storage_level=0.5,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                maximum=234,
                lifetime=20,
                interest_rate=0.05,
                overall_maximum=1000,
                overall_minimum=2,
            ),
        )
        self.energysystem.add(bel, storage)
        msg = (
            "For a multi-period model, initial_storage_level is"
            " not supported.\nIt needs to be removed since it"
            " has no effect.\nstorage_content will be zero,"
            " until there is some usable storage capacity installed."
        )
        with pytest.raises(ValueError, match=msg):
            self.get_om()

    def test_storage_invest_1_missing_lifetime(self):
        """Test error thrown if storage misses necessary lifetime"""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=40,
            lifetime_outflow=40,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                maximum=234,
                interest_rate=0.05,
                overall_maximum=1000,
                overall_minimum=2,
            ),
        )
        self.energysystem.add(bel, storage)
        msg = (
            "You have to specify a lifetime "
            "for a Flow going into or out of a GenericStorage "
            "unit in a multi-period model!"
        )
        with pytest.raises(ValueError, match=msg):
            self.get_om()

    def test_onverter(self):
        """Constraint test of a LinearN1Converter without Investment."""
        bgas = solph.buses.Bus(label="gasBus")
        bbms = solph.buses.Bus(label="biomassBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        trf = solph.components.Converter(
            label="powerplantGasBiomass",
            inputs={bbms: solph.flows.Flow(), bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(variable_costs=50),
                bth: solph.flows.Flow(nominal_value=5e10, variable_costs=20),
            },
            conversion_factors={bgas: 0.4, bbms: 0.1, bel: 0.3, bth: 0.5},
        )
        self.energysystem.add(bgas, bbms, bel, bth, trf)
        self.compare_lp_files("converter_multi_period.lp")

    def test_converter_invest(self):
        """Constraint test of a LinearN1Converter with Investment."""
        bgas = solph.buses.Bus(label="gasBus")
        bcoal = solph.buses.Bus(label="coalBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        trf = solph.components.Converter(
            label="powerplant_gas_coal",
            inputs={bgas: solph.flows.Flow(), bcoal: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
                        maximum=1000,
                        ep_costs=20,
                        lifetime=20,
                        fixed_costs=10,
                    ),
                ),
                bth: solph.flows.Flow(variable_costs=20),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )
        self.energysystem.add(bgas, bcoal, bel, bth, trf)
        self.compare_lp_files("converter_invest_multi_period.lp")

    def test_converter_invest_with_existing(self):
        """Constraint test of a LinearN1Converter with Investment."""
        bgas = solph.buses.Bus(label="gasBus")
        bcoal = solph.buses.Bus(label="coalBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        trf = solph.components.Converter(
            label="powerplant_gas_coal",
            inputs={bgas: solph.flows.Flow(), bcoal: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
                        maximum=1000,
                        ep_costs=20,
                        existing=200,
                        lifetime=2,
                        age=1,
                    ),
                ),
                bth: solph.flows.Flow(variable_costs=20),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )
        self.energysystem.add(bgas, bcoal, bel, bth, trf)
        self.compare_lp_files("converter_invest_with_existing_multi_period.lp")

    def test_linear_converter_chp(self):
        """
        Constraint test of a Converter without Investment (two outputs).
        """
        bgas = solph.buses.Bus(label="gasBus")
        bheat = solph.buses.Bus(label="heatBus")
        bel = solph.buses.Bus(label="electricityBus")

        trf = solph.components.Converter(
            label="CHPpowerplantGas",
            inputs={
                bgas: solph.flows.Flow(nominal_value=1e11, variable_costs=50)
            },
            outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )
        self.energysystem.add(bgas, bheat, bel, trf)
        self.compare_lp_files("linear_converter_chp_multi_period.lp")

    def test_linear_converter_chp_invest(self):
        """Constraint test of a Converter with Investment (two outputs)."""
        bgas = solph.buses.Bus(label="gasBus")
        bheat = solph.buses.Bus(label="heatBus")
        bel = solph.buses.Bus(label="electricityBus")

        trf = solph.components.Converter(
            label="chp_powerplant_gas",
            inputs={
                bgas: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
                        maximum=1000, ep_costs=20, lifetime=50
                    ),
                )
            },
            outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )
        self.energysystem.add(bgas, bheat, bel, trf)
        self.compare_lp_files("linear_converter_chp_invest_multi_period.lp")

    def test_variable_chp(self):
        """Test ExctractionTurbineCHP basic functionality"""
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="heatBus")
        bgas = solph.buses.Bus(label="commodityBus")

        chp1 = solph.components.ExtractionTurbineCHP(
            label="variable_chp_gas1",
            inputs={bgas: solph.flows.Flow(nominal_value=100)},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5},
        )

        chp2 = solph.components.ExtractionTurbineCHP(
            label="variable_chp_gas2",
            inputs={bgas: solph.flows.Flow(nominal_value=100)},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5},
        )
        self.energysystem.add(bel, bth, bgas, chp1, chp2)
        self.compare_lp_files("variable_chp_multi_period.lp")

    def test_emission_budget_limit(self):
        """Test emissions budget limit constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={
                        "emission_factor": [0.5, -1.0, 2.0, 1.0, 0.5, 0.5]
                    },
                )
            },
        )
        source2 = solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={"emission_factor": 3.5},
                )
            },
        )

        # Should be ignored because the emission attribute is not defined.
        source3 = solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )
        self.energysystem.add(source1, source2, source3)
        om = self.get_om()

        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_budget_limit.lp", my_om=om)

    def test_periodical_emission_limit(self):
        """Test periodical emissions constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={
                        "emission_factor": [0.5, -1.0, 2.0, 1.0, 0.5, 0.5]
                    },
                )
            },
        )
        source2 = solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={"emission_factor": 3.5},
                )
            },
        )

        # Should be ignored because the emission attribute is not defined.
        source3 = solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )
        self.energysystem.add(source1, source2, source3)
        om = self.get_om()

        solph.constraints.emission_limit_per_period(om, limit=[300, 200, 100])

        self.compare_lp_files("periodical_emission_limit.lp", my_om=om)

    def test_periodical_emission_limit_missing_limit(self):
        """Test error for periodical emissions constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={
                        "emission_factor": [0.5, -1.0, 2.0, 1.0, 0.5, 0.5]
                    },
                )
            },
        )
        source2 = solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={"emission_factor": 3.5},
                )
            },
        )

        # Should be ignored because the emission attribute is not defined.
        source3 = solph.components.Source(
            label="source3", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )
        self.energysystem.add(source1, source2, source3)
        om = self.get_om()

        msg = (
            "You have to provide a limit for each period!\n"
            "If you provide a scalar value, this will be applied as a "
            "limit for each period."
        )
        with pytest.raises(ValueError, match=msg):
            solph.constraints.emission_limit_per_period(om, limit=None)

    def test_flow_count_limit(self):
        """Test limiting the count of nonconvex flows"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_value=100,
                    custom_attributes={"emission_factor": 0.5},
                )
            },
        )
        source2 = solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_value=100,
                    custom_attributes={"emission_factor": 0.5},
                )
            },
        )

        # Should be ignored because emission_factor is not defined.
        source3 = solph.components.Source(
            label="source3",
            outputs={
                bel: solph.flows.Flow(
                    nonconvex=solph.NonConvex(), nominal_value=100
                )
            },
        )

        # Should be ignored because it is not NonConvex.
        source4 = solph.components.Source(
            label="source4",
            outputs={
                bel: solph.flows.Flow(
                    custom_attributes={"emission_factor": 1.5},
                    min=0.3,
                    nominal_value=100,
                )
            },
        )
        self.energysystem.add(source1, source2, source3, source4)
        om = self.get_om()

        # one of the two flows has to be active
        solph.constraints.limit_active_flow_count_by_keyword(
            om, "emission_factor", lower_limit=1, upper_limit=2
        )

        self.compare_lp_files("flow_count_limit_multi_period.lp", my_om=om)

    def test_shared_limit(self):
        """Test an overall limit shared among components"""
        b1 = solph.buses.Bus(label="bus")

        storage1 = solph.components.GenericStorage(
            label="storage1",
            nominal_storage_capacity=5,
            inputs={b1: solph.flows.Flow()},
            outputs={b1: solph.flows.Flow()},
        )
        storage2 = solph.components.GenericStorage(
            label="storage2",
            nominal_storage_capacity=5,
            inputs={b1: solph.flows.Flow()},
            outputs={b1: solph.flows.Flow()},
        )
        self.energysystem.add(b1, storage1, storage2)
        model = self.get_om()

        components = [storage1, storage2]

        solph.constraints.shared_limit(
            model,
            model.GenericStorageBlock.storage_content,
            "limit_storage",
            components,
            [0.5, 1.25],
            upper_limit=7,
        )

        self.compare_lp_files("shared_limit_multi_period.lp", my_om=model)

    def test_equate_variables_constraint(self):
        """Testing the equate_variables function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        storage = solph.components.GenericStorage(
            label="storage",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            lifetime_inflow=3,
            lifetime_outflow=3,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, lifetime=3
            ),
        )
        sink = solph.components.Sink(
            label="Sink",
            inputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=500, lifetime=3)
                )
            },
        )
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=3)
                )
            },
        )
        self.energysystem.add(bus1, storage, sink, source)
        om = self.get_om()
        solph.constraints.equate_variables(
            om,
            om.InvestmentFlowBlock.invest[source, bus1, 0],
            om.InvestmentFlowBlock.invest[bus1, sink, 0],
            2,
        )
        solph.constraints.equate_variables(
            om,
            om.InvestmentFlowBlock.invest[source, bus1, 0],
            om.GenericInvestmentStorageBlock.invest[storage, 0],
        )

        self.compare_lp_files("connect_investment_multi_period.lp", my_om=om)

    def test_gradient(self):
        """Testing gradient constraints"""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="powerplant",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=999,
                    variable_costs=23,
                    positive_gradient_limit=0.03,
                    negative_gradient_limit=0.05,
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("source_with_gradient_multi_period.lp")

    def test_nonconvex_gradient(self):
        """Testing gradient constraints"""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="powerplant",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=999,
                    variable_costs=23,
                    nonconvex=solph.NonConvex(
                        positive_gradient_limit=0.03,
                        negative_gradient_limit=0.05,
                    ),
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("source_with_nonconvex_gradient_multi_period.lp")

    def test_periodical_investment_limit(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        storage = solph.components.GenericStorage(
            label="storage_invest_limit",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, lifetime=30
            ),
        )
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=100)
                )
            },
        )
        self.energysystem.add(bus1, storage, source)
        om = self.get_om()
        solph.constraints.investment_limit_per_period(
            om, limit=[500, 400, 300]
        )

        self.compare_lp_files("periodical_investment_limit.lp", my_om=om)

    def test_periodical_investment_limit_with_dsm1(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=100)
                )
            },
        )
        sinkdsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_DIW",
            approach="DIW",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            max_demand=1,
            delay_time=1,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=2,
                overall_maximum=1000,
                overall_minimum=200,
            ),
        )
        self.energysystem.add(bus1, source, sinkdsm)
        om = self.get_om()
        solph.constraints.investment_limit_per_period(
            om, limit=[400, 300, 200]
        )

        self.compare_lp_files(
            "periodical_investment_limit_with_dsm_DIW.lp", my_om=om
        )

    def test_periodical_investment_limit_with_dsm2(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=100)
                )
            },
        )
        sinkdsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_DLR",
            approach="DLR",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            max_demand=1,
            delay_time=1,
            shift_time=1,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=2,
                overall_maximum=1000,
                overall_minimum=200,
            ),
        )
        self.energysystem.add(bus1, source, sinkdsm)
        om = self.get_om()
        solph.constraints.investment_limit_per_period(
            om, limit=[400, 300, 200]
        )

        self.compare_lp_files(
            "periodical_investment_limit_with_dsm_DLR.lp", my_om=om
        )

    def test_periodical_investment_limit_with_dsm3(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=100)
                )
            },
        )
        sinkdsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_oemof",
            approach="oemof",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            max_demand=1,
            delay_time=1,
            shift_interval=2,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=2,
                overall_maximum=1000,
                overall_minimum=200,
            ),
        )
        self.energysystem.add(bus1, source, sinkdsm)
        om = self.get_om()
        solph.constraints.investment_limit_per_period(
            om, limit=[400, 300, 200]
        )

        self.compare_lp_files(
            "periodical_investment_limit_with_dsm_oemof.lp", my_om=om
        )

    def test_periodical_investment_limit_missing(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        storage = solph.components.GenericStorage(
            label="storage_invest_limit",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, lifetime=30
            ),
        )
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123, lifetime=100)
                )
            },
        )
        self.energysystem.add(bus1, storage, source)
        om = self.get_om()
        msg = "You have to provide an investment limit for each period!"
        with pytest.raises(ValueError, match=msg):
            solph.constraints.investment_limit_per_period(om, limit=None)

    def test_min_max_runtime(self):
        """Testing min and max runtimes for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_T")
        source = solph.components.Source(
            label="cheap_plant_min_down_constraints",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(
                        minimum_downtime=4,
                        minimum_uptime=2,
                        initial_status=1,
                        startup_costs=5,
                        shutdown_costs=7,
                    ),
                )
            },
        )
        self.energysystem.add(bus_t, source)
        self.compare_lp_files("min_max_runtime_multi_period.lp")

    def test_activity_costs(self):
        """Testing activity_costs attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        source = solph.components.Source(
            label="cheap_plant_activity_costs",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(
                        activity_costs=2,
                    ),
                )
            },
        )
        self.energysystem.add(bus_t, source)
        self.compare_lp_files("activity_costs_multi_period.lp")

    def test_inactivity_costs(self):
        """Testing inactivity_costs attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        source = solph.components.Source(
            label="cheap_plant_inactivity_costs",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(
                        inactivity_costs=2,
                    ),
                )
            },
        )
        self.energysystem.add(bus_t, source)
        self.compare_lp_files("inactivity_costs_multi_period.lp")

    def test_piecewise_linear_converter_cc(self):
        """Testing PiecewiseLinearConverter using CC formulation."""
        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="electricityBus")
        pwltf = solph.components.experimental.PiecewiseLinearConverter(
            label="pwltf",
            inputs={
                bgas: solph.flows.Flow(nominal_value=100, variable_costs=1)
            },
            outputs={bel: solph.flows.Flow()},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x**2,
            pw_repn="CC",
        )
        self.energysystem.add(bgas, bel, pwltf)
        self.compare_lp_files("piecewise_linear_converter_cc_multi_period.lp")

    def test_piecewise_linear_converter_dcc(self):
        """Testing PiecewiseLinearConverter using DCC formulation."""
        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="electricityBus")
        pwltf = solph.components.experimental.PiecewiseLinearConverter(
            label="pwltf",
            inputs={
                bgas: solph.flows.Flow(nominal_value=100, variable_costs=1)
            },
            outputs={bel: solph.flows.Flow()},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x**2,
            pw_repn="DCC",
        )
        self.energysystem.add(bgas, bel, pwltf)
        self.compare_lp_files("piecewise_linear_converter_dcc_multi_period.lp")

    def test_maximum_startups(self):
        """Testing maximum_startups attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        source = solph.components.Source(
            label="cheap_plant_maximum_startups",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(maximum_startups=2),
                )
            },
        )
        self.energysystem.add(bus_t, source)
        self.compare_lp_files("maximum_startups_multi_period.lp")

    def test_maximum_shutdowns(self):
        """Testing maximum_shutdowns attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        source = solph.components.Source(
            label="cheap_plant_maximum_shutdowns",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(maximum_shutdowns=2),
                )
            },
        )
        self.energysystem.add(bus_t, source)
        self.compare_lp_files("maximum_shutdowns_multi_period.lp")

    def test_offsetconverter(self):
        """Constraint test of a OffsetOffsetConverter."""
        bgas = solph.buses.Bus(label="gasBus")
        bth = solph.buses.Bus(label="thermalBus")

        min = 0.32
        eta_at_min = 0.7
        eta_at_nom = 0.9

        slope, offset = slope_offset_from_nonconvex_output(
            1, min, eta_at_nom, eta_at_min
        )

        otrf = solph.components.OffsetConverter(
            label="gasboiler",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bth: solph.flows.Flow(
                    nominal_value=100,
                    min=min,
                    nonconvex=solph.NonConvex(),
                )
            },
            conversion_factors={bgas: slope},
            normed_offsets={bgas: offset},
        )
        self.energysystem.add(bgas, bth, otrf)
        self.compare_lp_files("offsetconverter_multi_period.lp")

    def test_dsm_module_DIW(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DIW",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DIW_multi_period.lp")

    def test_dsm_module_DLR(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DLR",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DLR_multi_period.lp")

    def test_dsm_module_oemof(self):
        """Constraint test of SinkDSM with approach=oemof"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            approach="oemof",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            shift_interval=2,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_oemof_multi_period.lp")

    def test_dsm_module_DIW_extended(self):
        """Constraint test of SinkDSM with approach=DLR

        Test all possible parameters and constraints
        """

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8, 0.7, 0.7, 0.7],
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.3, 0.3, 0.4, 0.3, 0.3, 0.3],
            approach="DIW",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            efficiency=0.99,
            recovery_time_shift=2,
            recovery_time_shed=2,
            shed_time=2,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DIW_extended_multi_period.lp")

    def test_dsm_module_DLR_extended(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8, 0.7, 0.7, 0.7],
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.3, 0.3, 0.4, 0.3, 0.3, 0.3],
            approach="DLR",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            efficiency=0.99,
            recovery_time_shed=2,
            ActivateYearLimit=True,
            ActivateDayLimit=True,
            n_yearLimit_shift=100,
            n_yearLimit_shed=50,
            t_dayLimit=3,
            addition=False,
            fixes=False,
            shed_time=2,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DLR_extended_multi_period.lp")

    def test_dsm_module_oemof_extended(self):
        """Constraint test of SinkDSM with approach=oemof"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8, 0.7, 0.7, 0.7],
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.3, 0.3, 0.4, 0.3, 0.3, 0.3],
            approach="oemof",
            shift_interval=2,
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=2,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            efficiency=0.99,
            recovery_time_shed=2,
            shed_time=2,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_oemof_extended_multi_period.lp")

    def test_dsm_module_DIW_invest(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DIW",
            max_demand=[1, 2, 3],
            delay_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DIW_invest_multi_period.lp")

    def test_dsm_module_DIW_invest_remaining_value(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DIW",
            max_demand=[1, 2, 3],
            delay_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=[100, 90, 80],
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files(
            "dsm_module_DIW_invest_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_dsm_module_DLR_invest(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DLR",
            max_demand=[1, 2, 3],
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            n_yearLimit_shed=50,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DLR_invest_multi_period.lp")

    def test_dsm_module_DLR_invest_remaining_value(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach="DLR",
            max_demand=[1, 2, 3],
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            n_yearLimit_shed=50,
            investment=solph.Investment(
                ep_costs=[100, 90, 80],
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files(
            "dsm_module_DLR_invest_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_dsm_module_oemof_invest(self):
        """Constraint test of SinkDSM with approach=oemof and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            approach="oemof",
            max_demand=[1, 2, 3],
            shift_interval=2,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_oemof_invest_multi_period.lp")

    def test_dsm_module_oemof_invest_remaining_value(self):
        """Constraint test of SinkDSM with approach=oemof and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 6,
            capacity_up=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            capacity_down=[0.5, 0.4, 0.5, 0.3, 0.3, 0.3],
            approach="oemof",
            max_demand=[1, 2, 3],
            shift_interval=2,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=[100, 90, 80],
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files(
            "dsm_module_oemof_invest_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_nonconvex_investment_storage_without_offset(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage_non_convex",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=141,
                maximum=244,
                minimum=12,
                nonconvex=True,
                lifetime=20,
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_without_offset_multi_period.lp")

    def test_nonconvex_investment_storage_without_offset_remaining_value(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage_non_convex",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=141,
                maximum=244,
                minimum=12,
                nonconvex=True,
                lifetime=20,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bel, storage)
        self.compare_lp_files(
            "storage_invest_without_offset_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_nonconvex_investment_storage_with_offset(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage_non_convex",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                minimum=19,
                offset=5,
                nonconvex=True,
                maximum=1454,
                lifetime=20,
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_with_offset_multi_period.lp")

    def test_nonconvex_investment_storage_with_offset_remaining_value(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage_non_convex",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            lifetime_inflow=20,
            lifetime_outflow=20,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                minimum=19,
                offset=5,
                nonconvex=True,
                maximum=1454,
                lifetime=20,
            ),
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bel, storage)
        self.compare_lp_files(
            "storage_invest_with_offset_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_nonconvex_invest_storage_all_nonconvex(self):
        """All invest variables are free and nonconvex."""
        b1 = solph.buses.Bus(label="bus1")

        storage = solph.components.GenericStorage(
            label="storage_all_nonconvex",
            inputs={
                b1: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        nonconvex=True,
                        minimum=5,
                        offset=10,
                        maximum=30,
                        ep_costs=10,
                        lifetime=20,
                    )
                )
            },
            outputs={
                b1: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        nonconvex=True,
                        minimum=8,
                        offset=15,
                        ep_costs=10,
                        maximum=20,
                        lifetime=20,
                    )
                )
            },
            nominal_storage_capacity=solph.Investment(
                nonconvex=True,
                ep_costs=20,
                offset=30,
                minimum=20,
                maximum=100,
                lifetime=20,
            ),
        )
        self.energysystem.add(b1, storage)
        self.compare_lp_files("storage_invest_all_nonconvex_multi_period.lp")

    def test_nonconvex_invest_sink_without_offset(self):
        """Non convex invest flow without offset, with minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="sink_nonconvex_invest",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        minimum=15,
                        nonconvex=True,
                        maximum=172,
                        lifetime=20,
                    ),
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("flow_invest_without_offset_multi_period.lp")

    def test_nonconvex_invest_sink_without_offset_remaining_value(self):
        """Non convex invest flow without offset, with minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="sink_nonconvex_invest",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        minimum=15,
                        nonconvex=True,
                        maximum=172,
                        lifetime=20,
                    ),
                )
            },
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bel, sink)
        self.compare_lp_files(
            "flow_invest_without_offset_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_nonconvex_invest_source_with_offset(self):
        """Non convex invest flow with offset, with minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="source_nonconvex_invest",
            outputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        minimum=15,
                        maximum=20,
                        offset=34,
                        nonconvex=True,
                        lifetime=20,
                    ),
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("flow_invest_with_offset_multi_period.lp")

    def test_nonconvex_invest_source_with_offset_remaining_value(self):
        """Non convex invest flow with offset, with minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="source_nonconvex_invest",
            outputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        minimum=15,
                        maximum=20,
                        offset=34,
                        nonconvex=True,
                        lifetime=20,
                    ),
                )
            },
        )
        self.energysystem.use_remaining_value = True
        self.energysystem.add(bel, source)
        self.compare_lp_files(
            "flow_invest_with_offset_multi_period_remaining_value.lp"
        )
        self.energysystem.use_remaining_value = False

    def test_nonconvex_invest_source_with_offset_no_minimum(self):
        """Non convex invest flow with offset, without minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="source_nonconvex_invest",
            outputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        maximum=1234,
                        offset=34,
                        nonconvex=True,
                        lifetime=20,
                    ),
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files(
            "flow_invest_with_offset_no_minimum_multi_period.lp"
        )

    def test_summed_min_max_source(self):
        """Test sink with full_load_time_min and _max attribute"""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_min=3,
                    full_load_time_max=100,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=10,
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("summed_min_source_multi_period.lp")

    def test_flow_reaching_lifetime(self):
        """Test flow forced to zero once exceeding its lifetime"""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    variable_costs=25, max=0.8, nominal_value=10, lifetime=2
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("flow_reaching_lifetime.lp")

    def test_flow_reaching_lifetime_initial_age(self):
        """Test flow forced to zero once exceeding its lifetime with age"""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    variable_costs=25,
                    max=0.8,
                    nominal_value=10,
                    lifetime=2,
                    age=1,
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("flow_reaching_lifetime_initial_age.lp")

    @pytest.mark.filterwarnings(
        "ignore:Be aware that the fixed costs attribute is only:UserWarning"
    )
    def test_fixed_costs(self):
        """Test fixed_cost attribute for different kinds of flows"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="pv_forever",
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=25, max=0.8, nominal_value=10, fixed_costs=3
                )
            },
        )

        source2 = solph.components.Source(
            label="pv_with_lifetime",
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=25,
                    max=0.8,
                    nominal_value=10,
                    fixed_costs=3,
                    lifetime=20,
                )
            },
        )

        source3 = solph.components.Source(
            label="pv_with_lifetime_and_age",
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=25,
                    max=0.8,
                    nominal_value=10,
                    fixed_costs=3,
                    lifetime=20,
                    age=18,
                )
            },
        )
        self.energysystem.add(bel, source1, source2, source3)
        self.compare_lp_files("fixed_costs_sources.lp")

    def test_multi_period_varying_period_length(self):
        """Test multi period with varying period length"""

        # Define starting years of investment periods
        years = [2000, 2020, 2035, 2045, 2050, 2060, 2075, 2095]

        # Create a list of timeindex for each period
        periods = [
            pd.date_range(f"1/1/{i}", periods=3, freq="h") for i in years
        ]

        # Create an overall timeindex
        timeindex = pd.concat(
            [pd.Series(index=i, dtype="float64") for i in periods]
        ).index

        # Create an energy system
        es = solph.EnergySystem(
            timeindex=timeindex,
            timeincrement=[1] * len(timeindex),
            periods=periods,
            infer_last_interval=False,
        )

        # Create buses
        bel = solph.Bus(label="electricity", balanced=True)

        # Create a storage
        storage = solph.components.GenericStorage(
            label="storage",
            inputs={
                bel: solph.Flow(
                    variable_costs=0,
                    nominal_value=solph.Investment(
                        ep_costs=10,
                        existing=0,
                        lifetime=20,
                        age=0,
                        interest_rate=0.02,
                    ),
                )
            },
            outputs={
                bel: solph.Flow(
                    variable_costs=0,
                    nominal_value=solph.Investment(
                        ep_costs=10,
                        existing=0,
                        lifetime=20,
                        age=0,
                        interest_rate=0.02,
                    ),
                )
            },
            loss_rate=0.00,
            invest_relation_output_capacity=0.2,
            invest_relation_input_output=1,
            # inflow_conversion_factor=1,
            # outflow_conversion_factor=0.8,
            # nominal_storage_capacity=100,
            nominal_storage_capacity=solph.Investment(
                ep_costs=10,
                maximum=float("+inf"),
                existing=0,
                lifetime=20,
                age=0,
                fixed_costs=None,
                interest_rate=0.02,
            ),
        )
        # Create a DSM sink with DIW approach
        sinkdsm_diw = solph.components.experimental.SinkDSM(
            label="demand_dsm_diw",
            inputs={bel: solph.flows.Flow()},
            demand=[1] * len(timeindex),
            capacity_up=[0.5] * len(timeindex),
            capacity_down=[0.5] * len(timeindex),
            approach="DIW",
            max_demand=[1] * len(timeindex),
            delay_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=100,
                minimum=33,
                maximum=100,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )

        # Create a DSM sink with DLR approach
        sinkdsm_dlr = solph.components.experimental.SinkDSM(
            label="demand_dsm_dlr",
            inputs={bel: solph.flows.Flow()},
            demand=[1] * len(timeindex),
            capacity_up=[0.5] * len(timeindex),
            capacity_down=[0.5] * len(timeindex),
            approach="DLR",
            max_demand=[1] * len(timeindex),
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            n_yearLimit_shed=50,
            investment=solph.Investment(
                ep_costs=100,
                minimum=33,
                maximum=100,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )

        # Create a DSM sink with oemof approach
        sinkdsm_oemof = solph.components.experimental.SinkDSM(
            label="demand_dsm_oemof",
            inputs={bel: solph.flows.Flow()},
            demand=[1] * len(timeindex),
            capacity_up=[0.5] * len(timeindex),
            capacity_down=[0.5] * len(timeindex),
            approach="oemof",
            max_demand=[1] * len(timeindex),
            shift_interval=2,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                ep_costs=100,
                existing=50,
                minimum=33,
                maximum=100,
                age=1,
                lifetime=20,
                fixed_costs=20,
                overall_maximum=1000,
                overall_minimum=5,
            ),
        )

        # Add components to the energy system
        es.add(bel, storage, sinkdsm_diw, sinkdsm_dlr, sinkdsm_oemof)

        # Create an optimization problem
        om = solph.Model(es)

        # Compare the lp files
        self.compare_lp_files("multi_period_period_length.lp", my_om=om)
