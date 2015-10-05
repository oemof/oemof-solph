# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:22:56 2015

@author: simon
"""

try:
    from network.entities import Bus, Component
    from network.entities import components as cp
except:
    from .network.entities import Bus, Component
    from .network.entities import components as cp


def results_to_objects(instance, entities):
    """ write the results from a pyomo optimization problem back to the
    oemof-objects

    Parameters
    ------------
    instance : solved OptimizationModel() instance containing the results

    Returns
    ----------

    No return value specified.
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
            entity.results['soc'] = []
            for t in instance.timesteps:
                entity.results['soc'].append(
                    instance.soc[entity.uid, t].value)

    if(instance.invest is True):
        for entity in instance.entities:
            if isinstance(entity, cp.Transformer):
                entity.results['add_cap_out'] = \
                    instance.add_cap[entity.uid, entity.outputs[0].uid].value
            if isinstance(entity, cp.Source):
                entity.results['add_cap_out'] = \
                    instance.add_cap[entity.uid, entity.outputs[0].uid].value
            if isinstance(entity, cp.transformers.Storage):
                entity.results['add_cap_soc'] = \
                    instance.soc_add[entity.uid].value


def dual_variables_to_objects(instance):
    """ Extracts values from dual variables of `instance` and writes
    values back to bus-objects.

    Parameters
    ------------
    instance : solved OptimizationModel() instance containing the results

    Returns
    ----------

    No return value specified.
    """
    for b in instance.bus_objs:
        if b.type == "el" or b.type == "th":
            b.results["duals"] = []
            for t in instance.timesteps:
                b.results["duals"].append(
                    instance.dual[getattr(instance, "bus")[(b.uid, t)]])
    # print(b.results["duals"])
