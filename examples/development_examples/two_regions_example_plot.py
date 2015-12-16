#!/usr/bin/python3
# -*- coding: utf-8

import logging

from oemof.outputlib import stacked_time_plot_file as stplot
from oemof.tools import logger
from oemof.core import energy_system as es


logger.define_logging()

# Create an energy system
TwoRegExample = es.EnergySystem()

logging.info(TwoRegExample.restore())

bus2 = [obj for obj in TwoRegExample.entities if obj.uid == str((
    'bus', 'Landkreis Wittenberg', 'elec'))][0]

print("Inputs:")
for inp in bus2.inputs:
    print(inp.uid)
    print(TwoRegExample.results[inp][bus2][0:3])

print("Outputs:")
for out in bus2.outputs:
    print(out.uid)
    print(TwoRegExample.results[bus2][out][0:3])

stplot.stackplot()
