# -*- coding: utf-8 -*-

"""
Private helper functions.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: David Fuhrländer
SPDX-FileCopyrightText: Johannes Röder

SPDX-License-Identifier: MIT

"""

from warnings import warn

from oemof.tools import debugging

from tsam.timeseriesaggregation import TimeSeriesAggregation
from tsam.hyperparametertuning import HyperTunedAggregations
from typing import Dict, List

import copy
import pandas as pd
def check_node_object_for_missing_attribute(obj, attribute):
    """Raises a predefined warning if object does not have attribute.

    Arguments
    ---------

    obj : python object
    attribute : (string) name of the attribute to test for

    """
    if not getattr(obj, attribute):
        warn_if_missing_attribute(obj, attribute)


def warn_if_missing_attribute(obj, attribute):
    """Raises warning if attribute is missing for given object"""
    msg = (
        "Attribute <{0}> is missing in Node <{1}> of {2}.\n"
        "If this is intended and you know what you are doing you can"
        "disable the SuspiciousUsageWarning globally."
    )
    warn(
        msg.format(attribute, obj.label, type(obj)),
        debugging.SuspiciousUsageWarning,
    )

def aggregate_time_series(
    data_dict_to_aggregate: Dict[str, Dict[str, any]],
    number_of_typical_periods: int = 7,
    number_of_time_steps_per_periods : int = 24,
    number_of_segments_per_period :int = 16,
    segmentation : bool = False,
    cluster_method : str = 'hierarchical',
    sort_values : bool = True,
    minutes_per_time_step : int = 60,
    ):
    """Aggregate timeseries with the tsam-package.
    Firstly controls format of input data.
    Secondly does time series aggregation with tsam.
    Thirdly changes datetime index of dataframe of results.

    Arguments
    ---------
    #todo: Few explanations are copied 1to1 from tsam. Here has to be correctly linked to source!
    data_dict_to_aggregate : Dictionary of a dictionary with a time series and a weighted factor. The "timeseries" has
                             to have the datetime as index and the timeseries parameters as columns. Format:
                             data_dict_to_aggregate = {"name" : {"timeseries" : pd.Series, "weighted_factor" : float}
    number_of_typical_periods : (int) Number of typical Periods - equivalent to the number of clusters.
    number_of_time_steps_per_periods: (int)  Value which defines the length of a cluster period.
    number_of_segments_per_period: (int) Number of segments in which the typical periods should be subdivided -
                                    equivalent to the number of inner-period clusters.
    segmentation: (bool) Decision variable if typical periods should be subdivided
    cluster_method: (str) Chosen clustering method
                     Options are:
                    * 'averaging'
                    * 'k_means'
                    * 'k_medoids'
                    * 'k_maxoids'
                    * 'hierarchical'
                    * 'adjacent_periods'
    sort_values : (bool) #todo understand what this variable does
    """
    entry_format_timeseries = None
    for entry_name, entry_data in data_dict_to_aggregate.items():
        if not isinstance(entry_data, dict):
            raise ValueError(f"Entry '{entry_name}' should have a dictionary as its value.")

        required_keys = ["timeseries", "weighted_factor"]
        missing_keys = [key for key in required_keys if key not in entry_data]

        if entry_format_timeseries is None:
            entry_format_timeseries = entry_data["timeseries"].index
        else:
            if not entry_format_timeseries.equals(entry_data["timeseries"].index):
                raise ValueError(f"TimeSeries Format of at least'{entry_name}' is unequal to: {previous_entry_name}")
            previous_entry_name = entry_name
        if missing_keys:
            raise ValueError(f"Entry '{entry_name}' is missing the following keys: {', '.join(missing_keys)}")

        if not isinstance(entry_data["timeseries"], pd.Series):
            raise ValueError(f"Timeseries for entry '{entry_name}' should be a pd.Series.")

        if not all(isinstance(timestamp, (int, float)) for timestamp in entry_data["timeseries"]):
            raise ValueError(f"Timeseries for entry '{entry_name}' should contain only numeric timestamps.")

        if not isinstance(entry_data["weighted_factor"], (float, int)):
            raise ValueError(f"Weighted factor for entry '{entry_name}' should be a float.")

    if segmentation:
        if number_of_segments_per_period > number_of_time_steps_per_periods:
            ValueError(f"Number of segments per period equal to'{number_of_segments_per_period}'  has to be smaller than number of time steps per periods equal to {number_of_time_steps_per_periods}")

    hours_per_period = number_of_time_steps_per_periods * minutes_per_time_step / 60
    time_series_data = pd.DataFrame()
    weighted_factors_dict = {}
    for key, value in data_dict_to_aggregate.items():
        if 'timeseries' in value:
            time_series_data[key] = value['timeseries']
        if 'weighted_factor' in value:
            weighted_factors_dict[key] = value['weighted_factor']
    if segmentation:
        clusterClass = TimeSeriesAggregation(
            timeSeries=time_series_data,
            noTypicalPeriods=number_of_typical_periods,
            segmentation=segmentation,
            noSegments=number_of_segments_per_period,
            hoursPerPeriod=hours_per_period,
            clusterMethod=cluster_method,
            sortValues=sort_values,
            weightDict=weighted_factors_dict
        )
        data = pd.DataFrame.from_dict(clusterClass.clusterPeriodDict)
    else:
        clusterClass = TimeSeriesAggregation(
            timeSeries=time_series_data,
            noTypicalPeriods=number_of_typical_periods,
            hoursPerPeriod=hours_per_period,
            clusterMethod=cluster_method,
            sortValues=sort_values,
            weightDict=weighted_factors_dict,
        )
        data = pd.DataFrame.from_dict(clusterClass.clusterPeriodDict)

    hours_of_time_series = entry_format_timeseries.__len__()
    periods_name = clusterClass.clusterPeriodIdx
    periods_order = clusterClass.clusterOrder
    periods_total_occurrence = [
        (periods_order == typical_period_name).sum() for typical_period_name in periods_name
    ]
    start_date = entry_format_timeseries[0]
    if not sum(periods_total_occurrence) * hours_per_period == 8760:

        print("aggregated timeseries has: " +str(int(sum(periods_total_occurrence) * hours_per_period))+ " timesteps")
        print("unaggregated timeseries has: " +str(hours_of_time_series)+ " timesteps")
        print("therefore the occurrence of the typical periods for the objective weighting will be customized")
        customize_factor = hours_of_time_series / int(sum(periods_total_occurrence) * hours_per_period)
        result_list = [float(occurrence) * customize_factor for occurrence in periods_total_occurrence]
        periods_total_occurrence = result_list


    current_timestamp = pd.to_datetime(start_date)
    previous_period = 0
    objective_weighting = []
    extended_time_series = []
    minute_resolution_of_one_hour = 60
    if segmentation:
        for period, timestep, segmented_timestep in data.index:
            if previous_period == period:
                extended_time_series.append(current_timestamp)
            else:
                extended_time_series.append(current_timestamp)
                previous_period = period
            objective_weighting.append(periods_total_occurrence[period] * segmented_timestep)
            current_timestamp += pd.Timedelta(minutes=minute_resolution_of_one_hour * segmented_timestep)
    else:
        for period, timestep in data.index:
            if previous_period == period:
                extended_time_series.append(current_timestamp)
            else:
                extended_time_series.append(current_timestamp)
                previous_period = period
            objective_weighting.append(periods_total_occurrence[period])
            current_timestamp += pd.Timedelta(minutes=minute_resolution_of_one_hour)

    data.index = extended_time_series
    data_dict_aggregated = {}
    for name in data:
        if len(data[name]) == len(objective_weighting):
            data_dict_aggregated[name] = { "timeseries" : data[name]}
        else:
            raise ValueError(f"Aggregated timeseries for: '{data[name]}' has a different length as "
                             f"objective weighting list")
    return data_dict_aggregated, objective_weighting, clusterClass
