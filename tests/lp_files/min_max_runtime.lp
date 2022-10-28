\* Source Pyomo model name=Model *\

min
objective:
+7 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
+7 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
+7 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
+5 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
+5 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
+5 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
+10 flow(cheap_plant_min_down_constraints_Bus_T_0)
+10 flow(cheap_plant_min_down_constraints_Bus_T_1)
+10 flow(cheap_plant_min_down_constraints_Bus_T_2)

s.t.

c_e_BusBlock_balance(Bus_T_0)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_0)
= 0

c_e_BusBlock_balance(Bus_T_1)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_1)
= 0

c_e_BusBlock_balance(Bus_T_2)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_0)_:
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_1)_:
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_2)_:
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_0)_:
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
-1 flow(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_1)_:
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
-1 flow(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_2)_:
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
-1 flow(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_0)_:
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
+1 flow(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_1)_:
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
+1 flow(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_2)_:
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
+1 flow(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
<= 2

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
<= -2

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_e_NonConvexFlowBlock_min_uptime_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
= 2

c_e_NonConvexFlowBlock_min_uptime_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
= 2

c_e_NonConvexFlowBlock_min_uptime_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
= 2

c_e_NonConvexFlowBlock_min_downtime_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
= 2

c_e_NonConvexFlowBlock_min_downtime_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
= 2

c_e_NonConvexFlowBlock_min_downtime_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
= 2

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_0) <= 10
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_1) <= 10
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_2) <= 10
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1) <= 1
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2) <= +inf
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2) <= 1
binary
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_0)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_1)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
end
