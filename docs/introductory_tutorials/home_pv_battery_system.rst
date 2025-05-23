.. _home_pv_battery_system_label:

Home PV installation with battery storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get in touch with basic functionalities in oemof.solph, we will use this
tutorial to model the electricity supply of a single family household that
intents to install a PV plant in combination with a battery storage.
Therefore several spteps are considered:

* Step 1: Definition of the scenario
* Step 2: Adding fixed size PV
* Step 3: PV investment optimisation
* Step 4: PV investment optimisation with existing battery
* Step 5: Full investment optimisation
* Step 6: Autarky of the system


Step 1: Definition of the scenario
----------------------------------

Imagine you want to set up a PV plant on top of a single family house.
How would you find out which system fits best and why?
Here are some possible points to think about:

* Which area (e.g. on the roof) can be covered and how large is it?
* How much energy will you consume or be able to feed into the grid?
* How much will you have to pay for the system?

Especially for single-family homes without energy storage, the load can be
very volatile: Switching on and off e.g. the oven can change the demand from
several 10 Watts to several kW. This is particularly important when alignment
of supply and demand. For this tutorial, we use hourly aggregated data from
real-world measurements
(:download:`pv_example_data.csv </../tutorials/introductory/home_pv/pv_example_data.csv>`).
This can be seen as a compromise: A finer
resolution increases computatonal time but we want fast results in tutorial.
The full dataset (which has 10-minute resolution) is described in the paper
`Dataset on electrical single-family house and heat pump load profiles in
Germany <https://doi.org/10.1038/s41597-022-01156-1>`_.
The PV time series has been created using
`PVGIS <https://re.jrc.ec.europa.eu/pvg_tools/en/>`_.

First, let us import all needed packages:
``os`` is handy to for file handling,
``matplotlib`` is for plotting,
``networkx`` as well as ``oemof.network.graph``
can be used to visualise the energy system graph, and
``pandas`` is for (input and output) data handling.


.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [imports]
    :end-before: [input_data]

Now, let us load the input data and have an initial look at it.
If the data provides time information, it is a good idea to directly
consider it. This also allows to work with time stamps when handling the data.
For illustation, we plot the first week of March 2020.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [input_data]
    :end-before: [energy_system]

The style has been chosen to reflect that the data is defined on the
time intervals maked by the beginning time step. This means that 1.5 kW
is probably not the peak load within the displayed week but only the
peek hourly average.
In contrast to the demand, the PV gain is given in normalised units and
has to be multiplied by the installed PV capacity to yield the electricity
production.

.. figure:: /./_files/tutorial_home-pv/home_pv_input-data_light.svg
    :align: center
    :alt: Input data
    :figclass: only-light

.. figure:: /./_files/tutorial_home-pv/home_pv_input-data_dark.svg
    :align: center
    :alt: Input data
    :figclass: only-dark


The model differentiates between time points and time steps.
As solph supports mixing differnt length of time steps in one model,
we need N+1 time points to define N time steps.
If the index does not contain the last time point,
the last interval can be infered based on ``index.freq``.

.. note::

    You need N+1 point in time to define N time steps.

The ``EnergySystem`` acts as a container.
You will need to add everything that is part of the energy system.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [energy_system]
    :end-before: [dispatch_model]

Now, to the actual energy system.
It is modelled in the form of a mathematical graph.
Energy flows along the edges (``Flow``) from node to node.
First of all, where is an electricity ``Bus``, which is used as a central
point for the rest of the network to connect.
Secondly, there is a ``Sink`` to model the enery demand.
It takes an input from ``el_bus``.
Note that we set ``nominal_capacity=1`` as the time series
is already in kW.
While this can be considered as a hack,
it is common practice to do so:
In the model, it is no issue to run in overload.
As the last component, we add another ``Bus`` wich represents
the electricity grid.
Often, a ``Source`` would be used instead.
However, to emphasise that the same grid is used for purchasing electricity
and for feeding in, we use an nbalanced bus, also referred to as a "slack bus".

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [dispatch_model]
    :end-before: [graph_plotting]

To obtain results, we have to create an optimisation model from the
``EnergySystem`` and solve it.
To see diagnostic output, ``solve_kwargs={"tee": True}`` can be set,
by default (False) it will be silent.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [model_optimisation]
    :end-before: [results]

If the model cannot find an optimal solution,
``model.solve()`` will fail. You can try this, e.g. by setting
``nominal_capacity=0.5`` to the ``Flow`` between grid and el_bus
(the one that has the variable costs defined).
When the optimisation is finished,
we can proceed with evaluating the results.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
    :language: python
    :start-after: [results]

At first, we look at the total costs.
As we used these for our objective value, it is directly accassible in the
``meta_results``.
Because we want to evaluate differnt contibutions later,
we also manually calculate the costs manually.
To no surprise the numbers are the same:

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value"
    :widths: auto

    "Annual costs for grid electricity",   "€", 629.90
    "Total annual costs",                  "€", 629.90

To have a look at the flows from and to the "electricity" bus.
The function ``solph.views.node(...)`` can help.
It compiles the respective ``DataFrame`` so that it can be directly used.

