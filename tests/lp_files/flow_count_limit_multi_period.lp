\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_emission_factor_constraint(0)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_0)
+1 NonConvexFlowBlock_status(source2_electricityBus_0)
-1 emission_factor(0)
= 0

c_e_emission_factor_constraint(1)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_1)
+1 NonConvexFlowBlock_status(source2_electricityBus_1)
-1 emission_factor(1)
= 0

c_e_emission_factor_constraint(2)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_2)
+1 NonConvexFlowBlock_status(source2_electricityBus_2)
-1 emission_factor(2)
= 0

c_e_emission_factor_constraint(3)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_3)
+1 NonConvexFlowBlock_status(source2_electricityBus_3)
-1 emission_factor(3)
= 0

c_e_emission_factor_constraint(4)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_4)
+1 NonConvexFlowBlock_status(source2_electricityBus_4)
-1 emission_factor(4)
= 0

c_e_emission_factor_constraint(5)_:
+1 NonConvexFlowBlock_status(source1_electricityBus_5)
+1 NonConvexFlowBlock_status(source2_electricityBus_5)
-1 emission_factor(5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_0)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_0)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_1)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_1)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_2)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_2)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_3)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_3)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_4)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_4)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source1_electricityBus_5)_:
-100 NonConvexFlowBlock_status(source1_electricityBus_5)
+1 NonConvexFlowBlock_status_nominal(source1_electricityBus_5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_0)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_0)
-100 NonConvexFlowBlock_status(source3_electricityBus_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_1)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_1)
-100 NonConvexFlowBlock_status(source3_electricityBus_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_2)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_2)
-100 NonConvexFlowBlock_status(source3_electricityBus_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_3)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_3)
-100 NonConvexFlowBlock_status(source3_electricityBus_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_4)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_4)
-100 NonConvexFlowBlock_status(source3_electricityBus_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source3_electricityBus_5)_:
+1 NonConvexFlowBlock_status_nominal(source3_electricityBus_5)
-100 NonConvexFlowBlock_status(source3_electricityBus_5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_0)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_0)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_1)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_1)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_2)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_2)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_3)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_3)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_4)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_4)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(source2_electricityBus_5)_:
-100 NonConvexFlowBlock_status(source2_electricityBus_5)
+1 NonConvexFlowBlock_status_nominal(source2_electricityBus_5)
= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_0_0)_:
-1 flow(source1_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_0_1)_:
-1 flow(source1_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_1_2)_:
-1 flow(source1_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_1_3)_:
-1 flow(source1_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_2_4)_:
-1 flow(source1_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_min(source1_electricityBus_2_5)_:
-1 flow(source1_electricityBus_2_5)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_0_0)_:
-1 flow(source3_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_0_1)_:
-1 flow(source3_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_1_2)_:
-1 flow(source3_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_1_3)_:
-1 flow(source3_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_2_4)_:
-1 flow(source3_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_min(source3_electricityBus_2_5)_:
-1 flow(source3_electricityBus_2_5)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_0_0)_:
-1 flow(source2_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_0_1)_:
-1 flow(source2_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_1_2)_:
-1 flow(source2_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_1_3)_:
-1 flow(source2_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_2_4)_:
-1 flow(source2_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_min(source2_electricityBus_2_5)_:
-1 flow(source2_electricityBus_2_5)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_0_0)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_0)
+1 flow(source1_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_0_1)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_1)
+1 flow(source1_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_1_2)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_2)
+1 flow(source1_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_1_3)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_3)
+1 flow(source1_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_2_4)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_4)
+1 flow(source1_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_max(source1_electricityBus_2_5)_:
-1 NonConvexFlowBlock_status_nominal(source1_electricityBus_5)
+1 flow(source1_electricityBus_2_5)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_0_0)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_0)
+1 flow(source3_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_0_1)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_1)
+1 flow(source3_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_1_2)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_2)
+1 flow(source3_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_1_3)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_3)
+1 flow(source3_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_2_4)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_4)
+1 flow(source3_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_max(source3_electricityBus_2_5)_:
-1 NonConvexFlowBlock_status_nominal(source3_electricityBus_5)
+1 flow(source3_electricityBus_2_5)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_0_0)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_0)
+1 flow(source2_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_0_1)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_1)
+1 flow(source2_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_1_2)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_2)
+1 flow(source2_electricityBus_1_2)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_1_3)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_3)
+1 flow(source2_electricityBus_1_3)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_2_4)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_4)
+1 flow(source2_electricityBus_2_4)
<= 0

