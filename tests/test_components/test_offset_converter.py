from oemof import solph
from oemof.solph._plumbing import sequence
import numpy as np
import pytest


def create_energysystem_stub(num_in, num_out):

    es = solph.EnergySystem(timeindex=solph.create_time_index(year=2023, number=9), infer_last_interval=True)

    for i in range(num_in):
        bus_label = f"bus input {i}"
        b = solph.Bus(bus_label)
        es.add(b)
        es.add(solph.components.Source(f"source {i}", outputs={b: solph.Flow()}))

    for o in range(num_out):
        bus_label = f"bus output {o}"
        b = solph.Bus(bus_label)
        es.add(b)
        es.add(solph.components.Sink(f"sink {o}", inputs={b: solph.Flow()}))

    return es


def calculate_slope_and_offset_with_reference_to_input(P_max, P_min, eta_max, eta_min):
    slope = (P_max * eta_max - P_min * eta_min) / (P_max - P_min)
    offset = eta_max - slope
    return slope, offset


def calculate_slope_and_offset_with_reference_to_output(P_max, P_min, eta_max, eta_min):
    slope = (P_max / eta_max - P_min / eta_min) / (P_max - P_min)
    offset = 1 / eta_max - slope
    return slope, offset

def solve_and_extract_results(es):
    model = solph.Model(es)
    model.solve("gurobi")
    return solph.views.convert_keys_to_strings(model.results())


def add_OffsetConverter(es, reference_bus, nominal_value, minimal_value, eta_at_nom, eta_at_min):

    oc_inputs = {b: solph.Flow() for label, b in es.node.items() if "bus input" in label}
    oc_outputs = {b: solph.Flow() for label, b in es.node.items() if "bus output" in label}

    if reference_bus in oc_outputs:
        f = oc_outputs[reference_bus]
        get_slope_and_offset = calculate_slope_and_offset_with_reference_to_output
        fix = [0] + np.linspace(minimal_value, nominal_value, 9).tolist()
    else:
        f = oc_inputs[reference_bus]
        get_slope_and_offset = calculate_slope_and_offset_with_reference_to_input
        fix = [0] + np.linspace(minimal_value * eta_at_min[es.node["bus output 0"]], nominal_value * eta_at_nom[es.node["bus output 0"]], 9).tolist()

    fix_flow = es.flows()[es.node["bus output 0"], es.node["sink 0"]]
    fix_flow.fix = fix
    fix_flow.nominal_value = 1

    es.add(solph.components.Source("slack source", outputs={es.node["bus output 0"]: solph.Flow(variable_costs=1000)}))

    slopes = {}
    offsets = {}

    for bus in list(oc_inputs) + list(oc_outputs):
        if bus == reference_bus:
            continue
        slope, offset = get_slope_and_offset(nominal_value, minimal_value, eta_at_nom[bus], eta_at_min[bus])
        slopes[bus] = slope
        offsets[bus] = offset

    f.nonconvex = solph.NonConvex()
    f.nominal_value = nominal_value
    f.min = sequence(minimal_value / nominal_value)

    oc = solph.components.OffsetConverter(
        label="offset converter",
        inputs=oc_inputs,
        outputs=oc_outputs,
        conversion_factors=slopes,
        normed_offsets=offsets
    )

    es.add(oc)


def test_OffsetConverter_single_input_single_output_with_output_reference():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_value = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus input 0"]: 0.7}
    eta_at_min = {es.groups["bus input 0"]: 0.5}

    add_OffsetConverter(es, es.groups["bus output 0"], nominal_value, minimal_value, eta_at_nom, eta_at_min)

    results = solve_and_extract_results(es)
    efficiency = (
        results["offset converter", "bus output 0"]["sequences"]["flow"]
        / results["bus input 0", "offset converter"]["sequences"]["flow"]
    )

    checksum = 5.622
    assert pytest.approx(efficiency.sum(), abs=0.001) == checksum


def test_OffsetConverter_single_input_single_output_with_output_reference_eta_decreasing():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_value = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus input 0"]: 0.5}
    eta_at_min = {es.groups["bus input 0"]: 0.7}

    add_OffsetConverter(es, es.groups["bus output 0"], nominal_value, minimal_value, eta_at_nom, eta_at_min)

    results = solve_and_extract_results(es)
    efficiency = (
        results["offset converter", "bus output 0"]["sequences"]["flow"]
        / results["bus input 0", "offset converter"]["sequences"]["flow"]
    )

    checksum = 5.028
    assert pytest.approx(efficiency.sum(), abs=0.001) == checksum


def test_OffsetConverter_single_input_single_output_with_input_reference():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_value = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus output 0"]: 0.7}
    eta_at_min = {es.groups["bus output 0"]: 0.5}

    add_OffsetConverter(es, es.groups["bus input 0"], nominal_value, minimal_value, eta_at_nom, eta_at_min)

    results = solve_and_extract_results(es)
    efficiency = (
        results["offset converter", "bus output 0"]["sequences"]["flow"]
        / results["bus input 0", "offset converter"]["sequences"]["flow"]
    )

    checksum = 5.700
    assert pytest.approx(efficiency.sum(), abs=0.001) == checksum


def test_OffsetConverter_single_input_single_output_with_input_reference_eta_decreasing():
    num_in = 1
    num_out = 1
    es = create_energysystem_stub(num_in, num_out)

    nominal_value = 10
    minimal_value = 3

    eta_at_nom = {es.groups["bus output 0"]: 0.5}
    eta_at_min = {es.groups["bus output 0"]: 0.7}

    add_OffsetConverter(es, es.groups["bus input 0"], nominal_value, minimal_value, eta_at_nom, eta_at_min)

    results = solve_and_extract_results(es)
    efficiency = (
        results["offset converter", "bus output 0"]["sequences"]["flow"]
        / results["bus input 0", "offset converter"]["sequences"]["flow"]
    )

    checksum = 5.099
    assert pytest.approx(efficiency.sum(), abs=0.001) == checksum
