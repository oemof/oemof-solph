\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(cheap_plant_activity_costs_Bus_C_0_0)
+10 flow(cheap_plant_activity_costs_Bus_C_0_1)
+9.80392156862745 flow(cheap_plant_activity_costs_Bus_C_1_2)
+9.80392156862745 flow(cheap_plant_activity_costs_Bus_C_1_3)
+9.611687812379854 flow(cheap_plant_activity_costs_Bus_C_2_4)
+9.611687812379854 flow(cheap_plant_activity_costs_Bus_C_2_5)
+2 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
+2 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
+1.9607843137254901 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
+1.9607843137254901 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
+1.9223375624759707 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
+1.9223375624759707 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)

s.t.

c_e_BusBlock_balance(Bus_C_0_0)_:
+1 flow(cheap_plant_activity_costs_Bus_C_0_0)
= 0

c_e_BusBlock_balance(Bus_C_0_1)_:
+1 flow(cheap_plant_activity_costs_Bus_C_0_1)
= 0

c_e_BusBlock_balance(Bus_C_1_2)_:
+1 flow(cheap_plant_activity_costs_Bus_C_1_2)
= 0

c_e_BusBlock_balance(Bus_C_1_3)_:
+1 flow(cheap_plant_activity_costs_Bus_C_1_3)
= 0

c_e_BusBlock_balance(Bus_C_2_4)_:
+1 flow(cheap_plant_activity_costs_Bus_C_2_4)
= 0

c_e_BusBlock_balance(Bus_C_2_5)_:
+1 flow(cheap_plant_activity_costs_Bus_C_2_5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_0)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_1)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_2)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_3)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_4)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_activity_costs_Bus_C_5)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_5)
= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_0_0)_:
-1 flow(cheap_plant_activity_costs_Bus_C_0_0)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_0_1)_:
-1 flow(cheap_plant_activity_costs_Bus_C_0_1)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_1_2)_:
-1 flow(cheap_plant_activity_costs_Bus_C_1_2)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_1_3)_:
-1 flow(cheap_plant_activity_costs_Bus_C_1_3)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_3)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_2_4)_:
-1 flow(cheap_plant_activity_costs_Bus_C_2_4)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_4)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_2_5)_:
-1 flow(cheap_plant_activity_costs_Bus_C_2_5)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_5)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_0_0)_:
+1 flow(cheap_plant_activity_costs_Bus_C_0_0)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_0_1)_:
+1 flow(cheap_plant_activity_costs_Bus_C_0_1)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_1_2)_:
+1 flow(cheap_plant_activity_costs_Bus_C_1_2)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_1_3)_:
+1 flow(cheap_plant_activity_costs_Bus_C_1_3)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_3)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_2_4)_:
+1 flow(cheap_plant_activity_costs_Bus_C_2_4)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_4)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_2_5)_:
+1 flow(cheap_plant_activity_costs_Bus_C_2_5)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_5)
<= 0

bounds
   0 <= flow(cheap_plant_activity_costs_Bus_C_0_0) <= 10.0
   0 <= flow(cheap_plant_activity_costs_Bus_C_0_1) <= 10.0
   0 <= flow(cheap_plant_activity_costs_Bus_C_1_2) <= 10.0
   0 <= flow(cheap_plant_activity_costs_Bus_C_1_3) <= 10.0
   0 <= flow(cheap_plant_activity_costs_Bus_C_2_4) <= 10.0
   0 <= flow(cheap_plant_activity_costs_Bus_C_2_5) <= 10.0
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_2) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_3) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_4) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_activity_costs_Bus_C_5) <= +inf
binary
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
end
