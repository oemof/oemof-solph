# -*- coding: utf-8 -*-

"""
General description
-------------------
This example focuses on the modelling of an OffsetConverters representing
a diesel generator in a hybrid mini-grid system considering its real efficiency
curve based on the min/max load and efficiency.

The system consists of the following components:
    - pv: solar potential to generate electricity
    - diesel_source: input diesel for the diesel genset
    - diesel_genset: generates ac electricity
    - rectifier: converts generated ac electricity from the diesel genset
                    to dc electricity
    - inverter: converts generated dc electricity from the pv to ac electricity
    - battery: stores the generated dc electricity
    - demand_el: ac electricity demand (given as a separate csv file)
    - excess_el: allows for some electricity overproduction


Code
----
Download source code: :download:`offset_diesel_genset_nonconvex_investment.py </../examples/offset_converter_example/offset_diesel_genset_nonconvex_investment.py>`

.. dropdown:: Click to display code

    .. literalinclude:: /../examples/offset_converter_example/offset_diesel_genset_nonconvex_investment.py
        :language: python
        :lines: 44-

Data
----
Download data: :download:`input_data.csv </../examples/offset_converter_example/diesel_genset_data.csv>`

Installation requirements
-------------------------
This example requires the version v0.5.x of oemof. Install by:

    pip install 'oemof.solph>=0.5,<0.6'

"""

__copyright__ = "oemof developer group"
__license__ = "MIT"

import os
import time
from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd

