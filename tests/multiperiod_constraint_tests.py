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
from nose.tools import assert_raises
from nose.tools import eq_
from oemof.network.network import Node

from oemof import solph

logging.disable(logging.INFO)


class TestsConstraintMultiperiod:
    @classmethod
    def setup_class(cls):
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        t_idx_1_Series = pd.Series(
            index=pd.date_range('1/1/2020', periods=2, freq='H'))
        t_idx_2_Series = pd.Series(
            index=pd.date_range('1/1/2030', periods=2, freq='H'))
        t_idx_3_Series = pd.Series(
            index=pd.date_range('1/1/2040', periods=2, freq='H'))

        cls.date_time_index = pd.concat([t_idx_1_Series, t_idx_2_Series,
                                         t_idx_3_Series]).index

        cls.tmppath = solph.helpers.extend_basic_path("tmp")
        logging.info(cls.tmppath)

    def setup(self):
        self.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeindex=self.date_time_index,
            timeincrement=[1] * len(self.date_time_index)
        )
        Node.registry = self.energysystem

    def get_om(self):
        return solph.MultiPeriodModel(
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

    def test_linear_multiperiod_transformer(self):
        """Constraint test of a multiperiod Transformer without Investment."""
        bgas = solph.Bus(label="gas",
                         multiperiod=True)

        bel = solph.Bus(label="electricity",
                        multiperiod=True)

        solph.Transformer(
            label="powerplantGas",
            inputs={bgas: solph.Flow(multiperiod=True)},
            outputs={bel: solph.Flow(nominal_value=10e10,
                                     variable_costs=50,
                                     multiperiod=True)},
            conversion_factors={bel: 0.58},
        )

        self.compare_lp_files("linear_multiperiod_transformer.lp")

    def test_linear_multiperiod_transformer_invest(self):
        """Constraint test of a multiperiod Transformer with Investment."""

        bgas = solph.Bus(label="gas",
                         multiperiod=True)

        bel = solph.Bus(label="electricity",
                        multiperiod=True)

        solph.Transformer(
            label="powerplant_gas",
            inputs={bgas: solph.Flow()},
            outputs={
                bel: solph.Flow(
                    variable_costs=50,
                    multiperiodinvestment=(
                        solph.MultiPeriodInvestment(
                            maximum=1000,
                            ep_costs=500000,
                            lifetime=20)
                    ),
                )
            },
            conversion_factors={bel: 0.58},
        )

        self.compare_lp_files("linear_multiperiod_transformer_invest.lp")

    def test_max_source_min_sink_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="wind",
            outputs={
                bel: solph.Flow(
                    nominal_value=54,
                    max=(0.85, 0.95, 0.61, 0.85, 0.95, 0.61),
                    multiperiod=True
                )
            },
        )

        solph.Sink(
            label="minDemand",
            inputs={
                bel: solph.Flow(
                    nominal_value=54,
                    min=(0.84, 0.94, 0.59, 0.84, 0.94, 0.59),
                    variable_costs=14,
                    multiperiod=True
                )
            },
        )

        self.compare_lp_files("max_source_min_sink_multiperiod.lp")

    def test_fixed_source_variable_sink_multiperiod(self):
        """Constraint test with a fixed source and a variable sink."""

        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="wind",
            outputs={
                bel: solph.Flow(
                    fix=[0.43, 0.72, 0.29, 0.43, 0.72, 0.29],
                    nominal_value=10e5,
                    multiperiod=True
                )
            },
        )

        solph.Sink(label="excess",
                   inputs={bel: solph.Flow(variable_costs=40,
                                           multiperiod=True)})

        self.compare_lp_files("fixed_source_variable_sink_multiperiod.lp")

    def test_nominal_value_to_zero_multiperiod(self):
        """If the nominal value is set to zero nothing should happen."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(label="s1", outputs={bel: solph.Flow(
            nominal_value=0,
            multiperiod=True
        )})
        self.compare_lp_files("nominal_value_to_zero_multiperiod.lp")

    def test_fixed_source_invest_sink_multiperiod(self):
        """Wrong constraints for fixed source + invest sink w. `summed_max`."""

        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="wind",
            outputs={
                bel: solph.Flow(fix=[12, 16, 14, 12, 16, 14],
                                nominal_value=1000000,
                                multiperiod=True)},
        )

        solph.Sink(
            label="excess",
            inputs={
                bel: solph.Flow(
                    summed_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=500, maximum=10e5, existing=50,
                        lifetime=20, age=1
                    ),
                )
            },
        )

        self.compare_lp_files("fixed_source_invest_sink_multiperiod.lp")

    def test_invest_source_fixed_sink_multiperiod(self):
        """Constraint test with a fixed sink and a dispatch invest source."""

        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="pv",
            outputs={
                bel: solph.Flow(
                    max=[45, 83, 65, 45, 83, 65],
                    variable_costs=13,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=123,
                        lifetime=20
                    ),
                )
            },
        )

        solph.Sink(
            label="excess",
            inputs={bel: solph.Flow(fix=[0.5, 0.8, 0.3, 0.5, 0.8, 0.3],
                                    nominal_value=1e5,
                                    multiperiod=True)},
        )

        self.compare_lp_files("invest_source_fixed_sink_multiperiod.lp")

    def test_storage_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage_no_invest",
            inputs={bel: solph.Flow(nominal_value=16667,
                                    variable_costs=56,
                                    multiperiod=True)},
            outputs={bel: solph.Flow(nominal_value=16667,
                                     variable_costs=24,
                                     multiperiod=True)},
            nominal_storage_capacity=10e4,
            loss_rate=0.13,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            initial_storage_level=0.4,
            multiperiod=True
        )

        self.compare_lp_files("storage_multiperiod.lp")

    # TODO: Fix implementation and get test working!
    # def test_storage_invest_1_multiperiod(self):
    #     """All invest variables are coupled. The invest variables of the
    #     Flows
    #     will be created during the initialisation of the storage e.g. battery
    #     """
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storage1",
    #         inputs={bel: solph.Flow(variable_costs=56,
    #                                 multiperiod=True)},
    #         outputs={bel: solph.Flow(variable_costs=24,
    #                                  multiperiod=True)},
    #         nominal_storage_capacity=None,
    #         loss_rate=0.13,
    #         max_storage_level=0.9,
    #         min_storage_level=0.1,
    #         invest_relation_input_capacity=1 / 6,
    #         invest_relation_output_capacity=1 / 6,
    #         inflow_conversion_factor=0.97,
    #         outflow_conversion_factor=0.86,
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=145,
    #             maximum=234,
    #             lifetime=20,
    #             age=10
    #         ),
    #     )
    #
    #     self.compare_lp_files("storage_invest_1_multiperiod.lp")

    def test_storage_invest_2_multiperiod(self):
        """All can be free extended to their own cost."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage2",
            inputs={bel: solph.Flow(
                multiperiodinvestment=solph.MultiPeriodInvestment(
                    ep_costs=99,
                    lifetime=20
                ))},
            outputs={bel: solph.Flow(
                multiperiodinvestment=solph.MultiPeriodInvestment(
                    ep_costs=9,
                    lifetime=20,
                ))},
            multiperiodinvestment=solph.MultiPeriodInvestment(
                ep_costs=145,
                lifetime=20
            ),
            initial_storage_level=0.5,
        )
        self.compare_lp_files("storage_invest_2_multiperiod.lp")

    def test_storage_invest_3_multiperiod(self):
        """The storage capacity is fixed, but the Flows can be extended.
        e.g. PHES with a fixed basin but the pump and the turbine can be
        adapted
        """
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage3",
            inputs={bel: solph.Flow(
                multiperiodinvestment=solph.MultiPeriodInvestment(
                    ep_costs=99,
                    lifetime=20
                ))},
            outputs={bel: solph.Flow(
                multiperiodinvestment=solph.MultiPeriodInvestment(
                    ep_costs=9,
                    lifetime=20
                ))},
            nominal_storage_capacity=5000,
            multiperiod=True
        )
        self.compare_lp_files("storage_invest_3_multiperiod.lp")

    def test_storage_invest_4_multiperiod(self):
        """Only the storage capacity can be extended."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage4",
            inputs={bel: solph.Flow(nominal_value=80,
                                    multiperiod=True)},
            outputs={bel: solph.Flow(nominal_value=100,
                                     multiperiod=True)},
            multiperiodinvestment=solph.MultiPeriodInvestment(
                ep_costs=145,
                maximum=500,
                lifetime=20
            ),
        )
        self.compare_lp_files("storage_invest_4_multiperiod.lp")

    def test_storage_invest_5_multiperiod(self):
        """The storage capacity is fixed, but the Flows can be extended.
        e.g. PHES with a fixed basin but the pump and the turbine can be
        adapted. The installed capacity of the pump is 10 % bigger than the
        the capacity of the turbine due to 'invest_relation_input_output=1.1'.
        """
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage5",
            inputs={
                bel: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=99,
                        existing=110,
                        lifetime=20,
                        age=18
                    )
                )
            },
            outputs={
                bel: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=9,
                        existing=100,
                        lifetime=20,
                        age=18
                    )
                )
            },
            invest_relation_input_output=1.1,
            nominal_storage_capacity=10000,
            multiperiod=True
        )
        self.compare_lp_files("storage_invest_5_multiperiod.lp")

    def test_storage_invest_6_multiperiod(self):
        """Like test_storage_invest_5 but there can also be an investment in
        the basin.
        """
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage6",
            inputs={
                bel: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=99,
                        existing=110,
                        lifetime=20,
                        age=18
                    )
                )
            },
            outputs={
                bel: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=9,
                        existing=100,
                        lifetime=20,
                        age=18
                    )
                )
            },
            invest_relation_input_output=1.1,
            multiperiodinvestment=solph.MultiPeriodInvestment(
                ep_costs=145,
                existing=10000,
                lifetime=40,
                age=39
            ),
        )
        self.compare_lp_files("storage_invest_6_multiperiod.lp")

    def test_storage_minimum_invest_multiperiod(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.Flow(multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True)},
            multiperiodinvestment=solph.MultiPeriodInvestment(
                ep_costs=145, minimum=100, maximum=200, lifetime=20
            ),
        )

        self.compare_lp_files("storage_invest_minimum_multiperiod.lp")

    def test_storage_unbalanced_multiperiod(self):
        """Testing a unbalanced storage (e.g. battery)."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.Flow(multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True)},
            nominal_storage_capacity=1111,
            initial_storage_level=None,
            balanced=False,
            invest_relation_input_capacity=1,
            invest_relation_output_capacity=1,
            multiperiod=True
        )
        self.compare_lp_files("storage_unbalanced_multiperiod.lp")

    # def test_storage_invest_unbalanced_multiperiod(self):
    #     """Testing a unbalanced storage (e.g. battery)."""
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storage1",
    #         inputs={bel: solph.Flow(multiperiod=True)},
    #         outputs={bel: solph.Flow(multiperiod=True)},
    #         nominal_storage_capacity=None,
    #         initial_storage_level=0.5,
    #         balanced=False,
    #         invest_relation_input_capacity=1,
    #         invest_relation_output_capacity=1,
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=145,
    #             lifetime=20
    #         ),
    #     )
    #     self.compare_lp_files("storage_invest_unbalanced_multiperiod.lp")

    def test_storage_fixed_losses_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.components.GenericStorage(
            label="storage_no_invest",
            inputs={bel: solph.Flow(
                nominal_value=16667,
                variable_costs=56,
                multiperiod=True
            )},
            outputs={bel: solph.Flow(
                nominal_value=16667,
                variable_costs=24,
                multiperiod=True
            )},
            nominal_storage_capacity=1e5,
            loss_rate=0.13,
            fixed_losses_relative=0.01,
            fixed_losses_absolute=3,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            initial_storage_level=0.4,
            multiperiod=True
        )

        self.compare_lp_files("storage_fixed_losses_multiperiod.lp")

    # def test_storage_invest_1_fixed_losses_multiperiod(self):
    #     """All invest variables are coupled. The invest variables of the
    #     Flows
    #     will be created during the initialisation of the storage e.g. battery
    #     """
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storage1",
    #         inputs={bel: solph.Flow(variable_costs=56, multiperiod=True)},
    #         outputs={bel: solph.Flow(variable_costs=24, multiperiod=True)},
    #         nominal_storage_capacity=None,
    #         loss_rate=0.13,
    #         fixed_losses_relative=0.01,
    #         fixed_losses_absolute=3,
    #         max_storage_level=0.9,
    #         min_storage_level=0.1,
    #         invest_relation_input_capacity=1 / 6,
    #         invest_relation_output_capacity=1 / 6,
    #         inflow_conversion_factor=0.97,
    #         outflow_conversion_factor=0.86,
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=145,
    #             maximum=234,
    #             lifetime=20
    #         ),
    #     )
    #
    #     self.compare_lp_files("storage_invest_1_fixed_losses_multiperiod.lp")

    def test_transformer_multiperiod(self):
        """Constraint test of a LinearN1Transformer without Investment."""
        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bbms = solph.Bus(label="biomassBus",
                         multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        bth = solph.Bus(label="thermalBus",
                        multiperiod=True)

        solph.Transformer(
            label="powerplantGasCoal",
            inputs={bbms: solph.Flow(multiperiod=True),
                    bgas: solph.Flow(multiperiod=True)},
            outputs={
                bel: solph.Flow(variable_costs=50, multiperiod=True),
                bth: solph.Flow(nominal_value=5e10, variable_costs=20,
                                multiperiod=True),
            },
            conversion_factors={bgas: 0.4, bbms: 0.1, bel: 0.3, bth: 0.5},
        )

        self.compare_lp_files("transformer_multiperiod.lp")

    def test_transformer_invest_multiperiod(self):
        """Constraint test of a LinearN1Transformer with Investment."""

        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bcoal = solph.Bus(label="coalBus",
                          multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        bth = solph.Bus(label="thermalBus",
                        multiperiod=True)

        solph.Transformer(
            label="powerplant_gas_coal",
            inputs={bgas: solph.Flow(multiperiod=True),
                    bcoal: solph.Flow(multiperiod=True)},
            outputs={
                bel: solph.Flow(
                    variable_costs=50,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        maximum=1000,
                        ep_costs=20,
                        lifetime=20
                    ),
                ),
                bth: solph.Flow(variable_costs=20, multiperiod=True),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )

        self.compare_lp_files("transformer_invest_multiperiod.lp")

    def test_transformer_invest_with_existing_multiperiod(self):
        """Constraint test of a LinearN1Transformer with Investment."""

        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bcoal = solph.Bus(label="coalBus",
                          multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        bth = solph.Bus(label="thermalBus",
                        multiperiod=True)

        solph.Transformer(
            label="powerplant_gas_coal",
            inputs={bgas: solph.Flow(multiperiod=True),
                    bcoal: solph.Flow(multiperiod=True)},
            outputs={
                bel: solph.Flow(
                    variable_costs=50,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        overall_maximum=2500,
                        maximum=1000,
                        ep_costs=20,
                        existing=200,
                        lifetime=30,
                        age=27
                    ),
                ),
                bth: solph.Flow(variable_costs=20,
                                multiperiod=True),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )

        self.compare_lp_files(
            "transformer_invest_with_existing_multiperiod.lp"
        )

    def test_linear_transformer_chp_multiperiod(self):
        """
        Constraint test of a Transformer without Investment (two outputs).
        """
        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bheat = solph.Bus(label="heatBus",
                          multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Transformer(
            label="CHPpowerplantGas",
            inputs={bgas: solph.Flow(nominal_value=10e10,
                                     variable_costs=50,
                                     multiperiod=True
                                     )},
            outputs={bel: solph.Flow(multiperiod=True),
                     bheat: solph.Flow(multiperiod=True)},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )

        self.compare_lp_files("linear_transformer_chp_multiperiod.lp")

    def test_linear_transformer_chp_invest_multiperiod(self):
        """Constraint test of a Transformer with Investment (two outputs)."""

        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bheat = solph.Bus(label="heatBus",
                          multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Transformer(
            label="chp_powerplant_gas",
            inputs={
                bgas: solph.Flow(
                    variable_costs=50,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        minimum=100,
                        maximum=1000,
                        ep_costs=20,
                        lifetime=30
                    ),
                )
            },
            outputs={bel: solph.Flow(multiperiod=True),
                     bheat: solph.Flow(multiperiod=True)},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )

        self.compare_lp_files("linear_transformer_chp_invest_multiperiod.lp")

    def test_variable_chp_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        bth = solph.Bus(label="heatBus",
                        multiperiod=True)
        bgas = solph.Bus(label="commodityBus",
                         multiperiod=True)

        solph.components.ExtractionTurbineCHP(
            label="variable_chp_gas1",
            inputs={bgas: solph.Flow(nominal_value=100,
                                     multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True),
                     bth: solph.Flow(multiperiod=True)},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5},
            multiperiod=True
        )

        solph.components.ExtractionTurbineCHP(
            label="variable_chp_gas2",
            inputs={bgas: solph.Flow(nominal_value=100,
                                     multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True),
                     bth: solph.Flow(multiperiod=True)},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5},
            multiperiod=True
        )

        self.compare_lp_files("variable_chp_multiperiod.lp")

    def test_generic_minvest_limit_multiperiod(self):
        """"""
        bus = solph.Bus(label="bus_1",
                        multiperiod=True)

        solph.Source(
            label="source_0",
            outputs={
                bus: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=50,
                        space=4,
                        lifetime=20
                    )
                )
            },
        )

        solph.Source(
            label="source_1",
            outputs={
                bus: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=100,
                        space=1,
                        lifetime=20
                    )
                )
            },
        )

        solph.Source(
            label="source_2",
            outputs={
                bus: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=75,
                        lifetime=20
                    )
                )
            },
        )

        om = self.get_om()

        om = solph.constraints.additional_multiperiodinvestment_flow_limit(
            om, "space", limit=20
        )

        self.compare_lp_files("generic_invest_limit_multiperiod.lp", my_om=om)

    def test_emission_constraints_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="source1",
            outputs={
                bel: solph.Flow(
                    nominal_value=100,
                    emission_factor=[0.5, -1.0, 2.0, 0.5, -1.0, 2.0],
                    multiperiod=True
                )},
        )
        solph.Source(
            label="source2",
            outputs={bel: solph.Flow(
                nominal_value=100,
                emission_factor=3.5,
                multiperiod=True
            )},
        )

        # Should be ignored because the emission attribute is not defined.
        solph.Source(
            label="source3",
            outputs={bel: solph.Flow(
                nominal_value=100,
                multiperiod=True
            )}
        )

        om = self.get_om()

        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_limit_multiperiod.lp", my_om=om)

    # TODO: Fix this! There seems to be a grouping issue
    # def test_flow_count_limit_multiperiod(self):
    #     """"""
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.Source(
    #         label="source1",
    #         outputs={
    #             bel: solph.Flow(
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(),
    #                 nominal_value=100,
    #                 emission_factor=[0.5, -1.0, 2.0, 0.5, -1.0, 2.0]
    #             )
    #         },
    #     )
    #     solph.Source(
    #         label="source2",
    #         outputs={
    #             bel: solph.Flow(
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(),
    #                 nominal_value=100,
    #                 emission_factor=3.5
    #             )
    #         },
    #     )
    #
    #     # Should be ignored because emission_factor is not defined.
    #     solph.Source(
    #         label="source3",
    #         outputs={
    #             bel: solph.Flow(
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(),
    #                 nominal_value=100)
    #         },
    #     )
    #
    #     # Should be ignored because it is not NonConvex.
    #     solph.Source(
    #         label="source4",
    #         outputs={
    #             bel: solph.Flow(
    #                 emission_factor=1.5,
    #                 min=0.3,
    #                 nominal_value=100,
    #                 multiperiod=True
    #             )
    #         },
    #     )
    #
    #     om = self.get_om()
    #
    #     # one of the two flows has to be active
    #     solph.constraints.limit_active_flow_count_by_keyword(
    #         om, "emission_factor", lower_limit=1, upper_limit=2
    #     )
    #
    #     self.compare_lp_files("flow_count_limit_multiperiod.lp", my_om=om)

    def test_shared_limit_multiperiod(self):
        """"""
        b1 = solph.Bus(label="bus",
                       multiperiod=True)

        storage1 = solph.components.GenericStorage(
            label="storage1",
            nominal_storage_capacity=5,
            inputs={b1: solph.Flow(multiperiod=True)},
            outputs={b1: solph.Flow(multiperiod=True)},
            multiperiod=True
        )
        storage2 = solph.components.GenericStorage(
            label="storage2",
            nominal_storage_capacity=5,
            inputs={b1: solph.Flow(multiperiod=True)},
            outputs={b1: solph.Flow(multiperiod=True)},
            multiperiod=True
        )

        model = self.get_om()

        components = [storage1, storage2]

        solph.constraints.shared_limit(
            model,
            model.GenericMultiPeriodStorageBlock.storage_content,
            "limit_storage",
            components,
            [0.5, 1.25],
            upper_limit=7,
        )

        self.compare_lp_files("shared_limit_multiperiod.lp", my_om=model)

    def test_flow_without_emission_for_emission_constraint_multiperiod(self):
        """"""

        def define_emission_limit():
            bel = solph.Bus(label="electricityBus",
                            multiperiod=True)
            solph.Source(
                label="source1",
                outputs={
                    bel: solph.Flow(nominal_value=100, emission_factor=0.8,
                                    multiperiod=True)
                },
            )
            solph.Source(
                label="source2", outputs={bel: solph.Flow(nominal_value=100,
                                                          multiperiod=True)}
            )
            om = self.get_om()
            solph.constraints.emission_limit(om, om.flows, limit=777)

        assert_raises(AttributeError, define_emission_limit)

    def test_flow_wo_emission_for_emission_constraint_noerr_multiperiod(self):
        """"""
        bel = solph.Bus(label="electricityBus",
                        multieriod=True)
        solph.Source(
            label="source1",
            outputs={bel: solph.Flow(nominal_value=100, emission_factor=0.8,
                                     multiperiod=True)},
        )
        solph.Source(
            label="source2", outputs={bel: solph.Flow(nominal_value=100,
                                                      multiperiod=True)}
        )
        om = self.get_om()
        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_limit_multiperiod_2.lp", my_om=om)

    # TODO: Fix storage issue
    # def test_equate_variables_constraint_multiperiod(self):
    #     """Testing the equate_variables function in the constraint module."""
    #     bus1 = solph.Bus(label="Bus1",
    #                      multiperiod=True)
    #     storage = solph.components.GenericStorage(
    #         label="storage_constraint",
    #         invest_relation_input_capacity=0.2,
    #         invest_relation_output_capacity=0.2,
    #         inputs={bus1: solph.Flow(multiperiod=True)},
    #         outputs={bus1: solph.Flow(multiperiod=True)},
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=145,
    #             lifetime=20
    #         ),
    #     )
    #     sink = solph.Sink(
    #         label="Sink",
    #         inputs={
    #             bus1: solph.Flow(
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     ep_costs=500,
    #                     lifetime=100
    #                 ))
    #         },
    #     )
    #     source = solph.Source(
    #         label="Source",
    #         outputs={
    #             bus1: solph.Flow(
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     ep_costs=123,
    #                     lifetime=25
    #                 ))
    #         },
    #     )
    #     om = self.get_om()
    #     solph.constraints.equate_variables(
    #         om,
    #         om.MultiPeriodInvestmentFlow.invest[source, bus1, 0],
    #         om.MultiPeriodInvestmentFlow.invest[bus1, sink, 0],
    #         2,
    #     )
    #     solph.constraints.equate_variables(
    #         om,
    #         om.MultiPeriodInvestmentFlow.invest[source, bus1, 0],
    #         om.GenericMultiPeriodInvestmentStorageBlock.invest[storage, 0],
    #     )
    #
    #     self.compare_lp_files("connect_investment_multiperiod.lp", my_om=om)

    def test_integer_flow_multiperiod(self):
        """Testing forcing flows to integer values."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="powerplant",
            outputs={
                bel: solph.Flow(
                    nominal_value=999,
                    variable_costs=23,
                    integer=True,
                    multiperiod=True
                )
            },
        )

        self.compare_lp_files("source_with_integer_flow_multiperiod.lp")

    def test_gradient_multiperiod(self):
        """Testing gradient implementation for convex flows."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="powerplant",
            outputs={
                bel: solph.Flow(
                    nominal_value=999,
                    variable_costs=23,
                    positive_gradient={"ub": 0.03, "costs": 7},
                    negative_gradient={"ub": 0.05, "costs": 8},
                    multiperiod=True
                )
            },
        )

        self.compare_lp_files("source_with_gradient_multiperiod.lp")

    def test_summed_max_min_multiperiod(self):
        """Testing summed max and summed min for convex multiperiod flows."""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)

        solph.Source(
            label="powerplant",
            outputs={
                bel: solph.Flow(
                    nominal_value=999,
                    variable_costs=23,
                    summed_max=100,
                    summed_min=1,
                    multiperiod=True
                )
            },
        )

        self.compare_lp_files("source_with_summed_max_min_multiperiod.lp")

    def test_multiperiodinvestment_limit(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.Bus(label="Bus1",
                         multiperiod=True)
        solph.components.GenericStorage(
            label="storage_invest_limit",
            inputs={bus1: solph.Flow(multiperiod=True)},
            outputs={bus1: solph.Flow(multiperiod=True)},
            multiperiodinvestment=solph.MultiPeriodInvestment(
                ep_costs=145,
                lifetime=20),
        )
        solph.Source(
            label="Source",
            outputs={
                bus1: solph.Flow(
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=123,
                        lifetime=20
                    ))
            },
        )
        om = self.get_om()
        solph.constraints.multiperiodinvestment_limit(om, limit=900)

        self.compare_lp_files("multiperiodinvestment_limit.lp", my_om=om)

    def test_summed_min_investment_multiperiod(self):
        """Testing summed min for investment flows"""
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)

        solph.Transformer(
            label="powerplant",
            inputs={bgas: solph.Flow(multiperiod=True)},
            outputs={
                bel: solph.Flow(
                    variable_costs=23,
                    summed_min=1000,
                    multiperiodinvestment=solph.MultiPeriodInvestment(
                        ep_costs=100,
                        lifetime=40
                    )
                )
            },
        )
        om = self.get_om()

        self.compare_lp_files(
            "transformer_with_summed_min_investment_multiperiod.lp", my_om=om)

    # TODO: Fix this one (see above; NonConvex for multiperiod models)
    # def test_min_max_runtime_multiperiod(self):
    #     """Testing min and max runtimes for nonconvex flows."""
    #     bus_t = solph.Bus(label="Bus_T",
    #                       multiperiod=True)
    #     solph.Source(
    #         label="cheap_plant_min_down_constraints",
    #         outputs={
    #             bus_t: solph.Flow(
    #                 nominal_value=10,
    #                 min=0.5,
    #                 max=1.0,
    #                 variable_costs=10,
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(
    #                     minimum_downtime=4,
    #                     minimum_uptime=2,
    #                     initial_status=2,
    #                     startup_costs=5,
    #                     shutdown_costs=7,
    #                 ),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("min_max_runtime_multiperiod.lp")

    # def test_activity_costs_multiperiod(self):
    #     """Testing activity_costs attribute for nonconvex flows."""
    #     bus_t = solph.Bus(label="Bus_C",
    #                       multiperiod=True)
    #     solph.Source(
    #         label="cheap_plant_activity_costs",
    #         outputs={
    #             bus_t: solph.Flow(
    #                 nominal_value=10,
    #                 min=0.5,
    #                 max=1.0,
    #                 variable_costs=10,
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(
    #                     activity_costs=2),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("activity_costs_multiperiod.lp")

    def test_piecewise_linear_transformer_cc_multiperiod(self):
        """Testing PiecewiseLinearTransformer using CC formulation."""
        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        solph.custom.PiecewiseLinearTransformer(
            label="pwltf",
            inputs={bgas: solph.Flow(nominal_value=100, variable_costs=1,
                                     multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True)},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x ** 2,
            pw_repn="CC",
            multiperiod=True
        )
        self.compare_lp_files("piecewise_linear_transformer_cc_multiperiod.lp")

    def test_piecewise_linear_transformer_dcc_multiperiod(self):
        """Testing PiecewiseLinearTransformer using DCC formulation."""
        bgas = solph.Bus(label="gasBus",
                         multiperiod=True)
        bel = solph.Bus(label="electricityBus",
                        multiperiod=True)
        solph.custom.PiecewiseLinearTransformer(
            label="pwltf",
            inputs={bgas: solph.Flow(nominal_value=100, variable_costs=1,
                                     multiperiod=True)},
            outputs={bel: solph.Flow(multiperiod=True)},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x ** 2,
            pw_repn="DCC",
            multiperiod=True
        )
        self.compare_lp_files(
            "piecewise_linear_transformer_dcc_multiperiod.lp")

    # def test_maximum_startups_multiperiod(self):
    #     """Testing maximum_startups attribute for nonconvex flows."""
    #     bus_t = solph.Bus(label="Bus_C",
    #                       multiperiod=True)
    #     solph.Source(
    #         label="cheap_plant_maximum_startups",
    #         outputs={
    #             bus_t: solph.Flow(
    #                 nominal_value=10,
    #                 min=0.5,
    #                 max=1.0,
    #                 variable_costs=10,
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(
    #                     maximum_startups=2),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("maximum_startups_multiperiod.lp")

    # def test_maximum_shutdowns_multiperiod(self):
    #     """Testing maximum_shutdowns attribute for nonconvex flows."""
    #     bus_t = solph.Bus(label="Bus_C",
    #                       multiperiod=True)
    #     solph.Source(
    #         label="cheap_plant_maximum_shutdowns",
    #         outputs={
    #             bus_t: solph.Flow(
    #                 nominal_value=10,
    #                 min=0.5,
    #                 max=1.0,
    #                 variable_costs=10,
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(
    #                     maximum_shutdowns=2),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("maximum_shutdowns_multiperiod.lp")

    # def test_offsettransformer(self):
    #     """Constraint test of a OffsetTransformer."""
    #     bgas = solph.Bus(label="gasBus",
    #                      multiperiod=True)
    #     bth = solph.Bus(label="thermalBus",
    #                     multiperiod=True)
    #
    #     solph.components.OffsetTransformer(
    #         label="gasboiler",
    #         inputs={
    #             bgas: solph.Flow(
    #                 multiperiodnonconvex=solph.MultiPeriodNonConvex(),
    #                 nominal_value=100,
    #                 min=0.32,
    #             )
    #         },
    #         outputs={bth: solph.Flow(multiperiod=True)},
    #         coefficients=[-17, 0.9],
    #     )
    #
    #     self.compare_lp_files("offsettransformer_multiperiod.lp")

    def test_dsm_module_DIW_multiperiod(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.Bus(label="bus_elec",
                           multiperiod=True)
        solph.custom.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.Flow(multiperiod=True)},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach='DIW',
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
            multiperiod=True
        )
        self.compare_lp_files('dsm_module_DIW_multiperiod.lp')

    def test_dsm_module_DLR_multiperiod(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.Bus(label='bus_elec',
                           multiperiod=True)
        solph.custom.SinkDSM(
            label='demand_dsm',
            inputs={b_elec: solph.Flow(multiperiod=True)},
            demand=[1] * 6,
            capacity_up=[0.5] * 6,
            capacity_down=[0.5] * 6,
            approach='DLR',
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=2,
            shift_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
            multiperiod=True
        )
        self.compare_lp_files('dsm_module_DLR_multiperiod.lp')

    def test_dsm_module_oemof(self):
        """Constraint test of SinkDSM with approach=oemof"""

        b_elec = solph.Bus(label="bus_elec",
                           multiperiod=True)
        solph.custom.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.Flow(multiperiod=True)},
            demand=[1] * 6,
            capacity_up=[0.5, 0.4, 0.5, 0.5, 0.4, 0.5],
            capacity_down=[0.5, 0.4, 0.5, 0.5, 0.4, 0.5],
            approach='oemof',
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            shift_interval=2,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
            multiperiod=True
        )
        self.compare_lp_files('dsm_module_oemof_multiperiod.lp')

    # def test_nonconvex_investment_storage_without_offset_multiperiod(self):
    #     """All invest variables are coupled. The invest variables of the
    #     Flows
    #     will be created during the initialisation of the storage e.g. battery
    #     """
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storage_non_convex",
    #         inputs={bel: solph.Flow(variable_costs=56, multiperiod=True)},
    #         outputs={bel: solph.Flow(variable_costs=24, multiperiod=True)},
    #         nominal_storage_capacity=None,
    #         loss_rate=0.13,
    #         max_storage_level=0.9,
    #         min_storage_level=0.1,
    #         invest_relation_input_capacity=1 / 6,
    #         invest_relation_output_capacity=1 / 6,
    #         inflow_conversion_factor=0.97,
    #         outflow_conversion_factor=0.86,
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=141, maximum=244, minimum=12, nonconvex=True,
    #             lifetime=20
    #         ),
    #     )
    #
    #     self.compare_lp_files("storage_invest_without_offset_multiperiod.lp")
    #
    # def test_nonconvex_investment_storage_with_offset_multiperiod(self):
    #     """All invest variables are coupled. The invest variables of the
    #     Flows
    #     will be created during the initialisation of the storage e.g. battery
    #     """
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storagenon_convex",
    #         inputs={bel: solph.Flow(variable_costs=56, multiperiod=True)},
    #         outputs={bel: solph.Flow(variable_costs=24, multiperiod=True)},
    #         nominal_storage_capacity=None,
    #         loss_rate=0.13,
    #         max_storage_level=0.9,
    #         min_storage_level=0.1,
    #         invest_relation_input_capacity=1 / 6,
    #         invest_relation_output_capacity=1 / 6,
    #         inflow_conversion_factor=0.97,
    #         outflow_conversion_factor=0.86,
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             ep_costs=145,
    #             minimum=19,
    #             offset=5,
    #             nonconvex=True,
    #             maximum=1454,
    #             lifetime=20
    #         ),
    #     )
    #
    #     self.compare_lp_files("storage_invest_with_offset_multiperiod.lp")
    #
    # def test_nonconvex_invest_storage_all_nonconvex_multiperiod(self):
    #     """All invest variables are free and nonconvex."""
    #     b1 = solph.Bus(label="bus1",
    #                    multiperiod=True)
    #
    #     solph.components.GenericStorage(
    #         label="storage_all_nonconvex",
    #         inputs={
    #             b1: solph.Flow(
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     nonconvex=True,
    #                     minimum=5,
    #                     offset=10,
    #                     maximum=30,
    #                     ep_costs=10,
    #                     lifetime=20
    #                 )
    #             )
    #         },
    #         outputs={
    #             b1: solph.Flow(
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     nonconvex=True,
    #                     minimum=8,
    #                     offset=15,
    #                     ep_costs=10,
    #                     maximum=20,
    #                     lifetime=20
    #                 )
    #             )
    #         },
    #         multiperiodinvestment=solph.MultiPeriodInvestment(
    #             nonconvex=True, ep_costs=20, offset=30, minimum=20,
    #             maximum=100, lifetime=20
    #         ),
    #     )
    #
    #     self.compare_lp_files("storage_invest_all_nonconvex_multiperiod.lp")
    #
    # def test_nonconvex_invest_sink_without_offset_multiperiod(self):
    #     """Non convex invest flow without offset, with minimum."""
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.Sink(
    #         label="sink_nonconvex_invest",
    #         inputs={
    #             bel: solph.Flow(
    #                 summed_max=2.3,
    #                 variable_costs=25,
    #                 max=0.8,
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     ep_costs=500, minimum=15, nonconvex=True,
    #                     maximum=172,
    #                     lifetime=20
    #                 ),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("flow_invest_without_offset_multiperiod.lp")
    #
    # def test_nonconvex_invest_source_with_offset_multiperiod(self):
    #     """Non convex invest flow with offset, with minimum."""
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.Source(
    #         label="source_nonconvex_invest",
    #         inputs={
    #             bel: solph.Flow(
    #                 summed_max=2.3,
    #                 variable_costs=25,
    #                 max=0.8,
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     ep_costs=500,
    #                     minimum=15,
    #                     maximum=20,
    #                     offset=34,
    #                     nonconvex=True,
    #                     lifetime=20
    #                 ),
    #             )
    #         },
    #     )
    #     self.compare_lp_files("flow_invest_with_offset_multiperiod.lp")
    #
    # def test_nonconvex_invest_source_with_offset_no_min_multiperiod(self):
    #     """Non convex invest flow with offset, without minimum."""
    #     bel = solph.Bus(label="electricityBus",
    #                     multiperiod=True)
    #
    #     solph.Source(
    #         label="source_nonconvex_invest",
    #         inputs={
    #             bel: solph.Flow(
    #                 summed_max=2.3,
    #                 variable_costs=25,
    #                 max=0.8,
    #                 multiperiodinvestment=solph.MultiPeriodInvestment(
    #                     ep_costs=500, maximum=1234, offset=34,
    #                     nonconvex=True,
    #                     lifetime=20
    #                 ),
    #             )
    #         },
    #     )
    #     self.compare_lp_files(
    #         "flow_invest_with_offset_no_minimum_multiperiod.lp")
