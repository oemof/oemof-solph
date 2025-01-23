import warnings

import numpy as np
import pytest
from oemof.tools.debugging import ExperimentalFeatureWarning

from oemof import solph
from oemof.solph._plumbing import sequence
from oemof.solph.components._offset_converter import (
    slope_offset_from_nonconvex_input,
)
from oemof.solph.components._offset_converter import (
    slope_offset_from_nonconvex_output,
)


def create_energysystem_stub(num_in, num_out):
    es = solph.EnergySystem(
        timeindex=solph.create_time_index(year=2023, number=9),
        infer_last_interval=True,
    )

    for i in range(num_in):
        bus_label = f"bus input {i}"
        b = solph.Bus(bus_label)
        es.add(b)
        es.add(
            solph.components.Source(f"source {i}", outputs={b: solph.Flow()})
        )

    for o in range(num_out):
        bus_label = f"bus output {o}"
        b = solph.Bus(bus_label)
        es.add(b)
        es.add(solph.components.Sink(f"sink {o}", inputs={b: solph.Flow()}))

    return es


def solve_and_extract_results(es):
    model = solph.Model(es)
    model.solve("cbc")
    results = solph.views.convert_keys_to_strings(model.results())

    assert (
        model.solver_results["Solver"][0]["Termination condition"]
        != "infeasible"
    )
    return results


def check_results(
    results,
    reference_bus,
    nominal_capacity,
    minimal_value,
    eta_at_nom,
    eta_at_min,
):
    for bus in eta_at_nom:
        if "input" in reference_bus.label:
            slope, offset = slope_offset_from_nonconvex_input(
                1,
                minimal_value / nominal_capacity,
                eta_at_nom[bus],
                eta_at_min[bus],
            )
            reference_flow = results[reference_bus.label, "offset converter"][
                "sequences"
            ]["flow"]
            reference_flow_status = results[
                reference_bus.label, "offset converter"
            ]["sequences"]["status"]
        else:
            slope, offset = slope_offset_from_nonconvex_output(
                1,
                minimal_value / nominal_capacity,
                eta_at_nom[bus],
                eta_at_min[bus],
            )
            reference_flow = results["offset converter", reference_bus.label][
                "sequences"
            ]["flow"]
            reference_flow_status = results[
                "offset converter", reference_bus.label
            ]["sequences"]["status"]

        flow_expected = (
            offset * nominal_capacity * reference_flow_status
            + slope * reference_flow
        )
        if "input" in bus.label:
            flow_actual = results[bus.label, "offset converter"]["sequences"][
                "flow"
            ]
        else:
            flow_actual = results["offset converter", bus.label]["sequences"][
                "flow"
            ]

        np.testing.assert_array_almost_equal(flow_actual, flow_expected)


def add_OffsetConverter(
    es, reference_bus, nominal_capacity, minimal_value, eta_at_nom, eta_at_min
):
    # Use of experimental API to access nodes by label.
    # Can be removed with future release of network.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        oc_inputs = {
            b: solph.Flow()
            for label, b in es.node.items()
            if "bus input" in label
        }
        oc_outputs = {
            b: solph.Flow()
            for label, b in es.node.items()
            if "bus output" in label
        }

        if reference_bus in oc_outputs:
            f = oc_outputs[reference_bus]
            get_slope_and_offset = slope_offset_from_nonconvex_output
            fix = [0] + np.linspace(
                minimal_value, nominal_capacity, 9
            ).tolist()
        else:
            f = oc_inputs[reference_bus]
            get_slope_and_offset = slope_offset_from_nonconvex_input
            fix = [0] + np.linspace(
                minimal_value * eta_at_min[es.node["bus output 0"]],
                nominal_capacity * eta_at_nom[es.node["bus output 0"]],
                9,
            ).tolist()

        fix_flow = es.flows()[es.node["bus output 0"], es.node["sink 0"]]
        fix_flow.fix = fix
        fix_flow.nominal_capacity = 1

        slopes = {}
        offsets = {}

        for bus in list(oc_inputs) + list(oc_outputs):
            if bus == reference_bus:
                continue
            slope, offset = get_slope_and_offset(
                1,
                minimal_value / nominal_capacity,
                eta_at_nom[bus],
                eta_at_min[bus],
            )
            slopes[bus] = slope
            offsets[bus] = offset

        f.nonconvex = solph.NonConvex()
        f.nominal_capacity = nominal_capacity
        f.min = sequence(minimal_value / nominal_capacity)

        oc = solph.components.OffsetConverter(
            label="offset converter",
            inputs=oc_inputs,
            outputs=oc_outputs,
            conversion_factors=slopes,
            normed_offsets=offsets,
        )

        es.add(oc)


