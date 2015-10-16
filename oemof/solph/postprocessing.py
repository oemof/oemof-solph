# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:22:56 2015

@author: simon
"""
import pandas as pd

try:
    from network.entities import Bus, Component
    from network.entities import components as cp
except:
    from ..core.network.entities import Bus, Component
    from ..core.network.entities import components as cp


def results_to_objects(instance):
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
                entity.results['add_out'] = \
                    instance.add_out[entity.uid].value
            if isinstance(entity, cp.Source):
                entity.results['add_out'] = \
                    instance.add_out[entity.uid].value
            if isinstance(entity, cp.transformers.Storage):
                entity.results['add_cap'] = \
                    instance.add_cap[entity.uid].value


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


def results_to_excel(instance=None, filename="/home/simon/results.xls", ):
    """ Write results from pyomo.ConcreteModel() instance to excel file
    """
    writer = pd.ExcelWriter(filename)

    input = pd.DataFrame()
    output = pd.DataFrame()
    storages = pd.DataFrame()

    for entity in instance.entities:
        if (isinstance(entity, cp.Transformer) or
                isinstance(entity, cp.Source)):
            # write outputs
            O = [e.uid for e in entity.outputs[:]]
            for o in O:
                temp_lst = []
                for t in instance.timesteps:
                    temp_lst.append(instance.w[entity.uid, o, t].value)
                output[entity.uid+"_"+o] = temp_lst

            I = [i.uid for i in entity.inputs[:]]
            for i in I:
                temp_lst = []
                for t in instance.timesteps:
                    temp_lst.append(
                        instance.w[i, entity.uid, t].value)
                input[entity.uid+"_"+i] = temp_lst

        if isinstance(entity, cp.transformers.Storage):
            temp_lst = []
            for t in instance.timesteps:
                temp_lst.append(instance.soc[entity.uid, t].value)
            storages[entity.uid] = temp_lst

    output.to_excel(writer, "Output")
    input.to_excel(writer, "Input")
    storages.to_excel(writer, "Storages_SOC")
    writer.save()
