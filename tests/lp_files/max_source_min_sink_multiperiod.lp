\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+14 flow(electricityBus_minDemand_0_0)
+14 flow(electricityBus_minDemand_0_1)
+13.725490196078431 flow(electricityBus_minDemand_1_2)
+13.725490196078431 flow(electricityBus_minDemand_1_3)
+13.456362937331795 flow(electricityBus_minDemand_2_4)
+13.456362937331795 flow(electricityBus_minDemand_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_minDemand_0_0)
+1 flow(wind_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_minDemand_0_1)
+1 flow(wind_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_minDemand_1_2)
+1 flow(wind_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_minDemand_1_3)
+1 flow(wind_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_minDemand_2_4)
+1 flow(wind_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_minDemand_2_5)
+1 flow(wind_electricityBus_2_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   45.359999999999999 <= flow(electricityBus_minDemand_0_0) <= 54
   50.759999999999998 <= flow(electricityBus_minDemand_0_1) <= 54
   31.859999999999999 <= flow(electricityBus_minDemand_1_2) <= 54
   45.359999999999999 <= flow(electricityBus_minDemand_1_3) <= 54
   50.759999999999998 <= flow(electricityBus_minDemand_2_4) <= 54
   31.859999999999999 <= flow(electricityBus_minDemand_2_5) <= 54
   0 <= flow(wind_electricityBus_0_0) <= 45.899999999999999
   0 <= flow(wind_electricityBus_0_1) <= 51.299999999999997
   0 <= flow(wind_electricityBus_1_2) <= 32.939999999999998
   0 <= flow(wind_electricityBus_1_3) <= 45.899999999999999
   0 <= flow(wind_electricityBus_2_4) <= 51.299999999999997
   0 <= flow(wind_electricityBus_2_5) <= 32.939999999999998
end
