\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_emission_factor_constraint(0)_:
+1 NonConvexFlow_status(source1_electricityBus_0)
+1 NonConvexFlow_status(source2_electricityBus_0)
-1 emission_factor(0)
= 0

c_e_emission_factor_constraint(1)_:
+1 NonConvexFlow_status(source1_electricityBus_1)
+1 NonConvexFlow_status(source2_electricityBus_1)
-1 emission_factor(1)
= 0

c_e_emission_factor_constraint(2)_:
+1 NonConvexFlow_status(source1_electricityBus_2)
+1 NonConvexFlow_status(source2_electricityBus_2)
-1 emission_factor(2)
= 0

c_e_Bus_balance(electricityBus_0)_:
+1 flow(source1_electricityBus_0)
+1 flow(source2_electricityBus_0)
+1 flow(source3_electricityBus_0)
+1 flow(source4_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(source1_electricityBus_1)
+1 flow(source2_electricityBus_1)
+1 flow(source3_electricityBus_1)
+1 flow(source4_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(source1_electricityBus_2)
+1 flow(source2_electricityBus_2)
+1 flow(source3_electricityBus_2)
+1 flow(source4_electricityBus_2)
= 0

c_l_NonConvexFlow_min(source1_electricityBus_0)_:
+1 flow(source1_electricityBus_0)
>= 0

c_l_NonConvexFlow_min(source1_electricityBus_1)_:
+1 flow(source1_electricityBus_1)
>= 0

c_l_NonConvexFlow_min(source1_electricityBus_2)_:
+1 flow(source1_electricityBus_2)
>= 0

c_l_NonConvexFlow_min(source2_electricityBus_0)_:
+1 flow(source2_electricityBus_0)
>= 0

c_l_NonConvexFlow_min(source2_electricityBus_1)_:
+1 flow(source2_electricityBus_1)
>= 0

c_l_NonConvexFlow_min(source2_electricityBus_2)_:
+1 flow(source2_electricityBus_2)
>= 0

c_l_NonConvexFlow_min(source3_electricityBus_0)_:
+1 flow(source3_electricityBus_0)
>= 0

c_l_NonConvexFlow_min(source3_electricityBus_1)_:
+1 flow(source3_electricityBus_1)
>= 0

c_l_NonConvexFlow_min(source3_electricityBus_2)_:
+1 flow(source3_electricityBus_2)
>= 0

c_u_NonConvexFlow_max(source1_electricityBus_0)_:
-100 NonConvexFlow_status(source1_electricityBus_0)
+1 flow(source1_electricityBus_0)
<= 0

c_u_NonConvexFlow_max(source1_electricityBus_1)_:
-100 NonConvexFlow_status(source1_electricityBus_1)
+1 flow(source1_electricityBus_1)
<= 0

c_u_NonConvexFlow_max(source1_electricityBus_2)_:
-100 NonConvexFlow_status(source1_electricityBus_2)
+1 flow(source1_electricityBus_2)
<= 0

c_u_NonConvexFlow_max(source2_electricityBus_0)_:
-100 NonConvexFlow_status(source2_electricityBus_0)
+1 flow(source2_electricityBus_0)
<= 0

c_u_NonConvexFlow_max(source2_electricityBus_1)_:
-100 NonConvexFlow_status(source2_electricityBus_1)
+1 flow(source2_electricityBus_1)
<= 0

c_u_NonConvexFlow_max(source2_electricityBus_2)_:
-100 NonConvexFlow_status(source2_electricityBus_2)
+1 flow(source2_electricityBus_2)
<= 0

c_u_NonConvexFlow_max(source3_electricityBus_0)_:
-100 NonConvexFlow_status(source3_electricityBus_0)
+1 flow(source3_electricityBus_0)
<= 0

c_u_NonConvexFlow_max(source3_electricityBus_1)_:
-100 NonConvexFlow_status(source3_electricityBus_1)
+1 flow(source3_electricityBus_1)
<= 0

c_u_NonConvexFlow_max(source3_electricityBus_2)_:
-100 NonConvexFlow_status(source3_electricityBus_2)
+1 flow(source3_electricityBus_2)
<= 0

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
   30 <= flow(source4_electricityBus_0) <= 100
   30 <= flow(source4_electricityBus_1) <= 100
   30 <= flow(source4_electricityBus_2) <= 100
   1 <= emission_factor(0) <= 2
   1 <= emission_factor(1) <= 2
   1 <= emission_factor(2) <= 2
   0 <= NonConvexFlow_status(source1_electricityBus_0) <= 1
   0 <= NonConvexFlow_status(source1_electricityBus_1) <= 1
   0 <= NonConvexFlow_status(source1_electricityBus_2) <= 1
   0 <= NonConvexFlow_status(source2_electricityBus_0) <= 1
   0 <= NonConvexFlow_status(source2_electricityBus_1) <= 1
   0 <= NonConvexFlow_status(source2_electricityBus_2) <= 1
   0 <= NonConvexFlow_status(source3_electricityBus_0) <= 1
   0 <= NonConvexFlow_status(source3_electricityBus_1) <= 1
   0 <= NonConvexFlow_status(source3_electricityBus_2) <= 1
binary
  NonConvexFlow_status(source1_electricityBus_0)
  NonConvexFlow_status(source1_electricityBus_1)
  NonConvexFlow_status(source1_electricityBus_2)
  NonConvexFlow_status(source2_electricityBus_0)
  NonConvexFlow_status(source2_electricityBus_1)
  NonConvexFlow_status(source2_electricityBus_2)
  NonConvexFlow_status(source3_electricityBus_0)
  NonConvexFlow_status(source3_electricityBus_1)
  NonConvexFlow_status(source3_electricityBus_2)
end