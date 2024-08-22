import numpy as np

from oemof import solph


def test_storage_level_constraint():
    n_time_steps = 10

    es = solph.EnergySystem(
        timeindex=solph.create_time_index("2022-01-01", number=n_time_steps),
        infer_last_interval=False,
    )

    multiplexer = solph.Bus(
        label="multiplexer",
    )

    storage_level = np.linspace(1, 0, num=n_time_steps + 1)

    storage = solph.components.GenericStorage(
        label="storage",
        nominal_capacity=3,
        initial_storage_level=1,
        balanced=True,
        storage_costs=0.1,
        min_storage_level=storage_level,
        inputs={multiplexer: solph.Flow()},
        outputs={multiplexer: solph.Flow()},
    )

    es.add(multiplexer, storage)

    in_100 = solph.components.Source(
        label="in_100",
        outputs={
            multiplexer: solph.Flow(nominal_capacity=5, variable_costs=0.1)
        },
    )
    in_050 = solph.components.Source(
        label="in_050",
        outputs={
            multiplexer: solph.Flow(nominal_capacity=5, variable_costs=0.1)
        },
    )
    in_000 = solph.components.Source(
        label="in_000",
        outputs={
            multiplexer: solph.Flow(nominal_capacity=5, variable_costs=0.1)
        },
    )

    out_000 = solph.components.Sink(
        label="out_000",
        inputs={multiplexer: solph.Flow(nominal_capacity=5)},
    )
    out_050 = solph.components.Sink(
        label="out_050",
        inputs={multiplexer: solph.Flow(nominal_capacity=5)},
    )
    out_100 = solph.components.Sink(
        label="out_100",
        inputs={multiplexer: solph.Flow(nominal_capacity=5)},
    )
    es.add(in_000, in_050, in_100, out_000, out_050, out_100)

    model = solph.Model(es)

    solph.constraints.storage_level_constraint(
        model=model,
        name="multiplexer",
        storage_component=storage,
        multiplexer_bus=multiplexer,
        input_levels={
            in_100: 1.0,
            in_050: 0.5,
        },  # in_000 is always active (implicit), no variable
        output_levels={
            out_100: 1.0,
            out_050: 0.5,
            out_000: 0.0,  # out_000 is always active (explicit)
        },
    )
    model.solve()

    my_results = solph.processing.results(model)

    assert list(
        my_results[(in_100, None)]["sequences"]["multiplexer_active_input"][
            :-1
        ]
    ) == n_time_steps * [0]
    assert list(
        my_results[(out_100, None)]["sequences"]["multiplexer_active_output"][
            :-1
        ]
    ) == (n_time_steps - 1) * [0] + [1]

    assert list(
        my_results[(in_050, None)]["sequences"]["multiplexer_active_input"][
            :-1
        ]
    ) == n_time_steps // 2 * [1] + n_time_steps // 2 * [0]
    assert list(
        my_results[(out_050, None)]["sequences"]["multiplexer_active_output"][
            :-1
        ]
    ) == n_time_steps // 2 * [1] + (n_time_steps // 2 - 1) * [0] + [1]

    assert list(
        my_results[(out_000, None)]["sequences"]["multiplexer_active_output"][
            :-1
        ]
    ) == n_time_steps * [1]
    assert (in_000, None) not in my_results.keys()
