\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(bus_diesel_0)_:
+1 flow(bus_diesel_diesel_genset_0)
= 0

c_e_BusBlock_balance(bus_diesel_1)_:
+1 flow(bus_diesel_diesel_genset_1)
= 0

c_e_BusBlock_balance(bus_diesel_2)_:
+1 flow(bus_diesel_diesel_genset_2)
= 0

c_e_BusBlock_balance(bus_electricity_0)_:
+1 flow(diesel_genset_bus_electricity_0)
= 0

c_e_BusBlock_balance(bus_electricity_1)_:
+1 flow(diesel_genset_bus_electricity_1)
= 0

c_e_BusBlock_balance(bus_electricity_2)_:
+1 flow(diesel_genset_bus_electricity_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_0)_:
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_1)_:
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_2)_:
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_0)_:
+0.20000000000000001 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
-1 flow(diesel_genset_bus_electricity_0)
<= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_1)_:
+0.20000000000000001 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
-1 flow(diesel_genset_bus_electricity_1)
<= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_2)_:
+0.20000000000000001 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
-1 flow(diesel_genset_bus_electricity_2)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_0)_:
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
+1 flow(diesel_genset_bus_electricity_0)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_1)_:
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
+1 flow(diesel_genset_bus_electricity_1)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_2)_:
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
+1 flow(diesel_genset_bus_electricity_2)
<= 0

c_e_OffsetTransformerBlock_relation(diesel_genset_0)_:
+2.5 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
-1 flow(bus_diesel_diesel_genset_0)
+0.5 flow(diesel_genset_bus_electricity_0)
= 0

c_e_OffsetTransformerBlock_relation(diesel_genset_1)_:
+2.5 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
-1 flow(bus_diesel_diesel_genset_1)
+0.5 flow(diesel_genset_bus_electricity_1)
= 0

c_e_OffsetTransformerBlock_relation(diesel_genset_2)_:
+2.5 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
-1 flow(bus_diesel_diesel_genset_2)
+0.5 flow(diesel_genset_bus_electricity_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_diesel_diesel_genset_0) <= +inf
   0 <= flow(bus_diesel_diesel_genset_1) <= +inf
   0 <= flow(bus_diesel_diesel_genset_2) <= +inf
   0 <= flow(diesel_genset_bus_electricity_0) <= 100
   0 <= flow(diesel_genset_bus_electricity_1) <= 100
   0 <= flow(diesel_genset_bus_electricity_2) <= 100
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_0) <= 1
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_1) <= 1
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_2) <= 1
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2) <= +inf
binary
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
end