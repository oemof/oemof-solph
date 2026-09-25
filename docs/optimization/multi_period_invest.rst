.. _optimization_multi_period_label:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pathway planning (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you might be interested in how energy systems could evolve in the longer-term, e.g. until 2045 or 2050 to meet some
carbon neutrality and climate protection or RES and energy efficiency targets.

While in principle, you could try to model this in oemof.solph using default investments as described above (see :ref:`optimization_invest_label`),
you would make the implicit assumption that your entire system is built at the start of your optimization and doesn't change over time.

There was a working implementation, that was hard to maintain. If you want to use it, it is best to use solph v0.5.x.
Afterwards, it was gradually removed and will be replaced by a more lightweight and flexible version.
