\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_u_integral_limit_emission_factor_upper_limit_:
+0.5 flow(source1_electricityBus_0)
-1.0 flow(source1_electricityBus_1)
+2.0 flow(source1_electricityBus_2)
+1 flow(source1_electricityBus_3)
+0.5 flow(source1_electricityBus_4)
+0.5 flow(source1_electricityBus_5)
+3.5 flow(source2_electricityBus_0)
+3.5 flow(source2_electricityBus_1)
+3.5 flow(source2_electricityBus_2)
+3.5 flow(source2_electricityBus_3)
+3.5 flow(source2_electricityBus_4)
+3.5 flow(source2_electricityBus_5)
<= 777

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(source1_electricityBus_0) <= 100
   0 <= flow(source1_electricityBus_1) <= 100
   0 <= flow(source1_electricityBus_2) <= 100
   0 <= flow(source1_electricityBus_3) <= 100
   0 <= flow(source1_electricityBus_4) <= 100
   0 <= flow(source1_electricityBus_5) <= 100
   0 <= flow(source2_electricityBus_0) <= 100
   0 <= flow(source2_electricityBus_1) <= 100
   0 <= flow(source2_electricityBus_2) <= 100
   0 <= flow(source2_electricityBus_3) <= 100
   0 <= flow(source2_electricityBus_4) <= 100
   0 <= flow(source2_electricityBus_5) <= 100
end
