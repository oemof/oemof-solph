\* Source Pyomo model name=OperationalModel *\

min 
objective:
+14 flow(electricityBus_minDemand_0)
+14 flow(electricityBus_minDemand_1)
+14 flow(electricityBus_minDemand_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_minDemand_0)
+1 flow(wind_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_minDemand_1)
+1 flow(wind_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_minDemand_2)
+1 flow(wind_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   25.199999999999999 <= flow(electricityBus_minDemand_0) <= 30
   28.199999999999999 <= flow(electricityBus_minDemand_1) <= 30
   17.699999999999999 <= flow(electricityBus_minDemand_2) <= 30
   0 <= flow(wind_electricityBus_0) <= 45.899999999999999
   0 <= flow(wind_electricityBus_1) <= 51.299999999999997
   0 <= flow(wind_electricityBus_2) <= 32.939999999999998
end
