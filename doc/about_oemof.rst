##########################################
 About oemof
##########################################

This overview was developed to make oemof easy to use and develop. It describes general ideas and structures of oemof and its modules.

.. contents::
    :depth: 1
    :local:
    :backlinks: top
    

The idea of an open framework
==============================

The Open Energy System Modeling Framework has been developed for the modeling and analysis of energy supply systems considering power and heat as well as prospectively mobility.

oemof is programmed in Python and uses several Python packages for scientific applications (e.g. mathematical optimisation, network analysis, data analyses), optionally in combination with a PostgreSQL/PostGIS Database. It offers a toolbox of various functionalities needed to build energy system models in high temporal and spatial resolution. For instance, the wind energy feed-in in a model region based on weather data can be modelled, the CO2-minimal operation of biomass power plants can be calculated or the future energy supply of Europe can be simulated.

The framework consists of different packages. For the communication between these packages interfaces are provided. 
The oemof packages and their modules are used to build what we call 'application' and depicts
a concrete energy system model (or a subprocess of this model). The following image 
illustrates this idea:

.. 	image:: _files/framework_concept.svg
   :height: 744px
   :width: 1052 px
   :scale: 30 %
   :alt: alternate text
   :align: center

Besides other applications the apps "renpass-gis" and "reegis" are currently developed based on the framework. 
"renpass-gis" enables the simulation of a future European energy system with a high spatial and temporal resolution. 
Different expansion pathways of conventional power plants, renewable energies and net infrastructure can be considered. The app "reegis" provides a simulation of a regional heat and power supply system. 
These two examples show that the modular approach of the framework allows 
applications with very different objectives. 


.. _why_contribute_label:

Why should I contribute?
========================

 * You do not want to start at the very beginning. You are not the first one, who wants to set up energy models. You can just set on existing code.
 * You want your code to be more stable. - If other people use your code, they may find bugs or will have ideas to improve it.
 * Tired of "write-only-code". - If you want to understand your code a year after you have written it you have to document it anyway. why not joining a group and do it together.
 * You want to talk to other people when you are deadlocked. - People are even more willing to help, if they are interested in what you are doing because they can use it afterwards.
 
We know, sometimes it is difficult to start on an existing concept. It will take some time to understand it and you will need extra time to document you own stuff. But once you understand the libraries you will get lots of interesting features, always with the option to fit them to your own needs. We will do our best to help you.

Just contact us, if you have any questions.


Why are we developing oemof? 
==============================
Energy system models often do not have publicly accessible source code and freely available data and are poorly documented. The missing transparency slows down the scientific discussion on  model quality with regard to certain problems such as grid extension. Besides, energy system models are often developed for a certain application and cannot be adjusted (or only with great effort) to other requirements.

The Center for Sustainable Energy Systems (ZNES) together with the Reiner Lemoine Institute (RLI) in Berlin and the Otto-von-Guericke-University of Magdeburg (OVGU) are developing an Open Energy System Modelling Framework (oemof) that addresses these problems by offering a free, open and clearly documented framework for energy system modelling. This transparent approach allows a sound scientific discourse on the underlying models and data. In this way the assessment of quality and significance of undertaken analyses is improved. Moreover, the modular composition of the framework supports the adjustment to a large number of application purposes. The open source approach allows a collaborative development of the framework that offers several advantages:

- **Synergies** - By developing collaboratively synergies between the participating institutes can be utilized.

- **Debugging** - Through the input of a larger group of users and developers bugs are identified and fixed at an earlier stage.

- **Advancement** - The oemof-based application profits from further development of the framework.

