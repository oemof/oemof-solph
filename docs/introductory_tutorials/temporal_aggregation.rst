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

Setting up energy systems has already been discussed in the other tutorials.
Thus, we only stay on the surface here.
The model describes a (potentially all-electric) single-family home.
There are demands that cannot be optimised, in contrast to the EV
tutorial, here we also consider the wall box a fixed demand.

.. figure:: /./_files/tutorial_temporal-aggregation/example_energy_system.png
    :alt: Time series of solar PV data aggregated with different time resolutions.

The energy system allows investments into battery (``GenericStorage``),
pv (``Flow`` out of a ``Source``), as well as a heat pump and a gas boiler
(boths ``Flow``s out of ``Converter`` s).
For reference, you can have a look at the full code until here:

:download:`timeindex_1_segmentation.py </../tutorials/advanced/time_index/timeindex_1_segmentation.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/advanced/time_index/timeindex_1_segmentation.py
        :language: python



Step 3: Optimization using time series aggregation
--------------------------------------------------
In this section, we introduce *time series aggregation* with
`tsam - time series aggregation module
<https://tsam.readthedocs.io/en/latest/>`_.

At the time of writing, the TSAM integration in ``oemof.solph`` is implemented via
the *multi-period* (pathway planning) interface. For Step 3, we use **exactly one**
investment period. This means that investment decisions are still made *once* for
the whole horizon (as in the standard upfront-investment approach from Step 2),
but the **operational time series** are replaced by an aggregated representation.

Please note that this feature is still **experimental** and may therefore contain bugs.

We use the same input data and energy system setup as in Step 1 and Step 2.

Concept: clustering to typical periods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The basic idea of time series aggregation for energy system design is to replace a
long time series (e.g. one year of hourly data) by a **small set of representative
periods** (often called *typical periods*). The optimisation problem is then solved
only for these typical periods, while the objective function accounts for how often
each typical period occurs in the original time set.

Example:
A full year (365 days) can be clustered into 10 typical periods of length 24 hours.
In other words, the year is represented by 10 typical days ``(A, B, C, ...)`` plus an
*order* that maps each original day to one of these typical days in th year:

``(A, A, B, A, A, C, A ..., C)``

Variable flows in the objective function are weighted according to the frequency of
their corresponding typical periods in the original time set.

If a **storage** is included, the typical periods must be linked to represent storage
carry-over between periods. For this, we use an approach introduced by
Kotzur et al. by splitting the storage state into two parts:

* **intra storage level**: the change of storage level *within* a typical period
* **inter storage level**: the storage level in between two periodd in the
  original sequence of periods

The total storage level is represented as a superposition of both. For details, see
`Time series aggregation for energy system design: Modeling seasonal storage
<https://www.sciencedirect.com/science/article/pii/S0306261918300242>`_.

Effect on the optimisation model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To explain on a high level the influence on our optimization model,
we use the 10 typical days example ``(A, B, C, ...)``:

*Without storage*, the operational part of the model is reduced because only the
flows for the typical days are optimised (10 × 24 hours), instead of all 365 days.

*With storage*, the model still optimises the flows for the typical periods. In addition,
the intra storage level is optimised for each representative period (10 × 24 hours).
In our example with 24-hour periods, the original time set is split into 365 periods.
Therefore the inter-period storage level occurs 365 times (one value per original day).
Overall, this typically leads to a significant reduction in runtime.,

If you add constraints with **binary variables**, an important modelling question is
which time grid these binaries should use when using TSAM. For a first insight,
see `Operational Optimization of Seasonal Ice-Storage Systems with Time-Series Aggregation
<https://doi.org/10.3390/en18225988>`_.


Clustering the input time series with TSAM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To cluster input time series with TSAM, you need to define:

* ``noTypicalPeriods``: the number of typical periods (e.g. 10 typical days)
* ``hoursPerPeriod``: the length of each period in hours (e.g. 24 for typical days)
* ``clusterMethod``: the clustering algorithm

These parameter names follow TSAM’s terminology. In this tutorial we use hourly data.
Non-hourly resolutions might be possible to solve, but isn't tested in detail.

The influence of different aggregation methods is discussed in
`Impact of different time series aggregation methods on optimal energy system design
<https://www.sciencedirect.com/science/article/pii/S0960148117309783>`_.

The clustering step can then be implemented as follows:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_2_typical_periods.py
    :language: python
    :start-after: [tsam_aggregation_start]
    :end-before: [tsam_aggregation_end]

Building the energy system with an aggregated time index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compared to the standard approach, setting up the ``EnergySystem`` differs slightly.
In addition to the aggregated ``timeindex``, you need to provide:

* ``timesteps_per_period``: number of time steps per typical period
* ``order``: mapping from original periods to typical periods

This is shown in the following snippet:

.. literalinclude:: /../tutorials/advanced/time_index/timeindex_2_typical_periods.py
    :language: python
    :start-after: [ti_index_and_energy_system_start]
    :end-before: [ti_index_and_energy_system_end]

Post-processing and sensitivity to aggregation choices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In post-processing, the optimised flows and storage levels are **disaggregated**
back to the original time grid. This means you can process and plot results in the
same way as in the non-aggregated examples.

However, the choice of aggregation parameters (number and length of typical periods)
can have a strong influence on the results. To illustrate this, we run the optimisation
for different numbers of typical periods, using typical period lengths of **24 hours**
and **168 hours**:

.. figure:: /./_files/tutorial_temporal-aggregation/investment_bar_tsam_typical_periods_length_24.png
    :align: right
    :alt: Investments for different numbers of typical periods (24-hour periods).

.. figure:: /./_files/tutorial_temporal-aggregation/investment_bar_tsam_typical_periods_length_168.png
    :align: right
    :alt: Investments for different numbers of typical periods (168-hour periods).

The complete code for this step can be found at:

:download:`timeindex_2_typical_periods.py </../tutorials/advanced/time_index/timeindex_2_typical_periods.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/advanced/time_index/timeindex_2_typical_periods.py
        :language: python


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

The complete code for this step can be found at:

:download:`timeindex_3_pathway_planning.py </../tutorials/advanced/time_index/timeindex_3_pathway_planning.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/advanced/time_index/timeindex_3_pathway_planning.py
        :language: python
