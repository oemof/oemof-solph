\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+0.8 flow(source1_electricityBus_0)
+0.8 flow(source1_electricityBus_1)
+0.8 flow(source1_electricityBus_2)
<= 777

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(source1_electricityBus_0)
+1 flow(source2_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(source1_electricityBus_1)
+1 flow(source2_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(source1_electricityBus_2)
+1 flow(source2_electricityBus_2)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(source1_electricityBus_0) <= 100
   0 <= flow(source1_electricityBus_1) <= 100
   0 <= flow(source1_electricityBus_2) <= 100
   0 <= flow(source2_electricityBus_0) <= 100
   0 <= flow(source2_electricityBus_1) <= 100
   0 <= flow(source2_electricityBus_2) <= 100
end
