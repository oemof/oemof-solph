\* Source Pyomo model name=Model *\

min 
objective:
+611.56718125290342 InvestmentFlowBlock_invest(electricityBus_excess_0)
+599.57566789500333 InvestmentFlowBlock_invest(electricityBus_excess_1)
+587.8192822500032 InvestmentFlowBlock_invest(electricityBus_excess_2)
+25 flow(electricityBus_excess_0_0)
+25 flow(electricityBus_excess_0_1)
+24.509803921568626 flow(electricityBus_excess_1_2)
+24.509803921568626 flow(electricityBus_excess_1_3)
+24.029219530949632 flow(electricityBus_excess_2_4)
+24.029219530949632 flow(electricityBus_excess_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_excess_0_0)
= -12000000

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_excess_0_1)
= -16000000

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_excess_1_2)
= -14000000

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_excess_1_3)
= -18000000

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_excess_2_4)
= -18000000

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_excess_2_5)
= -18000000

c_e_InvestmentFlowBlock_total_rule(electricityBus_excess_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_excess_0)
+1 InvestmentFlowBlock_total(electricityBus_excess_0)
= 50

c_e_InvestmentFlowBlock_total_rule(electricityBus_excess_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_excess_1)
+1 InvestmentFlowBlock_old(electricityBus_excess_1)
-1 InvestmentFlowBlock_total(electricityBus_excess_0)
+1 InvestmentFlowBlock_total(electricityBus_excess_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_excess_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_excess_2)
+1 InvestmentFlowBlock_old(electricityBus_excess_2)
-1 InvestmentFlowBlock_total(electricityBus_excess_1)
+1 InvestmentFlowBlock_total(electricityBus_excess_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_excess_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_excess_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_excess_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_excess_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_excess_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_excess_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_excess_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_excess_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_excess_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_excess_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_excess_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_excess_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_excess_0)_:
+1 InvestmentFlowBlock_old(electricityBus_excess_0)
-1 InvestmentFlowBlock_old_end(electricityBus_excess_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_excess_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_excess_1)_:
+1 InvestmentFlowBlock_old(electricityBus_excess_1)
-1 InvestmentFlowBlock_old_end(electricityBus_excess_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_excess_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_excess_2)_:
+1 InvestmentFlowBlock_old(electricityBus_excess_2)
-1 InvestmentFlowBlock_old_end(electricityBus_excess_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_excess_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_0_0)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_0)
+1 flow(electricityBus_excess_0_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_0_1)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_0)
+1 flow(electricityBus_excess_0_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_1_2)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_1)
+1 flow(electricityBus_excess_1_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_1_3)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_1)
+1 flow(electricityBus_excess_1_3)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_2_4)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_2)
+1 flow(electricityBus_excess_2_4)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_excess_2_5)_:
-0.80000000000000004 InvestmentFlowBlock_total(electricityBus_excess_2)
+1 flow(electricityBus_excess_2_5)
<= 0

c_u_InvestmentFlowBlock_full_load_time_max(electricityBus_excess)_:
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_excess_0)
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_excess_1)
-2.2999999999999998 InvestmentFlowBlock_total(electricityBus_excess_2)
+1 flow(electricityBus_excess_0_0)
+1 flow(electricityBus_excess_0_1)
+1 flow(electricityBus_excess_1_2)
+1 flow(electricityBus_excess_1_3)
+1 flow(electricityBus_excess_2_4)
+1 flow(electricityBus_excess_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_excess_0_0) <= +inf
   0 <= flow(electricityBus_excess_0_1) <= +inf
   0 <= flow(electricityBus_excess_1_2) <= +inf
   0 <= flow(electricityBus_excess_1_3) <= +inf
   0 <= flow(electricityBus_excess_2_4) <= +inf
   0 <= flow(electricityBus_excess_2_5) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_excess_0) <= 1000000
   0 <= InvestmentFlowBlock_invest(electricityBus_excess_1) <= 1000000
   0 <= InvestmentFlowBlock_invest(electricityBus_excess_2) <= 1000000
   0 <= InvestmentFlowBlock_total(electricityBus_excess_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_excess_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_excess_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_excess_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_excess_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_excess_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_excess_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_excess_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_excess_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_excess_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_excess_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_excess_2) <= +inf
end