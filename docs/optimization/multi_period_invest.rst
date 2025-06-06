.. _optimization_multi_period_label:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Multi-period optimization (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you might be interested in how energy systems could evolve in the longer-term, e.g. until 2045 or 2050 to meet some
carbon neutrality and climate protection or RES and energy efficiency targets.

While in principle, you could try to model this in oemof.solph using the standard investment mode described above (see :ref:`optimization_invest_label`),
you would make the implicit assumption that your entire system is built at the start of your optimization and doesn't change over time.
To address this shortcoming, the multi-period (investment) feature has been introduced. Be aware that it is still experimental.
So feel free to report any bugs or unexpected behaviour if you come across them.

While in principle, you can define a dispatch-only multi-period system, this doesn't make much sense. The power of the multi-period feature
only unfolds if you look at long-term investments. Let's see how.

First, you start by defining your energy system as you might have done before, but you

* choose a longer-term time horizon (spanning multiple years, i.e. multiple periods) and
* explicitly define the `periods` attribute of your energy system which lists the time steps for each period.

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph

    my_index = pd.date_range('1/1/2013', periods=17520, freq='h')
    periods = [
        pd.date_range('1/1/2013', periods=8760, freq='h'),
        pd.date_range('1/1/2014', periods=8760, freq='h'),
    ]
    my_energysystem = solph.EnergySystem(timeindex=my_index, periods=periods)

If you want to use a multi-period model you have define periods of your energy system explicitly. This way,
you are forced to critically think, e.g. about handling leap years, and take some design decisions. It is possible to
define periods with different lengths, but remember that decommissioning of components is possible only at the
beginning of each period. This means that if the life of a component is just a little longer, it will remain for the
entire next period. This can have a particularly large impact the longer your periods are.

To assist you, here is a plain python snippet that includes leap years which you can just copy
and adjust to your needs:

.. code-block:: python

    def determine_periods(datetimeindex):
        """Explicitly define and return periods of the energy system

        Leap years have 8784 hourly time steps, regular years 8760.

        Parameters
        ----------
        datetimeindex : pd.date_range
            DatetimeIndex of the model comprising all time steps

        Returns
        -------
        periods : list
            periods for the optimization run
        """
        years = sorted(list(set(getattr(datetimeindex, "year"))))
        periods = []
        filter_series = datetimeindex.to_series()
        for number, year in enumerate(years):
            start = filter_series.loc[filter_series.index.year == year].min()
            end = filter_series.loc[filter_series.index.year == year].max()
            periods.append(pd.date_range(start, end, freq=datetimeindex.freq))

        return periods

So if you want to use this, the above would simplify to:

.. code-block:: python

    import pandas as pd
    import oemof.solph as solph

    # Define your method (or import it from somewhere else)
    def determine_periods(datetimeindex):
        ...

    my_index = pd.date_range('1/1/2013', periods=17520, freq='h')
    periods = determine_periods(my_index)  # Make use of method
    my_energysystem = solph.EnergySystem(timeindex=my_index, periods=periods)


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

    electrical_sink = solph.components.Sink(
        label="electricity_demand",
        inputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=1000, fix=[0.8] * len(my_index)
            )
        },
    )

So defining buses is the same as for standard models. Also defining components that do not have any investments associated with
them or any lifetime limitations is the same.

Now if you want to have components that can be invested into, you use the investment option, just as in :ref:`optimization_invest_label`,
but with a few minor additions and modifications in the investment object itself which you specify by additional attributes:

* You have to specify a `lifetime` attribute. This is the components assumed technical lifetime in years. If it is 20 years,
  the model invests into it and your simulation has a 30 years horizon, the plant will be decommissioned. Now the model is
  free to reinvest or choose another option to fill up the missing capacity.
* You can define an initial `age` if you have `existing` capacity. If you do not specify anything, the default value 0 will be used,
  meaning your `existing` capacity has just been newly invested.
* You also can define `fixed_costs`, i.e. costs that occur every period independent of the plants usage.