.. figure:: /./_files/tutorial_home-pv/home_pv_result-1_light.svg
    :align: center
    :alt: Result time-series
    :figclass: only-light

.. figure:: /./_files/tutorial_home-pv/home_pv_result-1_dark.svg
    :align: center
    :alt: Result time-series
    :figclass: only-dark

As grid supply is the only option, both lines of course overlap perfectly.

.. admonition:: Learning
    :class: important

    The model balances supply and demand along flows in a graph based model.

You can get the complete (uncommented) code for this step:
:download:`home_pv_1.py </../tutorials/introductory/home_pv/home_pv_1.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
        :language: python


Step 2: Adding fixed size PV
----------------------------

So far so good. But what would happen if we had an existing PV plant?
Let us simply add one to the system by creating a suitable source.
We might have five kW installed and therefore enter a nominal capacity of five.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
    :language: python
    :start-after: [pv_system]
    :end-before: [graph_plotting]

Note that we set the PV yield time series using the max parameter:
It is always possible to not take the energy.
In our case, however, we want to allow feeding into the grid.
Thus, the corresponding ``Bus`` needs to accept an incoming ``Flow``.
It is possible, to add ``Flow`` s to existing nodes:

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
    :language: python
    :start-after: [grid_feedin]
    :end-before: [add_grid]

However, the ``Flow`` is typically directly added when defining the grid.
So, alternatively, you can just change the previos definition to look like:

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [grid_conection]
    :end-before: [add_grid]

Note that feeding into the grid will make sense if there is compensation
(or if the PV output is set to have a ``fix``
production instead of a maximum one).
For our example, we take 6 ct/kWh as compensation for feed-in.

As building the PV system is free for the model (it is already present),
we manually add an annuity to have the PV system included in the total costs.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
    :language: python
    :start-after: [results]
    :end-before: [result_plotting]

.. figure:: /./_files/tutorial_home-pv/home_pv_result-2_light.svg
    :align: center
    :alt: Result time-series
    :figclass: only-light

.. figure:: /./_files/tutorial_home-pv/home_pv_result-2_dark.svg
    :align: center
    :alt: Result time-series
    :figclass: only-dark

In this scenario, the objective value is negative,
so a revenue is accieved.
This is ostly because of feeding in,
deand and supply do hardly match in this scenario.
However, correcting this by adding the annuity of the PV system
leaves us with (positive) costs.

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value (no PW)", "Value (5 kW PV)"
    :widths: auto

    "Annual costs for grid electricity",   "€", 629.90, 365.32
    "Annual revenue from feed-in",         "€", ,       451.61
    "Annuity for the PV system",           "€", ,       375.00
    "Total annual costs",                  "€", 629.90, 479.03
    "Autarky",                             "%", 0.00,   42.00

.. admonition:: Learning
    :class: important

    You can give negative costs to model a revenue.

You can get the complete (uncommented) code for this step:
:download:`home_pv_2.py </../tutorials/introductory/home_pv/home_pv_2.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
        :language: python


Step 3: PV investment optimisation
----------------------------------

Now, compared to dispatch with a fixed PV plant,
almost everything else stays the same, except for one thing:
the nominal capacity of the PV plant.
That’s because we want to find out which peak power
the system should have to minimise our costs.
Therefore an investment object with a periodical cost
of 75 Euros per kW is assigned.
These costs represent an assumed investment cost of 1500 Euros per kW
divided by an estimated life time of 20 years as a straight-line deprecation.
To make sure the model converges, we set a maximum capacity:
If building the PV system was profitable,
the optimiser would try to build an infinite size PV system,
which would effectively prevent the model from converging.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [pv_system]
    :end-before: [graph_plotting]

However, in this case we did not need to set the limit.
The assumed annuity is so high that the costs of the produced electricity
are above 6 ct/kWh.
The resulting optimal PV size

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [result_pv]
    :end-before: [results]

is 4.13 kW, which is even smaller than what we tried before.

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value"
    :widths: auto

    "Optimal PV size",                     "kW",    4.13
    "Annual costs for grid electricity",   "€",     376.59
    "Annual revenue from feed-in",         "€",     347.64
    "Annuity for the PV system",           "€",     309.40
    "Total annual costs",                  "€",     477.41
    "Autarky",                             "%",     40.21


