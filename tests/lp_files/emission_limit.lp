\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_emission_limit_:
+0.5 flow(source1_electricityBus_0)
+0.5 flow(source1_electricityBus_1)
+0.5 flow(source1_electricityBus_2)
+0.80000000000000004 flow(source2_electricityBus_0)
+0.80000000000000004 flow(source2_electricityBus_1)
+0.80000000000000004 flow(source2_electricityBus_2)
<= 777

c_e_Bus_balance(electricityBus_0)_:
+1 flow(source1_electricityBus_0)
+1 flow(source2_electricityBus_0)
+1 flow(source3_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(source1_electricityBus_1)
+1 flow(source2_electricityBus_1)
+1 flow(source3_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(source1_electricityBus_2)
+1 flow(source2_electricityBus_2)
+1 flow(source3_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source1_electricityBus_0) <= 100
   0 <= flow(source1_electricityBus_1) <= 100
   0 <= flow(source1_electricityBus_2) <= 100
   0 <= flow(source2_electricityBus_0) <= 100
   0 <= flow(source2_electricityBus_1) <= 100
   0 <= flow(source2_electricityBus_2) <= 100
   0 <= flow(source3_electricityBus_0) <= 100
   0 <= flow(source3_electricityBus_1) <= 100
   0 <= flow(source3_electricityBus_2) <= 100
end
