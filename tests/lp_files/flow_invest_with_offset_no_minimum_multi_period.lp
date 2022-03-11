\* Source Pyomo model name=Model *\

min 
objective:
+611.56718125290342 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_0)
+599.57566789500333 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_1)
+587.8192822500032 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_2)
+34 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_0)
+33.333333333333329 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_1)
+32.679738562091501 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_2)
+25 flow(electricityBus_source_nonconvex_invest_0_0)
+25 flow(electricityBus_source_nonconvex_invest_0_1)
+24.509803921568626 flow(electricityBus_source_nonconvex_invest_1_2)
+24.509803921568626 flow(electricityBus_source_nonconvex_invest_1_3)
+24.029219530949632 flow(electricityBus_source_nonconvex_invest_2_4)
+24.029219530949632 flow(electricityBus_source_nonconvex_invest_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(electricityBus_source_nonconvex_invest_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(electricityBus_source_nonconvex_invest_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(electricityBus_source_nonconvex_invest_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(electricityBus_source_nonconvex_invest_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(electricityBus_source_nonconvex_invest_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(electricityBus_source_nonconvex_invest_2_5)
= 0

c_l_InvestmentFlowBlock_minimum_rule(electricityBus_source_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_0)
>= 0

c_l_InvestmentFlowBlock_minimum_rule(electricityBus_source_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_1)
>= 0

c_l_InvestmentFlowBlock_minimum_rule(electricityBus_source_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_2)
>= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_source_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_0)
-1234 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_source_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_1)
-1234 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_1)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_source_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_2)
-1234 InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_2)
<= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_source_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_0)
+1 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_source_nonconvex_invest_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_1)
+1 InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_1)
-1 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0)
+1 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_source_nonconvex_invest_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_2)
+1 InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_2)
-1 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1)
+1 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_source_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_source_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_source_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_source_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_source_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_source_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_source_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_0)
-1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_source_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_1)
-1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_source_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_2)
-1 InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_0_0)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0)
+1 flow(electricityBus_source_nonconvex_invest_0_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_0_1)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0)
+1 flow(electricityBus_source_nonconvex_invest_0_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_1_2)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1)
+1 flow(electricityBus_source_nonconvex_invest_1_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_1_3)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1)
+1 flow(electricityBus_source_nonconvex_invest_1_3)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_2_4)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_2)
+1 flow(electricityBus_source_nonconvex_invest_2_4)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_source_nonconvex_invest_2_5)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_2)
+1 flow(electricityBus_source_nonconvex_invest_2_5)
<= 0

c_u_InvestmentFlowBlock_summed_max(electricityBus_source_nonconvex_invest)_:
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0)
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1)
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_2)
+1 flow(electricityBus_source_nonconvex_invest_0_0)
+1 flow(electricityBus_source_nonconvex_invest_0_1)
+1 flow(electricityBus_source_nonconvex_invest_1_2)
+1 flow(electricityBus_source_nonconvex_invest_1_3)
+1 flow(electricityBus_source_nonconvex_invest_2_4)
+1 flow(electricityBus_source_nonconvex_invest_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_source_nonconvex_invest_0_0) <= +inf
   0 <= flow(electricityBus_source_nonconvex_invest_0_1) <= +inf
   0 <= flow(electricityBus_source_nonconvex_invest_1_2) <= +inf
   0 <= flow(electricityBus_source_nonconvex_invest_1_3) <= +inf
   0 <= flow(electricityBus_source_nonconvex_invest_2_4) <= +inf
   0 <= flow(electricityBus_source_nonconvex_invest_2_5) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_0) <= 1234
   0 <= InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_1) <= 1234
   0 <= InvestmentFlowBlock_invest(electricityBus_source_nonconvex_invest_2) <= 1234
   0 <= InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_source_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_source_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_source_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_source_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_0) <= 1
   0 <= InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_1) <= 1
   0 <= InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_2) <= 1
binary
  InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_0)
  InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_1)
  InvestmentFlowBlock_invest_status(electricityBus_source_nonconvex_invest_2)
end
