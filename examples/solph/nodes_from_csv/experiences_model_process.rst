Documentation of the renpassG!S modelling process (focus on market price modeling)
=================

Experiences
------------------

* The residual load has a big impact on the price.
  Thus it is important to determine the load and must-run capacities e.g. is important how big the biomass or RoR capacities are.
  High transmission capacities in combination with high must-run capacities in neigbour regions also have a big impact e.g. high RoR shares for CH or AT.
  Also non-availabilities of power plants have to be considered and influence the merit order significantly.

* Resource prices and power plant efficiencies also have a big impact in the price. They should be checked and verified using different sources as 
  they are varying in literature.
  Efficiency classes per energy source only generate smaller steps but do have a significant impact on the price if the classes are quite narrow.

* For connector capacities (NTCs) the same applies

* Still quite undetailed models with only one power plant per energy source and not many assumptions e.g. minimum full-load hours already deliver
  the right tendencies in the energy system. But with a low capacity resolution (few "big" power plants) some technologies
  and equivalent variable and marginal costs, some technologies e.g. gas or biomass do not enter the market as observed
  in reality.

* Gradients (positive and negative) are memory consuming (> 16 GB) and can kill the python instance or solver

Open questions?
------------------

* Impact of gradients: more fluctuations? Also see: Biggar, 2014. The Economics of Electricity Markets, p. 111 ff.
* Impact of minimum up and downtimes: more fluctuations? Also see: Biggar, 2014. The Economics of Electricity Markets

