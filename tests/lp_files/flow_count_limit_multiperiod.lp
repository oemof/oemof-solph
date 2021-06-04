\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_emission_factor_constraint(0)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_0)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_0)
-1 emission_factor(0)
= 0

c_e_emission_factor_constraint(1)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_1)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_1)
-1 emission_factor(1)
= 0

c_e_emission_factor_constraint(2)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_2)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_2)
-1 emission_factor(2)
= 0

c_e_emission_factor_constraint(3)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_3)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_3)
-1 emission_factor(3)
= 0

c_e_emission_factor_constraint(4)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_4)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_4)
-1 emission_factor(4)
= 0

c_e_emission_factor_constraint(5)_:
+1 MultiPeriodNonConvexFlow_status(source1_electricityBus_5)
+1 MultiPeriodNonConvexFlow_status(source2_electricityBus_5)
-1 emission_factor(5)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(source1_electricityBus_0_0)
+1 flow(source2_electricityBus_0_0)
+1 flow(source3_electricityBus_0_0)
+1 flow(source4_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(source1_electricityBus_0_1)
+1 flow(source2_electricityBus_0_1)
+1 flow(source3_electricityBus_0_1)
+1 flow(source4_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(source1_electricityBus_1_2)
+1 flow(source2_electricityBus_1_2)
+1 flow(source3_electricityBus_1_2)
+1 flow(source4_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(source1_electricityBus_1_3)
+1 flow(source2_electricityBus_1_3)
+1 flow(source3_electricityBus_1_3)
+1 flow(source4_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(source1_electricityBus_2_4)
+1 flow(source2_electricityBus_2_4)
+1 flow(source3_electricityBus_2_4)
+1 flow(source4_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(source1_electricityBus_2_5)
+1 flow(source2_electricityBus_2_5)
+1 flow(source3_electricityBus_2_5)
+1 flow(source4_electricityBus_2_5)
= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_0_0)_:
+1 flow(source1_electricityBus_0_0)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_0_1)_:
+1 flow(source1_electricityBus_0_1)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_1_2)_:
+1 flow(source1_electricityBus_1_2)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_1_3)_:
+1 flow(source1_electricityBus_1_3)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_2_4)_:
+1 flow(source1_electricityBus_2_4)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source1_electricityBus_2_5)_:
+1 flow(source1_electricityBus_2_5)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_0_0)_:
+1 flow(source2_electricityBus_0_0)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_0_1)_:
+1 flow(source2_electricityBus_0_1)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_1_2)_:
+1 flow(source2_electricityBus_1_2)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_1_3)_:
+1 flow(source2_electricityBus_1_3)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_2_4)_:
+1 flow(source2_electricityBus_2_4)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source2_electricityBus_2_5)_:
+1 flow(source2_electricityBus_2_5)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_0_0)_:
+1 flow(source3_electricityBus_0_0)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_0_1)_:
+1 flow(source3_electricityBus_0_1)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_1_2)_:
+1 flow(source3_electricityBus_1_2)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_1_3)_:
+1 flow(source3_electricityBus_1_3)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_2_4)_:
+1 flow(source3_electricityBus_2_4)
>= 0

c_l_MultiPeriodNonConvexFlow_min(source3_electricityBus_2_5)_:
+1 flow(source3_electricityBus_2_5)
>= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_0_0)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_0)
+1 flow(source1_electricityBus_0_0)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_0_1)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_1)
+1 flow(source1_electricityBus_0_1)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_1_2)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_2)
+1 flow(source1_electricityBus_1_2)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_1_3)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_3)
+1 flow(source1_electricityBus_1_3)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_2_4)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_4)
+1 flow(source1_electricityBus_2_4)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source1_electricityBus_2_5)_:
-100 MultiPeriodNonConvexFlow_status(source1_electricityBus_5)
+1 flow(source1_electricityBus_2_5)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_0_0)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_0)
+1 flow(source2_electricityBus_0_0)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_0_1)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_1)
+1 flow(source2_electricityBus_0_1)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_1_2)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_2)
+1 flow(source2_electricityBus_1_2)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_1_3)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_3)
+1 flow(source2_electricityBus_1_3)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_2_4)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_4)
+1 flow(source2_electricityBus_2_4)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source2_electricityBus_2_5)_:
-100 MultiPeriodNonConvexFlow_status(source2_electricityBus_5)
+1 flow(source2_electricityBus_2_5)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_0_0)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_0)
+1 flow(source3_electricityBus_0_0)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_0_1)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_1)
+1 flow(source3_electricityBus_0_1)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_1_2)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_2)
+1 flow(source3_electricityBus_1_2)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_1_3)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_3)
+1 flow(source3_electricityBus_1_3)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_2_4)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_4)
+1 flow(source3_electricityBus_2_4)
<= 0

c_u_MultiPeriodNonConvexFlow_max(source3_electricityBus_2_5)_:
-100 MultiPeriodNonConvexFlow_status(source3_electricityBus_5)
+1 flow(source3_electricityBus_2_5)
<= 0

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
   30 <= flow(source4_electricityBus_0_0) <= 100
   30 <= flow(source4_electricityBus_0_1) <= 100
   30 <= flow(source4_electricityBus_1_2) <= 100
   30 <= flow(source4_electricityBus_1_3) <= 100
   30 <= flow(source4_electricityBus_2_4) <= 100
   30 <= flow(source4_electricityBus_2_5) <= 100
   1 <= emission_factor(0) <= 2
   1 <= emission_factor(1) <= 2
   1 <= emission_factor(2) <= 2
   1 <= emission_factor(3) <= 2
   1 <= emission_factor(4) <= 2
   1 <= emission_factor(5) <= 2
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_0) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_1) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_2) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_3) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_4) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source1_electricityBus_5) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_0) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_1) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_2) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_3) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_4) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source2_electricityBus_5) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_0) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_1) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_2) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_3) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_4) <= 1
   0 <= MultiPeriodNonConvexFlow_status(source3_electricityBus_5) <= 1
binary
  MultiPeriodNonConvexFlow_status(source1_electricityBus_0)
  MultiPeriodNonConvexFlow_status(source1_electricityBus_1)
  MultiPeriodNonConvexFlow_status(source1_electricityBus_2)
  MultiPeriodNonConvexFlow_status(source1_electricityBus_3)
  MultiPeriodNonConvexFlow_status(source1_electricityBus_4)
  MultiPeriodNonConvexFlow_status(source1_electricityBus_5)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_0)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_1)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_2)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_3)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_4)
  MultiPeriodNonConvexFlow_status(source2_electricityBus_5)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_0)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_1)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_2)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_3)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_4)
  MultiPeriodNonConvexFlow_status(source3_electricityBus_5)
end
