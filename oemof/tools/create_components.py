#!/usr/bin/python
# -*- coding: utf-8


def instant_flow_heater(bus_low, bus_high):
    f = ((bus_high.temperature - bus_low.temperature) /
         (bus_low.temperature - bus_high.re_temperature))
    f[f < 0] = 0
    return f
