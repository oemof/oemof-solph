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

.. figure:: /./_files/home_pv_input-data_light.svg
    :align: center
    :alt: Input data
    :figclass: only-light

.. figure:: /./_files/home_pv_input-data_dark.svg
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

    The total annual costs are 629.90 €.
    
    The annual costs for grid electricity are 629.90 €.

To have a look at the flows from and to the "electricity" bus.
The function ``solph.views.node(...)`` can help.
It compiles the respective ``DataFrame`` so that it can be directly used.

.. figure:: /./_files/home_pv_result-1_light.svg
    :align: center
    :alt: Input data
    :figclass: only-light

.. figure:: /./_files/home_pv_result-2_dark.svg
    :align: center
    :alt: Input data
    :figclass: only-dark

As grid supply is the only option, both lines of course overlap perfectly.

You can get the complete (uncommented) code for this step:
:download:`home_pv_1.py </../tutorials/introductory/home_pv/home_pv_1.py>`

.. dropdown:: Click to display the code

    .. literalinclude:: /../tutorials/introductory/home_pv/home_pv_1.py
        :language: python


Step 2: Adding fixed size PV
----------------------------

The grid connection needs to accept an incoming ``Flow``.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
    :language: python
    :start-after: [pv_system]
    :end-before: [graph_plotting]

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_2.py
    :language: python
    :start-after: [results]

As the PV system is free for the model itself,
we manually add an annuity to have the PV system included in the total costs.

    The annual costs for grid electricity are 365.32 €.

    The annual revenue from feed-in is 435.48 €.
    
    The annuity for the PV system is 375.00 €.
    
    The total annual costs are 479.03 €.


Step 3: PV investment optimisation
----------------------------------

In our example, the incoming ``Flow``
can of course directly be added when defining the grid is defined.

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [grid_conection]
    :end-before: [graph_plotting]

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [results]

    The optimal PV size is 4.13 kW.

    The annual costs for grid electricity are 376.59 €.
    
    The annual revenue from feed-in is 347.64 €.
    
    The annuity for the PV system is 309.40 €.
    
    The total annual costs are 477.41 €.


Step 4: PV investment optimisation with existing battery
--------------------------------------------------------

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_4.py
    :language: python
    :start-after: [battery]
    :end-before: [graph_plotting]

.. literalinclude:: /../tutorials/introductory/home_pv/home_pv_3.py
    :language: python
    :start-after: [results]

    The optimal PV size is 4.81 kW.

    The annual costs for grid electricity are 193.48 €.
    
    The annual revenue from feed-in is 347.99 €.
    
    The annuity for the PV system is 360.79 €.
    
    The annuity for the battery is 200.00 €.
    
    The total annual costs are 545.48 €.


Step 5: Full investment optimisation
------------------------------------

Inverter exra.


Step 6: Autarky of the system
-----------------------------

