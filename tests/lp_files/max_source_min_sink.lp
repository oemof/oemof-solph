\* Source Pyomo model name=Model *\

min 
objective:
+14 flow(electricityBus_minDemand_0)
+14 flow(electricityBus_minDemand_1)
+14 flow(electricityBus_minDemand_2)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
-1 flow(electricityBus_minDemand_0)
+1 flow(wind_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
-1 flow(electricityBus_minDemand_1)
+1 flow(wind_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
-1 flow(electricityBus_minDemand_2)
+1 flow(wind_electricityBus_2)
= 0

bounds
   45.36 <= flow(electricityBus_minDemand_0) <= 54
   50.76 <= flow(electricityBus_minDemand_1) <= 54
   31.86 <= flow(electricityBus_minDemand_2) <= 54
   0 <= flow(wind_electricityBus_0) <= 45.9
   0 <= flow(wind_electricityBus_1) <= 51.3
   0 <= flow(wind_electricityBus_2) <= 32.94
end
