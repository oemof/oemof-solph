.. _oemof_outputlib_label:

#####################
oemof-outputlib
#####################

For version 0.2, the outputlib has been refactored to main
function of the outputlib is to collect and organise results.

The outputlib converts the results to a pandas MultiIndex DataFrame. In this way we make the full power of the pandas package available to process the results. See the `pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_  to learn how to `visualise <http://pandas.pydata.org/pandas-docs/version/0.18.1/visualization.html>`_, `read or write <http://pandas.pydata.org/pandas-docs/stable/io.html>`_ or how to `access parts of the DataFrame <http://pandas.pydata.org/pandas-docs/stable/advanced.html>`_ to process them.

Tools for plotting optimization results that were part of the outputlib earlier are
no longer part of this module,as the requirements to plotting functions greatly depend on the situation.

Those who need a tool for quick visualisation of results will find basic plotting
functionalities in a distinct new repository `oemof_visio <https://github.com/oemof/oemof_visio>`


.. contents::
    :depth: 1
    :local:
    :backlinks: top



processing.results(om)
meta_results = processing.meta_results(om)

