# -*- coding: utf-8 -*-
"""Unit tests for VariableSplitConverter and VariableSplitConverterBlock."""

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
