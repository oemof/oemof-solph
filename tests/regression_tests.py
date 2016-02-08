from oemof.core.energy_system import EnergySystem as ES, Simulation
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components.sinks import Simple as Sink
from oemof.core.network.entities.components.transformers import Storage
from oemof.solph.optimization_model import OptimizationModel as OM
from oemof.solph import predefined_objectives as po

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

