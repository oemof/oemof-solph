\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(bus_diesel_0_0)_:
+1 flow(bus_diesel_diesel_genset_0_0)
= 0

c_e_BusBlock_balance(bus_diesel_0_1)_:
+1 flow(bus_diesel_diesel_genset_0_1)
= 0

c_e_BusBlock_balance(bus_diesel_0_2)_:
+1 flow(bus_diesel_diesel_genset_0_2)
= 0

c_e_BusBlock_balance(bus_electricity_0_0)_:
+1 flow(diesel_genset_bus_electricity_0_0)
= 0

c_e_BusBlock_balance(bus_electricity_0_1)_:
+1 flow(diesel_genset_bus_electricity_0_1)
= 0

c_e_BusBlock_balance(bus_electricity_0_2)_:
+1 flow(diesel_genset_bus_electricity_0_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_0)_:
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_1)_:
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(diesel_genset_bus_electricity_2)_:
+1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
-100 NonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_0_0)_:
-1 flow(diesel_genset_bus_electricity_0_0)
+0.2 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
<= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_0_1)_:
-1 flow(diesel_genset_bus_electricity_0_1)
+0.2 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
<= 0

c_u_NonConvexFlowBlock_min(diesel_genset_bus_electricity_0_2)_:
-1 flow(diesel_genset_bus_electricity_0_2)
+0.2 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_0_0)_:
+1 flow(diesel_genset_bus_electricity_0_0)
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_0_1)_:
+1 flow(diesel_genset_bus_electricity_0_1)
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
<= 0

c_u_NonConvexFlowBlock_max(diesel_genset_bus_electricity_0_2)_:
+1 flow(diesel_genset_bus_electricity_0_2)
-1 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
<= 0

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_0)_:
-1 flow(bus_diesel_diesel_genset_0_0)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_0)
+0.08928571428571486 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
= 0

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_1)_:
-1 flow(bus_diesel_diesel_genset_0_1)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_1)
+0.08928571428571486 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
= 0

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_2)_:
-1 flow(bus_diesel_diesel_genset_0_2)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_2)
+0.08928571428571486 NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(bus_diesel_diesel_genset_0_0) <= +inf
   0 <= flow(bus_diesel_diesel_genset_0_1) <= +inf
   0 <= flow(bus_diesel_diesel_genset_0_2) <= +inf
   0 <= flow(diesel_genset_bus_electricity_0_0) <= 100
   0 <= flow(diesel_genset_bus_electricity_0_1) <= 100
   0 <= flow(diesel_genset_bus_electricity_0_2) <= 100
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1) <= +inf
   0 <= NonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2) <= +inf
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_0) <= 1
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_1) <= 1
   0 <= NonConvexFlowBlock_status(diesel_genset_bus_electricity_2) <= 1
binary
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
  NonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
end
