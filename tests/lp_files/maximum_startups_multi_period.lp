\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(cheap_plant_maximum_startups_Bus_C_0_0)
+10 flow(cheap_plant_maximum_startups_Bus_C_0_1)
+9.8039215686274499 flow(cheap_plant_maximum_startups_Bus_C_1_2)
+9.8039215686274499 flow(cheap_plant_maximum_startups_Bus_C_1_3)
+9.6116878123798539 flow(cheap_plant_maximum_startups_Bus_C_2_4)
+9.6116878123798539 flow(cheap_plant_maximum_startups_Bus_C_2_5)

s.t.

c_e_BusBlock_balance(Bus_C_0_0)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_0_0)
= 0

c_e_BusBlock_balance(Bus_C_0_1)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_0_1)
= 0

c_e_BusBlock_balance(Bus_C_1_2)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_1_2)
= 0

c_e_BusBlock_balance(Bus_C_1_3)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_1_3)
= 0

c_e_BusBlock_balance(Bus_C_2_4)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_2_4)
= 0

c_e_BusBlock_balance(Bus_C_2_5)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_2_5)
= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_0_0)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0)
-1 flow(cheap_plant_maximum_startups_Bus_C_0_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_0_1)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1)
-1 flow(cheap_plant_maximum_startups_Bus_C_0_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_1_2)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2)
-1 flow(cheap_plant_maximum_startups_Bus_C_1_2)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_1_3)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3)
-1 flow(cheap_plant_maximum_startups_Bus_C_1_3)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_2_4)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4)
-1 flow(cheap_plant_maximum_startups_Bus_C_2_4)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_startups_Bus_C_2_5)_:
+5 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_5)
-1 flow(cheap_plant_maximum_startups_Bus_C_2_5)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_0_0)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0)
+1 flow(cheap_plant_maximum_startups_Bus_C_0_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_0_1)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1)
+1 flow(cheap_plant_maximum_startups_Bus_C_0_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_1_2)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2)
+1 flow(cheap_plant_maximum_startups_Bus_C_1_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_1_3)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3)
+1 flow(cheap_plant_maximum_startups_Bus_C_1_3)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_2_4)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4)
+1 flow(cheap_plant_maximum_startups_Bus_C_2_4)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_startups_Bus_C_2_5)_:
-10 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_5)
+1 flow(cheap_plant_maximum_startups_Bus_C_2_5)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_0)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_1)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_1)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_2)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_2)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_3)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_3)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_4)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_4)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_maximum_startups_Bus_C_5)_:
-1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_5)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4)
+1 NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_5)
<= 0

c_u_NonConvexFlowBlock_max_startup_constr(cheap_plant_maximum_startups_Bus_C)_:
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_1)
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_2)
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_3)
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_4)
+1 NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_5)
<= 2

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(cheap_plant_maximum_startups_Bus_C_0_0) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_0_1) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_1_2) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_1_3) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_2_4) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_2_5) <= 10
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_5) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_2) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_3) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_4) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_5) <= 1
binary
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_0)
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_1)
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_2)
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_3)
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_4)
  NonConvexFlowBlock_status(cheap_plant_maximum_startups_Bus_C_5)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_0)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_1)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_2)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_3)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_4)
  NonConvexFlowBlock_startup(cheap_plant_maximum_startups_Bus_C_5)
end
