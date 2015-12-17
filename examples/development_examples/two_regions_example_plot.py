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

tmp_in = {}
tmp_out = {}

for inp in bus2.inputs:
    tmp_in[inp.uid] = TwoRegExample.results[inp][bus2]
for out in bus2.outputs:
    tmp_out[out.uid] = TwoRegExample.results[bus2][out]

stplot.busplot(inputs=tmp_in, outputs=tmp_out)
