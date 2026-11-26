# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: oemof e.V. and contributors

"""
General description
-------------------
This example is not a real use case of an energy system but an example to show
how a combined heat and power plant (chp) with an extraction turbine works in
contrast to a chp (eg. block device) with a fixed heat fraction. Both chp
plants distribute power and heat to a separate heat and power Bus with a heat
and power demand. The i/o balance plot shows that the fixed chp plant produces
heat and power excess and therefore needs more natural gas. The bar plot just
shows the difference in the usage of natural gas.

Code
----
Download source code: :download:`variable_chp.py </../examples/variable_chp/variable_chp.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/variable_chp/variable_chp.py
        :language: python
        :lines: 53-

Data
----
Download data: :download:`variable_chp.csv </../examples/variable_chp/variable_chp.csv>`

Installation requirements
-------------------------

This example requires oemof.solph (at least v0.5.0), install by:

.. code:: bash

    pip install oemof.solph>=0.5

Optional to see the i/o balance plot:

.. code:: bash

    pip install git+https://github.com/oemof/oemof_visio.git

License
-------
SPDX-License-Identifier: MIT

"""

###############################################################################
# imports
###############################################################################

import logging
import os
import warnings

import matplotlib.pyplot as plt
import pandas as pd
from oemof.tools import logger

from oemof import solph

# import oemof plots
try:
    from oemof.visio import plot as oeplot
except ImportError:
    oeplot = None


def shape_legend(node, reverse=True, **kwargs):
    handels = kwargs["handles"]
    labels = kwargs["labels"]
    axes = kwargs["ax"]
    parameter = {}

    new_labels = []
    for label in labels:
        label = label.replace("(", "")
        label = label.replace("), flow)", "")
        label = label.replace(node, "")
        label = label.replace(",", "")
        label = label.replace(" ", "")
        new_labels.append(label)
    labels = new_labels

    parameter["bbox_to_anchor"] = kwargs.get("bbox_to_anchor", (1, 0.5))
    parameter["loc"] = kwargs.get("loc", "center left")
    parameter["ncol"] = kwargs.get("ncol", 1)
    plotshare = kwargs.get("plotshare", 0.9)

    if reverse:
        handels.reverse()
        labels.reverse()

    box = axes.get_position()
    axes.set_position([box.x0, box.y0, box.width * plotshare, box.height])

    parameter["handles"] = handels
    parameter["labels"] = labels
    axes.legend(**parameter)
    return axes


def write_lp_file(model):
    lp_filename = os.path.join(
        solph.helpers.extend_basic_path("lp_files"), "variable_chp.lp"
    )
    logging.info("Store lp-file in {0}.".format(lp_filename))
    model.write(lp_filename, io_options={"symbolic_solver_labels": True})


