"""
Test for creating an MultiPeriod dispatch optimization model

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
from oemof.solph import processing
from oemof.solph import views


def test_multiperiod_dispatch_model(solver="cbc"):
    """Test a simple multiperiod dispatch model
     for multiple SinkDSM approaches"""

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
    bus_el_FR = network.Bus(label='FR_bus_el',
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
        outputs={bus_el: network.Flow(
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
    source_wind_FR = network.Source(
        label='FR_source_wind',
        outputs={bus_el_FR: network.Flow(
            variable_costs=0,
            fix=[45] * len(timeindex),
            nominal_value=1,
            multiperiod=True)})
    source_shortage_FR = network.Source(
        label='FR_source_shortage',
        outputs={bus_el_FR: network.Flow(
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
    sink_el_FR = network.Sink(
        label='FR_sink_el',
        inputs={bus_el_FR: network.Flow(
            fix=[50] * len(timeindex),
            nominal_value=1,
            multiperiod=True)})
    sink_excess_FR = network.Sink(
        label='FR_sink_excess',
        inputs={bus_el_FR: network.Flow(
            variable_costs=1e3,
            nominal_value=1e10,
            multiperiod=True)})

    # Create multiperiod transformers
    pp_lignite = network.Transformer(
        label='DE_pp_lignite',
        inputs={bus_lignite: network.Flow(
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            nominal_value=100,
            variable_costs=1
        )},
        conversion_factors={bus_el: 0.38})

    pp_hardcoal = network.Transformer(
        label='DE_pp_hardcoal',
        inputs={bus_hardcoal: network.Flow(
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            nominal_value=100,
            variable_costs=2
        )},
        conversion_factors={bus_el: 0.45})

    pp_natgas_CCGT = network.Transformer(
        label='DE_pp_natgas_CCGT',
        inputs={bus_natgas: network.Flow(
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            nominal_value=100,
            variable_costs=3,
        )},
        conversion_factors={bus_el: 0.6})

    pp_natgas_GT = network.Transformer(
        label='DE_pp_natgas_GT',
        inputs={bus_natgas: network.Flow(
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            nominal_value=100,
            variable_costs=4,
        )},
        conversion_factors={bus_el: 0.4})

    storage_el = components.GenericStorage(
        label='DE_storage_el',
        inputs={bus_el: network.Flow(
            nominal_value=20,
            variable_costs=0,
            max=1,
            multiperiod=True)},
        outputs={bus_el: network.Flow(
            nominal_value=20,
            variable_costs=0,
            max=1,
            multiperiod=True)},
        nominal_storage_capacity=20,
        loss_rate=0,
        initial_storage_level=0,
        max_storage_level=1,
        min_storage_level=0,
        inflow_conversion_factor=1,
        outflow_conversion_factor=1,
        balanced=True,
        multiperiod=True,
        fixed_costs=10,
    )

    link_DE_FR = custom.Link(
        label='link_DE_FR',
        inputs={
            bus_el: network.Flow(
                nominal_value=10,
                multiperiod=True),
            bus_el_FR: network.Flow(
                nominal_value=10,
                multiperiod=True)
        },
        outputs={
            bus_el_FR: network.Flow(
                multiperiod=True
            ),
            bus_el: network.Flow(
                multiperiod=True
            )
        },
        conversion_factors={
            (bus_el, bus_el_FR): 0.999999,
            (bus_el_FR, bus_el): 0.999999},
        multiperiod=True
    )

    approach = "DLR"

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
        'max_demand': 20,
        'max_capacity_down': 10,
        'max_capacity_up': 10,
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
        multiperiod=True
    )

    es.add(source_lignite, source_hardcoal, source_natgas, source_wind,
           source_shortage,
           bus_lignite, bus_hardcoal, bus_natgas, bus_el,
           pp_lignite, pp_hardcoal, pp_natgas_CCGT, pp_natgas_GT,
           sink_el, sink_excess, storage_el,
           source_wind_FR, source_shortage_FR,
           bus_el_FR, sink_el_FR, sink_excess_FR, link_DE_FR,
           dsm_unit,
           )

    om = models.MultiPeriodModel(es, discount_rate=0.02)
    om.receive_duals()
    om.solve(solver=solver)

    results = processing.results(om)
    test_results = {
        "DE_source_lignite": 0,
        "DE_source_hardcoal": 0,
        "DE_source_natgas": 0,
        "DE_source_wind": 830,
        "DE_source_shortage": 0,
        "DE_bus_lignite": 44,
        "DE_bus_hardcoal": 88,
        "DE_bus_natgas": 176,
        "DE_bus_el": 1909,
        "DE_pp_lignite": 115,
        "DE_pp_hardcoal": 0,
        "DE_pp_natgas_CCGT": 0,
        "DE_pp_natgas_GT": 0,
        "DE_sink_el": 720,
        "DE_sink_excess": 0,
        "DE_storage_el": 285,
        "FR_source_wind": 405,
        "FR_source_shortage": 0,
        "FR_bus_el": 909,
        "FR_sink_el": 450,
        "FR_sink_excess": 0,
        "link_DE_FR": 90,
        "demand_dsm": 180
    }

    for key in test_results.keys():
        eq_((int(views.node(results, key)['sequences']
                 .sum(axis=0).round(0).sum())), test_results[key])
