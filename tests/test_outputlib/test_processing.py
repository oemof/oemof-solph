import pandas as pd

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import create_time_index
from oemof.solph import processing
from oemof.solph.buses import Bus
from oemof.solph.components import Sink
from oemof.solph.components import Source
from oemof.solph.flows import Flow


def test_custom_attribut_with_numeric_value():
    date_time_index = create_time_index(2012, number=6)
    energysystem = EnergySystem(timeindex=date_time_index)
    bs = Bus(label="bus")
    energysystem.add(bs)
    src_custom_int = Source(
        label="source_with_custom_attribute_int",
        outputs={bs: Flow(nominal_value=5, fix=[3] * 7)},
        custom_properties={"integer": 9},
    )
    s1 = pd.Series([1.4, 2.3], index=["a", "b"])
    snk_custom_float = Sink(
        label="source_with_custom_attribute_float",
        inputs={bs: Flow()},
        custom_properties={"numpy-float": s1["a"]},
    )
    src_custom_str = Source(
        label="source_with_custom_attribute_string",
        outputs={bs: Flow(nominal_value=5, fix=[3] * 7)},
        custom_properties={"string": "name"},
    )
    energysystem.add(snk_custom_float, src_custom_int, src_custom_str)

    # create optimization model based on energy_system
    optimization_model = Model(energysystem=energysystem)

    parameter = processing.parameter_as_dict(optimization_model)
    assert (
        parameter[snk_custom_float, None]["scalars"][
            "custom_properties_numpy-float"
        ]
        == 1.4
    )
    assert (
        parameter[src_custom_int, None]["scalars"]["custom_properties_integer"]
        == 9
    )
    assert (
        parameter[src_custom_str, None]["scalars"]["custom_properties_string"]
        == "name"
    )
