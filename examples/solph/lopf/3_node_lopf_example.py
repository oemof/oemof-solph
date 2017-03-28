# -*- coding: utf-8 -*-
"""
"""
# ############################### imports #####################################
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

# solph imports
from oemof.solph import (Sink, Source, LinearTransformer, ElectricalBus, Flow,
                         OperationalModel, EnergySystem, Bus, ElectricalLine)
import oemof.outputlib as output
from oemof.tools import logger

# ####################### data & initialization ###############################


def initialise_energysystem(periods=5):
    """
    """
    datetimeindex = pd.date_range('1/1/2012', periods=periods, freq='H')

    return EnergySystem(timeindex=datetimeindex)


# ######################### create energysystem components ####################
def simulate(energysystem, filename=None, solver='cbc', tee_switch=True):
    """
    """

    logging.info("Creating objects")
    # resource buses
    bcoal = Bus(label="coal", balanced=False)
    bgas = Bus(label="gas", balanced=False)
    boil = Bus(label="oil", balanced=False)
    blig = Bus(label="lignite", balanced=False)

    # electricity and heat
    b_el1 = ElectricalBus(label="b_el1", voltage_angle_max=12)
    b_el2 = ElectricalBus(label="b_el2", voltage_angle_max=15)
    b_el3 = ElectricalBus(label="b_el2", voltage_angle_max=20)
    ElectricalLine(label="line1",
                   inputs={b_el1: Flow()},
                   outputs={b_el2: Flow()}, reactance=0.2)
    ElectricalLine(label="line2",
                   inputs={b_el2: Flow()},
                   outputs={b_el3: Flow()}, reactance=0.2)
    ElectricalLine(label="line3",
                   inputs={b_el1: Flow()},
                   outputs={b_el3: Flow()}, reactance=0.2)

    # ################################ optimization ############################
    # create Optimization model based on energy_system
    logging.info("Create optimization problem")
    om = OperationalModel(es=energysystem)

    # solve with specific optimization options (passed to pyomo)
    logging.info("Solve optimization problem")
    om.solve(solver=solver,
             solve_kwargs={'tee': tee_switch, 'keepfiles': False})

    # write back results from optimization object to energysystem
    om.results()

    return om


def get_results(energysystem):
    """Shows how to extract single time series from DataFrame.

    Parameters
    ----------
    energysystem : solph.EnergySystem

    Returns
    -------
    dict : Some results.
    """
    logging.info('Check the results')

    myresults = output.DataFramePlot(energy_system=energysystem)

    grouped = myresults.groupby(level=[0, 1, 2]).sum()
    rdict = {r + (k,): v
             for r, kv in grouped.iterrows()
             for k, v in kv.to_dict().items()}

    rdict['objective'] = energysystem.results.objective

    return rdict


def run_lopf(**kwargs):
    import pprint as pp
    logger.define_logging()
    esys = initialise_energysystem()
    simulate(esys, **kwargs)
    pp.pprint(get_results(esys))


if __name__ == "__main__":
    run_lopf()
