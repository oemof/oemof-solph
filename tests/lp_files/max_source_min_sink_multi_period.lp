\* Source Pyomo model name=Model *\

min 
objective:
+14 flow(electricityBus_minDemand_0)
+14 flow(electricityBus_minDemand_1)
+13.72549019607843 flow(electricityBus_minDemand_2)
+13.72549019607843 flow(electricityBus_minDemand_3)
+13.456362937331795 flow(electricityBus_minDemand_4)
+13.456362937331795 flow(electricityBus_minDemand_5)

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

c_e_BusBlock_balance(electricityBus_3)_:
-1 flow(electricityBus_minDemand_3)
+1 flow(wind_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
-1 flow(electricityBus_minDemand_4)
+1 flow(wind_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
-1 flow(electricityBus_minDemand_5)
+1 flow(wind_electricityBus_5)
= 0

bounds
   45.36 <= flow(electricityBus_minDemand_0) <= 54
   50.76 <= flow(electricityBus_minDemand_1) <= 54
   31.86 <= flow(electricityBus_minDemand_2) <= 54
   37.8 <= flow(electricityBus_minDemand_3) <= 54
   52.379999999999995 <= flow(electricityBus_minDemand_4) <= 54
   4.859999999999999 <= flow(electricityBus_minDemand_5) <= 54
   0 <= flow(wind_electricityBus_0) <= 45.9
   0 <= flow(wind_electricityBus_1) <= 51.3
   0 <= flow(wind_electricityBus_2) <= 32.94
   0 <= flow(wind_electricityBus_3) <= 38.879999999999995
   0 <= flow(wind_electricityBus_4) <= 53.46
   0 <= flow(wind_electricityBus_5) <= 5.4
end
