.. _temporal_aggregation_tutorial_label:

Time indexes and temporal aggregation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tutorial starts with something very fundamental
that people often do not think about for a long time:
The choice of the time increment.
This part is independent from solph and very suitable for beginners.
The last steps are presenting experimental features of solph,
namely time series aggregation and pathway planning.
These can be considered advanced usage.
The full tutorial consists of the following:

* Step 1: Sampling of high resolution input data
* Step 2: Upfront investment using different time resolutions
* Step 3: Upfront investment using time series aggregation
* Step 4: Pathway planning using time series aggregation


Step 1: Sampling of high resolution input data
----------------------------------------------

Temporal and spatial resolution are often connected.
If you average over multiple locations, volatililty in the data is reduced,
reducing the effect of temporal aggregation.
We take a detatched single family home with just one inhabitant as our basis,
because a significant influence of the aggregation is expected here.
Further, we use real-world data as synthetic data might feature repetitive
features, putting a bias to the aggreagtion that is planned later.

We use building 27 plus the south-facing PV
from the one-minute resolution dataset described of the
`Dataset on electrical single-family house and heat pump load profiles in
Germany <https://doi.org/10.1038/s41597-022-01156-1>`_,
which is also available at
`doi: 10.5281/zenodo.5642902 <https://doi.org/10.5281/zenodo.5642902>`.
The data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,
and M. Knoop under Creative Commons Attribution 4.0 International
License.

.. figure:: /./_files/tutorial_temporal-aggregation/time_steps.png
    :align: center
    :alt: Illustrative sketch of the time index definitions.

But first, let us go through some basics about the time index.
As mentioned in :link: basic_concepts_energy_system_label,
we use N+1 points in time to define N time intervals.
At the first glance, this might seem to add extra complication,
but being explicit and clear helps formulating models
that are precise, comprehensible, and physically correct.
The function `solph.create_time_index()` takes the number of
time intervals as a imput, so you can take a shortcut here:

.. code-block:: python

    >>> from oemof import solph
    >>> es = solph.EnergySystem(
    ...    timeindex=solph.create_time_index(2025, interval=0.5, number=2)
    ... )
    >>> print(list(es.timeindex))
    [Timestamp('2025-01-01 00:00:00'), Timestamp('2025-01-01 00:30:00'), Timestamp('2025-01-01 01:00:00')]

    >>> print(list(es.timeincrement))
    [0.5, 0.5]

It should be mentioned that the exact time stamp mostly helps with data
processing. If they do not matter, you can simply give a number of ascending
values. The time increment then is the difference between those.
Except for the time index, the following energy system will produce exactly
the same results.

.. code-block:: python

    >>> from oemof import solph
    >>> es = solph.EnergySystem(timeindex=[2, 2.5, 3])
    >>> print(es.timeindex)
    [2, 2.5, 3]
    >>> print(list(es.timeincrement))
    [0.5, 0.5]


.. figure:: /./_files/tutorial_temporal-aggregation/2019-11-3_PV-timeseries.png
    :align: center
    :alt: Solar PV data aggregated with different time resolutions.
