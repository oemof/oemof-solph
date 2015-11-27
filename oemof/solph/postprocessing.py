# -*- coding: utf-8 -*-
"""
@author: Simon Hilpert simon.hilpert@fh-flensburg.de
"""

try:
    from network.entities import Bus, Component
    from network.entities import components as cp
except:
    from ..core.network.entities import Bus, Component
    from ..core.network.entities import components as cp
    from ..core.network.entities.components.transformers import Storage

def results_to_objects(instance):
    """ write the results from a pyomo optimization problem back to the
    oemof-objects

    Parameters
    ----------
    instance : solved OptimizationModel() instance containing the results
    """
    for entity in instance.entities:
        if (isinstance(entity, cp.Transformer) or
                isinstance(entity, cp.Source)):
            # write outputs
            O = [e.uid for e in entity.outputs[:]]
            for o in O:
                entity.results['out'][o] = []
                for t in instance.timesteps:
                    entity.results['out'][o].append(
                        instance.w[entity.uid, o, t].value)

            I = [i.uid for i in entity.inputs[:]]
            for i in I:
                entity.results['in'][i] = []
                for t in instance.timesteps:
                    entity.results['in'][i].append(
                        instance.w[i, entity.uid, t].value)

        if isinstance(entity, cp.sources.DispatchSource):
            entity.results['in'][entity.uid] = []
            for t in instance.timesteps:
                entity.results['in'][entity.uid].append(
                    instance.w[entity.uid, entity.outputs[0].uid, t].bounds[1])

        # write results to instance.simple_sink_objs
        # (will be the value of simple sink in general)
        if isinstance(entity, cp.Sink):
            i = entity.inputs[0].uid
            entity.results['in'][i] = []
            for t in instance.timesteps:
                entity.results['in'][i].append(
                    instance.w[i, entity.uid, t].value)
        if isinstance(entity, cp.transformers.Storage):
            entity.results['cap'] = []
            for t in instance.timesteps:
                entity.results['cap'].append(
                    getattr(instance, str(Storage)).cap[entity.uid, t].value)


def bus_duals_to_objects(instance):
    """ Extracts values from dual variables of `instance` and writes
    values back to bus-objects.

    Parameters
    ----------
    instance : solved OptimizationModel() instance containing the results
    """
    for b in getattr(instance, str(Bus)).objs:
        if b.balanced:
            b.results["shadowprice"] = []
            for t in instance.timesteps:
                b.results["shadowprice"].append(
                    instance.dual[getattr(
                        getattr(instance,str(Bus)), "balance")[(b.uid, t)]])
