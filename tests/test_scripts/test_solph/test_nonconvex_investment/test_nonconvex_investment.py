# -*- coding: utf-8 -*-

"""
This test contains a NonConvexInvestFlow class.


SPDX-FileCopyrightText: Saeed Sayadi
SPDX-FileCopyrightText: Pierre-François Duc

SPDX-License-Identifier: MIT

General description
-------------------
This example illustrates the application of the NonConvexInvestFlow to
a diesel generator in a hybrid mini-grid system.

There are the following components:

    - pv: solar potential to generate electricity
    - diesel_source: input diesel for the diesel genset
    - diesel_genset: generates ac electricity
    - rectifier: converts generated ac electricity from the diesel genset
                 to dc electricity
    - inverter: converts generated dc electricity from the pv to ac electricity
    - battery: stores the generated dc electricity
    - demand_el: ac electricity demand (given as a separate *.csv file)
    - excess_el: allows for some electricity overproduction



Installation requirements
-------------------------
This example requires the version v0.5.x of oemof.solph. Install by:

    pip install 'oemof.solph>=0.5,<0.6'

"""

__copyright__ = "oemof developer group"
__license__ = "MIT"

import os
from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd

from oemof import solph

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def test_nonconvex_investment(solver="cbc"):
    ##########################################################################
    # Initialize the energy system and calculate necessary parameters
    ##########################################################################
    start = "2022-01-01"

    # The maximum number of days depends on the given *.csv file.
    n_days = 10
    n_days_in_year = 365

    # Create date and time objects.
    start_date_obj = datetime.strptime(start, "%Y-%m-%d")
    start_date = start_date_obj.date()
    start_datetime = datetime.combine(
        start_date_obj.date(), start_date_obj.time()
    )
    end_datetime = start_datetime + timedelta(days=n_days)

    # Import data.
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_directory, "diesel_genset_data.csv")
    data = pd.read_csv(filepath_or_buffer=filename)

    # Change index of data to be able to select data based on the time range.
    data.index = pd.date_range(start="2022-01-01", periods=len(data), freq="H")

    # Choose the range of the solar potential and demand
    # based on the selected simulation period.
    solar_potential = data.SolarGen.loc[start_datetime:end_datetime]
    hourly_demand = data.Demand.loc[start_datetime:end_datetime]
    peak_solar_potential = solar_potential.max()
    peak_demand = hourly_demand.max()

    # Create the energy system.
    date_time_index = pd.date_range(
        start=start_date, periods=n_days * 24, freq="H"
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
                nominal_value=None,
                investment=solph.Investment(
                    ep_costs=epc_pv * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
    )

    # -------------------- TRANSFORMERS --------------------
    # The diesel genset assumed to have a fixed efficiency of 33%.

    # The output power of the diesel genset can only vary between
    # the given minimum and maximum loads, which represent the fraction
    # of the optimal capacity obtained from the optimization.

    # If the `min` attribute is set to 0, the NonConvex attribute
    # has no effect, so the flow will be similar to the `InvestmentFlow`
    # and it is better to avoid using the `NonConvexInvestFlow` for such cases.

    epc_diesel_genset = 84.80  # currency/kW/year
    variable_cost_diesel_genset = 0.045  # currency/kWh
    min_load = 0.2
    max_load = 1.0
    diesel_genset = solph.components.Transformer(
        label="diesel_genset",
        inputs={b_diesel: solph.flows.Flow()},
        outputs={
            b_el_ac: solph.flows.Flow(
                nominal_value=None,
                variable_costs=variable_cost_diesel_genset,
                min=min_load,
                max=max_load,
                investment=solph.Investment(
                    ep_costs=epc_diesel_genset * n_days / n_days_in_year,
                    maximum=2 * peak_demand,
                ),
                nonconvex=solph.NonConvex(),
            )
        },
        conversion_factors={b_el_ac: 0.33},
    )

    # The rectifier assumed to have a fixed efficiency of 98%.
    epc_rectifier = 62.35  # currency/kW/year
    rectifier = solph.components.Transformer(
        label="rectifier",
        inputs={
            b_el_ac: solph.flows.Flow(
                nominal_value=None,
                investment=solph.Investment(
                    ep_costs=epc_rectifier * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
        outputs={b_el_dc: solph.flows.Flow()},
        conversion_factor={
            b_el_dc: 0.98,
        },
    )

    # The inverter assumed to have a fixed efficiency of 98%.
    epc_inverter = 62.35  # currency/kW/year
    inverter = solph.components.Transformer(
        label="inverter",
        inputs={
            b_el_dc: solph.flows.Flow(
                nominal_value=None,
                investment=solph.Investment(
                    ep_costs=epc_inverter * n_days / n_days_in_year
                ),
                variable_costs=0,
            )
        },
        outputs={b_el_ac: solph.flows.Flow()},
        conversion_factor={
            b_el_ac: 0.98,
        },
    )

    # -------------------- STORAGE --------------------
    epc_battery = 101.00  # currency/kWh/year
    battery = solph.components.GenericStorage(
        label="battery",
        nominal_storage_capacity=None,
        investment=solph.Investment(
            ep_costs=epc_battery * n_days / n_days_in_year
        ),
        inputs={b_el_dc: solph.flows.Flow(variable_costs=0)},
        outputs={
            b_el_dc: solph.flows.Flow(investment=solph.Investment(ep_costs=0))
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
                nominal_value=peak_demand,
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

    # The higher the MipGap or ratioGap, the faster the solver would converge,
    # but the less accurate the results would be.
    solver_option = {"gurobi": {"MipGap": "0.02"}, "cbc": {"ratioGap": "0.02"}}

    model = solph.Model(energy_system)
    model.solve(
        solver=solver,
        solve_kwargs={"tee": True},
        cmdline_options=solver_option[solver],
    )

    ##########################################################################
    # Process the results
    ##########################################################################
    results = solph.processing.results(model)

    results_diesel_genset = solph.views.node(
        results=results, node="diesel_genset"
    )

    # -------------------- SEQUENCES (DYNAMIC) --------------------

    # Hourly profiles for electricity production in the diesel genset.
    sequences_diesel_genset = results_diesel_genset["sequences"][
        (("diesel_genset", "electricity_ac"), "flow")
    ]

    # -------------------- SCALARS (STATIC) --------------------
    capacity_diesel_genset = results_diesel_genset["scalars"][
        (("diesel_genset", "electricity_ac"), "invest")
    ]

    # Define a tolerance to force 'too close' numbers to the `min_load`
    # and to 0 to be the same as the `min_load` and 0.
    tol = 1e-8
    load_diesel_genset = sequences_diesel_genset / capacity_diesel_genset
    sequences_diesel_genset[np.abs(load_diesel_genset) < tol] = 0
    sequences_diesel_genset[np.abs(load_diesel_genset - min_load) < tol] = (
        min_load * capacity_diesel_genset
    )
    sequences_diesel_genset[np.abs(load_diesel_genset - max_load) < tol] = (
        max_load * capacity_diesel_genset
    )

    # Calculate the operation load of the diesel genset
    load_diesel_genset = sequences_diesel_genset / capacity_diesel_genset

    # check min load
    # Error message in case the test fails.
    msg = "Diesel genset operates below the defined `min_load`."
    assert all(
        (0 < load < min_load) is False for load in load_diesel_genset
    ), msg

    # check max load
    # Error message in case the test fails.
    msg = "Diesel genset operates above the defined `max_load`."
    assert all((load > max_load) is False for load in load_diesel_genset), msg