def main(optimize=True, solver="cbc"):
    # Read data file
    filename = os.path.join(os.path.dirname(__file__), "variable_chp.csv")
    try:
        data = pd.read_csv(filename)
        data["demand_th"] *= 741000
        y_lim_elec = 350000
        y_lim_heat = 600000

    except FileNotFoundError:
        msg = "Data file not found: {0}. Only one value used!"
        warnings.warn(msg.format(filename), UserWarning)
        data = pd.DataFrame({"demand_el": [500], "demand_th": [344]})
        y_lim_elec = 5
        y_lim_heat = 10
    logger.define_logging()
    logging.info("Initialize the energy system")

    # create time index for 192 hours in May.
    date_time_index = solph.create_time_index(2012, number=len(data))

    energysystem = solph.EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )

    ##########################################################################
    # Create oemof.solph objects
    ##########################################################################
    logging.info("Create oemof.solph objects")

    # create natural gas bus
    energysystem.add(solph.Bus(label="bgas"))

    # create commodity object for gas resource
    energysystem.add(
        solph.components.Source(
            label="rgas",
            outputs={energysystem.node["bgas"]: solph.Flow(variable_costs=50)},
        )
    )

    # create two electricity buses and two heat buses
    energysystem.add(solph.Bus(label="bel"))
    energysystem.add(solph.Bus(label="bel2"))
    energysystem.add(solph.Bus(label="bth"))
    energysystem.add(solph.Bus(label="bth2"))

    # create excess components for the elec/heat bus to allow overproduction
    energysystem.add(
        solph.components.Sink(
            label="excess_bth_2",
            inputs={energysystem.node["bth2"]: solph.Flow()},
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="excess_therm",
            inputs={energysystem.node["bth"]: solph.Flow()},
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="excess_bel_2",
            inputs={energysystem.node["bel2"]: solph.Flow()},
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="excess_elec",
            inputs={energysystem.node["bel"]: solph.Flow()},
        )
    )

    # create simple sink object for electrical demand for each electrical bus
    energysystem.add(
        solph.components.Sink(
            label="demand_elec",
            inputs={
                energysystem.node["bel"]: solph.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="demand_el_2",
            inputs={
                energysystem.node["bel2"]: solph.Flow(
                    fix=data["demand_el"], nominal_capacity=1
                )
            },
        )
    )

    # create simple sink object for heat demand for each thermal bus
    energysystem.add(
        solph.components.Sink(
            label="demand_therm",
            inputs={
                energysystem.node["bth"]: solph.Flow(
                    fix=data["demand_th"], nominal_capacity=1
                )
            },
        )
    )
    energysystem.add(
        solph.components.Sink(
            label="demand_th_2",
            inputs={
                energysystem.node["bth2"]: solph.Flow(
                    fix=data["demand_th"], nominal_capacity=1
                )
            },
        )
    )

    # This is just a dummy Converter with a nominal input of zero
    energysystem.add(
        solph.components.Converter(
            label="fixed_chp_gas",
            inputs={energysystem.node["bgas"]: solph.Flow(nominal_capacity=0)},
            outputs={
                energysystem.node["bel"]: solph.Flow(),
                energysystem.node["bth"]: solph.Flow(),
            },
            conversion_factors={
                energysystem.node["bel"]: 0.3,
                energysystem.node["bth"]: 0.5,
            },
        )
    )

    # create a fixed Converter to distribute to the heat_2 and elec_2 buses
    energysystem.add(
        solph.components.Converter(
            label="fixed_chp_gas_2",
            inputs={
                energysystem.node["bgas"]: solph.Flow(nominal_capacity=10e10)
            },
            outputs={
                energysystem.node["bel2"]: solph.Flow(),
                energysystem.node["bth2"]: solph.Flow(),
            },
            conversion_factors={
                energysystem.node["bel2"]: 0.3,
                energysystem.node["bth2"]: 0.5,
            },
        )
    )

    # create a fixed Converter to distribute to the heat and elec buses
    # Try with iterable or floats and try with equal points
    # If allow_equal_states=False equal states are not allowed and will
    # raise an error even if the equal state is just in one time step.
    # Otherwise, only in this time step two more constraints will be
    # written to the lp-file to avoid mismatches.

    energysystem.add(
        solph.components.VariableSplitConverter(
            label="variable_chp_gas",
            inputs={
                energysystem.node["bgas"]: solph.Flow(nominal_capacity=10e10)
            },
            outputs={
                energysystem.node["bth"]: solph.Flow(),
                energysystem.node["bel"]: solph.Flow(),
            },
            conversion_factors={
                energysystem.node["bel"]: 0.5,
                energysystem.node["bth"]: 0.2,
            },
            allow_equal_states=False,
            conversion_factors_secondary_state={
                energysystem.node["bel"]: 0.3,
                energysystem.node["bth"]: 0.5,
            },
        )
    )

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if not optimize:
        return energysystem

    logging.info("Optimise the energy system")

    om = solph.Model(energysystem)

    # If uncomment the following line you can store the lp file but you should
    # use less timesteps (3) to make it better readable and smaller.
    # write_lp_file(om)

    logging.info("Solve the optimization problem")
    om.solve(solver=solver, solve_kwargs={"tee": False})

    results = solph.processing.results(om)

    ##########################################################################
    # Plot the results
    ##########################################################################

    myresults = solph.views.node(results, "bgas")
    myresults = myresults["sequences"].sum(axis=0)
    myresults = myresults.drop(myresults.index[0]).reset_index(drop=True)
    myresults = myresults.rename({0: "fixed", 1: "variable", 2: "total"})
    myresults.plot(kind="bar", rot=0, title="Usage of natural gas")
    plt.show()

    # Create a plot with 6 tiles that shows the difference between the
    # Converter and the ExtractionTurbineCHP used for chp plants.
    smooth_plot = True

    if oeplot:
        logging.info("Plot the results")

        cdict = {
            (("variable_chp_gas", "bel"), "flow"): "#42c77a",
            (("fixed_chp_gas_2", "bel2"), "flow"): "#20b4b6",
            (("fixed_chp_gas", "bel"), "flow"): "#20b4b6",
            (("fixed_chp_gas", "bth"), "flow"): "#20b4b6",
            (("variable_chp_gas", "bth"), "flow"): "#42c77a",
            (("bth", "demand_therm"), "flow"): "#5b5bae",
            (("bth2", "demand_th_2"), "flow"): "#5b5bae",
            (("bel", "demand_elec"), "flow"): "#5b5bae",
            (("bel2", "demand_el_2"), "flow"): "#5b5bae",
            (("bth", "excess_therm"), "flow"): "#f22222",
            (("bth2", "excess_bth_2"), "flow"): "#f22222",
            (("bel", "excess_elec"), "flow"): "#f22222",
            (("bel2", "excess_bel_2"), "flow"): "#f22222",
            (("fixed_chp_gas_2", "bth2"), "flow"): "#20b4b6",
        }

        fig = plt.figure(figsize=(18, 9))
        plt.rc("legend", **{"fontsize": 13})
        plt.rcParams.update({"font.size": 13})
        fig.subplots_adjust(
            left=0.07,
            bottom=0.12,
            right=0.86,
            top=0.93,
            wspace=0.03,
            hspace=0.2,
        )

        # subplot of electricity bus (fixed chp) [1]
        electricity_2 = solph.views.node(results, "bel2")
        x_length = len(electricity_2["sequences"].index)
        myplot = oeplot.io_plot(
            bus_label="bel2",
            df=electricity_2["sequences"],
            cdict=cdict,
            smooth=smooth_plot,
            line_kwa={"linewidth": 4},
            ax=fig.add_subplot(3, 2, 1),
            inorder=[(("fixed_chp_gas_2", "bel2"), "flow")],
            outorder=[
                (("bel2", "demand_el_2"), "flow"),
                (("bel2", "excess_bel_2"), "flow"),
            ],
        )
        myplot["ax"].set_ylabel("Power in MW")
        myplot["ax"].set_ylim([0, y_lim_elec])
        myplot["ax"].set_xlabel("")
        myplot["ax"].get_xaxis().set_visible(False)
        myplot["ax"].set_xlim(0, x_length)
        myplot["ax"].set_title("Electricity output (fixed chp)")
        myplot["ax"].legend_.remove()

        # subplot of electricity bus (variable chp) [2]
        electricity = solph.views.node(results, "bel")
        myplot = oeplot.io_plot(
            bus_label="bel",
            df=electricity["sequences"],
            cdict=cdict,
            smooth=smooth_plot,
            line_kwa={"linewidth": 4},
            ax=fig.add_subplot(3, 2, 2),
            inorder=[
                (("fixed_chp_gas", "bel"), "flow"),
                (("variable_chp_gas", "bel"), "flow"),
            ],
            outorder=[
                (("bel", "demand_elec"), "flow"),
                (("bel", "excess_elec"), "flow"),
            ],
        )
        myplot["ax"].get_yaxis().set_visible(False)
        myplot["ax"].set_ylim([0, y_lim_elec])
        myplot["ax"].set_xlabel("")
        myplot["ax"].get_xaxis().set_visible(False)
        myplot["ax"].set_title("Electricity output (variable chp)")
        myplot["ax"].set_xlim(0, x_length)
        shape_legend("bel", plotshare=1, **myplot)

        # subplot of heat bus (fixed chp) [3]
        heat_2 = solph.views.node(results, "bth2")
        myplot = oeplot.io_plot(
            bus_label="bth2",
            df=heat_2["sequences"],
            cdict=cdict,
            smooth=smooth_plot,
            line_kwa={"linewidth": 4},
            ax=fig.add_subplot(3, 2, 3),
            inorder=[(("fixed_chp_gas_2", "bth2"), "flow")],
            outorder=[
                (("bth2", "demand_th_2"), "flow"),
                (("bth2", "excess_bth_2"), "flow"),
            ],
        )
        myplot["ax"].set_ylabel("Power in MW")
        myplot["ax"].set_ylim([0, y_lim_heat])
        myplot["ax"].get_xaxis().set_visible(False)
        myplot["ax"].set_title("Heat output (fixed chp)")
        myplot["ax"].set_xlim(0, x_length)
        myplot["ax"].legend_.remove()

        # subplot of heat bus (variable chp) [4]
        heat = solph.views.node(results, "bth")
        myplot = oeplot.io_plot(
            bus_label="bth",
            df=heat["sequences"],
            cdict=cdict,
            smooth=smooth_plot,
            line_kwa={"linewidth": 4},
            ax=fig.add_subplot(3, 2, 4),
            inorder=[
                (("fixed_chp_gas", "bth"), "flow"),
                (("variable_chp_gas", "bth"), "flow"),
            ],
            outorder=[
                (("bth", "demand_therm"), "flow"),
                (("bth", "excess_therm"), "flow"),
            ],
        )
        myplot["ax"].set_ylim([0, y_lim_heat])
        myplot["ax"].get_yaxis().set_visible(False)
        myplot["ax"].get_xaxis().set_visible(False)
        myplot["ax"].set_title("Heat output (variable chp)")
        myplot["ax"].set_xlim(0, x_length)
        shape_legend("bth", plotshare=1, **myplot)

        if smooth_plot:
            style = None
        else:
            style = "steps-mid"

        # subplot of efficiency (fixed chp) [5]
        fix_chp_gas2 = solph.views.node(results, "fixed_chp_gas_2")
        ngas = fix_chp_gas2["sequences"][(("bgas", "fixed_chp_gas_2"), "flow")]
        elec = fix_chp_gas2["sequences"][(("fixed_chp_gas_2", "bel2"), "flow")]
        heat = fix_chp_gas2["sequences"][(("fixed_chp_gas_2", "bth2"), "flow")]
        e_ef = elec.div(ngas)
        h_ef = heat.div(ngas)
        df_eff_fix = pd.DataFrame(
            pd.concat([h_ef, e_ef], axis=1, keys=["bth", "bel"])
        )
        my_ax = df_eff_fix.reset_index(drop=True).plot(
            drawstyle=style, ax=fig.add_subplot(3, 2, 5), linewidth=2
        )
        my_ax.set_ylabel("efficiency")
        my_ax.set_ylim([0, 0.55])
        my_ax.set_xlabel("May 2012")
        my_ax = oeplot.set_datetime_ticks(
            my_ax,
            df_eff_fix.index,
            tick_distance=24,
            date_format="%d",
            offset=12,
            tight=True,
        )
        my_ax.set_title("Efficiency (fixed chp)")
        my_ax.legend_.remove()

        # subplot of efficiency (variable chp) [6]
        var_chp_gas = solph.views.node(results, "variable_chp_gas")
        ngas = var_chp_gas["sequences"][(("bgas", "variable_chp_gas"), "flow")]
        elec = var_chp_gas["sequences"][(("variable_chp_gas", "bel"), "flow")]
        heat = var_chp_gas["sequences"][(("variable_chp_gas", "bth"), "flow")]
        e_ef = elec.div(ngas)
        h_ef = heat.div(ngas)
        e_ef.name = "electricity           "
        h_ef.name = "bth"
        df_eff_var = pd.DataFrame(pd.concat([h_ef, e_ef], axis=1))
        # df_eff_var.sort_values("bth").reset_index(drop=True).T.sum().T
        # plt.show()
        my_ax = df_eff_var.reset_index(drop=True).plot(
            drawstyle=style, ax=fig.add_subplot(3, 2, 6), linewidth=2
        )
        my_ax.set_ylim([0, 0.55])
        my_ax = oeplot.set_datetime_ticks(
            my_ax,
            df_eff_var.index,
            tick_distance=24,
            date_format="%d",
            offset=12,
            tight=True,
        )
        my_ax.get_yaxis().set_visible(False)
        my_ax.set_xlabel("May 2012")

        my_ax.set_title("Efficiency (variable chp)")
        my_box = my_ax.get_position()
        my_ax.set_position(
            [my_box.x0, my_box.y0, my_box.width * 1, my_box.height]
        )
        my_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)

        # plt.show()
        df_eff_var.set_index("bth", drop=True).plot(
            title="Variable CHP", marker="o"
        )
        df_eff_fix.round(2).set_index("bth", drop=True).plot(
            title="Fixed CHP", marker="o"
        )
        plt.show()

    else:
        logging.warning(
            "You have to install 'oemof-visio' to see the i/o-plot"
        )
        logging.warning(
            "Use: pip install git+https://github.com/oemof/oemof_visio.git"
        )

    return None


if __name__ == "__main__":
    main()
