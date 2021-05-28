\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+23 flow(powerplant_electricityBus_0_0)
+23 flow(powerplant_electricityBus_0_1)
+22.549019607843135 flow(powerplant_electricityBus_1_2)
+22.549019607843135 flow(powerplant_electricityBus_1_3)
+22.106881968473662 flow(powerplant_electricityBus_2_4)
+22.106881968473662 flow(powerplant_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(powerplant_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(powerplant_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(powerplant_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(powerplant_electricityBus_2_5)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_0_0)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_0)
-1 flow(powerplant_electricityBus_0_0)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_0_1)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_1)
-1 flow(powerplant_electricityBus_0_1)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_1_2)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_2)
-1 flow(powerplant_electricityBus_1_2)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_1_3)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_3)
-1 flow(powerplant_electricityBus_1_3)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_2_4)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_4)
-1 flow(powerplant_electricityBus_2_4)
= 0

c_e_MultiPeriodFlow_integer_flow_constr(powerplant_electricityBus_2_5)_:
+1 MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_5)
-1 flow(powerplant_electricityBus_2_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0_0) <= 999
   0 <= flow(powerplant_electricityBus_0_1) <= 999
   0 <= flow(powerplant_electricityBus_1_2) <= 999
   0 <= flow(powerplant_electricityBus_1_3) <= 999
   0 <= flow(powerplant_electricityBus_2_4) <= 999
   0 <= flow(powerplant_electricityBus_2_5) <= 999
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_0) <= +inf
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_1) <= +inf
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_2) <= +inf
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_3) <= +inf
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_4) <= +inf
   0 <= MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_5) <= +inf
general
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_0)
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_0_1)
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_2)
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_1_3)
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_4)
  MultiPeriodFlow_integer_flow(powerplant_electricityBus_2_5)
end
