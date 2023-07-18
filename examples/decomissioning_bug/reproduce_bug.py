from oemof import solph
import pandas as pd

# Create an energy system


t_idx_1 = pd.date_range("1/1/2015", periods=3, freq="H")
t_idx_2 = pd.date_range("1/1/2035", periods=3, freq="H")
t_idx_3 = pd.date_range("1/1/2050", periods=3, freq="H")

# Create an overall timeindex
t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
t_idx_3_series = pd.Series(index=t_idx_3, dtype="float64")

timeindex = pd.concat(
    [t_idx_1_series, t_idx_2_series, t_idx_3_series]
).index

periods = [t_idx_1, t_idx_2, t_idx_3]

es = solph.EnergySystem(timeindex=timeindex,
                        timeincrement=[1] * len(timeindex),
                        periods=periods,
                        infer_last_interval=False)

df_profiles = pd.read_csv("profiles.csv", index_col=0, parse_dates=True)

bel = solph.Bus(label="electricity", balanced=True)

storage = solph.components.GenericStorage(
    label="storage",
    inputs={bel: solph.Flow(variable_costs=0,
                            investment=solph.Investment(
                                ep_costs=10,
                                existing=0,
                                lifetime=20,
                                age=0,
                                interest_rate=0.02,
                            ))},

    outputs={bel: solph.Flow(variable_costs=0,
                             investment=solph.Investment(
                                 ep_costs=10,
                                 existing=0,
                                 lifetime=20,
                                 age=0,
                                 interest_rate=0.02,
                             ))},
    loss_rate=0.00,
    invest_relation_output_capacity=0.2,
    invest_relation_input_output=1,
    # inflow_conversion_factor=1,
    # outflow_conversion_factor=0.8,
    # nominal_storage_capacity=100,
    investment=solph.Investment(ep_costs=10,
                                maximum=float("+inf"),
                                existing=0,
                                lifetime=20,
                                age=0,
                                fixed_costs=None,
                                interest_rate=0.02,
                                ),
)

demand = solph.components.Sink(
    label="demand",
    inputs={bel: solph.Flow(fix=df_profiles["demand"],
                            nominal_value=1e5)},
)

pv = solph.components.Source(
    label="pv",
    outputs={bel: solph.Flow(
        fix=df_profiles["pv-profile"],
        investment=solph.Investment(
            ep_costs=20,
            maximum=float("+inf"),
            minimum=0,
            lifetime=20,
            age=0,
            interest_rate=0.02,
        ))
    }
)

wind = solph.components.Source(
    label="wind",
    outputs={bel: solph.Flow(fix=df_profiles["wind-profile"],
                             investment=solph.Investment(ep_costs=50,
                                                         maximum=float("+inf"),
                                                         minimum=0,
                                                         lifetime=20,
                                                         age=0,
                                                         interest_rate=0.02,
                                                         ))

             }
)
es.add(bel, storage, demand, pv, wind)

# Create an optimization problem and solve it
om = solph.Model(es)

# Solve the optimization problem
om.solve(solver="cbc", solve_kwargs={"tee": True})

results = om.results()

result_views = solph.views.convert_keys_to_strings(results)

# Investment results for
# storage capacity investment
df_storage_invest_mwh = result_views[('storage', 'None')]['period_scalars']
# capacity investment
df_storage_invest_mw = result_views[('storage', 'electricity')]['period_scalars']

print("done")
