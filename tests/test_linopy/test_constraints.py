# -*- coding: utf-8 -*-

"""Equivalence of the linopy and the Pyomo backend for the functions in
solph.constraints, and custom constraints written against each backend.

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest
from pyomo import environ as po

from oemof import solph

pytest.importorskip("linopy")

from oemof.solph._linopy import LinopyModel  # noqa: E402
from oemof.solph._models import Model as PyomoModel  # noqa: E402

from .equivalence import assert_backends_agree  # noqa: E402

N_STEPS = 24
RNG = np.random.default_rng(11)
PRICE = 30 + 60 * RNG.random(N_STEPS)
DEMAND = 3 + 2 * RNG.random(N_STEPS)


def _es():
    idx = pd.date_range("2025-01-01", periods=N_STEPS, freq="h")
    return solph.EnergySystem(timeindex=idx, infer_last_interval=True)


def _two_party_storage_system():
    """Two parties with their own storage, sharing one physical limit."""
    es = _es()
    for party in ("a", "b"):
        bus = solph.Bus(f"el {party}")
        es.add(
            bus,
            solph.components.Source(
                f"grid {party}",
                outputs={bus: solph.Flow(variable_costs=PRICE)},
            ),
            solph.components.Sink(
                f"demand {party}",
                inputs={bus: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
            ),
            solph.components.GenericStorage(
                f"storage {party}",
                inputs={bus: solph.Flow(nominal_capacity=4)},
                outputs={bus: solph.Flow(nominal_capacity=4)},
                nominal_capacity=20,
                balanced=True,
            ),
        )
    return es


def _solve_with(model_class, add_constraints, solver="highs"):
    model = model_class(_two_party_storage_system())
    add_constraints(model)
    return model, model.solve(solver=solver)


def test_shared_limit():
    def add(model):
        storages = [model.es.groups["storage a"], model.es.groups["storage b"]]
        solph.constraints.shared_limit(
            model,
            model.GenericStorageBlock.storage_content,
            "shared_storage",
            storages,
            [1, 1],
            upper_limit=25,
        )

    _, pyomo = _solve_with(PyomoModel, add)
    _, linopy_ = _solve_with(LinopyModel, add)
    assert linopy_.solver["objective"] == pytest.approx(
        pyomo.solver["objective"], rel=1e-6
    )
    np.testing.assert_allclose(
        linopy_.get("shared_storage").to_numpy().ravel(),
        pyomo.get("shared_storage").to_numpy().ravel(),
        atol=1e-6,
    )


def _investment_system():
    es = _es()
    el = solph.Bus("el")
    es.add(el)
    es.add(
        solph.components.Source(
            "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
        ),
        solph.components.Source(
            "cheap",
            outputs={
                el: solph.Flow(
                    variable_costs=5,
                    nominal_capacity=solph.Investment(
                        ep_costs=40, custom_properties={"space": 2}
                    ),
                )
            },
        ),
        solph.components.Sink(
            "demand",
            inputs={el: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
        ),
        solph.components.GenericStorage(
            "battery",
            # custom_properties={}: additional_investment_flow_limit fails
            # for investments without custom_properties (both backends)
            inputs={
                el: solph.Flow(
                    nominal_capacity=solph.Investment(custom_properties={})
                )
            },
            outputs={
                el: solph.Flow(
                    nominal_capacity=solph.Investment(custom_properties={})
                )
            },
            nominal_capacity=solph.Investment(ep_costs=3),
            invest_relation_input_capacity=1 / 4,
            invest_relation_output_capacity=1 / 4,
            storage_costs=0.1,
        ),
    )
    return es


@pytest.mark.parametrize(
    "add",
    [
        lambda m: solph.constraints.investment_limit(m, limit=60),
        lambda m: solph.constraints.additional_investment_flow_limit(
            m, "space", limit=4
        ),
    ],
    ids=["investment_limit", "additional_investment_flow_limit"],
)
def test_investment_limits(add):
    def build():
        return _investment_system()

    pyomo_model = PyomoModel(build())
    add(pyomo_model)
    pyomo = pyomo_model.solve(solver="highs")
    linopy_model = LinopyModel(build())
    add(linopy_model)
    linopy_ = linopy_model.solve(solver="highs")
    assert linopy_.solver["objective"] == pytest.approx(
        pyomo.solver["objective"], rel=1e-6
    )
    # the limit binds in both
    assert linopy_.solver["objective"] > (
        LinopyModel(build()).solve(solver="highs").solver["objective"] + 1e-6
    )


def test_integral_limit_expression_value():
    def build():
        es = _investment_system()
        for (i, o), flow in es.flows().items():
            if i.label == "grid":
                flow.custom_properties["emission_factor"] = 0.4
        return es

    pyomo_model = PyomoModel(build())
    solph.constraints.emission_limit(pyomo_model, limit=8)
    pyomo_model.solve(solver="highs")
    linopy_model = LinopyModel(build())
    solph.constraints.emission_limit(linopy_model, limit=8)
    linopy_model.solve(solver="highs")
    assert linopy_model.integral_limit_emission_factor() == pytest.approx(
        pyomo_model.integral_limit_emission_factor(), rel=1e-6
    )


def _custom_constraint_es():
    es = solph.EnergySystem(
        timeindex=pd.date_range("1/1/2012", periods=4, freq="h"),
        infer_last_interval=True,
    )
    boil = solph.Bus(label="oil", balanced=False)
    blig = solph.Bus(label="lignite", balanced=False)
    b_el = solph.Bus(label="b_el")
    es.add(boil, blig, b_el)
    es.add(
        solph.components.Sink(
            label="Sink",
            inputs={
                b_el: solph.Flow(nominal_capacity=40, fix=[0.5, 0.4, 0.3, 1])
            },
        ),
        solph.components.Converter(
            label="pp_oil",
            inputs={boil: solph.Flow()},
            outputs={b_el: solph.Flow(nominal_capacity=50, variable_costs=25)},
            conversion_factors={b_el: 0.39},
        ),
        solph.components.Converter(
            label="pp_lig",
            inputs={blig: solph.Flow()},
            outputs={b_el: solph.Flow(nominal_capacity=50, variable_costs=10)},
            conversion_factors={b_el: 0.41},
        ),
    )
    return es


OUTFLOW_SHARE = np.array([1, 0.5, 0, 0.3])


def test_custom_constraints_pyomo_and_linopy():
    """The example of test_add_constraints written for both backends:
    the oil plant must deliver a share of all inflows into it, and the
    fuel use is limited."""
    # Pyomo: rules over om.flow[i, o, t]
    es = _custom_constraint_es()
    boil, b_el = es.groups["oil"], es.groups["b_el"]
    pp_oil = es.groups["pp_oil"]
    om = PyomoModel(es)
    om.inflow_share = po.Constraint(
        om.TIMESTEPS,
        rule=lambda m, t: om.flow[boil, pp_oil, t]
        >= OUTFLOW_SHARE[t]
        * sum(om.flow[i, o, t] for (i, o) in om.FLOWS if o == pp_oil),
    )
    om.fuel_limit = po.Constraint(
        expr=sum(om.flow[boil, pp_oil, t] for t in om.TIMESTEPS) <= 60
    )
    pyomo = om.solve(solver="highs")

    # linopy: the same with flow_var() and linopy expressions
    es = _custom_constraint_es()
    boil, pp_oil = es.groups["oil"], es.groups["pp_oil"]
    lm = LinopyModel(es)
    inflows = sum(lm.flow_var(i, o) for (i, o) in lm.FLOWS if o == pp_oil)
    share = pd.Series(OUTFLOW_SHARE).to_xarray().rename(index="timestep")
    lm.linopy.add_constraints(
        lm.flow_var(boil, pp_oil) - share * inflows >= 0, name="inflow_share"
    )
    lm.linopy.add_constraints(
        lm.flow_var(boil, pp_oil).sum() <= 60, name="fuel_limit"
    )
    linopy_ = lm.solve(solver="highs")
    assert linopy_.solver["objective"] == pytest.approx(
        pyomo.solver["objective"], rel=1e-6
    )
    assert b_el is not None


def test_equate_variables_with_block_views():
    def build():
        es = _investment_system()
        el = es.groups["el"]
        es.add(
            solph.components.Source(
                "second",
                outputs={
                    el: solph.Flow(
                        variable_costs=6,
                        nominal_capacity=solph.Investment(ep_costs=35),
                    )
                },
            )
        )
        return es

    def add(model):
        es = model.es
        el = es.groups["el"]
        solph.constraints.equate_variables(
            model,
            model.InvestmentFlowBlock.invest[es.groups["cheap"], el, 0],
            model.InvestmentFlowBlock.invest[es.groups["second"], el, 0],
            2,
        )

    pyomo_model = PyomoModel(build())
    add(pyomo_model)
    pyomo = pyomo_model.solve(solver="highs")
    linopy_model = LinopyModel(build())
    add(linopy_model)
    linopy_ = linopy_model.solve(solver="highs")
    assert linopy_.solver["objective"] == pytest.approx(
        pyomo.solver["objective"], rel=1e-6
    )


def test_constraint_functions_from_flow_count_example():
    """limit_active_flow_count_by_keyword on both backends."""

    def build():
        es = _es()
        el = solph.Bus("el")
        es.add(el)
        for k in range(3):
            es.add(
                solph.components.Source(
                    f"unit {k}",
                    outputs={
                        el: solph.Flow(
                            nominal_capacity=3,
                            minimum=0.3,
                            variable_costs=10 + k,
                            nonconvex=solph.NonConvex(),
                            custom_properties={"keyword1": "group"},
                        )
                    },
                )
            )
        es.add(
            solph.components.Source(
                "grid", outputs={el: solph.Flow(variable_costs=PRICE)}
            ),
            solph.components.Sink(
                "demand",
                inputs={el: solph.Flow(fix=DEMAND / 5, nominal_capacity=5)},
            ),
        )
        return es

    def run(model_class):
        model = model_class(build())
        solph.constraints.limit_active_flow_count_by_keyword(
            model, "keyword1", lower_limit=1, upper_limit=2
        )
        return model.solve(solver="highs")

    assert run(LinopyModel).solver["objective"] == pytest.approx(
        run(PyomoModel).solver["objective"], rel=1e-6
    )


def test_equate_flows_equivalence():
    def build():
        return _two_party_storage_system()

    def add(model):
        g = model.es.groups
        solph.constraints.equate_flows(
            model,
            [(g["grid a"], g["el a"])],
            [(g["grid b"], g["el b"])],
            factor1=1,
        )

    pyomo_model = PyomoModel(build())
    add(pyomo_model)
    linopy_model = LinopyModel(build())
    add(linopy_model)
    assert linopy_model.solve(solver="highs").solver[
        "objective"
    ] == pytest.approx(
        pyomo_model.solve(solver="highs").solver["objective"], rel=1e-6
    )


def test_assert_backends_agree_is_importable():
    assert callable(assert_backends_agree)


def test_pyomo_components_are_refused():
    """A Pyomo constraint assigned to a LinopyModel must not be ignored."""
    model = LinopyModel(_two_party_storage_system())
    with pytest.raises(TypeError, match="Pyomo component"):
        model.my_limit = po.Constraint(rule=lambda m: po.Constraint.Skip)
