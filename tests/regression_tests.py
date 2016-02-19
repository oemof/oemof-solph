from oemof.core.energy_system import EnergySystem as ES, Simulation
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components.sinks import Simple as Sink
from oemof.core.network.entities.components.sources import FixedSource as FS
from oemof.core.network.entities.components.transformers import Storage
from oemof.outputlib.to_pandas import ResultsDataFrame as RDF
from oemof.solph.optimization_model import OptimizationModel as OM
from oemof.solph import predefined_objectives as po

from nose.tools import eq_, ok_
import pandas as pd

import logging

def test_issue_74():
    logging.disable(logging.CRITICAL)

    Storage.optimization_options.update({'investment': True})
    sim = Simulation(timesteps=[0],
                     objective_options={'function': po.minimize_cost})
    es  = ES(simulation=sim)
    bus = Bus(uid="bus")
    store = Storage(uid="store", inputs=[bus], outputs=[bus], c_rate_out=0.1,
                    c_rate_in=0.1)
    sink  = Sink(uid="sink", inputs=[bus], val=[1])

    om = OM(es)
    om.objective.set_value(-1)
    es.results=om.results()

    try:
        es.dump()
    except AttributeError:
        assert False, "EnergySystem#dump should not raise `AttributeError`."

def test_bus_to_sink_outputs_in_results_dataframe():
    logging.disable(logging.CRITICAL)
    failed = False
    # TODO: Show this to the other devs as an example why class level variables
    #       for program flow are bad (globals in disuise).
    Storage.optimization_options.update({'investment': False})
    FS.optimization_options.update({'investment': False})

    sim = Simulation(timesteps=[0],
                     objective_options={'function': po.minimize_cost})
    tix = time_index=pd.period_range('1970-01-01', periods=1, freq='H')
    es  = ES(simulation=sim, time_idx=tix)
    bus = Bus(uid="bus")
    source = FS(uid="source", outputs=[bus], val=[0.5], out_max=[1])
    sink  = Sink(uid="sink", inputs=[bus], val=[1])

    om = OM(es)
    es.results=om.results()
    es.results[bus][sink] = [0.7]
    rdf = RDF(energy_system=es)
    try:
        eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"),:
                    ].val[0],
            0.7,
            "Output from bus to sink does not have the correct value.")
    except KeyError:
        failed = True
    if failed:
        assert False, \
               "Output from bus to sink does not appear in results dataframe."

    es.results[bus][bus] = [-1]
    rdf = RDF(energy_system=es)
    try:
        eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"),:
                    ].val[0],
            0.7,
            "Output from bus to sink does not have the correct value.")
    except KeyError:
        failed = True
    if failed:
        assert False, \
               ("Output from bus (with duals) to sink " +
                "does not appear in results dataframe.")

