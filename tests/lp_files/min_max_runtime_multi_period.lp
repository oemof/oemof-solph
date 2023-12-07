\* Source Pyomo model name=Model *\

min 
objective:
+10 flow(cheap_plant_min_down_constraints_Bus_T_0_0)
+10 flow(cheap_plant_min_down_constraints_Bus_T_0_1)
+9.80392156862745 flow(cheap_plant_min_down_constraints_Bus_T_1_2)
+9.80392156862745 flow(cheap_plant_min_down_constraints_Bus_T_1_3)
+9.611687812379854 flow(cheap_plant_min_down_constraints_Bus_T_2_4)
+9.611687812379854 flow(cheap_plant_min_down_constraints_Bus_T_2_5)
+5 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
+5 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
+4.901960784313725 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
+4.901960784313725 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_3)
+4.805843906189927 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_4)
+4.805843906189927 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_5)
+7 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
+7 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
+6.862745098039215 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
+6.862745098039215 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_3)
+6.728181468665897 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_4)
+6.728181468665897 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_5)

s.t.

c_e_BusBlock_balance(Bus_T_0_0)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_0_0)
= 0

c_e_BusBlock_balance(Bus_T_0_1)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_0_1)
= 0

c_e_BusBlock_balance(Bus_T_1_2)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_1_2)
= 0

c_e_BusBlock_balance(Bus_T_1_3)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_1_3)
= 0

c_e_BusBlock_balance(Bus_T_2_4)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_2_4)
= 0

c_e_BusBlock_balance(Bus_T_2_5)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_2_5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_0)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
= 10

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_1)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
= 10

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_2)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_3)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_3)
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_4)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_4)
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(cheap_plant_min_down_constraints_Bus_T_5)_:
+1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_5)
-10 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_0_0)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_0_0)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_0_1)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_0_1)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_1_2)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_1_2)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_1_3)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_1_3)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_3)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_2_4)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_2_4)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_4)
<= 0

c_u_NonConvexFlowBlock_min(cheap_plant_min_down_constraints_Bus_T_2_5)_:
-1 flow(cheap_plant_min_down_constraints_Bus_T_2_5)
+0.5 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_5)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_0_0)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_0_0)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_0_1)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_0_1)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_1_2)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_1_2)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_1_3)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_1_3)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_3)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_2_4)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_2_4)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_4)
<= 0

c_u_NonConvexFlowBlock_max(cheap_plant_min_down_constraints_Bus_T_2_5)_:
+1 flow(cheap_plant_min_down_constraints_Bus_T_2_5)
-1 NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_5)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
<= 1

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_3)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_3)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_4)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_4)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
<= 0

c_u_NonConvexFlowBlock_startup_constr(cheap_plant_min_down_constraints_Bus_T_5)_:
-1 NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_5)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_0)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_1)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_2)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
<= -1

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_3)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_3)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_4)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_4)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
<= 0

c_u_NonConvexFlowBlock_shutdown_constr(cheap_plant_min_down_constraints_Bus_T_5)_:
-1 NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_5)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
<= 0

c_u_NonConvexFlowBlock_min_uptime_constr(cheap_plant_min_down_constraints_Bus_T_3)_:
-2 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
<= 0

c_u_NonConvexFlowBlock_min_uptime_constr(cheap_plant_min_down_constraints_Bus_T_4)_:
-2 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
-1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
<= 0

c_u_NonConvexFlowBlock_min_downtime_constr(cheap_plant_min_down_constraints_Bus_T_3)_:
+4 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
-3 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
<= 4

c_u_NonConvexFlowBlock_min_downtime_constr(cheap_plant_min_down_constraints_Bus_T_4)_:
+4 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
-3 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
+1 NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
<= 4

bounds
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_0_0) <= 10.0
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_0_1) <= 10.0
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_1_2) <= 10.0
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_1_3) <= 10.0
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_2_4) <= 10.0
   0 <= flow(cheap_plant_min_down_constraints_Bus_T_2_5) <= 10.0
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_3) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_4) <= 1
   0 <= NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_5) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_3) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_4) <= 1
   0 <= NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_5) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_2) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_3) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_4) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4) <= 1
   0 <= NonConvexFlowBlock_status_nominal(cheap_plant_min_down_constraints_Bus_T_5) <= +inf
   0 <= NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5) <= 1
binary
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_0)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_1)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_2)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_3)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_4)
  NonConvexFlowBlock_startup(cheap_plant_min_down_constraints_Bus_T_5)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_0)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_1)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_2)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_3)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_4)
  NonConvexFlowBlock_shutdown(cheap_plant_min_down_constraints_Bus_T_5)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_2)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_3)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_4)
  NonConvexFlowBlock_status(cheap_plant_min_down_constraints_Bus_T_5)
end
