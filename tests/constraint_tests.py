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

logging.disable(logging.INFO)


class TestsConstraint:
    @classmethod
    def setup_class(cls):
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        cls.date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")

        cls.tmppath = solph.helpers.extend_basic_path("tmp")
        logging.info(cls.tmppath)

    def setup_method(self):
        self.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeindex=self.date_time_index,
            infer_last_interval=True,
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
                    line + " ".replace(" 0.0 ", " 0 ") for line in exp_diff
                ]
                gen_diff = [
                    line + " ".replace(" 0.0 ", " 0 ") for line in gen_diff
                ]

                assert len(exp_diff) == len(gen_diff)

                # Created the LP files do not have a reproducible
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

        self.compare_lp_files("linear_converter.lp")

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
                    nominal_value=solph.Investment(maximum=1000, ep_costs=20),
                )
            },
            conversion_factors={bel: 0.58},
        )
        self.energysystem.add(bgas, bel, converter)

        self.compare_lp_files("linear_converter_invest.lp")

    def test_nonconvex_invest_converter(self):
        """Non-convex invest flow with offset, without minimum."""
        bfuel = solph.buses.Bus(label="fuelBus")
        bel = solph.buses.Bus(label="electricityBus")

        converter = solph.components.Converter(
            label="converter_nonconvex_invest",
            inputs={bfuel: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=25,
                    min=0.25,
                    max=0.5,
                    nominal_value=solph.Investment(
                        ep_costs=500,
                        maximum=1234,
                    ),
                    nonconvex=solph.NonConvex(),
                )
            },
            conversion_factors={bel: 0.5},
        )
        self.energysystem.add(bfuel, bel, converter)
        self.compare_lp_files("flow_nonconvex_invest_bounded_converter.lp")

    def test_max_source_min_sink(self):
        """ """
        bel = solph.buses.Bus(label="electricityBus")

        wind = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(nominal_value=54, max=(0.85, 0.95, 0.61))
            },
        )

        demand = solph.components.Sink(
            label="minDemand",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=54, min=(0.84, 0.94, 0.59), variable_costs=14
                )
            },
        )
        self.energysystem.add(bel, wind, demand)
        self.compare_lp_files("max_source_min_sink.lp")

    def test_fixed_source_variable_sink(self):
        """Constraint test with a fixed source and a variable sink."""

        bel = solph.buses.Bus(label="electricityBus")

        wind = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(
                    fix=[0.43, 0.72, 0.29], nominal_value=1e6
                )
            },
        )

        excess = solph.components.Sink(
            label="excess", inputs={bel: solph.flows.Flow(variable_costs=40)}
        )

        self.energysystem.add(bel, wind, excess)
        self.compare_lp_files("fixed_source_variable_sink.lp")

    def test_nominal_value_to_zero(self):
        """If the nominal value is set to zero nothing should happen."""
        bel = solph.buses.Bus(label="electricityBus")

        s1 = solph.components.Source(
            label="s1", outputs={bel: solph.flows.Flow(nominal_value=0)}
        )
        self.energysystem.add(bel, s1)
        self.compare_lp_files("nominal_value_to_zero.lp")

    def test_fixed_source_invest_sink(self):
        """
        Wrong constraints for fixed source + invest sink w.
        `full_load_time_max`.
        """

        bel = solph.buses.Bus(label="electricityBus")

        wind = solph.components.Source(
            label="wind",
            outputs={
                bel: solph.flows.Flow(fix=[12, 16, 14], nominal_value=1e6)
            },
        )

        excess = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500, maximum=1e6, existing=50
                    ),
                )
            },
        )
        self.energysystem.add(bel, wind, excess)
        self.compare_lp_files("fixed_source_invest_sink.lp")

    def test_invest_source_fixed_sink(self):
        """Constraint test with a fixed sink and a dispatch invest source."""

        bel = solph.buses.Bus(label="electricityBus")

        pv = solph.components.Source(
            label="pv",
            outputs={
                bel: solph.flows.Flow(
                    max=[45, 83, 65],
                    variable_costs=13,
                    nominal_value=solph.Investment(ep_costs=123),
                )
            },
        )

        excess = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(fix=[0.5, 0.8, 0.3], nominal_value=1e5)
            },
        )
        self.energysystem.add(bel, pv, excess)
        self.compare_lp_files("invest_source_fixed_sink.lp")

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
            storage_costs=0.1,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            initial_storage_level=0.4,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage.lp")

    def test_storage_invest_1(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow(variable_costs=56)},
            outputs={bel: solph.flows.Flow(variable_costs=24)},
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, maximum=234
            ),
            loss_rate=0.13,
            max_storage_level=0.9,
            min_storage_level=0.1,
            invest_relation_input_capacity=1 / 6,
            invest_relation_output_capacity=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_1.lp")

    def test_storage_invest_2(self):
        """All can be free extended to their own cost."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage2",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=99)
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=9)
                )
            },
            nominal_storage_capacity=solph.Investment(ep_costs=145),
            initial_storage_level=0.5,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_2.lp")

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
                    nominal_value=solph.Investment(ep_costs=99)
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=9)
                )
            },
            nominal_storage_capacity=5000,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_3.lp")

    def test_storage_invest_4(self):
        """Only the storage capacity can be extended."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage4",
            inputs={bel: solph.flows.Flow(nominal_value=80)},
            outputs={bel: solph.flows.Flow(nominal_value=100)},
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, maximum=500
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_4.lp")

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
                    nominal_value=solph.Investment(ep_costs=99, existing=110)
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(existing=100)
                )
            },
            invest_relation_input_output=1.1,
            nominal_storage_capacity=10000,
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_5.lp")

    def test_storage_invest_6(self):
        """Like test_storage_invest_5 but there can also be an investment in
        the basin.
        """
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage6",
            inputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=99, existing=110)
                )
            },
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=solph.Investment(existing=100)
                )
            },
            invest_relation_input_output=1.1,
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, existing=10000
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_6.lp")

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
                ep_costs=145, minimum=100, maximum=200
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_minimum.lp")

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
        self.compare_lp_files("storage_unbalanced.lp")

    def test_storage_invest_unbalanced(self):
        """Testing a unbalanced storage (e.g. battery)."""
        bel = solph.buses.Bus(label="electricityBus")

        storage = solph.components.GenericStorage(
            label="storage1",
            inputs={bel: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow()},
            initial_storage_level=0.5,
            balanced=False,
            invest_relation_input_capacity=1,
            invest_relation_output_capacity=1,
            nominal_storage_capacity=solph.Investment(ep_costs=145),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_unbalanced.lp")

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
        self.compare_lp_files("storage_fixed_losses.lp")

    def test_storage_invest_1_fixed_losses(self):
        """All invest variables are coupled. The invest variables of the Flows
        will be created during the initialisation of the storage e.g. battery
        """
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
            nominal_storage_capacity=solph.Investment(
                ep_costs=145, minimum=1, maximum=234
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_1_fixed_losses.lp")

    def test_converter(self):
        """Constraint test of a LinearN1Converter without Investment."""
        bgas = solph.buses.Bus(label="gasBus")
        bbms = solph.buses.Bus(label="biomassBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        converter = solph.components.Converter(
            label="powerplantGasBiomass",
            inputs={bbms: solph.flows.Flow(), bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(variable_costs=50),
                bth: solph.flows.Flow(nominal_value=5e10, variable_costs=20),
            },
            conversion_factors={bgas: 0.4, bbms: 0.1, bel: 0.3, bth: 0.5},
        )

        self.energysystem.add(bgas, bbms, bel, bth, converter)

        self.compare_lp_files("converter.lp")

    def test_converter_invest(self):
        """Constraint test of a LinearN1Converter with Investment."""

        bgas = solph.buses.Bus(label="gasBus")
        bcoal = solph.buses.Bus(label="coalBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        converter = solph.components.Converter(
            label="powerplant_gas_coal",
            inputs={bgas: solph.flows.Flow(), bcoal: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(maximum=1000, ep_costs=20),
                ),
                bth: solph.flows.Flow(variable_costs=20),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )
        self.energysystem.add(bgas, bcoal, bel, bth, converter)

        self.compare_lp_files("converter_invest.lp")

    def test_converter_invest_with_existing(self):
        """Constraint test of a LinearN1Converter with Investment."""

        bgas = solph.buses.Bus(label="gasBus")
        bcoal = solph.buses.Bus(label="coalBus")
        bel = solph.buses.Bus(label="electricityBus")
        bth = solph.buses.Bus(label="thermalBus")

        converter = solph.components.Converter(
            label="powerplant_gas_coal",
            inputs={bgas: solph.flows.Flow(), bcoal: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(
                        maximum=1000, ep_costs=20, existing=200
                    ),
                ),
                bth: solph.flows.Flow(variable_costs=20),
            },
            conversion_factors={bgas: 0.58, bcoal: 0.2, bel: 0.3, bth: 0.5},
        )
        self.energysystem.add(bgas, bcoal, bel, bth, converter)

        self.compare_lp_files("converter_invest_with_existing.lp")

    def test_linear_converter_chp(self):
        """
        Constraint test of a Converter without Investment (two outputs).
        """
        bgas = solph.buses.Bus(label="gasBus")
        bheat = solph.buses.Bus(label="heatBus")
        bel = solph.buses.Bus(label="electricityBus")

        converter = solph.components.Converter(
            label="CHPpowerplantGas",
            inputs={
                bgas: solph.flows.Flow(nominal_value=1e11, variable_costs=50)
            },
            outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )
        self.energysystem.add(bgas, bheat, bel, converter)

        self.compare_lp_files("linear_converter_chp.lp")

    def test_linear_converter_chp_invest(self):
        """Constraint test of a Converter with Investment (two outputs)."""

        bgas = solph.buses.Bus(label="gasBus")
        bheat = solph.buses.Bus(label="heatBus")
        bel = solph.buses.Bus(label="electricityBus")

        converter = solph.components.Converter(
            label="chp_powerplant_gas",
            inputs={
                bgas: solph.flows.Flow(
                    variable_costs=50,
                    nominal_value=solph.Investment(maximum=1000, ep_costs=20),
                )
            },
            outputs={bel: solph.flows.Flow(), bheat: solph.flows.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5},
        )
        self.energysystem.add(bgas, bheat, bel, converter)

        self.compare_lp_files("linear_converter_chp_invest.lp")

    def test_link(self):
        """Constraint test of a Link."""
        bus_el_1 = solph.buses.Bus(label="el1")
        bus_el_2 = solph.buses.Bus(label="el2")

        link = solph.components.Link(
            label="link",
            inputs={
                bus_el_1: solph.flows.Flow(nominal_value=4),
                bus_el_2: solph.flows.Flow(nominal_value=2),
            },
            outputs={
                bus_el_1: solph.flows.Flow(),
                bus_el_2: solph.flows.Flow(),
            },
            conversion_factors={
                (bus_el_1, bus_el_2): 0.75,
                (bus_el_2, bus_el_1): 0.5,
            },
        )
        self.energysystem.add(bus_el_1, bus_el_2, link)
        self.compare_lp_files("link.lp")

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
        self.compare_lp_files("variable_chp.lp")

    def test_generic_invest_limit(self):
        """Test a generic keyword investment limit"""
        bus = solph.buses.Bus(label="bus_1")

        source_0 = solph.components.Source(
            label="source_0",
            outputs={
                bus: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        ep_costs=50,
                        custom_attributes={"space": 4},
                    )
                )
            },
        )

        source_1 = solph.components.Source(
            label="source_1",
            outputs={
                bus: solph.flows.Flow(
                    nominal_value=solph.Investment(
                        ep_costs=100, custom_attributes={"space": 1}
                    ),
                )
            },
        )

        source_2 = solph.components.Source(
            label="source_2",
            outputs={
                bus: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=75)
                )
            },
        )

        self.energysystem.add(bus, source_0, source_1, source_2)

        om = self.get_om()

        om = solph.constraints.additional_investment_flow_limit(
            om, "space", limit=20
        )

        self.compare_lp_files("generic_invest_limit.lp", my_om=om)

    def test_emission_constraints(self):
        """Test emissions constraint"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={"emission_factor": [0.5, -1.0, 2.0]},
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

        self.energysystem.add(bel, source1, source2, source3)

        om = self.get_om()

        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_limit.lp", my_om=om)

    def test_flow_count_limit(self):
        """Test limiting the count of nonconvex flows"""
        bel = solph.buses.Bus(label="electricityBus")

        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_value=100,
                    custom_attributes={"emission_factor": [0.5, -1.0, 2.0]},
                )
            },
        )
        source2 = solph.components.Source(
            label="source2",
            outputs={
                bel: solph.flows.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_value=100,
                    custom_attributes={"emission_factor": 3.5},
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
                    min=0.3,
                    nominal_value=100,
                    custom_attributes={"emission_factor": 1.5},
                )
            },
        )

        self.energysystem.add(bel, source1, source2, source3, source4)

        om = self.get_om()

        # one of the two flows has to be active
        solph.constraints.limit_active_flow_count_by_keyword(
            om, "emission_factor", lower_limit=1, upper_limit=2
        )

        self.compare_lp_files("flow_count_limit.lp", my_om=om)

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

        self.compare_lp_files("shared_limit.lp", my_om=model)

    def test_flow_without_emission_for_emission_constraint(self):
        """Test AttributeError if passed flow misses emission attribute"""
        with pytest.raises(AttributeError):
            bel = solph.buses.Bus(label="electricityBus")
            source1 = solph.components.Source(
                label="source1",
                outputs={
                    bel: solph.flows.Flow(
                        nominal_value=100,
                        custom_attributes={"emission_factor": 0.8},
                    )
                },
            )
            source2 = solph.components.Source(
                label="source2",
                outputs={bel: solph.flows.Flow(nominal_value=100)},
            )
            self.energysystem.add(bel, source1, source2)
            om = self.get_om()
            solph.constraints.emission_limit(om, om.flows, limit=777)

    def test_flow_without_emission_for_emission_constraint_no_error(self):
        """Test that no error is thrown if no flows are explicitly passed"""
        bel = solph.buses.Bus(label="electricityBus")
        source1 = solph.components.Source(
            label="source1",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    custom_attributes={"emission_factor": 0.8},
                )
            },
        )
        source2 = solph.components.Source(
            label="source2", outputs={bel: solph.flows.Flow(nominal_value=100)}
        )
        self.energysystem.add(bel, source1, source2)
        om = self.get_om()
        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files("emission_limit_no_error.lp", my_om=om)

    def test_equate_variables_constraint(self):
        """Testing the equate_variables function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        storage = solph.components.GenericStorage(
            label="storage",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(ep_costs=145),
        )
        sink = solph.components.Sink(
            label="Sink",
            inputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=500)
                )
            },
        )
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
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

        self.compare_lp_files("connect_investment.lp", my_om=om)

    def test_equate_flows_constraint(self):
        """Testing the equate_flows function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        sink = solph.components.Sink(
            label="Sink",
            inputs={
                bus1: solph.flows.Flow(
                    nominal_value=300,
                    variable_costs=2,
                    custom_attributes={"outgoing_flow": True},
                )
            },
        )
        source1 = solph.components.Source(
            label="Source1",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=400,
                    variable_costs=2,
                    custom_attributes={"incoming_flow": True},
                )
            },
        )
        source2 = solph.components.Source(
            label="Source2",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=200,
                    variable_costs=10,
                    custom_attributes={"incoming_flow": True},
                )
            },
        )
        self.energysystem.add(bus1, sink, source1, source2)
        om = self.get_om()
        solph.constraints.equate_flows_by_keyword(
            om,
            "incoming_flow",
            "outgoing_flow",
            2,
        )
        self.compare_lp_files("equate_flows.lp", my_om=om)

    def test_gradient(self):
        """Testing gradient constraints"""
        bel = solph.buses.Bus(label="electricityBus")

        pp = solph.components.Source(
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
        self.energysystem.add(bel, pp)
        self.compare_lp_files("source_with_gradient.lp")

    def test_nonconvex_gradient(self):
        """Testing gradient constraints"""
        bel = solph.buses.Bus(label="electricityBus")

        pp = solph.components.Source(
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
        self.energysystem.add(bel, pp)
        self.compare_lp_files("source_with_nonconvex_gradient.lp")

    def test_nonconvex_positive_gradient_error(self):
        """Testing nonconvex positive gradient error."""
        msg = (
            "You specified a positive gradient in your nonconvex "
            "option. This cannot be combined with a positive or a "
            "negative gradient for a standard flow!"
        )

        with pytest.raises(ValueError, match=msg):
            solph.flows.Flow(
                nonconvex=solph.NonConvex(
                    positive_gradient_limit=0.03,
                ),
                positive_gradient_limit=0.03,
            )

    def test_nonconvex_negative_gradient_error(self):
        """Testing nonconvex positive gradient error."""
        msg = (
            "You specified a negative gradient in your nonconvex "
            "option. This cannot be combined with a positive or a "
            "negative gradient for a standard flow!"
        )

        with pytest.raises(ValueError, match=msg):
            solph.flows.Flow(
                nonconvex=solph.NonConvex(
                    negative_gradient_limit=0.03,
                ),
                negative_gradient_limit=0.03,
            )

    def test_investment_limit(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        storage = solph.components.GenericStorage(
            label="storage_invest_limit",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(ep_costs=145),
        )
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
                )
            },
        )
        self.energysystem.add(bus1, storage, source)
        om = self.get_om()
        solph.constraints.investment_limit(om, limit=900)

        self.compare_lp_files("investment_limit.lp", my_om=om)

    def test_investment_limit_with_dsm1(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
                )
            },
        )
        dsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_DIW",
            approach="DIW",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            max_demand=[1] * 3,
            delay_time=1,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100, existing=50, minimum=33, maximum=100
            ),
        )
        self.energysystem.add(bus1, source, dsm)
        om = self.get_om()
        solph.constraints.investment_limit(om, limit=900)

        self.compare_lp_files("investment_limit_with_dsm_DIW.lp", my_om=om)

    def test_investment_limit_with_dsm2(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
                )
            },
        )
        dsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_DLR",
            approach="DLR",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            max_demand=[1] * 3,
            delay_time=1,
            shift_time=1,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100, existing=50, minimum=33, maximum=100
            ),
        )
        self.energysystem.add(bus1, source, dsm)
        om = self.get_om()
        solph.constraints.investment_limit(om, limit=900)

        self.compare_lp_files("investment_limit_with_dsm_DLR.lp", my_om=om)

    def test_investment_limit_with_dsm3(self):
        """Testing the investment_limit function in the constraint module."""
        bus1 = solph.buses.Bus(label="Bus1")
        source = solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
                )
            },
        )
        dsm = solph.components.experimental.SinkDSM(
            label="sink_dsm_oemof",
            approach="oemof",
            inputs={bus1: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            max_demand=[1] * 3,
            delay_time=1,
            shift_interval=2,
            cost_dsm_down_shift=0.5,
            cost_dsm_up=0.5,
            shed_eligibility=False,
            investment=solph.Investment(
                ep_costs=100, existing=50, minimum=33, maximum=100
            ),
        )
        self.energysystem.add(bus1, source, dsm)
        om = self.get_om()
        solph.constraints.investment_limit(om, limit=900)

        self.compare_lp_files("investment_limit_with_dsm_oemof.lp", my_om=om)

    def test_investment_limit_per_period_error_no_multi_period(self):
        """Test error being thrown if model is not a multi-period model"""
        bus1 = solph.buses.Bus(label="Bus1")
        solph.components.GenericStorage(
            label="storage_invest_limit",
            invest_relation_input_capacity=0.2,
            invest_relation_output_capacity=0.2,
            inputs={bus1: solph.flows.Flow()},
            outputs={bus1: solph.flows.Flow()},
            nominal_storage_capacity=solph.Investment(ep_costs=145),
        )
        solph.components.Source(
            label="Source",
            outputs={
                bus1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=123)
                )
            },
        )
        om = self.get_om()

        msg = (
            "investment_limit_per_period is only applicable "
            "for multi-period models.\nIn order to create such a model, "
            "explicitly set attribute `periods` of your energy system."
        )
        with pytest.raises(ValueError, match=msg):
            solph.constraints.investment_limit_per_period(om, limit=900)

    def test_min_max_runtime(self):
        """Testing min and max runtimes for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_T")
        pp = solph.components.Source(
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

        self.energysystem.add(bus_t, pp)
        self.compare_lp_files("min_max_runtime.lp")

    def test_activity_costs(self):
        """Testing activity_costs attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        pp = solph.components.Source(
            label="cheap_plant_activity_costs",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(activity_costs=2),
                )
            },
        )

        self.energysystem.add(bus_t, pp)
        self.compare_lp_files("activity_costs.lp")

    def test_inactivity_costs(self):
        """Testing inactivity_costs attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        pp = solph.components.Source(
            label="cheap_plant_inactivity_costs",
            outputs={
                bus_t: solph.flows.Flow(
                    nominal_value=10,
                    min=0.5,
                    max=1.0,
                    variable_costs=10,
                    nonconvex=solph.NonConvex(inactivity_costs=2),
                )
            },
        )

        self.energysystem.add(bus_t, pp)
        self.compare_lp_files("inactivity_costs.lp")

    def test_piecewise_linear_converter_cc(self):
        """Testing PiecewiseLinearConverter using CC formulation."""
        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="electricityBus")

        pwlcw = solph.components.experimental.PiecewiseLinearConverter(
            label="pwltf",
            inputs={
                bgas: solph.flows.Flow(nominal_value=100, variable_costs=1)
            },
            outputs={bel: solph.flows.Flow()},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x**2,
            pw_repn="CC",
        )
        self.energysystem.add(bgas, bel, pwlcw)
        self.compare_lp_files("piecewise_linear_converter_cc.lp")

    def test_piecewise_linear_converter_dcc(self):
        """Testing PiecewiseLinearConverter using DCC formulation."""
        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="electricityBus")

        pwlcw = solph.components.experimental.PiecewiseLinearConverter(
            label="pwltf",
            inputs={
                bgas: solph.flows.Flow(nominal_value=100, variable_costs=1)
            },
            outputs={bel: solph.flows.Flow()},
            in_breakpoints=[0, 25, 50, 75, 100],
            conversion_function=lambda x: x**2,
            pw_repn="DCC",
        )
        self.energysystem.add(bgas, bel, pwlcw)
        self.compare_lp_files("piecewise_linear_converter_dcc.lp")

    def test_maximum_startups(self):
        """Testing maximum_startups attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        pp = solph.components.Source(
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
        self.energysystem.add(bus_t, pp)
        self.compare_lp_files("maximum_startups.lp")

    def test_maximum_shutdowns(self):
        """Testing maximum_shutdowns attribute for nonconvex flows."""
        bus_t = solph.buses.Bus(label="Bus_C")
        pp = solph.components.Source(
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
        self.energysystem.add(bus_t, pp)
        self.compare_lp_files("maximum_shutdowns.lp")

    def test_offsetconverter_nonconvex(self):
        """Constraint test of an OffsetConverter only with NonConvex
        attribute."""
        b_diesel = solph.buses.Bus(label="bus_diesel")
        b_el = solph.buses.Bus(label="bus_electricity")

        min = 0.2
        eta_at_nom = 0.4
        eta_at_min = 0.35

        slope, offset = solph.components.slope_offset_from_nonconvex_output(
            1, min, eta_at_nom, eta_at_min
        )

        diesel_genset = solph.components.OffsetConverter(
            label="diesel_genset",
            inputs={
                b_diesel: solph.flows.Flow(),
            },
            outputs={
                b_el: solph.flows.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_value=100,
                    min=min,
                )
            },
            conversion_factors={b_diesel: slope},
            normed_offsets={b_diesel: offset},
        )
        self.energysystem.add(b_diesel, b_el, diesel_genset)

        self.compare_lp_files("offsetconverter_nonconvex.lp")

    def test_offsetconverter_nonconvex_investment(self):
        """Constraint test of an OffsetConverter with both NonConvex and
        Investment attributes."""
        b_diesel = solph.buses.Bus(label="bus_diesel")
        b_el = solph.buses.Bus(label="bus_electricity")

        min = 0.2
        eta_at_nom = 0.4
        eta_at_min = 0.35

        slope, offset = solph.components.slope_offset_from_nonconvex_output(
            1, min, eta_at_nom, eta_at_min
        )

        diesel_genset = solph.components.OffsetConverter(
            label="diesel_genset",
            inputs={b_diesel: solph.flows.Flow()},
            outputs={
                b_el: solph.flows.Flow(
                    min=min,
                    nonconvex=solph.NonConvex(),
                    nominal_value=solph.Investment(
                        ep_costs=100,
                        maximum=1234,
                    ),
                )
            },
            conversion_factors={b_diesel: slope},
            normed_offsets={b_diesel: offset},
        )
        self.energysystem.add(b_diesel, b_el, diesel_genset)

        self.compare_lp_files("offsetconverter_nonconvex_investment.lp")

    def test_dsm_module_DIW(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            approach="DIW",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )

        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DIW.lp")

    def test_dsm_module_DLR(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
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
        self.compare_lp_files("dsm_module_DLR.lp")

    def test_dsm_module_oemof(self):
        """Constraint test of SinkDSM with approach=oemof"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5, 0.4, 0.5],
            capacity_down=[0.5, 0.4, 0.5],
            approach="oemof",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            shift_interval=2,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_oemof.lp")

    def test_dsm_module_DIW_extended(self):
        """Constraint test of SinkDSM with approach=DLR

        Test all possible parameters and constraints
        """

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8],
            capacity_up=[0.5, 0.4, 0.5],
            capacity_down=[0.3, 0.3, 0.4],
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
        self.compare_lp_files("dsm_module_DIW_extended.lp")

    def test_dsm_module_DLR_extended(self):
        """Constraint test of SinkDSM with approach=DLR"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8],
            capacity_up=[0.5, 0.4, 0.5],
            capacity_down=[0.3, 0.3, 0.4],
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
        self.compare_lp_files("dsm_module_DLR_extended.lp")

    def test_dsm_module_oemof_extended(self):
        """Constraint test of SinkDSM with approach=oemof"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1, 0.9, 0.8],
            capacity_up=[0.5, 0.4, 0.5],
            capacity_down=[0.3, 0.3, 0.4],
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
        self.compare_lp_files("dsm_module_oemof_extended.lp")

    def test_dsm_module_DIW_invest(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            approach="DIW",
            max_demand=1,
            delay_time=1,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                existing=50,
                minimum=33,
                maximum=100,
                custom_attributes={"ep_cost": 100},
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DIW_invest.lp")

    def test_dsm_module_DLR_invest(self):
        """Constraint test of SinkDSM with approach=DLR and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            approach="DLR",
            max_demand=1,
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
                existing=50,
                minimum=33,
                maximum=100,
                custom_attributes={"ep_cost": 100},
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DLR_invest.lp")

    def test_dsm_module_oemof_invest(self):
        """Constraint test of SinkDSM with approach=oemof and investments"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5, 0.4, 0.5],
            capacity_down=[0.5, 0.4, 0.5],
            approach="oemof",
            max_demand=1,
            shift_interval=2,
            cost_dsm_down_shift=1,
            cost_dsm_up=1,
            cost_dsm_down_shed=100,
            shed_eligibility=True,
            recovery_time_shed=2,
            shed_time=2,
            investment=solph.Investment(
                existing=50,
                minimum=33,
                maximum=100,
                custom_attributes={"ep_cost": 100},
            ),
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_oemof_invest.lp")

    def test_dsm_module_DLR_delay_time(self):
        """Constraint test of SinkDSM with approach=DLR;
        testing for passing an iterable for delay_time"""

        b_elec = solph.buses.Bus(label="bus_elec")
        sinkdsm = solph.components.experimental.SinkDSM(
            label="demand_dsm",
            inputs={b_elec: solph.flows.Flow()},
            demand=[1] * 3,
            capacity_up=[0.5] * 3,
            capacity_down=[0.5] * 3,
            approach="DLR",
            max_demand=1,
            max_capacity_up=1,
            max_capacity_down=1,
            delay_time=[1, 3],
            shift_time=1,
            cost_dsm_down_shift=2,
            shed_eligibility=False,
        )
        self.energysystem.add(b_elec, sinkdsm)
        self.compare_lp_files("dsm_module_DLR_delay_time.lp")

    def test_invest_non_convex_flow(self):
        """Invest into a non-convex Flow"""
        b1 = solph.buses.Bus(label="b1")
        b2 = solph.buses.Bus(
            label="b2",
            inputs={
                b1: solph.Flow(
                    variable_costs=8,
                    min=0.25,
                    max=0.5,
                    nominal_value=solph.Investment(
                        ep_costs=0.75,
                        maximum=10,
                    ),
                    nonconvex=solph.NonConvex(),
                )
            },
            outputs={b1: solph.Flow()},
        )
        self.energysystem.add(b1, b2)
        self.compare_lp_files("invest_non_convex_flow.lp")

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
            nominal_storage_capacity=solph.Investment(
                ep_costs=141, maximum=244, minimum=12, nonconvex=True
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_without_offset.lp")

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
            nominal_storage_capacity=solph.Investment(
                ep_costs=145,
                minimum=19,
                offset=5,
                nonconvex=True,
                maximum=1454,
            ),
        )
        self.energysystem.add(bel, storage)
        self.compare_lp_files("storage_invest_with_offset.lp")

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
                    )
                )
            },
            nominal_storage_capacity=solph.Investment(
                nonconvex=True, ep_costs=20, offset=30, minimum=20, maximum=100
            ),
        )
        self.energysystem.add(b1, storage)
        self.compare_lp_files("storage_invest_all_nonconvex.lp")

    def test_nonconvex_invest_sink_without_offset(self):
        """Non-convex invest flow without offset, with minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="sink_nonconvex_invest",
            inputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500, minimum=15, nonconvex=True, maximum=172
                    ),
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("flow_invest_without_offset.lp")

    def test_nonconvex_invest_source_with_offset(self):
        """Non-convex invest flow with offset, with minimum."""
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
                    ),
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("flow_invest_with_offset.lp")

    def test_nonconvex_invest_source_with_offset_no_minimum(self):
        """Non-convex invest flow with offset, without minimum."""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="source_nonconvex_invest",
            outputs={
                bel: solph.flows.Flow(
                    full_load_time_max=2.3,
                    variable_costs=25,
                    max=0.8,
                    nominal_value=solph.Investment(
                        ep_costs=500, maximum=1234, offset=34, nonconvex=True
                    ),
                )
            },
        )
        self.energysystem.add(bel, source)
        self.compare_lp_files("flow_invest_with_offset_no_minimum.lp")

    def test_integral_limit_error_no_multi_period(self):
        """Test error being thrown if model is not a multi-period model"""
        bel = solph.buses.Bus(label="electricityBus")

        source = solph.components.Source(
            label="pv_source",
            outputs={
                bel: solph.flows.Flow(
                    nominal_value=100,
                    variable_costs=20,
                    fix=[0.3, 0.5, 0.8],
                    custom_attributes={"space": 40},
                )
            },
        )
        self.energysystem.add(bel, source)
        om = self.get_om()
        msg = (
            "generic_periodical_integral_limit is only applicable\n"
            "for multi-period models.\nFor standard models, use "
            "generic_integral_limit instead."
        )
        with pytest.raises(ValueError, match=msg):
            solph.constraints.generic_periodical_integral_limit(
                om, keyword="space"
            )

    def test_full_load_time_min_max_source(self):
        """Constraints test full_load_time_min and _max attribute of flow"""

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
        self.compare_lp_files("summed_min_source.lp")

    def test_integer_flow_source(self):
        """Test source with integer output"""
        bel = solph.buses.Bus(label="electricityBus")

        sink = solph.components.Sink(
            label="excess",
            inputs={
                bel: solph.flows.Flow(
                    variable_costs=25, max=1, nominal_value=10, integer=True
                )
            },
        )
        self.energysystem.add(bel, sink)
        self.compare_lp_files("integer_source.lp")

    def test_nonequidistant_storage(self):
        """Constraint test of an energy system
        with non-equidistant time index
        """
        idxh = pd.date_range("1/1/2017", periods=3, freq="h")
        idx2h = pd.date_range("1/1/2017 03:00:00", periods=2, freq="2H")
        idx30m = pd.date_range("1/1/2017 07:00:00", periods=4, freq="30min")
        timeindex = idxh.append([idx2h, idx30m])
        es = solph.EnergySystem(timeindex=timeindex, infer_last_interval=False)
        b_gas = solph.Bus(label="gas")
        b_th = solph.Bus(label="heat")
        boiler = solph.components.Converter(
            label="boiler",
            inputs={b_gas: solph.Flow(variable_costs=100)},
            outputs={b_th: solph.Flow(nominal_value=200)},
        )
        storage = solph.components.GenericStorage(
            label="storage",
            inputs={b_th: solph.Flow(nominal_value=100, variable_costs=56)},
            outputs={b_th: solph.Flow(nominal_value=100, variable_costs=24)},
            nominal_storage_capacity=300,
            loss_rate=0.1,
            initial_storage_level=1,
        )
        es.add(b_gas, b_th, boiler, storage)
        om = solph.Model(es)
        self.compare_lp_files("nonequidistant_timeindex.lp", my_om=om)

    def test_storage_level_constraint(self):
        """Constraint test of an energy system
        with storage_level_constraint
        """
        es = solph.EnergySystem(
            timeindex=pd.date_range("2022-01-01", freq="1H", periods=2),
            infer_last_interval=True,
        )

        multiplexer = solph.Bus(
            label="multiplexer",
        )

        storage = solph.components.GenericStorage(
            label="storage",
            nominal_storage_capacity=4,
            initial_storage_level=1,
            balanced=True,
            loss_rate=0.25,
            inputs={multiplexer: solph.Flow()},
            outputs={multiplexer: solph.Flow()},
        )

        es.add(multiplexer, storage)

        in_0 = solph.components.Source(
            label="in_0",
            outputs={
                multiplexer: solph.Flow(nominal_value=0.5, variable_costs=0.25)
            },
        )
        es.add(in_0)

        in_1 = solph.components.Source(
            label="in_1",
            outputs={multiplexer: solph.Flow(nominal_value=0.125)},
        )
        es.add(in_1)

        out_0 = solph.components.Sink(
            label="out_0",
            inputs={
                multiplexer: solph.Flow(
                    nominal_value=0.25, variable_costs=-0.125
                )
            },
        )
        es.add(out_0)

        out_1 = solph.components.Sink(
            label="out_1",
            inputs={
                multiplexer: solph.Flow(
                    nominal_value=0.125, variable_costs=-0.125
                )
            },
        )
        es.add(out_1)

        om = solph.Model(es)

        solph.constraints.storage_level_constraint(
            model=om,
            name="multiplexer",
            storage_component=storage,
            multiplexer_bus=multiplexer,
            input_levels={in_1: 1 / 4},  # in_0 is always active
            output_levels={out_0: 1 / 8, out_1: 1 / 2},
        )
        self.compare_lp_files("storage_level_constraint.lp", my_om=om)