Here is an example

.. code-block:: python

    hydrogen_power_plant = solph.components.Converter(
        label="hydrogen_pp",
        inputs={hydrogen_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=solph.Investment(
                    maximum=1000,
                    ep_costs=1e6,
                    lifetime=30,
                    fixed_costs=100,
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

.. warning::

    The `ep_costs` attribute for investments is used in a different way in a multi-period model. Instead
    of periodical costs, it depicts (nominal or real) investment expenses, so actual Euros you have to pay per kW or MW
    (or whatever power or energy unit) installed. Also, you can depict a change in investment expenses over time,
    so instead of providing a scalar value, you could define a list with investment expenses with one value for each period modelled.

    Annuities are calculated within the model. You do not have to do that.
    Also the model takes care of discounting future expenses / cashflows.

Below is what it would look like if you altered `ep_costs` and `fixed_costs` per period. This can be done by simply
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
                    ep_costs=[1e6, 1.1e6],
                    lifetime=30,
                    fixed_costs=[100, 110],
                ),
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.6},
    )

For components that is not invested into, you also can specify some additional attributes for their inflows and outflows:

* You can specify a `lifetime` attribute. This can be used to depict existing plants going offline when reaching their lifetime.
* You can define an initial `age`. Also, this can be used for existing plants.
* You also can define `fixed_costs`, i.e. costs that occur every period independent of the plants usage. How they are handled
  depends on whether the flow has a limited or an unlimited lifetime.

.. code-block:: python

    coal_power_plant = solph.components.Converter(
        label="existing_coal_pp",
        inputs={coal_bus: solph.flows.Flow()},
        outputs={
            electricity_bus: solph.flows.Flow(
                nominal_capacity=600,
                max=1,
                min=0.4,
                lifetime=50,
                age=46,
                fixed_costs=100,
                variable_costs=3,
            )
        },
        conversion_factors={electricity_bus: 0.36},
    )

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
    om.solve(solver="cbc", solve_kwargs={"tee": True})

    # Obtain results
    results = solph.processing.results(om)
    hydrogen_results = solph.views.node(results, "hydrogen_pp")

    # Show investment plan for hydrogen power plants
    print(hydrogen_results["period_scalars"])

The keys in the results dict in a multi-period model are "sequences" and "period_scalars".
So for sequences, it is all the same, while for scalar values, we now have values for each period.

Besides the `invest` variable, new variables are introduced as well. These are:

* `total`: The total capacity installed, i.e. how much is actually there in a given period.
* `old`: (Overall) capacity to be decommissioned in a given period.
* `old_end`: Endogenous capacity to be decommissioned in a given period. This is capacity that has been invested into
  in the model itself.
* `old_exo`: Exogenous capacity to be decommissioned in a given period. This is capacity that was already existing and
  given by the `existing` attribute.

.. note::

    * For storage units, the `initial_content` is not allowed combined with multi-period investments.
      The storage inflow and outflow are forced to zero until the storage unit is invested into.
    * You can specify periods of different lengths, but the frequency of your timeindex needs to be consistent. Also,
      you could use the `timeincrement` attribute of the energy system to model different weightings. Be aware that this
      has not yet been tested.
    * For now, both, the `timeindex` as well as the `timeincrement` of an energy system have to be defined since they
      have to be of the same length for a multi-period model.
    * You can choose whether to re-evaluate assets at the end of the optimization horizon. If you set attribute
      `use_remaining_value` of the energy system to True (defaults to False), this leads to the model evaluating the
      difference in the asset value at the end of the optimization horizon vs. at the time the investment was made.
      The difference in value is added to or subtracted from the respective investment costs increment,
      assuming assets are to be liquidated / re-evaluated at the end of the optimization horizon.
    * Also please be aware, that periods correspond to years by default. You could also choose
      monthly periods, but you would need to be very careful in parameterizing your energy system and your model and also,
      this would mean monthly discounting (if applicable) as well as specifying your plants lifetimes in months.
