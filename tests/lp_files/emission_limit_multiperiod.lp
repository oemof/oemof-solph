\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+0.5 flow(source1_electricityBus_0_0)
-1 flow(source1_electricityBus_0_1)
+2 flow(source1_electricityBus_1_2)
+0.5 flow(source1_electricityBus_1_3)
-1 flow(source1_electricityBus_2_4)
+2 flow(source1_electricityBus_2_5)
+3.5 flow(source2_electricityBus_0_0)
+3.5 flow(source2_electricityBus_0_1)
+3.5 flow(source2_electricityBus_1_2)
+3.5 flow(source2_electricityBus_1_3)
+3.5 flow(source2_electricityBus_2_4)
+3.5 flow(source2_electricityBus_2_5)
<= 777

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(source1_electricityBus_0_0)
+1 flow(source2_electricityBus_0_0)
+1 flow(source3_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(source1_electricityBus_0_1)
+1 flow(source2_electricityBus_0_1)
+1 flow(source3_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(source1_electricityBus_1_2)
+1 flow(source2_electricityBus_1_2)
+1 flow(source3_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(source1_electricityBus_1_3)
+1 flow(source2_electricityBus_1_3)
+1 flow(source3_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(source1_electricityBus_2_4)
+1 flow(source2_electricityBus_2_4)
+1 flow(source3_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(source1_electricityBus_2_5)
+1 flow(source2_electricityBus_2_5)
+1 flow(source3_electricityBus_2_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source1_electricityBus_0_0) <= 100
   0 <= flow(source1_electricityBus_0_1) <= 100
   0 <= flow(source1_electricityBus_1_2) <= 100
   0 <= flow(source1_electricityBus_1_3) <= 100
   0 <= flow(source1_electricityBus_2_4) <= 100
   0 <= flow(source1_electricityBus_2_5) <= 100
   0 <= flow(source2_electricityBus_0_0) <= 100
   0 <= flow(source2_electricityBus_0_1) <= 100
   0 <= flow(source2_electricityBus_1_2) <= 100
   0 <= flow(source2_electricityBus_1_3) <= 100
   0 <= flow(source2_electricityBus_2_4) <= 100
   0 <= flow(source2_electricityBus_2_5) <= 100
   0 <= flow(source3_electricityBus_0_0) <= 100
   0 <= flow(source3_electricityBus_0_1) <= 100
   0 <= flow(source3_electricityBus_1_2) <= 100
   0 <= flow(source3_electricityBus_1_3) <= 100
   0 <= flow(source3_electricityBus_2_4) <= 100
   0 <= flow(source3_electricityBus_2_5) <= 100
end
