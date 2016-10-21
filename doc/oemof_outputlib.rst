.. _oemof_outputlib_label:

#####################
oemof-outputlib
#####################

The outputlib converts the results to a pandas MultiIndex DataFrame. In this way we make the full power of the pandas package available to process the results. See the `pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_  to learn how to `visualise <http://pandas.pydata.org/pandas-docs/version/0.18.1/visualization.html>`_, `read or write <http://pandas.pydata.org/pandas-docs/stable/io.html>`_ or how to `access parts of the DataFrame <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`_ to process them.

However, oemof provides some functionality that makes your life easier, especially at the beginning.

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Slicing the DataFrame
---------------------

(-> :py:meth:`~oemof.outputlib.ResultsDataFrame.slice_by`)

You first need to create an instance of your MultiIndex DataFrame. On this DataFrame you can apply all functions provided by pandas. The slice_by method is an oemof method to access easily a specific component or bus to process or save the results. The *type* parameter signifies the direction of the flow, into or out of a bus. The following examples writes the output of a gas power plant to a csv-file. As we do slice the whole year, the *date_from/date_to* parameter is not necessary. We can use these parameters to slice shorter periods.

  .. code-block:: python
  
      myresults = outputlib.DataFramePlot(energy_system=my_energysystem)
      pp_gas = myresults.slice_by(obj_label='pp_gas', type='to_bus',
                                  date_from='2012-01-01 00:00:00',
                                  date_to='2012-12-31 23:00:00')
      pp_gas.to_csv('pp_gas.csv')solph.Flow()
      
      
You can use this approach also to plot the results, but plotting a slice of a DataFrame is not as easy as plotting a normal DataFrame so you can use the plotting class described in the next section.


Plotting parts of the DataFrame
-------------------------------
(-> :py:class:`~oemof.outputlib.DataFramePlot`)

This class will only add some methods to make things easier. It is still possible to access the full functionality of the `matplotlib <http://matplotlib.org/>`_ package.

Some feature provided by the outputlib:

* Configure the x-axis of you plot with date/time ticks depending on your requirements (:py:class:`~oemof.outputlib.DataFramePlot.set_datetime_ticks`)
* Placing the legend outside the plot (:py:class:`~oemof.outputlib.DataFramePlot.outside_legend`)
* Plotting a balance plot around a bus with all inputs/outputs (:py:class:`~oemof.outputlib.DataFramePlot.io_plot`)
* Use one specific color for every component of your energy model (:py:class:`~oemof.outputlib.DataFramePlot.color_from_dict`)
* Change the order of the flows in your subset for bar plots or stacked plots (:py:class:`~oemof.outputlib.DataFramePlot.rearrange_subset`)

The following examples shows how to use the `pandas plot method <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.plot.html>`_ with the oemof's DataFramePlot class. The parameter *linewidth* and *title* belong to pandas.

.. code-block:: python

    myplot = outputlib.DataFramePlot(energy_system=energysystem)
    myplot.slice_unstacked(bus_label="electricity", type="to_bus",
                           date_from="2012-01-01 00:00:00",
                           date_to="2012-01-31 00:00:00")
    myplot.plot(linewidth=2, title="January 2012")


The following examples shows how to combine code of the matplotlib with the DataFramePlot class. Matplotlib code is used to define the figure and the font size. With the *ax* parameter this configuration is passed to the pandas plot function. Further matplolib and oemof functions are used to design the plot.

.. code-block:: python

    fig = plt.figure(figsize=(24, 14))  # matplotlib
    plt.rc('legend', **{'fontsize': 19})  # matplotlib
    plt.rcParams.update({'font.size': 19})  # matplotlib
    plt.style.use('grayscale')  # matplotlib  # oemof
    myplot.slice_unstacked(bus_label="electricity", type="from_bus")
    myplot.plot(title="Year 2016", colormap='Spectral', linewidth=2, ax=fig.add_subplot(1, 1, 1))  # pandas
    myplot.ax.set_ylabel('Power in MW')  # matplotlib
    myplot.ax.set_xlabel('Date')  # matplotlib
    myplot.ax.set_title("Electricity bus")  # matplotlib
    myplot.set_datetime_ticks(number_autoticks=5, date_format='%d-%m-%Y')  # oemof
    myplot.outside_legend()  # oemof
    
    
Creating a colour dictionary
-----------------------------

A colour dictionary is useful to have the same colour for a specific component in every plot. Therefore you can define a colour for every component of your model using a dictionary. The key has to be the labell of the component while the value is the colour.

.. code-block:: python

    cdict = {'wind': '#5b5bae',
             'pv': 'blue',
             'storage': 'r',
             'demand': (0.34, 0.2, 0.89)}
             
As shown in the example there are different ways to defining a colour using matplolib. Have a look at the general description of `matplotlib colours <http://matplotlib.org/api/colors_api.html>`_ or use the `named colours <http://matplotlib.org/examples/color/named_colors.html>`_.
    

Creating an input/output plot for buses
---------------------------------------

An input/output plot (i/o-plot) can be used to see the balance around a bus. All input flows are plotted as a stacked line plot, all output flows as a stacked bar plot. See :py:class:`~oemof.outputlib.DataFramePlot.rearrange_subset` for all possible parameters. The following example shows the code of left plot below:

.. code-block:: python

    myplot = outputlib.DataFramePlot(energy_system=energysystem)
    handles, labels = myplot.io_plot(
        bus_label='electricity', cdict=cdict,
        barorder=['pv', 'wind', 'pp_gas', 'storage'],
        lineorder=['demand', 'storage', 'excess_bel'],
        line_kwa={'linewidth': 4},
        date_from="2012-06-01 00:00:00",
        date_to="2012-06-8 00:00:00",
        )
    myplot.ax.set_ylabel('Power in MW')
    myplot.ax.set_xlabel('Date')
    myplot.ax.set_title("Electricity bus")
    myplot.set_datetime_ticks(tick_distance=24, date_format='%d-%m-%Y')
    myplot.outside_legend(handles=handles, labels=labels)

    plt.show()

Due to the rearrangement of the order with in the i/o-plot (*barorder*, *lineorder*) the handles and labels are manipulated. Therefore you have to pass them in the new order to the *outside_legend* method to get the legend in the right order. Otherwise the legend will be outside but will be in the first order.


Typical outputs of the outputlib
--------------------------------

.. 	image:: _files/example_figures.png
   :scale: 100 %
   :alt: alternate text
   :align: center
 