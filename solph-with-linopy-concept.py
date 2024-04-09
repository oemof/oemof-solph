import pandas as pd
import linopy
from oemof import solph

import pyinstrument


run_model = pyinstrument.Profiler()
setup_model = pyinstrument.Profiler()


class BasicBlock:

    def __init__(self) -> None:
        pass

    def _create_variables(self, es, group=None):
        pass

    def _create_constraints(self, es, group=None):
        pass

    def _create_obejctive(self, es, group=None):
        pass


class SimpleFlowBlockLinopy(BasicBlock):

    def _create_variables(self, es, group=None):
        if group is None:
            return

        flow_labels = [f"{n[0]}--{n[1]}" for n in group]

        variables = es.m.add_variables(
            lower=0,
            name="_all_flow_variables",
            coords=[es.TIMESTEPS, flow_labels],
            dims=["time", "flow"]
        )

        for n, label in zip(group, flow_labels):

            if n[2].nominal_value is not None:
                n[2].min[len(es.TIMESTEPS) - 1]
                variables.lower.loc[:, label] = list(n[2].min)

                n[2].max[len(es.TIMESTEPS) - 1]
                variables.upper.loc[:, label] = list(n[2].max)

                if len(n[2].fix) > 1:
                    variables.lower.loc[:, label] = n[2].fix
                    variables.upper.loc[:, label] = n[2].fix
                elif n[2].fix[0] is not None:
                    variables.lower.loc[:, label] = n[2].fix[0]
                    variables.upper.loc[:, label] = n[2].fix[0]

                variables.lower.loc[:, label] *= n[2].nominal_value
                variables.upper.loc[:, label] *= n[2].nominal_value

    def _create_obejctive(self, es, group=None):
        if group is None:
            return

        variables = es.m.variables["_all_flow_variables"]

        for n in group:
            n[2].variable_costs[len(es.TIMESTEPS) - 1]
            es.m.objective += variables.loc[:, f"{n[0]}--{n[1]}"] * list(n[2].variable_costs) * es.objective_weighting.tolist()


class BusBlockLinopy(BasicBlock):

    def _create_constraints(self, es, group=None):
        if group is None:
            return

        variables = es.m.variables["_all_flow_variables"]

        for n in group:
            flow_labels_in = [f"{i.label}--{n.label}" for i in n.inputs]
            flow_labels_out = [f"{n.label}--{o.label}" for o in n.outputs]

            constraint = (
                variables.loc[:, flow_labels_in].sum(dims="flow")
                ==
                variables.loc[:, flow_labels_out].sum(dims="flow")
            )
            es.m.add_constraints(constraint, name=f"{n.label} balance")


class ConverterBlockLinopy(BasicBlock):

    def _create_constraints(self, es, group=None):
        if group is None:
            return

        flows = es.m.variables["_all_flow_variables"]
        for n in group:
            for c in n.conversion_factors.values():
                c[len(es.TIMESTEPS) - 1]

            ins = [i for i in n.inputs]
            outs = [o for o in n.outputs]

            for o in outs:
                flow_label_out = f"{n.label}--{o.label}"
                for i in ins:
                    flow_label_in = f"{i.label}--{n.label}"
                    constraint = (
                        flows.loc[:, flow_label_in] * list(n.conversion_factors[o])
                        ==
                        flows.loc[:, flow_label_out] * list(n.conversion_factors[i])
                    )
                    constraint_name = f"{n.label} conversion {i.label} to {o.label}"

                    if constraint_name in es.m.constraints:
                        es.m.remove_constraints(constraint_name)

                    es.m.add_constraints(constraint, name=constraint_name)


class EnergySystemLinopy(solph.EnergySystem):

    def __init__(self, timeindex=None, timeincrement=None, infer_last_interval=None, periods=None, use_remaining_value=False, groupings=None):
        super().__init__(timeindex, timeincrement, infer_last_interval, periods, use_remaining_value, groupings)
        self.m = linopy.Model()
        self.TIMESTEPS = self.timeincrement.index.values
        self.objective_weighting = self.timeincrement.values

    def _build(self):
        all_groups = self.groups
        sfbl = SimpleFlowBlockLinopy()
        sfbl._create_variables(self, all_groups[solph.flows._simple_flow_block.SimpleFlowBlock])

        BusBlockLinopy()._create_constraints(self, all_groups[solph.buses._bus.BusBlock])
        ConverterBlockLinopy()._create_constraints(self, all_groups[solph.components._converter.ConverterBlock])

        sfbl._create_obejctive(self, all_groups[solph.flows._simple_flow_block.SimpleFlowBlock])
        pass


    def flows(self):
        return {f"{k[0]}--{k[1]}": v for k, v in super().flows().items()}


setup_model.start()

es = EnergySystemLinopy(timeindex=solph.create_time_index(2012, number=8760))

b1 = solph.Bus(label="b1")
b2 = solph.Bus(label="b2")

source = solph.components.Source(
    label="source", outputs={b1: solph.Flow(variable_costs=5)}
)
sink = solph.components.Sink(
    label="sink", inputs={b2: solph.Flow(nominal_value=1, fix=1)}
)

converter = solph.components.Converter(
    label="converter",
    inputs={b1: solph.Flow()},
    outputs={b2: solph.Flow(nominal_value=10)},
    conversion_factors={b2: 0.9}
)

es.add(b1, b2, source, sink, converter)

es._build()

setup_model.stop()

run_model.start()

es.groups
es.m.solve(solver_name="highs")

df = pd.pivot_table(index="time", columns="flow", data=es.m.solution.to_dataframe())
print(df)

es.m.constraints

from oemof.solph._plumbing import sequence
converter.conversion_factors[b2] = sequence(0.8)

# selectively rebuild one constraint
ConverterBlockLinopy()._create_constraints(es, es.groups[solph.components._converter.ConverterBlock])

es.m.solve(solver_name="highs")
df = pd.pivot_table(index="time", columns="flow", data=es.m.solution.to_dataframe())
print(df)

run_model.stop()

with open("run.html", "w") as f:
    f.write(run_model.output_html())

with open("setup.html", "w") as f:
    f.write(setup_model.output_html())
