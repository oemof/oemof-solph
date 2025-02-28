"""
Test for creating an multi-period investment optimization model

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
import pytest

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import _options
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import flows
from oemof.solph import processing
from oemof.solph import views


@pytest.mark.filterwarnings(
    "ignore:Ensure that your timeindex and timeincrement are"
    " consistent.:UserWarning"
)
@pytest.mark.filterwarnings(
    "ignore:CAUTION! You specified the 'periods' attribute:UserWarning"
)
def test_multi_period_investment_model(solver="cbc"):
    """Test a simple multi_period investment model
    for multiple SinkDSM approaches"""

    for approach in ["oemof", "DLR", "DIW"]:
        t_idx_1 = pd.date_range("1/1/2020", periods=3, freq="h")
        t_idx_2 = pd.date_range("1/1/2030", periods=3, freq="h")
        t_idx_3 = pd.date_range("1/1/2040", periods=3, freq="h")

        # Create an overall timeindex
        t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
        t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
        t_idx_3_series = pd.Series(index=t_idx_3, dtype="float64")

        timeindex = pd.concat(
            [t_idx_1_series, t_idx_2_series, t_idx_3_series]
        ).index
        periods = [t_idx_1, t_idx_2, t_idx_3]

        es = EnergySystem(
            timeindex=timeindex,
            timeincrement=[1] * len(timeindex),
            periods=periods,
            infer_last_interval=False,
        )

        # Create buses
        bus_lignite = buses.Bus(label="DE_bus_lignite", balanced=True)
        bus_hardcoal = buses.Bus(label="DE_bus_hardcoal", balanced=True)
        bus_natgas = buses.Bus(label="DE_bus_natgas", balanced=True)
        bus_el = buses.Bus(label="DE_bus_el", balanced=True)
        bus_el_FR = buses.Bus(label="FR_bus_el", balanced=True)

        # Create sources
        source_lignite = components.Source(
            label="DE_source_lignite",
            outputs={bus_lignite: flows.Flow(variable_costs=5)},
        )
        source_hardcoal = components.Source(
            label="DE_source_hardcoal",
            outputs={bus_hardcoal: flows.Flow(variable_costs=10)},
        )
        source_natgas = components.Source(
            label="DE_source_natgas",
            outputs={bus_natgas: flows.Flow(variable_costs=20)},
        )
        source_wind = components.Source(
            label="DE_source_wind",
            outputs={
                bus_el: flows.Flow(
                    variable_costs=0,
                    fix=[110] + [90] * (len(timeindex) - 1),
                    nominal_capacity=1,
                )
            },
        )
        source_shortage = components.Source(
            label="DE_source_shortage",
            outputs={
                bus_el: flows.Flow(variable_costs=1e10, nominal_capacity=1e10)
            },
        )
        source_wind_FR = components.Source(
            label="FR_source_wind",
            outputs={
                bus_el_FR: flows.Flow(
                    variable_costs=0,
                    fix=[45] * len(timeindex),
                    nominal_capacity=1,
                )
            },
        )
        source_shortage_FR = components.Source(
            label="FR_source_shortage",
            outputs={
                bus_el_FR: flows.Flow(
                    variable_costs=1e10, nominal_capacity=1e10
                )
            },
        )

        # Create sinks
        sink_el = components.Sink(
            label="DE_sink_el",
            inputs={
                bus_el: flows.Flow(
                    fix=[80] * len(timeindex), nominal_capacity=1
                )
            },
        )
        sink_excess = components.Sink(
            label="DE_sink_excess",
            inputs={
                bus_el: flows.Flow(variable_costs=1e10, nominal_capacity=1e10)
            },
        )
        sink_el_FR = components.Sink(
            label="FR_sink_el",
            inputs={
                bus_el_FR: flows.Flow(
                    fix=[50] * len(timeindex), nominal_capacity=1
                )
            },
        )
        sink_excess_FR = components.Sink(
            label="FR_sink_excess",
            inputs={
                bus_el_FR: flows.Flow(
                    variable_costs=1e3, nominal_capacity=1e10
                )
            },
        )

        # Create converters
        pp_lignite = components.Converter(
            label="DE_pp_lignite",
            inputs={bus_lignite: flows.Flow()},
            outputs={
                bus_el: flows.Flow(
                    nominal_capacity=_options.Investment(
                        maximum=1000,
                        ep_costs=2e6,
                        existing=0,
                        lifetime=20,
                        age=0,
                    ),
                    variable_costs=1,
                )
            },
            conversion_factors={bus_el: 0.38},
        )

        pp_hardcoal = components.Converter(
            label="DE_pp_hardcoal",
            inputs={bus_hardcoal: flows.Flow()},  # )},
            outputs={
                bus_el: flows.Flow(
                    nominal_capacity=_options.Investment(
                        maximum=1000,
                        ep_costs=1.6e6,
                        existing=0,
                        lifetime=20,
                        age=0,
                    ),
                    variable_costs=2,
                )
            },
            conversion_factors={bus_el: 0.45},
        )

        pp_natgas_CCGT = components.Converter(
            label="DE_pp_natgas_CCGT",
            inputs={bus_natgas: flows.Flow()},  # )},
            outputs={
                bus_el: flows.Flow(
                    nominal_capacity=_options.Investment(
                        maximum=1000,
                        ep_costs=1e6,
                        existing=0,
                        lifetime=20,
                        age=0,
                    ),
                    variable_costs=3,
                )
            },
            conversion_factors={bus_el: 0.6},
        )

        pp_natgas_GT = components.Converter(
            label="DE_pp_natgas_GT",
            inputs={bus_natgas: flows.Flow()},  # )},
            outputs={
                bus_el: flows.Flow(
                    nominal_capacity=_options.Investment(
                        maximum=1000,
                        ep_costs=[0.6e6, 0.5e6, 0.8e6, 0.4e6],
                        existing=0,
                        lifetime=20,
                        age=0,
                        fixed_costs=1000,
                    ),
                    variable_costs=4,
                )
            },
            conversion_factors={bus_el: 0.4},
        )

        storage_el = components.GenericStorage(
            label="DE_storage_el",
            inputs={
                bus_el: flows.Flow(
                    variable_costs=0,
                    max=1,
                    nominal_capacity=_options.Investment(
                        maximum=20,
                        ep_costs=1000,
                        existing=10,
                        lifetime=2,
                        age=1,
                    ),
                )
            },
            outputs={
                bus_el: flows.Flow(
                    variable_costs=0,
                    max=1,
                    nominal_capacity=_options.Investment(
                        maximum=20,
                        ep_costs=1000,
                        existing=10,
                        lifetime=2,
                        age=1,
                    ),
                )
            },
            loss_rate=0,
            max_storage_level=1,
            min_storage_level=0,
            inflow_conversion_factor=1,
            outflow_conversion_factor=1,
            balanced=True,
            invest_relation_input_output=1,
            invest_relation_input_capacity=None,
            invest_relation_output_capacity=None,
            fixed_costs=10,
            nominal_capacity=_options.Investment(
                maximum=20,
                ep_costs=1000,
                existing=10,
                lifetime=2,
                age=1,
                fixed_costs=10,
            ),
        )

        link_DE_FR = components.Link(
            label="link_DE_FR",
            inputs={
                bus_el: flows.Flow(
                    nominal_capacity=10,
                ),
                bus_el_FR: flows.Flow(
                    nominal_capacity=10,
                ),
            },
            outputs={bus_el_FR: flows.Flow(), bus_el: flows.Flow()},
            conversion_factors={
                (bus_el, bus_el_FR): 0.999999,
                (bus_el_FR, bus_el): 0.999999,
            },
        )

        kwargs_all = {
            "label": "demand_dsm",
            "inputs": {
                bus_el: flows.Flow(
                    variable_costs=0,
                )
            },
            "demand": [1] * len(timeindex),
            "capacity_up": [1] * len(timeindex),
            "capacity_down": [1] * len(timeindex),
            "delay_time": 4,
            "shed_time": 2,
            "max_demand": [1] * len(es.periods),
            "recovery_time_shift": 0,
            "recovery_time_shed": 24,
            "cost_dsm_up": 0.01,
            "cost_dsm_down_shift": 0.01,
            "cost_dsm_down_shed": 1000,
            "efficiency": 1.0,
            "shed_eligibility": False,
            "shift_eligibility": True,
            "shift_time": 2,
        }

        kwargs_dict = {
            "oemof": {"shift_interval": 24},
            "DIW": {},
            "DLR": {
                "ActivateYearLimit": True,
                "ActivateDayLimit": True,
                "n_yearLimit_shift": 2,
                "n_yearLimit_shed": 10,
                "t_dayLimit": 2,
                "addition": True,
                "fixes": True,
            },
        }

        dsm_unit = components.experimental.SinkDSM(
            **kwargs_all,
            approach=approach,
            **kwargs_dict[approach],
            investment=_options.Investment(
                existing=10,
                maximum=20,
                ep_costs=10,
                lifetime=2,
                age=1,
            ),
        )

        es.add(
            source_lignite,
            source_hardcoal,
            source_natgas,
            source_wind,
            source_shortage,
            bus_lignite,
            bus_hardcoal,
            bus_natgas,
            bus_el,
            pp_lignite,
            pp_hardcoal,
            pp_natgas_CCGT,
            pp_natgas_GT,
            sink_el,
            sink_excess,
            storage_el,
            source_wind_FR,
            source_shortage_FR,
            bus_el_FR,
            sink_el_FR,
            sink_excess_FR,
            link_DE_FR,
            dsm_unit,
        )

        om = Model(es, discount_rate=0.02)
        om.receive_duals()
        om.solve(solver=solver)

        results = processing.results(om)
        test_results = {
            "DE_bus_el": pd.Series(
                {
                    "invest": 0,
                    "old": 20,
                    "old_end": 20,
                    "old_exo": 20,
                    "total": 20,
                },
                name="variable_name",
            ),
            "demand_dsm": pd.Series(
                {
                    "invest": 13,
                    "old": 10,
                    "old_end": 0,
                    "old_exo": 10,
                    "total": 37,
                },
                name="variable_name",
            ),
            "DE_storage_el": pd.Series(
                {
                    "invest": 0,
                    "old": 30,
                    "old_end": 0,
                    "old_exo": 30,
                    "total": 30,
                },
                name="variable_name",
            ),
        }

        for key in test_results.keys():
            assert (
                views.node(results, key)["period_scalars"]
                .sum(axis=0)
                .round(0)
                .convert_dtypes("int")
            ).any() == test_results[key].any()
