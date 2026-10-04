"""
Unit tests for VariableSplitConverter and VariableSplitConverterBlock.

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

import pandas as pd
import pytest

from oemof import solph
from oemof.solph.components import ExtractionTurbineCHP
from oemof.solph.components import VariableSplitConverter
from oemof.solph.components._variable_split_converter import (
    VariableSplitConverterBlock,
)
from oemof.solph.components._variable_split_converter import (
    _conversion_points_are_equal,
)


def test_variable_split_converter_function():
    data = pd.DataFrame(
        {
            "demand_el": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            "demand_th": [0.5, 2, 5, 7, 9, 0.5, 2, 5, 7, 9],
        }
    )
    abel = [0.5, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3]
    abth = [0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.5, 0.5, 0.5, 0.5]
    bbel = [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3]
    bbth = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.3]

    energysystem = solph.EnergySystem(timeincrement=[1] * 10)

    noded = dict()

    # create natural gas bus
    noded["bgas"] = solph.Bus(label="natural_gas")

    # create commodity object for gas resource
    noded["rgas"] = solph.components.Source(
        label="rgas", outputs={noded["bgas"]: solph.Flow(variable_costs=50)}
    )

    # create two electricity buses and two heat buses
    noded["bel"] = solph.Bus(label="electricity")
    noded["bel2"] = solph.Bus(label="electricity_2")
    noded["bth"] = solph.Bus(label="heat")
    noded["bth2"] = solph.Bus(label="heat_2")

    # create excess components for the elec/heat bus to allow overproduction
    noded["excess_bth_2"] = solph.components.Sink(
        label="excess_bth_2", inputs={noded["bth2"]: solph.Flow()}
    )
    noded["excess_therm"] = solph.components.Sink(
        label="excess_therm", inputs={noded["bth"]: solph.Flow()}
    )
    noded["excess_bel_2"] = solph.components.Sink(
        label="excess_bel_2", inputs={noded["bel2"]: solph.Flow()}
    )
    noded["excess_elec"] = solph.components.Sink(
        label="excess_elec", inputs={noded["bel"]: solph.Flow()}
    )

    # create simple sink object for electrical demand for each electrical bus
    noded["demand_elec"] = solph.components.Sink(
        label="demand_elec",
        inputs={
            noded["bel"]: solph.Flow(fix=data["demand_el"], nominal_capacity=1)
        },
    )
    noded["demand_el_2"] = solph.components.Sink(
        label="demand_el_2",
        inputs={
            noded["bel2"]: solph.Flow(
                fix=data["demand_el"], nominal_capacity=1
            )
        },
    )

    # create simple sink object for heat demand for each thermal bus
    noded["demand_therm"] = solph.components.Sink(
        label="demand_therm",
        inputs={
            noded["bth"]: solph.Flow(fix=data["demand_th"], nominal_capacity=1)
        },
    )
    noded["demand_therm_2"] = solph.components.Sink(
        label="demand_th_2",
        inputs={
            noded["bth2"]: solph.Flow(
                fix=data["demand_th"], nominal_capacity=1
            )
        },
    )

    # create a fixed Converter to distribute to the heat_2 and elec_2 buses
    noded["fixed_chp_gas_2"] = solph.components.Converter(
        label="fixed_chp_gas_2",
        inputs={noded["bgas"]: solph.Flow(nominal_capacity=10e10)},
        outputs={noded["bel2"]: solph.Flow(), noded["bth2"]: solph.Flow()},
        conversion_factors={noded["bel2"]: 0.3, noded["bth2"]: 0.5},
    )

    noded["variable_chp_gas"] = solph.components.VariableSplitConverter(
        label="variable_chp_gas",
        inputs={noded["bgas"]: solph.Flow(nominal_capacity=10e10)},
        outputs={noded["bth"]: solph.Flow(), noded["bel"]: solph.Flow()},
        conversion_factors={
            noded["bel"]: abel,
            noded["bth"]: abth,
        },
        allow_equal_states=True,
        conversion_factors_secondary_state={
            noded["bel"]: bbel,
            noded["bth"]: bbth,
        },
    )

    energysystem.add(*noded.values())

    om = solph.Model(energysystem)

    results = om.solve(solver="cbc", solve_kwargs={"tee": False})
    flows = results["flow"]
    ex_cols = [
        c for c in flows.columns if "excess" in c[1].label
    ]

    eff_fix_elec = (
        flows[("fixed_chp_gas_2", "electricity_2")]
        / flows[("natural_gas", "fixed_chp_gas_2")]
    )
    eff_fix_heat = (
        flows[("fixed_chp_gas_2", "heat_2")]
        / flows[("natural_gas", "fixed_chp_gas_2")]
    )
    eff_var_elec = (
        flows[("variable_chp_gas", "electricity")]
        / flows[("natural_gas", "variable_chp_gas")]
    )
    eff_var_heat = (
        flows[("variable_chp_gas", "heat")]
        / flows[("natural_gas", "variable_chp_gas")]
    )

    # Efficiencies of Convert must be fixed
    assert all(eff_fix_elec.round(9) == 0.3)
    assert all(eff_fix_heat.round(9) == 0.5)
    # Efficiencies of VariableSplitConverter must be within the linear function
    assert all(
        (
            round(-4 / 3 * eff_var_elec + 23 / 30, 6) == round(eff_var_heat, 6)
        ).iloc[0:5]
    )

    # Expected results
    columns = pd.MultiIndex.from_tuples(
        [
            ("electricity", "excess_elec"),
            ("electricity_2", "excess_bel_2"),
            ("heat", "excess_therm"),
            ("heat_2", "excess_bth_2"),
        ]
    )
    data = [
        [0.0, 0.0, 0.1, 4.5],
        [0.0, 0.0, 0.0, 3.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 1.2, 0.0, 0.0],
        [0.6, 2.4, 0.0, 0.0],
        [0.0, 0.0, 4.5, 4.5],
        [0.0, 0.0, 3.0, 3.0],
        [0.0, 0.0, 0.0, 0.0],
        [1.2, 1.2, 0.0, 0.0],
        [2.4, 2.4, 0.0, 0.0],
    ]
    df = pd.DataFrame(data, columns=columns)
    assert df.equals(flows[ex_cols])


# ---------------------------------------------------------------------------
# _conversion_points_are_equal
# ---------------------------------------------------------------------------
class TestConversionPointsAreEqual:
    def test_equal_scalar_dicts(self):
        assert _conversion_points_are_equal({"a": 1, "b": 2}, {"a": 1, "b": 2})

    def test_different_keys(self):
        assert not _conversion_points_are_equal({"a": 1}, {"b": 1})

    def test_subset_keys(self):
        assert not _conversion_points_are_equal({"a": 1, "b": 2}, {"a": 1})

    def test_same_keys_different_values(self):
        assert not _conversion_points_are_equal({"a": 1}, {"a": 2})

    def test_equal_sequence_values(self):
        assert _conversion_points_are_equal({"a": [1, 2, 3]}, {"a": [1, 2, 3]})

    def test_different_sequence_values(self):
        assert not _conversion_points_are_equal({"a": [1, 2]}, {"a": [1, 3]})


# ---------------------------------------------------------------------------
# VariableSplitConverter.__init__
# ---------------------------------------------------------------------------
@pytest.fixture
def buses():
    bgas = solph.buses.Bus(label="commodityBus")
    bel = solph.buses.Bus(label="electricityBus")
    bth = solph.buses.Bus(label="heatBus")
    return bgas, bel, bth


class TestVariableSplitConverterInit:
    def test_create_with_scalar_conversion_factors(self, buses):
        bgas, bel, bth = buses
        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.30, bth: 0.50},
            conversion_factors_secondary_state={bel: 0.48, bth: 0.10},
        )
        assert converter.allow_equal_states is False
        assert converter.conversion_factors[bel][0] == 0.30
        assert converter.conversion_factors_secondary_state[bth][0] == 0.10

    def test_extraction_turbine_warning(self, buses):
        bgas, bel, bth = buses
        with pytest.warns(FutureWarning, match="Class 'ExtractionTurbineCHP'"):
            converter = ExtractionTurbineCHP(
                label="chp",
                inputs={bgas: solph.flows.Flow()},
                outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
                conversion_factors={bel: 0.30, bth: 0.50},
                conversion_factor_full_condensation={bel: 0.48},
            )
        assert converter.allow_equal_states is False
        assert converter.conversion_factors[bel][0] == 0.30

    def test_mismatched_buses_raises(self, buses):
        bgas, bel, bth = buses
        other_bus = solph.buses.Bus(label="otherBus")
        with pytest.raises(ValueError, match="same buses"):
            VariableSplitConverter(
                label="chp",
                inputs={bgas: solph.flows.Flow()},
                outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
                conversion_factors={bel: 0.30, bth: 0.50},
                conversion_factors_secondary_state={
                    bel: 0.48,
                    other_bus: 0.10,
                },
            )

    def test_equal_scalar_states_raise_by_default(self, buses):
        bgas, bel, bth = buses
        with pytest.raises(ValueError, match="not okay"):
            VariableSplitConverter(
                label="chp",
                inputs={bgas: solph.flows.Flow()},
                outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
                conversion_factors={bel: 0.30, bth: 0.50},
                conversion_factors_secondary_state={bel: 0.30, bth: 0.50},
            )

    def test_equal_scalar_states_allowed_with_flag(self, buses):
        bgas, bel, bth = buses
        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.30, bth: 0.50},
            conversion_factors_secondary_state={bel: 0.30, bth: 0.50},
            allow_equal_states=True,
        )
        assert converter.allow_equal_states is True

    def test_equal_sequence_states_raise_by_default(self, buses):
        bgas, bel, bth = buses
        with pytest.raises(ValueError, match="not okay"):
            VariableSplitConverter(
                label="chp",
                inputs={bgas: solph.flows.Flow()},
                outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
                conversion_factors={bel: [0.30, 0.35], bth: [0.50, 0.45]},
                conversion_factors_secondary_state={
                    bel: [0.30, 0.40],
                    bth: [0.55, 0.40],
                },
            )

    def test_equal_sequence_states_allowed_with_flag(self, buses):
        bgas, bel, bth = buses
        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: [0.30, 0.35], bth: [0.50, 0.45]},
            conversion_factors_secondary_state={
                bel: [0.30, 0.40],
                bth: [0.55, 0.40],
            },
            allow_equal_states=True,
        )
        assert converter.allow_equal_states is True

    def test_non_overlapping_sequence_states_do_not_raise(self, buses):
        bgas, bel, bth = buses
        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: [0.30, 0.35], bth: [0.50, 0.45]},
            conversion_factors_secondary_state={
                bel: [0.48, 0.46],
                bth: [0.10, 0.12],
            },
        )
        assert converter.allow_equal_states is False

    def test_constraint_group_returns_block_class(self, buses):
        bgas, bel, bth = buses
        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={bel: solph.flows.Flow(), bth: solph.flows.Flow()},
            conversion_factors={bel: 0.30, bth: 0.50},
            conversion_factors_secondary_state={bel: 0.48, bth: 0.10},
        )
        assert converter.constraint_group() is VariableSplitConverterBlock

    def test_equal_states_mixed_degenerate_timesteps(self):
        idx = solph.create_time_index(2020, number=1)
        es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)

        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="elBus")
        bth = solph.buses.Bus(label="thBus")

        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(nominal_capacity=10),
                bth: solph.flows.Flow(nominal_capacity=10),
            },
            conversion_factors={bel: [0.30, 0.40], bth: [0.50, 0.45]},
            conversion_factors_secondary_state={
                bel: [0.35, 0.45],
                bth: [0.50, 0.40],
            },
            allow_equal_states=True,
        )

        source = solph.components.Source(
            label="gas_source",
            outputs={bgas: solph.flows.Flow(nominal_capacity=1000)},
        )
        sink_el = solph.components.Sink(
            label="el_sink",
            inputs={bel: solph.flows.Flow(nominal_capacity=10, fix=0.5)},
        )
        sink_th = solph.components.Sink(
            label="th_sink",
            inputs={bth: solph.flows.Flow(nominal_capacity=10, fix=0.3)},
        )

        es.add(bgas, bel, bth, converter, source, sink_el, sink_th)

        m = solph.Model(es)
        block = m.VariableSplitConverterBlock

        assert converter in block.EQUAL_STATES

        # Only t=0 is degenerate (coef_out_b == 0) -> only one constraint
        # per bound is built; t=1 is skipped (coef_out_b != 0).
        assert len(block.out_a_lower_bound) == 1
        assert len(block.out_a_upper_bound) == 1
        assert (converter, 0) in block.out_a_lower_bound
        assert (converter, 1) not in block.out_a_lower_bound
        assert (converter, 0) in block.out_a_upper_bound
        assert (converter, 1) not in block.out_a_upper_bound


# ---------------------------------------------------------------------------
# VariableSplitConverterBlock
# ---------------------------------------------------------------------------
class TestVariableSplitConverterBlock:
    def test_constraint_group_flag_is_true(self):
        assert VariableSplitConverterBlock.CONSTRAINT_GROUP is True

    def test_create_with_none_group_returns_none(self):
        block = VariableSplitConverterBlock()
        assert block._create(group=None) is None

    def test_model_build_creates_expected_constraints(self):
        idx = solph.create_time_index(2020, number=3)
        es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)

        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="elBus")
        bth = solph.buses.Bus(label="thBus")

        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(nominal_capacity=10),
                bth: solph.flows.Flow(nominal_capacity=10),
            },
            conversion_factors={bel: 0.30, bth: 0.50},
            conversion_factors_secondary_state={bel: 0.48, bth: 0.10},
        )

        source = solph.components.Source(
            label="gas_source",
            outputs={bgas: solph.flows.Flow(nominal_capacity=1000)},
        )
        sink_el = solph.components.Sink(
            label="el_sink",
            inputs={bel: solph.flows.Flow(nominal_capacity=10, fix=0.5)},
        )
        sink_th = solph.components.Sink(
            label="th_sink",
            inputs={bth: solph.flows.Flow(nominal_capacity=10, fix=0.3)},
        )

        es.add(bgas, bel, bth, converter, source, sink_el, sink_th)

        m = solph.Model(es)
        block = m.VariableSplitConverterBlock

        assert isinstance(block, VariableSplitConverterBlock)
        assert hasattr(block, "input_output_relation")
        assert hasattr(block, "out_b_lower_bound")
        assert hasattr(block, "out_b_upper_bound")

        n_timesteps = len(m.TIMESTEPS)
        assert len(block.input_output_relation) == n_timesteps
        assert len(block.out_b_lower_bound) == n_timesteps
        assert len(block.out_b_upper_bound) == n_timesteps

        # Without allow_equal_states, EQUAL_STATES must be empty and
        # the corresponding constraints must not be built for this
        # converter.
        assert converter not in block.EQUAL_STATES

    def test_model_build_with_equal_states_populates_equal_states_set(self):
        idx = solph.create_time_index(2020, number=2)
        es = solph.EnergySystem(timeindex=idx, infer_last_interval=True)

        bgas = solph.buses.Bus(label="gasBus")
        bel = solph.buses.Bus(label="elBus")
        bth = solph.buses.Bus(label="thBus")

        converter = VariableSplitConverter(
            label="chp",
            inputs={bgas: solph.flows.Flow()},
            outputs={
                bel: solph.flows.Flow(nominal_capacity=10),
                bth: solph.flows.Flow(nominal_capacity=10),
            },
            conversion_factors={bel: 0.30, bth: 0.50},
            conversion_factors_secondary_state={bel: 0.30, bth: 0.50},
            allow_equal_states=True,
        )

        source = solph.components.Source(
            label="gas_source",
            outputs={bgas: solph.flows.Flow(nominal_capacity=1000)},
        )
        sink_el = solph.components.Sink(
            label="el_sink",
            inputs={bel: solph.flows.Flow(nominal_capacity=10, fix=0.5)},
        )
        sink_th = solph.components.Sink(
            label="th_sink",
            inputs={bth: solph.flows.Flow(nominal_capacity=10, fix=0.3)},
        )

        es.add(bgas, bel, bth, converter, source, sink_el, sink_th)

        m = solph.Model(es)
        block = m.VariableSplitConverterBlock

        assert converter in block.EQUAL_STATES
