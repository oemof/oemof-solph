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
`doi: 10.5281/zenodo.5642902 <https://doi.org/10.5281/zenodo.5642902>`_.
The data is licensed from M. Schlemminger, T. Ohrdes, E. Schneider,
and M. Knoop under Creative Commons Attribution 4.0 International
License.

.. figure:: /./_files/tutorial_temporal-aggregation/time_steps.png
    :align: center
    :alt: Illustrative sketch of the time index definitions.

But first, let us go through some basics about the time index.
As mentioned in :ref:`basic_concepts_energy_system_label`,
we use N+1 points in time to define N time intervals.
At the first glance, this might seem to add extra complication,
but being explicit and clear helps formulating models
that are precise, comprehensible, and physically correct.
The function `solph.create_time_index()` takes the number of
time intervals as a input, so you can take a shortcut here:

.. code-block:: python

    >>> from oemof import solph
    >>> es = solph.EnergySystem(
    ...    timeindex=solph.create_time_index(2025, interval=0.5, number=2)
    ... )
    >>> print(list(es.timeindex))
    [Timestamp('2025-01-01 00:00:00'), Timestamp('2025-01-01 00:30:00'), Timestamp('2025-01-01 01:00:00')]

    >>> print(list(es.timeincrement))
    [0.5, 0.5]

It should be mentioned that the exact time stamp helps with data
processing but is not relevant for the optimisation.
Thus, you can also give a number of ascending values.
The time increment then is the difference between those.
Except for the time index, the following energy system will produce exactly
the same results.

.. code-block:: python

    >>> from oemof import solph
    >>> es = solph.EnergySystem(timeindex=[2, 2.5, 3])
    >>> print(es.timeindex)
    [2, 2.5, 3]
    >>> print(list(es.timeincrement))
    [0.5, 0.5]

Now, that we know how time steps are defined, let us look at a good choice
for the time intervals. Often, time steps are chosen to have the same length.
This is advantegous as they make the model easy to comprehend,
as you can convert between counting indexes and time by multiplying a constant.
This particularly simplifies formulations of constraints to the extend
that some uncommon use cases of solph are currently bound to fixed intervals.
Let us go through this based on our input data.

.. literalinclude:: /../tutorials/advanced/time_index/input_data.py
    :language: python
    :start-after: [main]

The script reads in the data, defines desired resolutions,
and then creates two figures, one for a time series plot,
one for a duration curve. In the loop, it resamples the data
to the set resolution and produces the step graphs for the two types of plots.
An example output is included in the following:

.. figure:: /./_files/tutorial_temporal-aggregation/2019-11-3_PV-timeseries.svg
    :align: left
    :alt: Time series of solar PV data aggregated with different time resolutions.
.. figure:: /./_files/tutorial_temporal-aggregation/2019-11-3_PV-duration.svg
    :align: right
    :alt: Duration of solar PV data aggregated with different time resolutions.

Of course, one day is not representative, but it is clearly visible that even
the resolution of 15-minutes cannot preserve the dynamics of the data.
Further, it should be noted that averaging the power values
reduces the peaks, while the total energy is preserved. Thus,
the lower resolutions systematically overestimate low loads.
Also note that we cut of the night from the graph,
because in the corresponding hours the PV data of course shows a flat zero.
So, what if we also just drop the nights from our data?
This is done by the following function, which just hardcodes the day to be
between 5 am and 9 pm. There are two nocturnal time steps of four hours each,
which extend from 9pm to 1 am and from 1 am to 5 am.
This is a conservative assumption, that should work all year long,
but already reduces the number of time steps by 25 %.

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_1_segmentation.py
    :language: python
    :start-after: [reshape_unevenly]
    :end-before: [prepare_technical_data]

Now, how will an optimisation problem react to this reduction?
Let us have a look!

Step 2: Setting up the Energy System Model
------------------------------------------

Step 4: Pathway planning using time series aggregation
------------------------------------------------------

In this section, we introduce *pathway planning*. Please note that this
feature is still experimental and may therefore contain bugs  
(known issues discovered while preparing this tutorial will be discussed).

Pathway planning differs from the previous examples in an important way:
**investment variables become time-dependent**.  
In the previous cases, all investment decisions were made *once* for the entire
optimization horizon. In pathway planning, investments may change at predefined
points in time. These points represent the years or periods in which new
investments can be made (or existing ones can be expanded).

Typically, investment decisions do *not* need to change as frequently as the
operational time steps of the model. For example, while the model may run on
hourly resolution, investment decisions might only be updated every five years.
Therefore, you need to define *two kinds of time indices*:

1. A "normal" time index for the operational resolution (discussed earlier)
2. A set of investment times/periods (times when new capacity can be installed)

.. figure:: /./_files/tutorial_temporal-aggregation/set_of_investment_times.png
    :align: right
    :alt: Sketch of time index and invesment times.

Although pathway planning is theoretically compatible with all previously
discussed ways of defining time indices, in the current version of
``oemof.solph`` you **must use time series aggregation together with pathway
planning**. (We aim to remove this restriction in future versions.)

Starting from your original one-year dataset (and assuming that demand and
generation patterns do not change significantly between years), you create an
aggregated time index in the same way as in Step 3.

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [tsam]
    :end-before: [time_series_multiperiod]

To implement pathway planning in ``solph``, three additional steps are required:

1. Build one **continuous operational time index** covering the entire optimization horizon.
2. Create a **list of time indices**, one for each investment period.
3. Create a **dictionary of TSAM parameters**, also one entry per investment period.

Suppose you want to allow investment changes every five years, e.g. in  
``[2025, 2030, 2035, 2040, 2045]``.  
To reduce runtime, each 5‑year period will be represented by *one aggregated year*.

Currently, ``oemof.solph`` does not support "skipping" years directly.
Therefore, you must as a work around define investment years as a continuous
sequence, e.g.:

``[2025, 2026, 2027, 2028, 2029]`` 

These then can be mapped to your intenden resolution of five years. This will 
require some preprocessing in cost data etc., which will be explained further 
down.

You can then perform the three steps described above:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [time_series_multiperiod]
    :end-before: [time_series_data]

Next, you can build your energy system:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [energy_system]
    :end-before: [solve]

Now the hardest part is done! 

From here, you can construct your system exactly as in previous examples.
However, keep in mind:

* All *operational* time series must span the **entire optimization horizon**
* Their index/length must match the **combined** time index you created earlier

Since we assume that demand and production profiles remain constant across
years, we can simply repeat the original one-year dataset over the
length of the horizon:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [time_series_data]
    :end-before: [investments]

Although the model internally treats each period as one year, investment
decisions actually represent five-year steps (as discussedabove). To maintain 
the correct ratio of investment costs to variable costs,
we scale the **lifetime** and **investment costs** by the length of the 
investment period.

Example:  
A battery has a real lifetime of 10 years.  
Since one model "year" represents 5 real years:

* Effective lifetime in the model: ``10 / 5 = 2``
* Investment costs and offsets must also be divided by 5

This ensures that discounting and cost comparisons remain realistic.

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [investments]
    :end-before: [energy_system]

Finally, adjust the **discount rate** to reflect that each model period
represents five real years. This ensures that net‑present‑value calculations
are consistent with your investment period length:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
    :language: python
    :start-after: [discount]
    :end-before: [expand]

Now you can solve the model and plot the results:

.. figure:: /./_files/tutorial_temporal-aggregation/multi_period_results.png
    :align: right
    :alt: results of pathway planning.
