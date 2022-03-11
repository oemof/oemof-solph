\* Source Pyomo model name=Model *\

min 
objective:
+2 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
+2 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
+1.9607843137254901 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
+1.9607843137254901 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
+1.9223375624759707 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
+1.9223375624759707 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
+10 flow(cheap_plant_activity_costs_Bus_C_0_0)
+10 flow(cheap_plant_activity_costs_Bus_C_0_1)
+9.8039215686274499 flow(cheap_plant_activity_costs_Bus_C_1_2)
+9.8039215686274499 flow(cheap_plant_activity_costs_Bus_C_1_3)
+9.6116878123798539 flow(cheap_plant_activity_costs_Bus_C_2_4)
+9.6116878123798539 flow(cheap_plant_activity_costs_Bus_C_2_5)

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

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_0_0)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
-1 flow(cheap_plant_activity_costs_Bus_C_0_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_0_1)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
-1 flow(cheap_plant_activity_costs_Bus_C_0_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_1_2)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
-1 flow(cheap_plant_activity_costs_Bus_C_1_2)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_1_3)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
-1 flow(cheap_plant_activity_costs_Bus_C_1_3)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_2_4)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
-1 flow(cheap_plant_activity_costs_Bus_C_2_4)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_activity_costs_Bus_C_2_5)_:
+5 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
-1 flow(cheap_plant_activity_costs_Bus_C_2_5)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_0_0)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
+1 flow(cheap_plant_activity_costs_Bus_C_0_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_0_1)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
+1 flow(cheap_plant_activity_costs_Bus_C_0_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_1_2)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
+1 flow(cheap_plant_activity_costs_Bus_C_1_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_1_3)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
+1 flow(cheap_plant_activity_costs_Bus_C_1_3)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_2_4)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
+1 flow(cheap_plant_activity_costs_Bus_C_2_4)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_activity_costs_Bus_C_2_5)_:
-10 NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
+1 flow(cheap_plant_activity_costs_Bus_C_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(cheap_plant_activity_costs_Bus_C_0_0) <= 10
   0 <= flow(cheap_plant_activity_costs_Bus_C_0_1) <= 10
   0 <= flow(cheap_plant_activity_costs_Bus_C_1_2) <= 10
   0 <= flow(cheap_plant_activity_costs_Bus_C_1_3) <= 10
   0 <= flow(cheap_plant_activity_costs_Bus_C_2_4) <= 10
   0 <= flow(cheap_plant_activity_costs_Bus_C_2_5) <= 10
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5) <= 1
binary
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_0)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_1)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_2)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_3)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_4)
  NonConvexFlowBlock_status(cheap_plant_activity_costs_Bus_C_5)
end
