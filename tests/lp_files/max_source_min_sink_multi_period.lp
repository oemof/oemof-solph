\* Source Pyomo model name=Model *\

min 
objective:
+14 flow(electricityBus_minDemand_0_0)
+14 flow(electricityBus_minDemand_0_1)
+13.72549019607843 flow(electricityBus_minDemand_1_2)
+13.72549019607843 flow(electricityBus_minDemand_1_3)
+13.456362937331795 flow(electricityBus_minDemand_2_4)
+13.456362937331795 flow(electricityBus_minDemand_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_minDemand_0_0)
+1 flow(wind_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_minDemand_0_1)
+1 flow(wind_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_minDemand_1_2)
+1 flow(wind_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_minDemand_1_3)
+1 flow(wind_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_minDemand_2_4)
+1 flow(wind_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_minDemand_2_5)
+1 flow(wind_electricityBus_2_5)
= 0

bounds
   45.36 <= flow(electricityBus_minDemand_0_0) <= 54
   50.76 <= flow(electricityBus_minDemand_0_1) <= 54
   31.86 <= flow(electricityBus_minDemand_1_2) <= 54
   37.8 <= flow(electricityBus_minDemand_1_3) <= 54
   52.379999999999995 <= flow(electricityBus_minDemand_2_4) <= 54
   4.859999999999999 <= flow(electricityBus_minDemand_2_5) <= 54
   0 <= flow(wind_electricityBus_0_0) <= 45.9
   0 <= flow(wind_electricityBus_0_1) <= 51.3
   0 <= flow(wind_electricityBus_1_2) <= 32.94
   0 <= flow(wind_electricityBus_1_3) <= 38.879999999999995
   0 <= flow(wind_electricityBus_2_4) <= 53.46
   0 <= flow(wind_electricityBus_2_5) <= 5.4
end
