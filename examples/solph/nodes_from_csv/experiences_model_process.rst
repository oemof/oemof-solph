Documentation of the renpassG!S modelling process (focus market price modeling)
=================

Experiences
------------------

* The residual load has a big impact on the price.
  Thus it is important to determine the load and must-run capacities e.g. is important how big the biomass or RoR capacities are.
  High transmission capacities in combination with high must-run capacities in neigbour regions also have a big impact e.g. high RoR shares for CH or AT.

* Resource prices and power plant efficiencies also have a big impact in the price. They should be checked and verified using different sources as 
  they are varying in literature.
  Efficiency classes per energy source only generate smaller steps but do have a significant impact on the price if the classes are quite narrow.

* Still quite undetailed models with only one power plant per energy source and not many assumptions e.g. minimum full-load hours already deliver the right tendencies in the energy system.

* Gradients (positive and negative) are memory consuming (> 16 GB) and can kill the python instance or solver

Open questions?
------------------

* Impact of gradients: more fluctuations? Also see: Biggar, 2014. The Economics of Electricity Markets, p. 111 ff.
* Impact of minimum up and downtimes: more fluctuations? Also see: Biggar, 2014. The Economics of Electricity Markets

