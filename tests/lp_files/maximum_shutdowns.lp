\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(cheap_plant_maximum_shutdowns_Bus_C_0_0)
+10 flow(cheap_plant_maximum_shutdowns_Bus_C_0_1)
+10 flow(cheap_plant_maximum_shutdowns_Bus_C_0_2)

s.t.

c_e_BusBlock_balance(Bus_C_0_0)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_0)
= 0

c_e_BusBlock_balance(Bus_C_0_1)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_1)
= 0

c_e_BusBlock_balance(Bus_C_0_2)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_maximum_shutdowns_Bus_C_0)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_0)
-10 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_maximum_shutdowns_Bus_C_1)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_1)
-10 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_maximum_shutdowns_Bus_C_2)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_2)
-10 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_2)
= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_shutdowns_Bus_C_0_0)_:
-1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_0)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_shutdowns_Bus_C_0_1)_:
-1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_1)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_maximum_shutdowns_Bus_C_0_2)_:
-1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_2)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_shutdowns_Bus_C_0_0)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_0)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_shutdowns_Bus_C_0_1)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_1)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_maximum_shutdowns_Bus_C_0_2)_:
+1 flow(cheap_plant_maximum_shutdowns_Bus_C_0_2)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_maximum_shutdowns_Bus_C_0)_:
-1 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_0)
-1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_0)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_maximum_shutdowns_Bus_C_1)_:
+1 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_0)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_1)
-1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_1)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_maximum_shutdowns_Bus_C_2)_:
+1 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_1)
-1 NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_2)
-1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_2)
<= 0

c_u_NonConvexFlowBlock_max_shutdown_constr(cheap_plant_maximum_shutdowns_Bus_C)_:
+1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_0)
+1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_1)
+1 NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_2)
<= 2

bounds
   0 <= flow(cheap_plant_maximum_shutdowns_Bus_C_0_0) <= 10.0
   0 <= flow(cheap_plant_maximum_shutdowns_Bus_C_0_1) <= 10.0
   0 <= flow(cheap_plant_maximum_shutdowns_Bus_C_0_2) <= 10.0
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_0) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_1) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_maximum_shutdowns_Bus_C_2) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_2) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_0) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_1) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_2) <= 1
binary
  NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_0)
  NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_1)
  NonConvexFlowBlock_status(cheap_plant_maximum_shutdowns_Bus_C_2)
  NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_0)
  NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_1)
  NonConvexFlowBlock_shutdown(cheap_plant_maximum_shutdowns_Bus_C_2)
end
