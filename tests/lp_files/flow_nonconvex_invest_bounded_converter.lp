\* Source Pyomo model name=Model *\

min 
objective:
+25 flow(converter_nonconvex_invest_electricityBus_0)
+25 flow(converter_nonconvex_invest_electricityBus_1)
+25 flow(converter_nonconvex_invest_electricityBus_2)
+500 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(converter_nonconvex_invest_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(converter_nonconvex_invest_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(converter_nonconvex_invest_electricityBus_2)
= 0

c_e_BusBlock_balance(fuelBus_0)_:
+1 flow(fuelBus_converter_nonconvex_invest_0)
= 0

c_e_BusBlock_balance(fuelBus_1)_:
+1 flow(fuelBus_converter_nonconvex_invest_1)
= 0

c_e_BusBlock_balance(fuelBus_2)_:
+1 flow(fuelBus_converter_nonconvex_invest_2)
= 0

c_e_ConverterBlock_relation(converter_nonconvex_invest_fuelBus_electricityBus_0)_:
+0.5 flow(fuelBus_converter_nonconvex_invest_0)
-1 flow(converter_nonconvex_invest_electricityBus_0)
= 0

c_e_ConverterBlock_relation(converter_nonconvex_invest_fuelBus_electricityBus_1)_:
+0.5 flow(fuelBus_converter_nonconvex_invest_1)
-1 flow(converter_nonconvex_invest_electricityBus_1)
= 0

c_e_ConverterBlock_relation(converter_nonconvex_invest_fuelBus_electricityBus_2)_:
+0.5 flow(fuelBus_converter_nonconvex_invest_2)
-1 flow(converter_nonconvex_invest_electricityBus_2)
= 0

c_l_InvestNonConvexFlowBlock_minimum_investment(converter_nonconvex_invest_electricityBus_0)_:
+1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
>= 0

c_u_InvestNonConvexFlowBlock_maximum_investment(converter_nonconvex_invest_electricityBus_0)_:
+1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
<= 1234

c_u_InvestNonConvexFlowBlock_min(converter_nonconvex_invest_electricityBus_0)_:
-1 flow(converter_nonconvex_invest_electricityBus_0)
+0.25 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestNonConvexFlowBlock_min(converter_nonconvex_invest_electricityBus_1)_:
-1 flow(converter_nonconvex_invest_electricityBus_1)
+0.25 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestNonConvexFlowBlock_min(converter_nonconvex_invest_electricityBus_2)_:
-1 flow(converter_nonconvex_invest_electricityBus_2)
+0.25 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestNonConvexFlowBlock_max(converter_nonconvex_invest_electricityBus_0)_:
+1 flow(converter_nonconvex_invest_electricityBus_0)
-0.5 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestNonConvexFlowBlock_max(converter_nonconvex_invest_electricityBus_1)_:
+1 flow(converter_nonconvex_invest_electricityBus_1)
-0.5 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestNonConvexFlowBlock_max(converter_nonconvex_invest_electricityBus_2)_:
+1 flow(converter_nonconvex_invest_electricityBus_2)
-0.5 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(converter_nonconvex_invest_electricityBus_0_0)_:
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0)
-1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(converter_nonconvex_invest_electricityBus_0_1)_:
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1)
-1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(converter_nonconvex_invest_electricityBus_0_2)_:
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2)
-1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(converter_nonconvex_invest_electricityBus_0_0)_:
-1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(converter_nonconvex_invest_electricityBus_0_1)_:
-1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(converter_nonconvex_invest_electricityBus_0_2)_:
-1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
+1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_three(converter_nonconvex_invest_electricityBus_0_0)_:
+1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
-1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0)
+1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_0)
<= 1234

c_u_InvestNonConvexFlowBlock_invest_nc_three(converter_nonconvex_invest_electricityBus_0_1)_:
+1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
-1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1)
+1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_1)
<= 1234

c_u_InvestNonConvexFlowBlock_invest_nc_three(converter_nonconvex_invest_electricityBus_0_2)_:
+1 InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0)
-1 InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2)
+1234 InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_2)
<= 1234

bounds
   0 <= flow(fuelBus_converter_nonconvex_invest_0) <= +inf
   0 <= flow(fuelBus_converter_nonconvex_invest_1) <= +inf
   0 <= flow(fuelBus_converter_nonconvex_invest_2) <= +inf
   0 <= flow(converter_nonconvex_invest_electricityBus_0) <= +inf
   0 <= flow(converter_nonconvex_invest_electricityBus_1) <= +inf
   0 <= flow(converter_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestNonConvexFlowBlock_invest(converter_nonconvex_invest_electricityBus_0) <= 1234
   0 <= InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_0) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_1) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(converter_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_0) <= 1
   0 <= InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_1) <= 1
   0 <= InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_2) <= 1
binary
  InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_0)
  InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_1)
  InvestNonConvexFlowBlock_status(converter_nonconvex_invest_electricityBus_2)
end