def test_custom_properties():
    bus1 = solph.Bus()
    bus2 = solph.Bus()
    oc = solph.components.OffsetConverter(
        inputs={
            bus1: solph.Flow(nominal_capacity=2, nonconvex=solph.NonConvex())
        },
        outputs={bus2: solph.Flow()},
        conversion_factors={bus2: 2},
        normed_offsets={bus2: -0.5},
        custom_properties={"foo": "bar"},
    )

    assert oc.custom_properties["foo"] == "bar"


def test_invalid_conversion_factor():
    bus1 = solph.Bus()
    bus2 = solph.Bus()
    with pytest.raises(ValueError, match="Conversion factors cannot be "):
        solph.components.OffsetConverter(
            inputs={
                bus1: solph.Flow(
                    nominal_capacity=2, nonconvex=solph.NonConvex()
                )
            },
            outputs={bus2: solph.Flow()},
            conversion_factors={
                bus1: 1,
                bus2: 2,
            },
            normed_offsets={bus2: -0.5},
        )


def test_invalid_normed_offset():
    bus1 = solph.Bus()
    bus2 = solph.Bus()
    with pytest.raises(ValueError, match="Normed offsets cannot be "):
        solph.components.OffsetConverter(
            inputs={
                bus1: solph.Flow(
                    nominal_capacity=2, nonconvex=solph.NonConvex()
                )
            },
            outputs={bus2: solph.Flow()},
            conversion_factors={
                bus2: 2,
            },
            normed_offsets={
                bus1: -0.2,
                bus2: -0.5,
            },
        )


def test_wrong_number_of_coefficients():
    bus1 = solph.Bus()
    bus2 = solph.Bus()
    with pytest.raises(ValueError, match="Two coefficients"):
        solph.components.OffsetConverter(
            inputs={
                bus1: solph.Flow(
                    nominal_capacity=2, nonconvex=solph.NonConvex()
                )
            },
            outputs={bus2: solph.Flow()},
            coefficients=(1, 2, 3),
        )


