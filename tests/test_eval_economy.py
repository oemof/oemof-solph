from oemof import solph


def results_opex():

    date_time_index = solph.create_time_index(2025, number=4)

    # create the energysystem and assign the time index
    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    el_bus = solph.buses.Bus("el_bus")
    heat_bus = solph.buses.Bus("heat_bus")

    energysystem.add(el_bus, heat_bus)

    source = solph.components.Source(
        "source",
        outputs={
            el_bus: solph.flows.Flow(variable_costs=[10, 15, 20, 30, 15])
        },
    )

    demand = solph.components.Sink(
        "heat_demand",
        inputs={
            heat_bus: solph.flows.Flow(fix=[15, 42, 3, 9, 12], nominal_value=1)
        },
    )

    hp = solph.components.Converter(
        "heat_pump",
        inputs={el_bus: solph.flows.Flow()},
        outputs={heat_bus: solph.flows.Flow()},
        conversion_factors={el_bus: 1 / 3},
    )

    energysystem.add(source, demand, hp)

    energysystem_model = solph.Model(energysystem)

    energysystem_model.solve(solver="cbc", solve_kwargs={"tee": True})

    results = solph.Results(energysystem_model)

    assert results.to_df("variable_costs").iloc[:, 2].values == [
        50,
        210,
        20,
        90,
        60,
    ]


def results_capex():

    date_time_index = solph.create_time_index(2025, number=4)

    # create the energysystem and assign the time index
    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    el_bus = solph.buses.Bus("el_bus")
    heat_bus = solph.buses.Bus("heat_bus")

    energysystem.add(el_bus, heat_bus)

    source = solph.components.Source(
        "source",
        outputs={el_bus: solph.flows.Flow()},
    )

    demand = solph.components.Sink(
        "heat_demand",
        inputs={
            heat_bus: solph.flows.Flow(fix=[15, 42, 3, 9, 12], nominal_value=1)
        },
    )

    hp = solph.components.Converter(
        "heat_pump",
        inputs={el_bus: solph.flows.Flow()},
        outputs={
            heat_bus: solph.flows.Flow(
                solph.Investment(ep_costs=100, fixed_costs=200)
            )
        },
        conversion_factors={el_bus: 1 / 3},
    )

    energysystem.add(source, demand, hp)

    energysystem_model = solph.Model(energysystem)

    energysystem_model.solve(solver="cbc", solve_kwargs={"tee": True})

    results = solph.Results(energysystem_model)

    assert results.to_df("investment_costs").iloc[0, 0] == 42 * 100 + 200


def results_storage():
    date_time_index = solph.create_time_index(2025, number=4)

    # create the energysystem and assign the time index
    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )

    bus = solph.buses.Bus("bus")
    energysystem.add(bus)

    source = solph.components.Source(
        "source",
        outputs={
            bus: solph.flows.Flow(fix=[20, 20, 10, 0, 0], nominal_value=1)
        },
    )

    demand = solph.components.Sink(
        "demand",
        inputs={bus: solph.flows.Flow(fix=10, nominal_value=1)},
    )

    storage = solph.components.GenericStorage(
        "storage",
        inputs={bus: solph.flows.Flow(solph.Investment(ep_costs=10))},
        outputs={bus: solph.flows.Flow()},
        nominal_capacity=solph.Investment(ep_costs=100),
    )
    energysystem.add(source, demand, storage)

    energysystem_model = solph.Model(energysystem)

    energysystem_model.solve(solver="cbc", solve_kwargs={"tee": True})

    results = solph.Results(energysystem_model)

    assert results.to_df("investment_costs").iloc[0, 0] == 100
    assert results.to_df("investment_costs").iloc[0, 1] == 2000
