"""
Test for creating an MultiPeriod optimization model

Create an energy system consisting of the following fleets
- lignite
- hardcoal
- CCGT
- GT
- Wind
- GenericStorage unit
- SinkDSM unit
for Germany

Add wind source and demand sink for FR and links for exchange.
"""

import pandas as pd
from nose.tools import eq_

from oemof.solph import components
from oemof.solph import custom
from oemof.solph import models
from oemof.solph import network
from oemof.solph import options
from oemof.solph import processing
from oemof.solph import views


def test_multiperiod_model(solver="cbc"):
    """Test a simple multiperiod investment model"""

    t_idx_1 = pd.date_range('1/1/2020', periods=3, freq='H')
    t_idx_2 = pd.date_range('1/1/2030', periods=3, freq='H')
    t_idx_3 = pd.date_range('1/1/2040', periods=3, freq='H')

    # Create an overall timeindex
    t_idx_1_Series = pd.Series(index=t_idx_1, dtype='float64')
    t_idx_2_Series = pd.Series(index=t_idx_2, dtype='float64')
    t_idx_3_Series = pd.Series(index=t_idx_3, dtype='float64')

    timeindex = pd.concat([t_idx_1_Series, t_idx_2_Series,
                           t_idx_3_Series]).index

    es = network.EnergySystem(timeindex=timeindex,
                              timeincrement=[1] * len(timeindex))

    # Create buses
    bus_lignite = network.Bus(label='DE_bus_lignite',
                              balanced=True,
                              multiperiod=True)
    bus_hardcoal = network.Bus(label='DE_bus_hardcoal',
                               balanced=True,
                               multiperiod=True)
    bus_natgas = network.Bus(label='DE_bus_natgas',
                             balanced=True,
                             multiperiod=True)
    bus_el = network.Bus(label='DE_bus_el',
                         balanced=True,
                         multiperiod=True)

    # Create sources
    source_lignite = network.Source(
        label='DE_source_lignite',
        outputs={bus_lignite: network.Flow(
            variable_costs=5,
            multiperiod=True)})
    source_hardcoal = network.Source(
        label='DE_source_hardcoal',
        outputs={bus_hardcoal: network.Flow(
            variable_costs=10,
            multiperiod=True)})
    source_natgas = network.Source(
        label='DE_source_natgas',
        outputs={bus_natgas: network.Flow(
            variable_costs=20,
            multiperiod=True)})
    source_wind = network.Source(
        label='DE_source_wind',
        outputs={bus_el: network.Flow(  # variable_costs=0)})
            variable_costs=0,
            fix=[110] + [90] * (len(timeindex) - 1),
            nominal_value=1,
            multiperiod=True)})
    source_shortage = network.Source(
        label='DE_source_shortage',
        outputs={bus_el: network.Flow(
            variable_costs=1e10,
            nominal_value=1e10,
            multiperiod=True)})

    # Create sinks
    sink_el = network.Sink(
        label='DE_sink_el',
        inputs={bus_el: network.Flow(
            fix=[80] * len(timeindex),
            nominal_value=1,
            multiperiod=True)})

    sink_excess = network.Sink(
        label='DE_sink_excess',
        inputs={bus_el: network.Flow(
            variable_costs=1e10,
            nominal_value=1e10,
            multiperiod=True)})

    # Create multiperiod transformers
    pp_lignite = network.Transformer(
        label='DE_pp_lignite',
        inputs={bus_lignite: network.Flow(
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=1000,
                ep_costs=2e6,
                existing=0,
                lifetime=20,
                age=0,
                interest_rate=0.02,
            ),
            variable_costs=1
        )},
        conversion_factors={bus_el: 0.38})

    pp_hardcoal = network.Transformer(
        label='DE_pp_hardcoal',
        inputs={bus_hardcoal: network.Flow(  # )},
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=1000,
                ep_costs=1.6e6,
                existing=0,
                lifetime=20,
                age=0,
                interest_rate=0.02,
            ),
            variable_costs=2
        )},
        conversion_factors={bus_el: 0.45})

    pp_natgas_CCGT = network.Transformer(
        label='DE_pp_natgas_CCGT',
        inputs={bus_natgas: network.Flow(  # )},
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=1000,
                ep_costs=1e6,
                existing=0,
                lifetime=20,
                age=0,
                interest_rate=0.02,
            ),
            variable_costs=3,
        )},
        conversion_factors={bus_el: 0.6})

    pp_natgas_GT = network.Transformer(
        label='DE_pp_natgas_GT',
        inputs={bus_natgas: network.Flow(  # )},
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=1000,
                ep_costs=[0.6e6, 0.5e6, 0.8e6, 0.4e6],
                existing=0,
                lifetime=20,
                age=0,
                interest_rate=0.02,
                fixed_costs=1000,
            ),
            variable_costs=4,
        )},
        conversion_factors={bus_el: 0.4})

    storage_el = components.GenericStorage(
        label='DE_storage_el',
        inputs={bus_el: network.Flow(
            variable_costs=0,
            max=1,
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=20,
                ep_costs=1000,
                existing=10,
                lifetime=2,
                age=1,
                interest_rate=0.02,
            )
        )},
        outputs={bus_el: network.Flow(
            variable_costs=0,
            max=1,
            multiperiodinvestment=options.MultiPeriodInvestment(
                maximum=20,
                ep_costs=1000,
                existing=10,
                lifetime=2,
                age=1,
                interest_rate=0.02,
            )
        )},
        loss_rate=0,
        initial_storage_level=0,
        max_storage_level=1,
        min_storage_level=0,
        inflow_conversion_factor=1,
        outflow_conversion_factor=1,
        balanced=True,
        invest_relation_input_output=1,
        invest_relation_input_capacity=None,
        invest_relation_output_capacity=None,
        fixed_costs=10,
        multiperiodinvestment=options.MultiPeriodInvestment(
            maximum=20,
            ep_costs=1000,
            existing=10,
            lifetime=2,
            age=1,
            interest_rate=0.02,
            fixed_costs=10,
        )
    )

    approach = 'DLR'

    kwargs_all = {
        'label': 'demand_dsm',
        'inputs': {bus_el: network.Flow(
            variable_costs=0,
            multiperiod=True
        )},
        'demand': [1] * len(timeindex),
        'capacity_up': [1] * len(timeindex),
        'capacity_down': [1] * len(timeindex),
        'delay_time': 4,
        'shed_time': 2,
        'recovery_time_shift': 0,
        'recovery_time_shed': 24,
        'cost_dsm_up': 0.01,
        'cost_dsm_down_shift': 0.01,
        'cost_dsm_down_shed': 1000,
        'efficiency': 1.0,
        'shed_eligibility': False,
        'shift_eligibility': True,
        'flex_share_down': 1,
        'flex_share_up': 1,
        'shift_time': 2}

    kwargs_dict = {
        'oemof': {'shift_interval': 24},

        'DIW': {},

        'DLR': {'ActivateYearLimit': True,
                'ActivateDayLimit': True,
                'n_yearLimit_shift': 2,
                'n_yearLimit_shed': 10,
                't_dayLimit': 2,
                'addition': True,
                'fixes': True},
    }

    dsm_unit = custom.SinkDSM(
        **kwargs_all,
        approach=approach,
        **kwargs_dict[approach],
        multiperiodinvestment=options.MultiPeriodInvestment(
            existing=10,
            maximum=20,
            ep_costs=10,
            lifetime=2,
            age=1,
            interest_rate=0.02
        )
    )

    es.add(source_lignite, source_hardcoal, source_natgas, source_wind,
           source_shortage,
           bus_lignite, bus_hardcoal, bus_natgas, bus_el,
           pp_lignite, pp_hardcoal, pp_natgas_CCGT, pp_natgas_GT,
           sink_el, sink_excess, storage_el,
           dsm_unit,
           )

    om = models.MultiPeriodModel(es, discount_rate=0.02)
    om.receive_duals()
    om.solve(solver=solver)

    results = processing.results(om)
    test_results = {
        "DE_bus_el": pd.Series(
            {"invest": 0,
             "old": 20,
             "old_end": 20,
             "old_exo": 20,
             "total": 20},
            name="variable_name"),
        "demand_dsm": pd.Series(
            {"invest": 13,
             "old": 10,
             "old_end": 0,
             "old_exo": 10,
             "total": 37},
            name="variable_name"),
        "DE_storage_el": pd.Series(
            {"invest": 0,
             "old": 30,
             "old_end": 0,
             "old_exo": 30,
             "total": 30},
            name="variable_name")
    }

    for key in test_results.keys():
        eq_((views.node(results, key)['scalars'].sum(axis=0).round(0)
             .convert_dtypes("int")).any(), test_results[key].any())
