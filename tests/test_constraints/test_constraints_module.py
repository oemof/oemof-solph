import pandas as pd

from oemof import solph


def test_special():
    date_time_index = pd.date_range("1/1/2012", periods=5, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bel = solph.buses.Bus(label="electricityBus")
    flow1 = solph.flows.Flow(
        nominal_value=100,
        custom_attributes={"my_factor": 0.8},
    )
    flow2 = solph.flows.Flow(nominal_value=50)
    src1 = solph.components.Source(label="source1", outputs={bel: flow1})
    src2 = solph.components.Source(label="source2", outputs={bel: flow2})
    energysystem.add(bel, src1, src2)
    model = solph.Model(energysystem)
    flow_with_keyword = {
        (src1, bel): flow1,
    }
    solph.constraints.generic_integral_limit(
        model, "my_factor", flow_with_keyword, limit=777
    )


def test_something_else():
    date_time_index = pd.date_range("1/1/2012", periods=5, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=True
    )
    bel1 = solph.buses.Bus(label="electricity1")
    bel2 = solph.buses.Bus(label="electricity2")
    energysystem.add(bel1, bel2)
    energysystem.add(
        solph.components.Converter(
            label="powerline_1_2",
            inputs={bel1: solph.flows.Flow()},
            outputs={
                bel2: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=20)
                )
            },
        )
    )
    energysystem.add(
        solph.components.Converter(
            label="powerline_2_1",
            inputs={bel2: solph.flows.Flow()},
            outputs={
                bel1: solph.flows.Flow(
                    nominal_value=solph.Investment(ep_costs=20)
                )
            },
        )
    )
    om = solph.Model(energysystem)
    line12 = energysystem.groups["powerline_1_2"]
    line21 = energysystem.groups["powerline_2_1"]
    solph.constraints.equate_variables(
        om,
        om.InvestmentFlowBlock.invest[line12, bel2, 0],
        om.InvestmentFlowBlock.invest[line21, bel1, 0],
        name="my_name",
    )