def test_OffsetConverter_single_input_output_ref_output():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus input 0"]: 0.7}
    eta_at_min = {es.groups["bus input 0"]: 0.5}

    add_OffsetConverter(
        es,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_OffsetConverter_single_input_output_ref_output_eta_decreasing():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus input 0"]: 0.5}
    eta_at_min = {es.groups["bus input 0"]: 0.7}

    add_OffsetConverter(
        es,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_OffsetConverter_single_input_output_ref_input():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus output 0"]: 0.7}
    eta_at_min = {es.groups["bus output 0"]: 0.5}

    add_OffsetConverter(
        es,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_OffsetConverter_single_input_output_ref_input_eta_decreasing():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus output 0"]: 0.5}
    eta_at_min = {es.groups["bus output 0"]: 0.7}

    add_OffsetConverter(
        es,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_OffsetConverter_double_input_output_ref_input():
    num_in = 2
    num_out = 2
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {
        es.groups["bus output 0"]: 0.7,
        es.groups["bus output 1"]: 0.2,
        es.groups["bus input 1"]: 0.2,
    }
    eta_at_min = {
        es.groups["bus output 0"]: 0.5,
        es.groups["bus output 1"]: 0.3,
        es.groups["bus input 1"]: 0.2,
    }

    add_OffsetConverter(
        es,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus input 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_OffsetConverter_double_input_output_ref_output():
    num_in = 2
    num_out = 2

    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {
        es.groups["bus input 0"]: 0.7,
        es.groups["bus output 1"]: 0.2,
        es.groups["bus input 1"]: 0.2,
    }
    eta_at_min = {
        es.groups["bus input 0"]: 0.5,
        es.groups["bus output 1"]: 0.3,
        es.groups["bus input 1"]: 0.2,
    }

    add_OffsetConverter(
        es,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    results = solve_and_extract_results(es)

    check_results(
        results,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )


def test_two_OffsetConverters_with_and_without_investment():
    num_in = 1
    num_out = 1

    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    eta_at_nom = {
        es.groups["bus input 0"]: 0.7,
    }
    eta_at_min = {
        es.groups["bus input 0"]: 0.5,
    }

    add_OffsetConverter(
        es,
        es.groups["bus output 0"],
        nominal_capacity,
        minimal_value,
        eta_at_nom,
        eta_at_min,
    )

    input_bus = es.groups["bus input 0"]

    oc = solph.components.OffsetConverter(
        label="investment offset converter",
        inputs={input_bus: solph.Flow()},
        outputs={
            es.groups["bus output 0"]: solph.Flow(
                nonconvex=solph.NonConvex(),
                nominal_capacity=solph.Investment(
                    maximum=nominal_capacity, ep_costs=10
                ),
            )
        },
        conversion_factors={input_bus: 1},
        normed_offsets={input_bus: 0},
    )

    es.add(oc)

    # Use of experimental API to access nodes by label.
    # Can be removed with future release of network.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", ExperimentalFeatureWarning)
        fix_flow = es.flows()[es.node["bus output 0"], es.node["sink 0"]]
        fix_flow.fix = [v * 2 for v in fix_flow.fix]
    # if the model solves it is feasible
    _ = solve_and_extract_results(es)


def test_OffsetConverter_05x_compatibility():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_capacity = 10
    minimal_value = 3

    # Use of experimental API to access nodes by label.
    # Can be removed with future release of network.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ExperimentalFeatureWarning)
        fix = [0] + np.linspace(minimal_value, nominal_capacity, 9).tolist()
        fix_flow = es.flows()[es.node["bus output 0"], es.node["sink 0"]]
        fix_flow.fix = fix
        fix_flow.nominal_capacity = 1

    eta_at_nom = 0.7
    eta_at_min = 0.5

    slope = (nominal_capacity - minimal_value) / (
        nominal_capacity / eta_at_nom - minimal_value / eta_at_min
    )
    offset = minimal_value / nominal_capacity * (1 - slope / eta_at_min)

    warnings.filterwarnings("ignore", "", DeprecationWarning)
    oc = solph.components.OffsetConverter(
        label="offset converter",
        inputs={es.groups["bus input 0"]: solph.Flow()},
        outputs={
            es.groups["bus output 0"]: solph.Flow(
                nonconvex=solph.NonConvex(),
                nominal_capacity=nominal_capacity,
                min=minimal_value / nominal_capacity,
            )
        },
        coefficients=(offset, slope),
    )

    es.add(oc)
    warnings.filterwarnings("always", "", DeprecationWarning)

    results = solve_and_extract_results(es)

    slope, offset = slope_offset_from_nonconvex_output(
        1, minimal_value / nominal_capacity, 0.7, 0.5
    )
    output_flow = results["offset converter", "bus output 0"]["sequences"][
        "flow"
    ]
    output_flow_status = results["offset converter", "bus output 0"][
        "sequences"
    ]["status"]

    input_flow_expected = (
        offset * nominal_capacity * output_flow_status + slope * output_flow
    )
    input_flow_actual = results["bus input 0", "offset converter"][
        "sequences"
    ]["flow"]

    np.testing.assert_array_almost_equal(
        input_flow_actual, input_flow_expected
    )


def test_error_handling():
    input_bus = solph.Bus("bus1")
    output_bus = solph.Bus("bus2")

    with pytest.raises(TypeError, match="cannot be used in combination"):
        warnings.filterwarnings("ignore", "", DeprecationWarning)
        _ = solph.components.OffsetConverter(
            label="offset converter",
            inputs={input_bus: solph.Flow()},
            outputs={
                output_bus: solph.Flow(
                    nonconvex=solph.NonConvex(),
                    nominal_capacity=10,
                    min=0.3,
                )
            },
            # values are arbitarty just to test the error
            coefficients=(-1, 0.4),
            conversion_factors={input_bus: 1},
            normed_offsets={input_bus: 0},
        )
        warnings.filterwarnings("always", "", DeprecationWarning)

        with pytest.raises(
            ValueError, match="Conversion factors cannot be specified for"
        ):
            _ = solph.components.OffsetConverter(
                label="offset converter",
                inputs={input_bus: solph.Flow()},
                outputs={
                    output_bus: solph.Flow(
                        nonconvex=solph.NonConvex(),
                        nominal_capacity=10,
                        min=0.3,
                    )
                },
                conversion_factors={input_bus: 1, output_bus: 1},
                normed_offsets={input_bus: 0},
            )

        with pytest.raises(
            ValueError, match="Normed offsets cannot be specified for"
        ):
            _ = solph.components.OffsetConverter(
                label="offset converter",
                inputs={input_bus: solph.Flow()},
                outputs={
                    output_bus: solph.Flow(
                        nonconvex=solph.NonConvex(),
                        nominal_capacity=10,
                        min=0.3,
                    )
                },
                conversion_factors={input_bus: 1},
                normed_offsets={input_bus: 0, output_bus: 0},
            )
