
Changelog
=========

0.4.0 (2020-06-04)
------------------

* First release of oemof.solph on PyPI.

0.4.1 (2020-06-24)
------------------

* Fixed incompatibility with recent Pyomo release (5.7)

0.4.2 (2021-XX-XX)
------------------

* Enhanced custom SinkDSM:
    * Renamed keyword argument `method` to `approach`
    * Renamed approaches `interval` to `oemof` and `delay` to `DIW`
    * Added modeling approach `DLR` (PhD thesis of Hans Christian Gils 2015)
    * Included load shedding
    * Introduced `recovery_time` in `DIW` approach
    * Introduced `shift_time` and other parameters for `DLR` approach
    * Included investments in DSM
    * Normalized keyword arguments `demand`, `cap_up` and `cap_do`
