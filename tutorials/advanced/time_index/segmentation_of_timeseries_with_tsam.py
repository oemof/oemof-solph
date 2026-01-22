import warnings
from pathlib import Path
import tsam.timeseriesaggregation as tsam

import numpy as np
import pandas as pd
from oemof.tools import debugging
from oemof.tools import logger

warnings.filterwarnings(
    "ignore", category=debugging.ExperimentalFeatureWarning
)
logger.define_logging()

file_path = Path(__file__).parent

df = pd.read_csv(
    Path(file_path, "energy.csv"),
)
df["time"] = pd.to_datetime(df["Unix Epoch"], unit="s")
# time als Index setzen
df = df.set_index("time")
df = df.drop(columns=["Unix Epoch"])
print(df)

time_index = df.index

# Dummy pv profile
h = np.arange(len(time_index))
pv_profile = df["PV (W)"]

# Dummy electricity profile
df["house_elec_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# Dummy heat profile
df["house_heat_kW"] = 0.3 + 0.7 * np.random.rand(len(time_index))

# EV-Ladeprofil
df["ev_charge_kW"] = (
    0.0  # wird automatisch auf alle Zeitschritte gebroadcastet
)

# COP-Profil (konstant, später evtl. temperaturabhängig)
df["cop_hp"] = 3.5

# Clustering of Input time-series with TSAM
# not a high number of typical periods works with high number of hours per
# period
typical_periods = 7
hours_per_period = 24 * 60

aggregation_no_segmentation = tsam.TimeSeriesAggregation(
    timeSeries=df,
    noTypicalPeriods=typical_periods,
    hoursPerPeriod=hours_per_period,
    clusterMethod="k_means",
    sortValues=False,
    rescaleClusterPeriods=False,
)
aggregation_no_segmentation.createTypicalPeriods()
tindex_agg = pd.date_range(
    "2022-01-01", periods=typical_periods * hours_per_period, freq="H"
)

print(aggregation_no_segmentation.typicalPeriods["house_elec_kW"])

# aggregation with segmentation
# has to be hourly values, other values don't work because it is to big
df = df.resample("1h").mean()
typical_periods = 40
hours_per_period = 24

aggregation_with_segmentation = tsam.TimeSeriesAggregation(
    timeSeries=df,
    noTypicalPeriods=typical_periods,
    hoursPerPeriod=hours_per_period,
    clusterMethod="k_means",
    sortValues=False,
    rescaleClusterPeriods=False,
    segmentation=True,
    noSegments=6,
)
aggregation_with_segmentation.createTypicalPeriods()

print(aggregation_with_segmentation.typicalPeriods["house_elec_kW"])
