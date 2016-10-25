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

The Open Energy System Modelling Framework has been developed for the modelling and analysis of energy supply systems considering power and heat as well as prospectively mobility.

Oemof is programmed in Python and uses several Python packages for scientific applications (e.g. mathematical optimisation, network analysis, data analyses), optionally in combination with a PostgreSQL/PostGIS Database. It offers a toolbox of various features needed to build energy system models in high temporal and spatial resolution. For instance, the wind energy feed-in in a model region based on weather data can be modelled, the CO2-minimal operation of biomass power plants can be calculated or the future energy supply of Europe can be simulated.

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
Different expansion pathways of conventional power plants, renewable energies and net infrastructure can be considered. The app "reegis" provides a simulation of a regional heat and power supply system. Another application is HESYSOPT which is desined to simulate combined heat and power systems with MILP on the component level. 
These three examples show that the modular approach of the framework allows applications with very different objectives. 


.. _why_contribute_label:

Why should I contribute?
========================

 * You do not want to start at the very beginning. - You are not the first one, who wants to set up a energy system model. So why not start with on existing code?
 * You want your code to be more stable. - If other people use your code, they may find bugs or will have ideas to improve it.
 * Tired of "write-only-code". - Developing as part of a framework encourages you to document sufficiently, so that after years you may still understand your own code. 
 * You want to talk to other people when you are deadlocked. - People are even more willing to help, if they are interested in what you are doing because they can use it afterwards.
 * You want your code to be seen and used. We try to make oemof more and more visible to the modelling community. Together it will be easier to increase the awareness of this framework and therefore for your contribution.
 
We know, sometimes it is difficult to start on an existing concept. It will take some time to understand it and you will need extra time to document your own stuff. But once you understand the libraries you will get lots of interesting features, always with the option to fit them to your own needs.

Just contact us, if you have any questions.


Join oemof with your own approach or project
============================================

Oemof is designed as a framework and there is a lot of space for own ideas or own libraries. No matter if you want a heuristic solver library or different linear solver library. You may want to add tools to analyse the results or something we never heard of. You want to add a GUI or your application to be linked to. We think, that working together in one framework will increase the probability that somebody will use and test your code (see :ref:`why_contribute_label`).

Interested? Together we can talk about how to transfer your ideas into oemof or even integrate your code. Maybe we just link to your project and try to adept the API for a better fit in the future.


Why are we developing oemof? 
==============================
Energy system models often do not have publicly accessible source code and freely available data and are poorly documented. The missing transparency slows down the scientific discussion on  model quality with regard to certain problems such as grid extension. Besides, energy system models are often developed for a certain application and cannot be adjusted (or only with great effort) to other requirements.

The Center for Sustainable Energy Systems (ZNES) together with the Reiner Lemoine Institute (RLI) in Berlin and the Otto-von-Guericke-University of Magdeburg (OVGU) are developing an Open Energy System Modelling Framework (oemof) that addresses these problems by offering a free, open and clearly documented framework for energy system modelling. This transparent approach allows a sound scientific discourse on the underlying models and data. In this way the assessment of quality and significance of undertaken analyses is improved. Moreover, the modular composition of the framework supports the adjustment to a large number of application purposes. The open source approach allows a collaborative development of the framework that offers several advantages:

- **Synergies** - By developing collaboratively synergies between the participating institutes can be utilized.

- **Debugging** - Through the input of a larger group of users and developers bugs are identified and fixed at an earlier stage.

- **Advancement** - The oemof-based application profits from further development of the framework.

