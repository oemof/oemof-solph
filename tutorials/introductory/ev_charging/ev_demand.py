import pandas as pd

# Define the trip demand series for the real trip scenario.
# As the demand is a power time series, it has N-1 entries
# when compared to the N entires of time axis for the energy.
ev_demand = pd.Series(0, index=time_index[:-1])

# Morning Driving: 07:00 to 08:00
driving_start_morning = pd.Timestamp("2025-01-01 07:10")
driving_end_morning = pd.Timestamp("2025-01-01 08:10")
ev_demand.loc[driving_start_morning:driving_end_morning] = 10  # kW

# Evening Driving: 17:00 to 18:00.
# Note that time points work even if they are not in the index.
driving_start_evening = pd.Timestamp("2025-01-01 16:13:37")
driving_end_evening = pd.Timestamp("2025-01-01 17:45:11")
ev_demand.loc[driving_start_evening:driving_end_evening] = 9  # kW
