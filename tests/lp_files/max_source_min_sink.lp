\* Source Pyomo model name=Model *\

min 
objective:
+14 flow(electricityBus_minDemand_0_0)
+14 flow(electricityBus_minDemand_0_1)
+14 flow(electricityBus_minDemand_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_minDemand_0_0)
+1 flow(wind_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_minDemand_0_1)
+1 flow(wind_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
-1 flow(electricityBus_minDemand_0_2)
+1 flow(wind_electricityBus_0_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   45.359999999999999 <= flow(electricityBus_minDemand_0_0) <= 54
   50.759999999999998 <= flow(electricityBus_minDemand_0_1) <= 54
   31.859999999999999 <= flow(electricityBus_minDemand_0_2) <= 54
   0 <= flow(wind_electricityBus_0_0) <= 45.899999999999999
   0 <= flow(wind_electricityBus_0_1) <= 51.299999999999997
   0 <= flow(wind_electricityBus_0_2) <= 32.939999999999998
end
