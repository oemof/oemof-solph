# -*- coding: utf-8 -*-
# basic example from oemof-examples
"""
General description
-------------------
A basic example to show how to model a simple energy system with oemof.solph.
The following energy system is modeled:
                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |
Data
----
basic_example.csv
Installation requirements
-------------------------
This example requires the version v0.4.x of oemof. Install by:
    pip install 'oemof.solph>=0.4,<0.5'
Optional:
    pip install matplotlib
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

# ****************************************************************************
# ********** PART 1 - Define and optimise the energy system ******************
# ****************************************************************************

###############################################################################
# imports
###############################################################################

# Default logger of oemof
from oemof.tools import logger
from oemof import solph

import logging
import os
import pandas as pd
import pprint as pp

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


solver = "cbc"  # 'glpk', 'gurobi',....
debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
number_of_time_steps = 24 * 7 * 8
solver_verbose = False  # show/hide solver output

# initiate the logger (see the API docs for more information)
logger.define_logging(
    logfile="oemof_example.log",
    screen_level=logging.INFO,
    file_level=logging.DEBUG,
)

logging.info("Initialize the energy system")
date_time_index = pd.date_range(
    "1/1/2012", periods=number_of_time_steps, freq="H"
)

energysystem = solph.EnergySystem(timeindex=date_time_index)

# Read data file
filename = os.path.join(os.getcwd(), "basic_example.csv")
data = pd.read_csv(filename)

##########################################################################
# Create oemof object
##########################################################################

logging.info("Create oemof objects")

# The bus objects were assigned to variables which makes it easier to connect
# components to these buses (see below).

# create natural gas bus
bgas = solph.Bus(label="natural_gas")

# create electricity bus
bel = solph.Bus(label="electricity")

# adding the buses to the energy system
energysystem.add(bgas, bel)

# create excess component for the electricity bus to allow overproduction
energysystem.add(solph.Sink(label="excess_bel", inputs={bel: solph.Flow()}))

# create source object representing the natural gas commodity (annual limit)
energysystem.add(
    solph.Source(
        label="rgas",
        outputs={bgas: solph.Flow(nominal_value=29825293, summed_max=1)},
    )
)

# create fixed source object representing wind power plants
energysystem.add(
    solph.Source(
        label="wind",
        outputs={bel: solph.Flow(fix=data["wind"], nominal_value=1000000)},
    )
)

# create fixed source object representing pv power plants
energysystem.add(
    solph.Source(
        label="pv",
        outputs={bel: solph.Flow(fix=data["pv"], nominal_value=582000)},
    )
)

# create simple sink object representing the electrical demand
energysystem.add(
    solph.Sink(
        label="demand",
        inputs={bel: solph.Flow(fix=data["demand_el"], nominal_value=1)},
    )
)

# create simple transformer object representing a gas power plant
energysystem.add(
    solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
        conversion_factors={bel: 0.58},
    )
)

# create storage object representing a battery
storage = solph.components.GenericStorage(
    nominal_storage_capacity=10077997,
    label="storage",
    inputs={bel: solph.Flow(nominal_value=10077997 / 6)},
    outputs={
        bel: solph.Flow(nominal_value=10077997 / 6, variable_costs=0.001)
    },
    loss_rate=0.00,
    initial_storage_level=None,
    inflow_conversion_factor=1,
    outflow_conversion_factor=0.8,
)

energysystem.add(storage)

##########################################################################
# Optimise the energy system and plot the results
##########################################################################

logging.info("Optimise the energy system")

# initialise the operational model
model = solph.Model(energysystem)

# This is for debugging only. It is not(!) necessary to solve the problem and
# should be set to False to save time and disc space in normal use. For
# debugging the timesteps should be set to 3, to increase the readability of
# the lp-file.
if debug:
    filename = os.path.join(
        solph.helpers.extend_basic_path("lp_files"), "basic_example.lp"
    )
    logging.info("Store lp-file in {0}.".format(filename))
    model.write(filename, io_options={"symbolic_solver_labels": True})

# if tee_switch is true solver messages will be displayed
logging.info("Solve the optimization problem")
model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

logging.info("Store the energy system with the results.")

# The processing module of the outputlib can be used to extract the results
# from the model transfer them into a homogeneous structured dictionary.

# add results to the energy system to make it possible to store them.
energysystem.results["main"] = solph.processing.results(model)
energysystem.results["meta"] = solph.processing.meta_results(model)

# The default path is the '.oemof' folder in your $HOME directory.
# The default filename is 'es_dump.oemof'.
# You can omit the attributes (as None is the default value) for testing cases.
# You should use unique names/folders for valuable results to avoid
# overwriting.

# store energy system with results
energysystem.dump(dpath=None, filename=None)

# ****************************************************************************
# ********** PART 2 - Processing the results *********************************
# ****************************************************************************

logging.info("**** The script can be divided into two parts here.")
logging.info("Restore the energy system and the results.")
energysystem = solph.EnergySystem()
energysystem.restore(dpath=None, filename=None)

# define an alias for shorter calls below (optional)
results = energysystem.results["main"]
storage = energysystem.groups["storage"]

# print a time slice of the state of charge
print("")
print("********* State of Charge (slice) *********")
print(
    results[(storage, None)]["sequences"][
        "2012-02-25 08:00:00":"2012-02-26 15:00:00"
    ]
)
print("")

# get all variables of a specific component/bus
custom_storage = solph.views.node(results, "storage")
electricity_bus = solph.views.node(results, "electricity")

# plot the time series (sequences) of a specific component/bus
if plt is not None:
    fig, ax = plt.subplots(figsize=(10, 5))
    custom_storage["sequences"].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(
        loc="upper center",
        prop={"size": 8},
        bbox_to_anchor=(0.5, 1.25),
        ncol=2,
    )
    fig.subplots_adjust(top=0.8)
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    electricity_bus["sequences"].plot(
        ax=ax, kind="line", drawstyle="steps-post"
    )
    plt.legend(
        loc="upper center", prop={"size": 8}, bbox_to_anchor=(0.5, 1.3), ncol=2
    )
    fig.subplots_adjust(top=0.8)
    plt.show()

# print the solver results
print("********* Meta results *********")
pp.pprint(energysystem.results["meta"])
print("")

# print the sums of the flows around the electricity bus
print("********* Main results *********")
print(electricity_bus["sequences"].sum(axis=0))

# Stochastic programming problem

def create_scenario(model,):

    return model
