from nose import tools
from oemof import solph


@tools.raises(AttributeError)
def test_generic_storage():
    """Duplicate definition inflow."""
    bel = solph.Bus(label='bel')
    solph.components.GenericStorage(
        label='storage',
        nominal_capacity=45,
        inputs={bel: solph.Flow(nominal_value=5, variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=35)


@tools.raises(AttributeError)
def test_generic_storage():
    """Duplicate definition inflow."""
    bel = solph.Bus(label='bel')
    solph.components.GenericStorage(
        label='storage',
        nominal_capacity=45,
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(nominal_value=5, variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=35)


@tools.raises(AttributeError)
def test_generic_storage():
    """Nominal value defined with investment model."""
    bel = solph.Bus(label='bel')
    solph.components.GenericStorage(
        label='storage',
        nominal_capacity=45,
        inputs={bel: solph.Flow(variable_costs=10e10)},
        outputs={bel: solph.Flow(variable_costs=10e10)},
        capacity_loss=0.00, initial_capacity=0,
        nominal_input_capacity_ratio=1/6,
        nominal_output_capacity_ratio=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        fixed_costs=35,
        investment=solph.Investment(ep_costs=23))