c_u_NonConvexFlowBlock_max(source2_electricityBus_2_5)_:
-1 NonConvexFlowBlock_status_nominal(source2_electricityBus_5)
+1 flow(source2_electricityBus_2_5)
<= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= NonConvexFlowBlock_status(source1_electricityBus_0) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_0) <= 1
   1 <= emission_factor(0) <= 2
   0 <= NonConvexFlowBlock_status(source1_electricityBus_1) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_1) <= 1
   1 <= emission_factor(1) <= 2
   0 <= NonConvexFlowBlock_status(source1_electricityBus_2) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_2) <= 1
   1 <= emission_factor(2) <= 2
   0 <= NonConvexFlowBlock_status(source1_electricityBus_3) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_3) <= 1
   1 <= emission_factor(3) <= 2
   0 <= NonConvexFlowBlock_status(source1_electricityBus_4) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_4) <= 1
   1 <= emission_factor(4) <= 2
   0 <= NonConvexFlowBlock_status(source1_electricityBus_5) <= 1
   0 <= NonConvexFlowBlock_status(source2_electricityBus_5) <= 1
   1 <= emission_factor(5) <= 2
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_2) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_3) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_4) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source1_electricityBus_5) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_0) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_0) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_1) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_1) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_2) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_2) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_3) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_3) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_4) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_4) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source3_electricityBus_5) <= +inf
   0 <= NonConvexFlowBlock_status(source3_electricityBus_5) <= 1
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_2) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_3) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_4) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(source2_electricityBus_5) <= +inf
   0 <= flow(source1_electricityBus_0_0) <= 100
   0 <= flow(source1_electricityBus_0_1) <= 100
   0 <= flow(source1_electricityBus_1_2) <= 100
   0 <= flow(source1_electricityBus_1_3) <= 100
   0 <= flow(source1_electricityBus_2_4) <= 100
   0 <= flow(source1_electricityBus_2_5) <= 100
   0 <= flow(source3_electricityBus_0_0) <= 100
   0 <= flow(source3_electricityBus_0_1) <= 100
   0 <= flow(source3_electricityBus_1_2) <= 100
   0 <= flow(source3_electricityBus_1_3) <= 100
   0 <= flow(source3_electricityBus_2_4) <= 100
   0 <= flow(source3_electricityBus_2_5) <= 100
   0 <= flow(source2_electricityBus_0_0) <= 100
   0 <= flow(source2_electricityBus_0_1) <= 100
   0 <= flow(source2_electricityBus_1_2) <= 100
   0 <= flow(source2_electricityBus_1_3) <= 100
   0 <= flow(source2_electricityBus_2_4) <= 100
   0 <= flow(source2_electricityBus_2_5) <= 100
binary
  NonConvexFlowBlock_status(source1_electricityBus_0)
  NonConvexFlowBlock_status(source2_electricityBus_0)
  NonConvexFlowBlock_status(source1_electricityBus_1)
  NonConvexFlowBlock_status(source2_electricityBus_1)
  NonConvexFlowBlock_status(source1_electricityBus_2)
  NonConvexFlowBlock_status(source2_electricityBus_2)
  NonConvexFlowBlock_status(source1_electricityBus_3)
  NonConvexFlowBlock_status(source2_electricityBus_3)
  NonConvexFlowBlock_status(source1_electricityBus_4)
  NonConvexFlowBlock_status(source2_electricityBus_4)
  NonConvexFlowBlock_status(source1_electricityBus_5)
  NonConvexFlowBlock_status(source2_electricityBus_5)
  NonConvexFlowBlock_status(source3_electricityBus_0)
  NonConvexFlowBlock_status(source3_electricityBus_1)
  NonConvexFlowBlock_status(source3_electricityBus_2)
  NonConvexFlowBlock_status(source3_electricityBus_3)
  NonConvexFlowBlock_status(source3_electricityBus_4)
  NonConvexFlowBlock_status(source3_electricityBus_5)
end
