\* Source Pyomo model name=Model *\

min
objective:
+0.75 InvestNonConvexFlowBlock_invest(b1_b2)
+8 flow(b1_b2_0)
+8 flow(b1_b2_1)
+8 flow(b1_b2_2)

s.t.

c_e_BusBlock_balance(b1_0)_:
-1 flow(b1_b2_0)
+1 flow(b2_b1_0)
= 0

c_e_BusBlock_balance(b1_1)_:
-1 flow(b1_b2_1)
+1 flow(b2_b1_1)
= 0

c_e_BusBlock_balance(b1_2)_:
-1 flow(b1_b2_2)
+1 flow(b2_b1_2)
= 0

c_e_BusBlock_balance(b2_0)_:
+1 flow(b1_b2_0)
-1 flow(b2_b1_0)
= 0

c_e_BusBlock_balance(b2_1)_:
+1 flow(b1_b2_1)
-1 flow(b2_b1_1)
= 0

c_e_BusBlock_balance(b2_2)_:
+1 flow(b1_b2_2)
-1 flow(b2_b1_2)
= 0

c_l_InvestNonConvexFlowBlock_minimum_rule(b1_b2)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2)
>= 0

c_u_InvestNonConvexFlowBlock_maximum_rule(b1_b2)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2)
<= 10

c_u_InvestNonConvexFlowBlock_min(b1_b2_0)_:
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
-1 flow(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_min(b1_b2_1)_:
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
-1 flow(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_min(b1_b2_2)_:
+0.25 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
-1 flow(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_0)_:
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
+1 flow(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_1)_:
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
+1 flow(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_max(b1_b2_2)_:
-0.5 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
+1 flow(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_one(b1_b2_0)_:
-10 InvestNonConvexFlowBlock_status(b1_b2_0)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_one(b1_b2_1)_:
-10 InvestNonConvexFlowBlock_status(b1_b2_1)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_one(b1_b2_2)_:
-10 InvestNonConvexFlowBlock_status(b1_b2_2)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_two(b1_b2_0)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_two(b1_b2_1)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_two(b1_b2_2)_:
-1 InvestNonConvexFlowBlock_invest(b1_b2)
+1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 0

c_u_InvestNonConvexFlowBlock_linearization_three(b1_b2_0)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2)
+10 InvestNonConvexFlowBlock_status(b1_b2_0)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_0)
<= 10

c_u_InvestNonConvexFlowBlock_linearization_three(b1_b2_1)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2)
+10 InvestNonConvexFlowBlock_status(b1_b2_1)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_1)
<= 10

c_u_InvestNonConvexFlowBlock_linearization_three(b1_b2_2)_:
+1 InvestNonConvexFlowBlock_invest(b1_b2)
+10 InvestNonConvexFlowBlock_status(b1_b2_2)
-1 InvestNonConvexFlowBlock_status_nominal(b1_b2_2)
<= 10

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(b1_b2_0) <= +inf
   0 <= flow(b1_b2_1) <= +inf
   0 <= flow(b1_b2_2) <= +inf
   0 <= flow(b2_b1_0) <= +inf
   0 <= flow(b2_b1_1) <= +inf
   0 <= flow(b2_b1_2) <= +inf
   0 <= InvestNonConvexFlowBlock_status(b1_b2_0) <= 1
   0 <= InvestNonConvexFlowBlock_status(b1_b2_1) <= 1
   0 <= InvestNonConvexFlowBlock_status(b1_b2_2) <= 1
   0 <= InvestNonConvexFlowBlock_invest(b1_b2) <= 10
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_0) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_1) <= +inf
   0 <= InvestNonConvexFlowBlock_status_nominal(b1_b2_2) <= +inf
binary
  InvestNonConvexFlowBlock_status(b1_b2_0)
  InvestNonConvexFlowBlock_status(b1_b2_1)
  InvestNonConvexFlowBlock_status(b1_b2_2)
end
