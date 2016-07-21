# -*- coding: utf-8 -*-
"""
Simple oemof energysystem example with multiple energysystems

Tested with oemof version 0.0.5

Info:
simon.hilpert@fh-flensburg.de
"""
import logging
from oemof.tools import logger
logger.define_logging()
msg = "This example does not work anymore and will be removed if not fixed "
msg += "until v0.1"
logging.error(msg)
exit(0)
from oemof.core import energy_system as es
from oemof.core.network.entities.buses import Bus
from oemof.core.network.entities.components import transports as transport

# 1st system
sys1 = es.EnergySystem()
bus11 = Bus(uid="b11")

# 2nd system
sys2 = es.EnergySystem()
bus21 = Bus(uid="b21")
bus22 = Bus(uid="b22")

# 3rd system
sys3 = es.EnergySystem()

# use entities from sys1 and sys2
sys3.entities = sys1.entities + sys2.entities

# connect buses with transport (adds transport object)
sys3.connect(bus11, bus21, in_max=10, out_max=9, eta=0.9,
			transport_class=transport.Simple)

# This bus is automatically added to the sys3 object as it is the last energy
# system object created
bus4 = Bus(uid="b4")

# to add to other energysystem use .add() method
sys1.add(bus4)
