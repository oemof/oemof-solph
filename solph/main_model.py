#!/usr/bin/python    # lint:ok
# -*- coding: utf-8 -*-

'''
Author: Guido Plessmann (guido.plessmann@rl-institut.de)
Changes by: Uwe Krien (uwe.krien@rl-institut.de)
Responsibility: Guido Plessmann, Uwe Krien
'''

import pulp
import logging

from . import objective as obj
from . import chp_constraints as chp
from . import control_constraints as ctrl
from . import demand_cover_constr as demand
from . import energy_production_constr as prod
from . import extend_bus_gas_constr as gas
from . import resource_buses_constr as resc
from . import storage_constraints as store
from . import transmission_grid_constr as trg


def create_storage_constraints(main_dc, prob, store_type):
    '''
    Returns prob extended by model storage constraints
    '''
    prob = store.storage_state(main_dc, store_type, prob)
    prob = store.storage_power_lim(main_dc, store_type, prob)
    return prob


def create_model_equations(main_dc):
    '''
    This functions creates all model (in-)equations by calling subfunctions
    '''

    # Create optimization problem
    logging.debug('Creating optimization problem...')
    prob = pulp.LpProblem('Cost Optimum', pulp.LpMinimize)

    # Create objective function
    logging.debug('Creating objective function...')
    prob = obj.objective(main_dc, prob)

    # Add constraints: Demand coverage
    logging.debug('Adding constraints: Demand coverage...')
    prob = demand.demand_coverage(main_dc, prob)

    # Add constraints: Direct feed-in
    logging.debug('Adding constraints: Direct feed-in...')
    prob = prod.direct_feed_in(main_dc, prob)

    # Add constraints: power_limits
    logging.debug('Adding constraints: power_limits...')
    prob = prod.gen_power_lim(main_dc, prob)

    # Adds constraints: Grid usage
    if main_dc['energy_system']['transmission']:
        logging.debug('Adding constraints: Grid usage')
        prob = trg.grid_constraint(main_dc, prob)
        # Install costs grid
        prob = trg.trg_power_lim(main_dc, prob)

    # Adds constraints: Fossil gas flow split
    if main_dc['check']['extend_nat_gas_bus']:
        logging.debug('Adding constraints: Fossil gas flow split')
        prob = gas.fossil_gas_flow_split(main_dc, prob)
        prob = gas.fossil_gas_consumption_split(main_dc, prob)

    # Add constraints: Resource bus with the yearly resource consumption limit
    logging.debug('Adding constraints: Direct feed-in...')
    prob = resc.resource_bus(main_dc, prob)

    # Adds constraints: Defined share of renewables
    if main_dc['simulation']['re_share']:
        logging.debug('Adding constraints of re-share.')
        prob = ctrl.renewables_share(main_dc, prob)

    # Adds constraints: electrical storages
    if 'elec' in main_dc['energy_system']['storages']:
        logging.debug('Adding constraints of storages.')
        prob = create_storage_constraints(main_dc, prob, 'elec')

    # Adds constraints: electrical storages
    if 'heat' in main_dc['energy_system']['storages']:
        logging.debug('Adding constraints of thermal storages.')
        prob = create_storage_constraints(main_dc, prob, 'heat')

    # Add chp constraints
    if main_dc['energy_system']['transformer']['chp']:
        logging.debug('Adding chp constraints.')
        prob = chp.chp_ratio(main_dc, prob)

    # Add biogas constraints
    if main_dc['check']['biogas']:
        logging.debug('Adding biogas constraints.')
        prob = gas.biogas_bus(main_dc, prob)

    # ramping power
    try:
        main_dc['lp']['ramping_power']
        prob = prod.ramping_power(main_dc, prob)
    except KeyError:  # ramp lp-variable was not created
        pass

    # caps, maximal limit of newly installed capacities
    if main_dc['simulation']['investment'] is True:
        logging.debug('Adding constraints: capacity limits...')
        prob = prod.caps(main_dc, prob)

    # Add constraints: Power to Gas
    if 'gas' in main_dc['energy_system']['transformer']:
        logging.debug('Adding constraints of gas bus')
        prob = gas.gas_bus(main_dc, prob)
        prob = gas.ptg_power_lim(main_dc, prob)

    # Add constraints: gas storage
    if 'gas' in main_dc['energy_system']['storages']:
        logging.debug('Adding constraints of storages for gas.')
        prob = create_storage_constraints(main_dc, prob, 'gas')

    return prob
