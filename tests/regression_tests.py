import logging

from nose.tools import eq_, ok_
import pandas as pd

from oemof.core.energy_system import EnergySystem as ES, Simulation
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components.sinks import Simple as Sink
from oemof.core.network.entities.components.sources import FixedSource as FS
from oemof.core.network.entities.components.transformers import Storage
from oemof.outputlib.to_pandas import ResultsDataFrame as RDF
from oemof.solph.optimization_model import OptimizationModel as OM
from oemof.solph import predefined_objectives as po

class TestSolphAndItsResults:
    def setup(self):
        logging.disable(logging.CRITICAL)

        self.failed = False

        sim = Simulation(timesteps=[0],
                         objective_options={'function': po.minimize_cost})
        tix = time_index = pd.period_range('1970-01-01', periods=1, freq='H')
        self.es = ES(simulation=sim, time_idx=tix)

        self.cleanup = []
        for k in [FS, Storage]:
            if 'investment' in k.optimization_options:
                value = k.optimization_options['investment']
                def f(k=k, value=value):
                    k.optimization_options['investment'] = value
                self.cleanup.append(f)
            else:
                def f(k=k):
                    if 'investment' in k.optimization_options:
                        del k.optimization_options['investment']
                self.cleanup.append(f)

    def teardown(self):
        logging.disable(logging.NOTSET)
        for f in self.cleanup: f()

    def test_issue_74(self):
        Storage.optimization_options.update({'investment': True})
        bus = Bus(uid="bus")
        store = Storage(uid="store", inputs=[bus], outputs=[bus], c_rate_out=0.1,
                        c_rate_in=0.1)
        sink = Sink(uid="sink", inputs=[bus], val=[1])

        es = self.es
        om = OM(es)
        om.objective.set_value(-1)
        es.results = om.results()

        try:
            es.dump()
        except AttributeError as ae:
            self.failed = ae
        if self.failed:
            ok_(False,
                "EnergySystem#dump should not raise `AttributeError`: \n" +
                " Error message: " + str(self.failed))

    def test_bus_to_sink_outputs_in_results_dataframe(self):
        bus = Bus(uid="bus")
        source = FS(uid="source", outputs=[bus], val=[0.5], out_max=[1])
        sink = Sink(uid="sink", inputs=[bus], val=[1])

        es = self.es
        om = OM(es)
        es.results = om.results()
        es.results[bus][sink] = [0.7]
        rdf = RDF(energy_system=es)
        try:
            eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"), :
                       ].val[0],
                0.7,
                "Output from bus to sink does not have the correct value.")
        except KeyError:
            self.failed = True
        if self.failed:
            ok_(False,
                "Output from bus to sink does not appear in results dataframe.")

        es.results[bus][bus] = [-1]
        rdf = RDF(energy_system=es)
        try:
            eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"), :
                       ].val[0],
                0.7,
                "Output from bus to sink does not have the correct value.")
        except KeyError:
            self.failed = True
        if self.failed:
            ok_(False,
                "Output from bus (with duals) to sink " +
                "does not appear in results dataframe.")


    def test_investment_defaults(self):
        for klass in [Storage, FS]:
            value = klass.optimization_options.get('investment')
            ok_(not value,
                "\n  Testing the default value at key 'investment' in \n    `" +
                str(klass) +
                ".optimization_options.`\n  Expected `False`, got `" +
                str(value) + "`.")

