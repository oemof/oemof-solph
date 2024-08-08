import pandas as pd
import pytest

from oemof import solph


def test_initial_status_off():
    date_time_index = pd.date_range("1/1/2012", periods=10, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bus = solph.buses.Bus(label="electricityBus", balanced=False)
    energysystem.add(bus)

    # negative costs but turned off initially
    flow = solph.flows.Flow(
        nominal_value=10,
        nonconvex=solph.NonConvex(initial_status=0, minimum_downtime=5),
        variable_costs=-1,
    )
    bus.inputs[bus] = flow

    model = solph.Model(energysystem)

    model.solve()

    results = solph.processing.results(model)

    assert (
        results[(bus, bus)]["sequences"]["flow"][:-1] == 5 * [0] + 5 * [10]
    ).all()


@pytest.mark.skip(reason="Reported issue (see #1099).")
def test_initial_status_on():
    date_time_index = pd.date_range("1/1/2012", periods=10, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bus = solph.buses.Bus(label="electricityBus", balanced=False)
    energysystem.add(bus)

    # positive costs but turned on initially
    flow = solph.flows.Flow(
        nominal_value=10,
        nonconvex=solph.NonConvex(initial_status=1, minimum_uptime=3),
        variable_costs=1,
    )
    bus.inputs[bus] = flow

    model = solph.Model(energysystem)

    model.solve()

    results = solph.processing.results(model)

    assert (
        results[(bus, bus)]["sequences"]["flow"][:-1] == 3 * [10] + 7 * [0]
    ).all()
