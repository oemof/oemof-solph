\* Source Pyomo model name=Model *\

min
objective:
+10 flow(cheap_plant_maximum_startups_Bus_C_0)
+10 flow(cheap_plant_maximum_startups_Bus_C_1)
+10 flow(cheap_plant_maximum_startups_Bus_C_2)

s.t.

c_e_Bus_balance(Bus_C_0)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_0)
= 0

c_e_Bus_balance(Bus_C_1)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_1)
= 0

c_e_Bus_balance(Bus_C_2)_:
+1 flow(cheap_plant_maximum_startups_Bus_C_2)
= 0

c_u_NonConvexFlow_min(cheap_plant_maximum_startups_Bus_C_0)_:
+5 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0)
-1 flow(cheap_plant_maximum_startups_Bus_C_0)
<= 0

c_u_NonConvexFlow_min(cheap_plant_maximum_startups_Bus_C_1)_:
+5 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1)
-1 flow(cheap_plant_maximum_startups_Bus_C_1)
<= 0

c_u_NonConvexFlow_min(cheap_plant_maximum_startups_Bus_C_2)_:
+5 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_2)
-1 flow(cheap_plant_maximum_startups_Bus_C_2)
<= 0

c_u_NonConvexFlow_max(cheap_plant_maximum_startups_Bus_C_0)_:
-10 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0)
+1 flow(cheap_plant_maximum_startups_Bus_C_0)
<= 0

c_u_NonConvexFlow_max(cheap_plant_maximum_startups_Bus_C_1)_:
-10 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1)
+1 flow(cheap_plant_maximum_startups_Bus_C_1)
<= 0

c_u_NonConvexFlow_max(cheap_plant_maximum_startups_Bus_C_2)_:
-10 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_2)
+1 flow(cheap_plant_maximum_startups_Bus_C_2)
<= 0

c_u_NonConvexFlow_startup_constr(cheap_plant_maximum_startups_Bus_C_0)_:
-1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0)
<= 0

c_u_NonConvexFlow_startup_constr(cheap_plant_maximum_startups_Bus_C_1)_:
-1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_1)
-1 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1)
<= 0

c_u_NonConvexFlow_startup_constr(cheap_plant_maximum_startups_Bus_C_2)_:
-1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_2)
-1 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1)
+1 NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_2)
<= 0

c_u_NonConvexFlow_max_startup_constr(cheap_plant_maximum_startups_Bus_C)_:
+1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_0)
+1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_1)
+1 NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_2)
<= 2

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(cheap_plant_maximum_startups_Bus_C_0) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_1) <= 10
   0 <= flow(cheap_plant_maximum_startups_Bus_C_2) <= 10
   0 <= NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0) <= 1
   0 <= NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1) <= 1
   0 <= NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_2) <= 1
   0 <= NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_0) <= 1
   0 <= NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_1) <= 1
   0 <= NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_2) <= 1
binary
  NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_0)
  NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_1)
  NonConvexFlow_status(cheap_plant_maximum_startups_Bus_C_2)
  NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_0)
  NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_1)
  NonConvexFlow_startup(cheap_plant_maximum_startups_Bus_C_2)
end
