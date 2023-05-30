\* Source Pyomo model name=Model *\

min 
objective:
+8 flow(b1_b2_0_0)
+8 flow(b1_b2_0_1)
+8 flow(b1_b2_0_2)
+0.75 InvestNonConvexFlowBlock_invest(b1_b2_0)

s.t.

c_e_BusBlock_balance(b2_0_0)_:
+1 flow(b1_b2_0_0)
-1 flow(b2_b1_0_0)
= 0

c_e_BusBlock_balance(b2_0_1)_:
+1 flow(b1_b2_0_1)
-1 flow(b2_b1_0_1)
= 0

c_e_BusBlock_balance(b2_0_2)_:
+1 flow(b1_b2_0_2)
-1 flow(b2_b1_0_2)
= 0

c_e_BusBlock_balance(b1_0_0)_:
-1 flow(b1_b2_0_0)
+1 flow(b2_b1_0_0)
= 0

c_e_BusBlock_balance(b1_0_1)_:
-1 flow(b1_b2_0_1)
+1 flow(b2_b1_0_1)
= 0

c_e_BusBlock_balance(b1_0_2)_:
-1 flow(b1_b2_0_2)
+1 flow(b2_b1_0_2)
= 0

c_l_InvestNonConvexFlowBlock_minimum_investment(b1_b2_0)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2_0)
>= 0

c_u_InvestNonConvexFlowBlock_maximum_investment(b1_b2_0)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2_0)
<= 10

c_u_InvestNonConvexFlowBlock_min(b1_b2_0_0)_:
-1 flow(b1_b2_0_0)
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_min(b1_b2_0_1)_:
-1 flow(b1_b2_0_1)
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_min(b1_b2_0_2)_:
-1 flow(b1_b2_0_2)
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_0_0)_:
+1 flow(b1_b2_0_0)
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_0_1)_:
+1 flow(b1_b2_0_1)
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_0_2)_:
+1 flow(b1_b2_0_2)
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(b1_b2_0_0)_:
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
-10 InvestNonConvexFlowBlock_status(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(b1_b2_0_1)_:
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
-10 InvestNonConvexFlowBlock_status(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_one(b1_b2_0_2)_:
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
-10 InvestNonConvexFlowBlock_status(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(b1_b2_0_0)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2_0)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(b1_b2_0_1)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2_0)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_two(b1_b2_0_2)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2_0)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_invest_nc_three(b1_b2_0_0)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2_0)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
+10 InvestNonConvexFlowBlock_status(b1_b2_0)
<= 10

c_u_InvestNonConvexFlowBlock_invest_nc_three(b1_b2_0_1)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2_0)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
+10 InvestNonConvexFlowBlock_status(b1_b2_1)
<= 10

c_u_InvestNonConvexFlowBlock_invest_nc_three(b1_b2_0_2)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2_0)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
+10 InvestNonConvexFlowBlock_status(b1_b2_2)
<= 10

bounds
   0 <= flow(b1_b2_0_0) <= +inf
   0 <= flow(b1_b2_0_1) <= +inf
   0 <= flow(b1_b2_0_2) <= +inf
   0 <= InvestNonConvexFlowBlock_invest(b1_b2_0) <= 10
   0 <= flow(b2_b1_0_0) <= +inf
   0 <= flow(b2_b1_0_1) <= +inf
   0 <= flow(b2_b1_0_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_0) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_1) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status(b1_b2_0) <= 1
   0 <= InvestNonConvexFlowBlock_status(b1_b2_1) <= 1
   0 <= InvestNonConvexFlowBlock_status(b1_b2_2) <= 1
binary
  InvestNonConvexFlowBlock_status(b1_b2_0)
  InvestNonConvexFlowBlock_status(b1_b2_1)
  InvestNonConvexFlowBlock_status(b1_b2_2)
end