from oemof import solph

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def get_data_from_file_path(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        dir = os.path.dirname(os.path.abspath(__file__))
        data = pd.read_csv(dir + "/" + file_path)
    return data


def main(optimize=True):
    ##########################################################################
    # Initialize the energy system and calculate necessary parameters
    ##########################################################################

    # Start time for calculating the total elapsed time.
    start_simulation_time = time.time()

    start = "2022-01-01"

    # The maximum number of days depends on the given csv file.
    n_days = 5
    n_days_in_year = 365

    # Create date and time objects.
    start_date_obj = datetime.strptime(start, "%Y-%m-%d")
    start_date = start_date_obj.date()
    start_time = start_date_obj.time()
    start_datetime = datetime.combine(
        start_date_obj.date(), start_date_obj.time()
    )
    end_datetime = start_datetime + timedelta(days=n_days)

    # Import data.
    data = get_data_from_file_path("diesel_genset_data.csv")

    # Change the index of data to be able to select data based on the time range.
    data.index = pd.date_range(start="2022-01-01", periods=len(data), freq="h")

    # Choose the range of the solar potential and demand
    # based on the selected simulation period.
    solar_potential = data.SolarGen.loc[start_datetime:end_datetime]
    hourly_demand = data.Demand.loc[start_datetime:end_datetime]
    peak_solar_potential = solar_potential.max()
    peak_demand = hourly_demand.max()

    # Create the energy system.
    date_time_index = pd.date_range(
        start=start_date, periods=n_days * 24, freq="h"
    )
    energy_system = solph.EnergySystem(timeindex=date_time_index)

    # -------------------- BUSES --------------------
    # Create electricity and diesel buses.
    b_el_ac = solph.buses.Bus(label="electricity_ac")
    b_el_dc = solph.buses.Bus(label="electricity_dc")
    b_diesel = solph.buses.Bus(label="diesel")

    # -------------------- SOURCES --------------------
    diesel_cost = 0.65  # currency/l
    diesel_density = 0.846  # kg/l
    diesel_lhv = 11.83  # kWh/kg
    diesel_source = solph.components.Source(
        label="diesel_source",
        outputs={
            b_diesel: solph.flows.Flow(
                variable_costs=diesel_cost / diesel_density / diesel_lhv
            )
        },
    )

    # EPC stands for the equivalent periodical costs.
    epc_pv = 152.62  # currency/kW/year
    pv = solph.components.Source(
        label="pv",
        outputs={
            b_el_dc: solph.flows.Flow(
                fix=solar_potential / peak_solar_potential,
                nominal_capacity=solph.Investment(
                    ep_costs=epc_pv * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
    )

    # -------------------- CONVERTERS --------------------
    # The diesel genset does not have a fixed nominal capacity and will be
    # optimized using the minimum and maximum loads and efficiencies.
    # In this case, the `Investment` and `NonConvex` attributes must be used. The
    # combination of these two attributes is utilized in the
    # `InvestNonConvexFlowBlock`.

    # If the nominal capacity of the genset is already known, only the `NonConvex`
    # attribute should be defined, and therefore, the `NonConvexFlowBlock` will
    # be used.

    # Specify the minimum and maximum loads and the corresponding efficiencies
    # for the diesel genset.
    min_load = 0.2
    max_load = 1.0
    min_efficiency = 0.20
    max_efficiency = 0.33

    # Calculate the two polynomial coefficients, i.e. the y-intersection and the
    # slope of the linear equation. There is a conveniece function for that
    # in solph:
    slope, offset = solph.components.slope_offset_from_nonconvex_output(
        max_load, min_load, max_efficiency, min_efficiency
    )

    epc_diesel_genset = 84.80  # currency/kW/year
    variable_cost_diesel_genset = 0.045  # currency/kWh
    diesel_genset = solph.components.OffsetConverter(
        label="diesel_genset",
        inputs={b_diesel: solph.flows.Flow()},
        outputs={
            b_el_ac: solph.flows.Flow(
                variable_costs=variable_cost_diesel_genset,
                min=min_load,
                max=max_load,
                nominal_capacity=solph.Investment(
                    ep_costs=epc_diesel_genset * n_days / n_days_in_year,
                    maximum=2 * peak_demand,
                ),
                nonconvex=solph.NonConvex(),
            ),
        },
        conversion_factors={b_diesel: slope},
        normed_offsets={b_diesel: offset},
    )

    # The rectifier assumed to have a fixed efficiency of 98%.
    epc_rectifier = 62.35  # currency/kW/year
    rectifier = solph.components.Converter(
        label="rectifier",
        inputs={
            b_el_ac: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    ep_costs=epc_rectifier * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
        outputs={b_el_dc: solph.flows.Flow()},
        conversion_factors={
            b_el_dc: 0.98,
        },
    )

    # The inverter assumed to have a fixed efficiency of 98%.
    epc_inverter = 62.35  # currency/kW/year
    inverter = solph.components.Converter(
        label="inverter",
        inputs={
            b_el_dc: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    ep_costs=epc_inverter * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
        outputs={b_el_ac: solph.flows.Flow()},
        conversion_factors={
            b_el_ac: 0.98,
        },
    )

    # -------------------- STORAGE --------------------
    epc_battery = 101.00  # currency/kWh/year
    battery = solph.components.GenericStorage(
        label="battery",
        nominal_capacity=solph.Investment(
            ep_costs=epc_battery * n_days / n_days_in_year
        ),
        inputs={b_el_dc: solph.flows.Flow(variable_costs=0)},
        outputs={
            b_el_dc: solph.flows.Flow(
                nominal_capacity=solph.Investment(ep_costs=0)
            )
        },
        initial_storage_level=0.0,
        min_storage_level=0.0,
        max_storage_level=1.0,
        balanced=True,
        inflow_conversion_factor=0.9,
        outflow_conversion_factor=0.9,
        invest_relation_input_capacity=1,
        invest_relation_output_capacity=0.5,
    )

    # -------------------- SINKS --------------------
    demand_el = solph.components.Sink(
        label="electricity_demand",
        inputs={
            b_el_ac: solph.flows.Flow(
                fix=hourly_demand / peak_demand,
                nominal_capacity=peak_demand,
            )
        },
    )

    excess_el = solph.components.Sink(
        label="excess_el",
        inputs={b_el_dc: solph.flows.Flow()},
    )

    # Add all objects to the energy system.
    energy_system.add(
        pv,
        diesel_source,
        b_el_dc,
        b_el_ac,
        b_diesel,
        inverter,
        rectifier,
        diesel_genset,
        battery,
        demand_el,
        excess_el,
    )

    ##########################################################################
    # Optimise the energy system
    ##########################################################################

    if optimize is False:
        return energy_system

    # The higher the MipGap or ratioGap, the faster the solver would converge,
    # but the less accurate the results would be.
    solver_option = {"gurobi": {"MipGap": "0.02"}, "cbc": {"ratioGap": "0.02"}}
    solver = "cbc"

    model = solph.Model(energy_system)
    model.solve(
        solver=solver,
        solve_kwargs={"tee": True},
        cmdline_options=solver_option[solver],
    )

    # End of the calculation time.
    end_simulation_time = time.time()

    ##########################################################################
    # Process the results
    ##########################################################################

    results = solph.processing.results(model)

    results_pv = solph.views.node(results=results, node="pv")
    results_diesel_source = solph.views.node(
        results=results, node="diesel_source"
    )
    results_diesel_genset = solph.views.node(
        results=results, node="diesel_genset"
    )
    results_inverter = solph.views.node(results=results, node="inverter")
    results_rectifier = solph.views.node(results=results, node="rectifier")
    results_battery = solph.views.node(results=results, node="battery")
    results_demand_el = solph.views.node(
        results=results, node="electricity_demand"
    )
    results_excess_el = solph.views.node(results=results, node="excess_el")

    # -------------------- SEQUENCES (DYNAMIC) --------------------
    # Hourly demand profile.
    sequences_demand = results_demand_el["sequences"][
        (("electricity_ac", "electricity_demand"), "flow")
    ]

    # Hourly profiles for solar potential and pv production.
    sequences_pv = results_pv["sequences"][(("pv", "electricity_dc"), "flow")]

    # Hourly profiles for diesel consumption and electricity production
    # in the diesel genset.
    # The 'flow' from oemof is in kWh and must be converted to
    # kg by dividing it by the lower heating value and then to
    # liter by dividing it by the diesel density.
    sequences_diesel_consumption = (
        results_diesel_source["sequences"][
            (("diesel_source", "diesel"), "flow")
        ]
        / diesel_lhv
        / diesel_density
    )

    # Hourly profile for the kWh of the diesel provided for the diesel genset
    sequences_diesel_consumption_kwh = results_diesel_source["sequences"][
        (("diesel_source", "diesel"), "flow")
    ]

    sequences_diesel_genset = results_diesel_genset["sequences"][
        (("diesel_genset", "electricity_ac"), "flow")
    ]

    # Hourly profiles for inverted electricity from dc to ac.
    sequences_inverter = results_inverter["sequences"][
        (("inverter", "electricity_ac"), "flow")
    ]

    # Hourly profiles for inverted electricity from ac to dc.
    sequences_rectifier = results_rectifier["sequences"][
        (("rectifier", "electricity_dc"), "flow")
    ]

    # Hourly profiles for excess ac and dc electricity production.
    sequences_excess = results_excess_el["sequences"][
        (("electricity_dc", "excess_el"), "flow")
    ]

    # -------------------- SCALARS (STATIC) --------------------
    capacity_diesel_genset = results_diesel_genset["scalars"][
        (("diesel_genset", "electricity_ac"), "invest")
    ]

    # Define a tolerance to force 'too close' numbers to the `min_load`
    # and to 0 to be the same as the `min_load` and 0.
    # Load is defined here in percentage.
    tol = 1e-8
    load_diesel_genset = sequences_diesel_genset / capacity_diesel_genset * 100
    sequences_diesel_genset[np.abs(load_diesel_genset) < tol] = 0
    sequences_diesel_genset[np.abs(load_diesel_genset - min_load) < tol] = (
        min_load * capacity_diesel_genset
    )
    sequences_diesel_genset[np.abs(load_diesel_genset - max_load) < tol] = (
        max_load * capacity_diesel_genset
    )

    # Calculate the efficiency of the diesel genset.
    # If the load is equal to 0, the efficiency will also be 0.
    # Efficiency is defined here in percentage.
    efficiency_diesel_genset = np.zeros(len(sequences_diesel_genset))
    for i in range(len(sequences_diesel_genset)):
        if sequences_diesel_consumption_kwh[i] != 0:
            efficiency_diesel_genset[i] = (
                sequences_diesel_genset[i]
                / sequences_diesel_consumption_kwh[i]
                * 100
            )

    capacity_pv = results_pv["scalars"][(("pv", "electricity_dc"), "invest")]
    capacity_inverter = results_inverter["scalars"][
        (("electricity_dc", "inverter"), "invest")
    ]
    capacity_rectifier = results_rectifier["scalars"][
        (("electricity_ac", "rectifier"), "invest")
    ]
    capacity_battery = results_battery["scalars"][
        (("electricity_dc", "battery"), "invest")
    ]

    total_cost_component = (
        (
            epc_diesel_genset * capacity_diesel_genset
            + epc_pv * capacity_pv
            + epc_rectifier * capacity_rectifier
            + epc_inverter * capacity_inverter
            + epc_battery * capacity_battery
        )
        * n_days
        / n_days_in_year
    )

    # The only componnet with the variable cost is the diesl genset
    total_cost_variable = (
        variable_cost_diesel_genset * sequences_diesel_genset.sum(axis=0)
    )

    total_cost_diesel = diesel_cost * sequences_diesel_consumption.sum(axis=0)
    total_revenue = (
        total_cost_component + total_cost_variable + total_cost_diesel
    )
    total_demand = sequences_demand.sum(axis=0)

    # Levelized cost of electricity in the system in currency's Cent per kWh.
    lcoe = 100 * total_revenue / total_demand

    # The share of renewable energy source used to cover the demand.
    res = (
        100
        * sequences_pv.sum(axis=0)
        / (sequences_diesel_genset.sum(axis=0) + sequences_pv.sum(axis=0))
    )

    # The amount of excess electricity (which must probably be dumped).
    excess_rate = (
        100
        * sequences_excess.sum(axis=0)
        / (sequences_excess.sum(axis=0) + sequences_demand.sum(axis=0))
    )

    ##########################################################################
    # Print the results in the terminal
    ##########################################################################

    if __name__ == "__main__":
        print("\n" + 50 * "*")
        print(
            f"Simulation Time: {end_simulation_time-start_simulation_time:.2f} s"
        )
        print(50 * "*")
        print(f"Peak Demand:\t {sequences_demand.max():.0f} kW")
        print(f"LCOE:\t\t {lcoe:.2f} cent/kWh")
        print(f"RES:\t\t {res:.0f}%")
        print(f"Excess:\t\t {excess_rate:.1f}% of the total production")
        print(50 * "*")
        print("Optimal Capacities:")
        print("-------------------")
        print(f"Diesel Genset:\t {capacity_diesel_genset:.0f} kW")
        print(f"PV:\t\t {capacity_pv:.0f} kW")
        print(f"Battery:\t {capacity_battery:.0f} kW")
        print(f"Inverter:\t {capacity_inverter:.0f} kW")
        print(f"Rectifier:\t {capacity_rectifier:.0f} kW")
        print(50 * "*")

        ##########################################################################
        # Plot the duration curve for the diesel genset
        ##########################################################################

        if plt is not None:
            # Create the duration curve for the diesel genset.
            fig1, ax = plt.subplots(figsize=(10, 5))

            # Sort the power generated by the diesel genset in a descending order.
            diesel_genset_duration_curve = np.sort(sequences_diesel_genset)[
                ::-1
            ]

            percentage = (
                100
                * np.arange(1, len(diesel_genset_duration_curve) + 1)
                / len(diesel_genset_duration_curve)
            )

            ax.scatter(
                percentage,
                diesel_genset_duration_curve,
                color="dodgerblue",
                marker="+",
            )

            # Plot a horizontal line representing the minimum load
            ax.axhline(
                y=min_load * capacity_diesel_genset,
                color="crimson",
                linestyle="--",
            )
            min_load_annotation_text = (
                f"minimum load: {min_load * capacity_diesel_genset:0.2f} kW"
            )
            ax.annotate(
                min_load_annotation_text,
                xy=(100, min_load * capacity_diesel_genset),
                xytext=(0, 5),
                textcoords="offset pixels",
                horizontalalignment="right",
                verticalalignment="bottom",
            )

            # Plot a horizontal line representing the maximum load
            ax.axhline(
                y=max_load * capacity_diesel_genset,
                color="crimson",
                linestyle="--",
            )
            max_load_annotation_text = (
                f"maximum load: {max_load * capacity_diesel_genset:0.2f} kW"
            )
            ax.annotate(
                max_load_annotation_text,
                xy=(100, max_load * capacity_diesel_genset),
                xytext=(0, -5),
                textcoords="offset pixels",
                horizontalalignment="right",
                verticalalignment="top",
            )

            ax.set_title(
                "Duration Curve for the Diesel Genset Electricity Production",
                fontweight="bold",
            )
            ax.set_ylabel("diesel genset production [kW]")
            ax.set_xlabel("percentage of annual operation [%]")

            # Create the second axis on the right side of the diagram
            # representing the operation load of the diesel genset.
            second_ax = ax.secondary_yaxis(
                "right",
                functions=(
                    lambda x: x / capacity_diesel_genset * 100,
                    lambda x: x * capacity_diesel_genset / 100,
                ),
            )
            second_ax.set_ylabel("diesel genset operation load [%]")

            #######################################################################
            # Plot the efficiency curve for the diesel genset
            #######################################################################

            fig2, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(
                load_diesel_genset,
                efficiency_diesel_genset,
                marker="+",
            )

            # Plot a horizontal line representing the minimum efficiency
            ax.axhline(
                y=min_efficiency * 100,
                color="crimson",
                linestyle="--",
            )
            min_efficiency_annotation_text = (
                f"minimum efficiency: {min_efficiency*100:0.0f}%"
            )
            ax.annotate(
                min_efficiency_annotation_text,
                xy=(100, min_efficiency * 100),
                xytext=(0, 10),
                textcoords="offset pixels",
                horizontalalignment="right",
                verticalalignment="bottom",
            )

            # Plot a horizontal line representing the maximum efficiency
            ax.axhline(
                y=max_efficiency * 100,
                color="crimson",
                linestyle="--",
            )
            max_efficiency_annotation_text = (
                f"maximum efficiency: {max_efficiency*100:0.0f}%"
            )
            ax.annotate(
                max_efficiency_annotation_text,
                xy=(100, max_efficiency * 100),
                xytext=(0, 10),
                textcoords="offset pixels",
                horizontalalignment="right",
                verticalalignment="bottom",
            )

            ax.set_title(
                "Efficiency Curve for Different Loads of the Diesel Genset",
                fontweight="bold",
            )
            ax.set_ylabel("efficiency [%]")
            ax.set_xlabel("diesel genset load [%]")

            ax.set_xlim(min_load * 100 - 5, max_load * 100 + 5)

            plt.show()


if __name__ == "__main__":
    main()