You can get the complete (uncommented) code for this step:
:download:`home_pv_3.py </../tutorials/introductory/home_pv/home_pv_3.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
        :language: python


.. admonition:: Learning
    :class: important

    You can use an ``Investment`` object for the ``nominal_capacity``
    to make the capacity an optimisation variable.


Step 4: PV investment optimisation with existing battery
--------------------------------------------------------

In the previous step we learned that in our assumed scenario,
compensation for feeding into the grid will not pay the PV system.
So, what if we had a big battery?
Let us just add one:

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_4.py
    :language: python
    :start-after: [battery]
    :end-before: [graph_plotting]

As before with the PV system, we manually add the deprecation of the battery
to the objective value to get the total costs of the system.

.. figure:: /./_files/tutorial_home-pv/home_pv_result-4_light.svg
    :align: center
    :alt: Result time-series
    :figclass: only-light

.. figure:: /./_files/tutorial_home-pv/home_pv_result-4_dark.svg
    :align: center
    :alt: Result time-series
    :figclass: only-dark

As can be seen in the time series, the Battery allows to use much of the
produced PV electricity.
Thus, total PV size is not increased too much.
With a battery that large, the it now dominates the total costs.

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value"
    :widths: auto

    "Optimal PV size",                     "kW",    5.67
    "Annual costs for grid electricity",   "€",     72.56
    "Annual revenue from feed-in",         "€",     383.39
    "Annuity for the PV system",           "€",     425.12
    "Annuity for the battery",             "€",     1000.00
    "Total annual costs",                  "€",     1267.65
    "Autarky",                             "%",     88.48

.. admonition:: Learning
    :class: important

    Energy storage is modelled using the ``GenericStorage`` class.


You can get the complete (uncommented) code for this step:
:download:`home_pv_4.py </../tutorials/introductory/home_pv/home_pv_4.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_4.py
        :language: python


Step 5: Full investment optimisation
------------------------------------

For a full investment optimisation, of course, we include optimising the
battery size. First, however, we will separate the PV system into
PV panels and inverter.
For clearity, we rename the former ``el_bus`` to ``ac_bus``
and create a separate ``dc_bus``.
As the numbers given in the input data already consider inverter losses,
we compensate for that by allowing higer DC gains from the panels,
the inverter then has a ``conversion_factor`` so that the ``Flow`` to the
AC bus is reduced by 5 %.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_5.py
    :language: python
    :start-after: [pv_system]
    :end-before: [battery]

Now, the optimiser can choose on the inverter
and number of PV panels separately.
Note that the costs for inverter and pv panels add up to the value we used
in the previous step.
For the sake of simplicity in this tutorial, the battery will remain
coupled to the AC system. We only let the optimisation decide on the size.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_5.py
    :language: python
    :start-after: [battery]
    :end-before: [graph_plotting]

We find that it is advisible to have an inverter that can only output
two thirds of the nominal power of the PV panels.
While the inverter is even smaller than in the previous steps,
the total power of the panels is increased.

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value"
    :widths: auto

    "Optimal PV size",                     "kW",    6.04
    "Optimal inverter size",               "kW",    4.10
    "Optimal battery size",                "kWh",   2.39
    "Annual costs for grid electricity",   "€",     156.35
    "Annual revenue from feed-in",         "€",     451.61
    "Annuity for the PV system",           "€",     362.27
    "Annuity for the battery",             "€",     89.53
    "Total annual costs",                  "€",     398.66
    "Autarky",                             "%",     75.18

.. admonition:: Learning
    :class: important

    ``Converter`` s are used to model (possibly lossy) conversion.

You can get the complete (uncommented) code for this step:
:download:`home_pv_5.py </../tutorials/introductory/home_pv/home_pv_5.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_5.py
        :language: python


Step 6: Autarky of the system
-----------------------------

The final step of the tutorial shows a way how to limit the energy supply
from the grid in order to guarantee a minimum autarky grade of our system
consisting of a combined PV and battery storage investment.

Since our total energy demand is almost 2100 kWh, we
could accomplish an autarky grade of 90 percent if we
limited the sum of thegrid energy supply to 210 kWh.
Choosing 42 kW as a reasonable dimensioned power,
multiplying it by five full load hours does the trick.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_6.py
    :language: python
    :start-after: [grid]
    :end-before: [pv_system]

So, finally let us compare the results from all different steps.

.. csv-table:: Result overview
    :header: "Quantity", "Unit", "Value (no PV)", "Value (5 kW PV)", "Value (opt. PV)", "Value (big bat.)", "Value (all opt.)", "Value (Autarky)"
    :widths: auto

    "Optimal PV size", "kW ", , , 4.13, 5.67, 6.04, 10
    "Optimal inverter size", "kW ", , , , , 4.1, 6.79
    "Optimal battery size", "kWh", , , , , 2.39, 5.01
    "Annual costs for grid electricity", "€ ", 629.9, 365.32, 376.59, 72.56, 156.35, 63
    "Annual revenue from feed-in", "€ ", , 451.61, 347.64, 383.39, 451.61, 821.78
    "Annuity for the PV system", "€ ", , 375, 309.4, 425.12, 362.27, 600
    "Annuity for the battery", "€ ", , , , 1000.00, 89.53, 188.02
    "Total annual costs", "€ ", 629.9, 479.03, 477.41, 1267.65, 398.66, 459.76
    "Autarky", "% ", 0, 42, 40.21, 88.48, 75.18, 90

.. admonition:: Learning
    :class: important

    You can define the full load time of a ``Flow``
    to limit its energy transfer.
    Here, this has been used to accieve a minimum autarky.

You can get the complete (uncommented) code for this step:
:download:`home_pv_6.py </../tutorials/introductory/home_pv/home_pv_6.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_6.py
        :language: python
