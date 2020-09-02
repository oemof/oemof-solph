import oemof.solph as solph
from collections import namedtuple
import oemof.solph.exnet as ex
import pandas as pd
from oemof.outputlib import *
import math

class Label(namedtuple('label', ['location','name', 'energy_carrier'])):
    __slots__ = ()
    def __str__(self):
        return '_'.join(map(str, self._asdict().values()))

datetimeindex = pd.date_range('1/1/2017', periods=3, freq='H')

es = solph.EnergySystem(timeindex=datetimeindex)

input_list=[]
input_list.append(-1)
i=0
while i<101:
    ob=i/100
    input_list.append(ob)
    i=i+1
output_list=[]
output_list.append(0)
for ob in input_list:
    if ob!=-1:
        s=math.sqrt(ob)
        output_list.append(s)

#####################################################################################################
#####################################################################################################
#####################################################################################################

b_gas1 = ex.GasBus(label=Label(name='b_gas1', location='C1', energy_carrier=''), slack=True)

b_gas2 = ex.GasBus(label=Label(name='b_gas2', location='C1', energy_carrier=''))

b_gas3 = ex.GasBus(label=Label(name='b_gas3', location='C1', energy_carrier=''))

b_gas4 = ex.GasBus(label=Label(name='b_gas4', location='C1', energy_carrier=''))

gas_line_12=ex.GasLine(label='gas_line_12',
                      inputs={b_gas1: solph.Flow(nominal_value=200)},
                      outputs={b_gas2: solph.Flow(nominal_value=200)},
                      input_list=input_list,
                      output_list=output_list,
                      K_1=100,
                      conv_factor=0.99)

gas_line_23=ex.GasLine(label='gas_line_23',
                      inputs={b_gas2: solph.Flow(nominal_value=200)},
                      outputs={b_gas3: solph.Flow(nominal_value=200)},
                      input_list=input_list,
                      output_list=output_list,
                      K_1=100,
                      conv_factor=0.99)

gas_line_24=ex.GasLine(label='gas_line_24',
                      inputs={b_gas2: solph.Flow(nominal_value=200)},
                      outputs={b_gas4: solph.Flow(nominal_value=200)},
                      input_list=input_list,
                      output_list=output_list,
                      K_1=100,
                      conv_factor=0.99)




#####################################################################################################
#####################################################################################################
#####################################################################################################

source_1=solph.Source(label='source_1',
                      outputs={b_gas1: solph.Flow(nominal_value=300)})


sink_1=solph.Sink(label='sink_1',
                  inputs={b_gas4: solph.Flow(nominal_value=10, actual_value=[1,1,0], fixed=True)})
#
sink_2=solph.Sink(label='sink_2',
                   inputs={b_gas3: solph.Flow(nominal_value=10, actual_value=[1,0,1], fixed=True)})



es.add(b_gas1)
es.add(b_gas2)
es.add(b_gas3)
es.add(b_gas4)
es.add(gas_line_12)
es.add(gas_line_23)
es.add(gas_line_24)


es.add(source_1)
es.add(sink_1)
es.add(sink_2)

model = solph.Model(es)
model.solve(solver='cbc', solve_kwargs={'tee': True})
model.results()
results = processing.results(model)


locationssystem=[]
locationssystem.append('C1')

from oemof.analysing_toolbox_v1_8 import  *

bk=blackbox(results, locationssystem, get_allpotentials=True)