\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_constraint_:
+0.80000000000000004 flow(source1_electricityBus_0_0)
+0.80000000000000004 flow(source1_electricityBus_0_1)
+0.80000000000000004 flow(source1_electricityBus_1_2)
+0.80000000000000004 flow(source1_electricityBus_1_3)
+0.80000000000000004 flow(source1_electricityBus_2_4)
+0.80000000000000004 flow(source1_electricityBus_2_5)
<= 777

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source1_electricityBus_0_0) <= 100
   0 <= flow(source1_electricityBus_0_1) <= 100
   0 <= flow(source1_electricityBus_1_2) <= 100
   0 <= flow(source1_electricityBus_1_3) <= 100
   0 <= flow(source1_electricityBus_2_4) <= 100
   0 <= flow(source1_electricityBus_2_5) <= 100
end
