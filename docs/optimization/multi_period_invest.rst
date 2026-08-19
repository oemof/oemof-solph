.. _optimization_multi_period_label:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pathway planning (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you might be interested in how energy systems could evolve in the longer-term, e.g. until 2045 or 2050 to meet some
carbon neutrality and climate protection or RES and energy efficiency targets.

While in principle, you could try to model this in oemof.solph using default investments as described above (see :ref:`optimization_invest_label`),
you would make the implicit assumption that your entire system is built at the start of your optimization and doesn't change over time.
To address this shortcoming, the pathway planning feature has been introduced. Be aware that it is still experimental.
So feel free to report any bugs or unexpected behaviour if you come across them.

For pathway planning, you define the usual time axis but also a number of points in time when installed capacities can change.
In rare cases, it might also be convenient to define a dispatch-only system using this feature. However, the power of the pathway-planning feature
fully unfolds if you look at long-term investments. Let's see how.

First, you start by defining your energy system as you might have done before, but you

* choose a longer-term time horizon (typically spanning multiple years) and
* explicitly define the `investment_times` attribute of your energy system which lists the time stamps at which capacitis may change.

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph

    my_index = pd.date_range('1/1/2013', periods=2*8760 + 1, freq='h')
    my_energysystem = solph.EnergySystem(
        timeindex=my_index,
        investment_times=[my_index[0], my_index[8760], my_index[-1]],
    )

The capacity periods work very similar to the normal timeindex:
You need to define the time step that closes the last interval,
and it is possible to define capacity periods with different lengths.


Then you add all the *components* and *buses* to your energy system, just as you are used to with, but with few additions.

.. code-block:: python

    hydrogen_bus = solph.buses.Bus(label="hydrogen")
    coal_bus = solph.buses.Bus(label="coal")
    electricity_bus = solph.buses.Bus(label="electricity")

    hydrogen_source = solph.components.Source(
        label="green_hydrogen",
        outputs={
            hydrogen_bus: solph.flows.Flow(
                variable_costs=[25] * 8760 + [30] * 8760
            )
        },
    )

    coal_source = solph.components.Source(
        label="hardcoal",
        outputs={
            coal_bus: solph.flows.Flow(variable_costs=[20] * 8760 + [24] * 8760)
        },
    )

So defining buses is the same as for standard models. Also defining components with constant capacities is the same.
Now, if you have componants that have a changing capacity, you can define that
using the capacitiy periods instead of changing values for fix.
Also, components that can be invested into (see :ref:`optimization_invest_label`),
behave slightly different as the optimal capacitiy can be chosen per period:


Here is an example

.. code-block:: python

    electrical_sink = solph.components.Sink(
        label="electricity_demand",
        inputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=[1000, 1100], fix=0.8
            )
        },
    )

    hydrogen_power_plant = solph.components.Converter(
        label="hydrogen_pp",
        inputs={hydrogen_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    maximum=1000,
                    ep_costs=30e3,
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

Below is what it would look like if you altered `ep_costs` per period. This can be done by simply
providing a list. Note that the length of the list must equal the number of periods of your model.
This would mean that for investments in the particular period, these values would be the one that are applied over their lifetime.

.. code-block:: python

    hydrogen_power_plant = solph.components.Converter(
        label="hydrogen_pp",
        inputs={hydrogen_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    maximum=1000,
                    ep_costs=[30e3, 29e3],
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

For components that is not invested into, you also can specify some additional attributes for their inflows and outflows:


To solve our model and retrieve results, you basically perform the same operations as for standard models.
So it works like this:

.. code-block:: python

    my_energysystem.add(
        hydrogen_bus,
        coal_bus,
        electricity_bus,
        hydrogen_source,
        coal_source,
        electrical_sink,
        hydrogen_power_plant,
        coal_power_plant,
    )

    om = solph.Model(my_energysystem)
    results = om.solve(solver="cbc", solve_kwargs={"tee": True})

    # Show investment for hydrogen power plants
    print(results["nominal_capacity"])
