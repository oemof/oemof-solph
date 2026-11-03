# -*- coding: utf-8 -*-

"""Tests for the investment_limit constraint

SPDX-FileCopyrightText: oemof e.V. and contributors

SPDX-License-Identifier: MIT
"""

import pandas as pd
from pyomo.core.expr.visitor import identify_variables
from pyomo.repn import generate_standard_repn

from oemof import solph


def _storage_only_energy_system(storage_count=3):
    """Energy system whose only investments are storage investments.

    No Flow carries an Investment. This is the scenario of issue #1076:
    ``investment_limit`` used to fail with
    ``AttributeError: 'InvestmentFlowBlock' object has no attribute
    'investment_costs'`` for such systems.
    """
    date_time_index = pd.date_range("1/1/2020", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
    )

    bus = solph.buses.Bus(label="bus")
    energysystem.add(bus)
    energysystem.add(
        solph.components.Source(
            label="source",
            outputs={
                bus: solph.Flow(nominal_capacity=10, fix=[1, 1, 1]),
            },
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="sink",
            inputs={bus: solph.Flow(nominal_capacity=10)},
        )
    )

    storages = []
    for i in range(storage_count):
        storage = solph.components.GenericStorage(
            label="storage" + str(i),
            inputs={bus: solph.Flow()},
            outputs={bus: solph.Flow()},
            balanced=True,
            nominal_capacity=solph.Investment(ep_costs=10),
        )
        storages.append(storage)
        energysystem.add(storage)

    return energysystem, bus, storages


def _coefficients_by_var_name(constraint):
    """Linear coefficients of a constraint body, keyed by variable name.

    Also asserts that the body is purely linear and has no constant
    term, so a caller comparing the returned dict checks the variable
    set, every coefficient, and the constant in one go.
    """
    repn = generate_standard_repn(constraint.body)
    assert repn.is_linear()
    assert repn.constant == 0
    return {
        var.name: coef
        for var, coef in zip(repn.linear_vars, repn.linear_coefs)
    }


def test_investment_limit_with_storage_investment_only():
    """investment_limit works if only storages have an Investment (#1076)."""
    energysystem, _, storages = _storage_only_energy_system()

    model = solph.Model(energysystem)

    # This call is the regression test for #1076: the constraint reads
    # `investment_costs` from every investment block that exists, and the
    # InvestmentFlowBlock exists (it is created for every model) even
    # though no flow has an investment. It used to fail with
    # AttributeError because that block did not provide the attribute.
    solph.constraints.investment_limit(model, limit=100)

    # Only the storage investment costs enter the constraint.
    invest_vars = {
        var.name for var in identify_variables(model.investment_limit.body)
    }
    expected = {
        model.GenericInvestmentStorageBlock.invest[storage, 0].name
        for storage in storages
    }
    assert invest_vars == expected

    # Each storage contributes its ep_costs (10, see the fixture) times
    # its invest variable, with no constant term.
    assert _coefficients_by_var_name(model.investment_limit) == {
        name: 10 for name in expected
    }

    # The limit is an upper bound only.
    assert model.investment_limit.lower is None
    assert model.investment_limit.upper() == 100


def test_storage_investment_without_investment_limit():
    """Control case: the same system builds fine without the limit.

    This is a modelling baseline, not direct coverage of
    ``investment_limit``: it pins down that the storage-only system and
    its storage investment block are well-formed on their own, so a
    failure of the other tests can be attributed to the constraint.
    """
    energysystem, _, _ = _storage_only_energy_system()

    model = solph.Model(energysystem)

    assert not hasattr(model, "investment_limit")
    assert hasattr(model.GenericInvestmentStorageBlock, "investment_costs")


def test_investment_limit_with_flow_and_storage_investment():
    """Flow and storage investment costs are both counted if both exist."""
    energysystem, bus, storages = _storage_only_energy_system(storage_count=1)

    source = solph.components.Source(
        label="investment_source",
        outputs={
            bus: solph.Flow(nominal_capacity=solph.Investment(ep_costs=5)),
        },
    )
    energysystem.add(source)

    model = solph.Model(energysystem)
    solph.constraints.investment_limit(model, limit=100)

    invest_vars = {
        var.name for var in identify_variables(model.investment_limit.body)
    }
    expected = {
        model.GenericInvestmentStorageBlock.invest[storages[0], 0].name,
        model.InvestmentFlowBlock.invest[source, bus, 0].name,
    }
    assert invest_vars == expected

    # Each investment contributes its own ep_costs (10 for the storage
    # from the fixture, 5 for the flow) times its invest variable, with
    # no constant term.
    assert _coefficients_by_var_name(model.investment_limit) == {
        model.GenericInvestmentStorageBlock.invest[storages[0], 0].name: 10,
        model.InvestmentFlowBlock.invest[source, bus, 0].name: 5,
    }

    # The limit is an upper bound only.
    assert model.investment_limit.lower is None
    assert model.investment_limit.upper() == 100
