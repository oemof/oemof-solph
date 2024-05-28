\* Source Pyomo model name=Model *\

min 
objective:
+100 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)

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

c_l_InvestNonConvexFlowBlock_minimum_investment(diesel_genset_bus_electricity_0)_:
+1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
>= 0

c_u_InvestNonConvexFlowBlock_maximum_investment(diesel_genset_bus_electricity_0)_:
+1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
<= 1234

c_u_InvestNonConvexFlowBlock_min(diesel_genset_bus_electricity_0_0)_:
-1 flow(diesel_genset_bus_electricity_0_0)
+0.2 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
<= 0

c_u_InvestNonConvexFlowBlock_min(diesel_genset_bus_electricity_0_1)_:
-1 flow(diesel_genset_bus_electricity_0_1)
+0.2 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
<= 0

c_u_InvestNonConvexFlowBlock_min(diesel_genset_bus_electricity_0_2)_:
-1 flow(diesel_genset_bus_electricity_0_2)
+0.2 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
<= 0

c_u_InvestNonConvexFlowBlock_max(diesel_genset_bus_electricity_0_0)_:
+1 flow(diesel_genset_bus_electricity_0_0)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
<= 0

c_u_InvestNonConvexFlowBlock_max(diesel_genset_bus_electricity_0_1)_:
+1 flow(diesel_genset_bus_electricity_0_1)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
<= 0

c_u_InvestNonConvexFlowBlock_max(diesel_genset_bus_electricity_0_2)_:
+1 flow(diesel_genset_bus_electricity_0_2)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(diesel_genset_bus_electricity_0_0)_:
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
-1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(diesel_genset_bus_electricity_0_1)_:
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
-1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(diesel_genset_bus_electricity_0_2)_:
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
-1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(diesel_genset_bus_electricity_0_0)_:
-1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(diesel_genset_bus_electricity_0_1)_:
-1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(diesel_genset_bus_electricity_0_2)_:
-1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
+1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_three(diesel_genset_bus_electricity_0_0)_:
+1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
+1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
<= 1234

c_u_InvestNonConvexFlowBlock_invest_nc_three(diesel_genset_bus_electricity_0_1)_:
+1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
+1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
<= 1234

c_u_InvestNonConvexFlowBlock_invest_nc_three(diesel_genset_bus_electricity_0_2)_:
+1 InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0)
-1 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
+1234 InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
<= 1234

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_0)_:
-1 flow(bus_diesel_diesel_genset_0_0)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_0)
+0.08928571428571486 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0)
= 0

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_1)_:
-1 flow(bus_diesel_diesel_genset_0_1)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_1)
+0.08928571428571486 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1)
= 0

c_e_OffsetConverterBlock_relation(diesel_genset_bus_electricity_bus_diesel_0_2)_:
-1 flow(bus_diesel_diesel_genset_0_2)
+2.410714285714285 flow(diesel_genset_bus_electricity_0_2)
+0.08928571428571486 InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2)
= 0

bounds
   0 <= InvestNonConvexFlowBlock_invest(diesel_genset_bus_electricity_0) <= 1234
   0 <= flow(bus_diesel_diesel_genset_0_0) <= +inf
   0 <= flow(bus_diesel_diesel_genset_0_1) <= +inf
   0 <= flow(bus_diesel_diesel_genset_0_2) <= +inf
   0 <= flow(diesel_genset_bus_electricity_0_0) <= +inf
   0 <= flow(diesel_genset_bus_electricity_0_1) <= +inf
   0 <= flow(diesel_genset_bus_electricity_0_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_0) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_1) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(diesel_genset_bus_electricity_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_0) <= 1
   0 <= InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_1) <= 1
   0 <= InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_2) <= 1
binary
  InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_0)
  InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_1)
  InvestNonConvexFlowBlock_status(diesel_genset_bus_electricity_2)
end
