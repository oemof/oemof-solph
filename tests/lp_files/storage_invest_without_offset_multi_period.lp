\* Source Pyomo model name=Model *\

min 
objective:
+56 flow(electricityBus_storage_non_convex_0_0)
+56 flow(electricityBus_storage_non_convex_0_1)
+54.90196078431372 flow(electricityBus_storage_non_convex_1_2)
+54.90196078431372 flow(electricityBus_storage_non_convex_1_3)
+53.82545174932718 flow(electricityBus_storage_non_convex_2_4)
+53.82545174932718 flow(electricityBus_storage_non_convex_2_5)
+24 flow(storage_non_convex_electricityBus_0_0)
+24 flow(storage_non_convex_electricityBus_0_1)
+23.52941176470588 flow(storage_non_convex_electricityBus_1_2)
+23.52941176470588 flow(storage_non_convex_electricityBus_1_3)
+23.06805074971165 flow(storage_non_convex_electricityBus_2_4)
+23.06805074971165 flow(storage_non_convex_electricityBus_2_5)
+24.868005934029988 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+16.413989016710378 GenericInvestmentStorageBlock_invest(storage_non_convex_1)
+8.125737136985347 GenericInvestmentStorageBlock_invest(storage_non_convex_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage_non_convex_0_0)
+1 flow(storage_non_convex_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage_non_convex_0_1)
+1 flow(storage_non_convex_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage_non_convex_1_2)
+1 flow(storage_non_convex_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage_non_convex_1_3)
+1 flow(storage_non_convex_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage_non_convex_2_4)
+1 flow(storage_non_convex_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage_non_convex_2_5)
+1 flow(storage_non_convex_electricityBus_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
-1 InvestmentFlowBlock_invest(electricityBus_storage_non_convex_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage_non_convex_1)_:
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_1)
-1 InvestmentFlowBlock_invest(electricityBus_storage_non_convex_1)
+1 InvestmentFlowBlock_old(electricityBus_storage_non_convex_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage_non_convex_2)_:
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_1)
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_2)
-1 InvestmentFlowBlock_invest(electricityBus_storage_non_convex_2)
+1 InvestmentFlowBlock_old(electricityBus_storage_non_convex_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_non_convex_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage_non_convex_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_non_convex_electricityBus_1)_:
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_1)
-1 InvestmentFlowBlock_invest(storage_non_convex_electricityBus_1)
+1 InvestmentFlowBlock_old(storage_non_convex_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_non_convex_electricityBus_2)_:
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_1)
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_2)
-1 InvestmentFlowBlock_invest(storage_non_convex_electricityBus_2)
+1 InvestmentFlowBlock_old(storage_non_convex_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage_non_convex_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage_non_convex_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage_non_convex_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_non_convex_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_non_convex_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_non_convex_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage_non_convex_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage_non_convex_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage_non_convex_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_non_convex_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_non_convex_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_non_convex_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage_non_convex_0)_:
-1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_0)
+1 InvestmentFlowBlock_old(electricityBus_storage_non_convex_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage_non_convex_1)_:
+1 InvestmentFlowBlock_old(electricityBus_storage_non_convex_1)
-1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage_non_convex_2)_:
+1 InvestmentFlowBlock_old(electricityBus_storage_non_convex_2)
-1 InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_non_convex_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_0)
+1 InvestmentFlowBlock_old(storage_non_convex_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_non_convex_electricityBus_1)_:
+1 InvestmentFlowBlock_old(storage_non_convex_electricityBus_1)
-1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_non_convex_electricityBus_2)_:
+1 InvestmentFlowBlock_old(storage_non_convex_electricityBus_2)
-1 InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_0_0)_:
+1 flow(electricityBus_storage_non_convex_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_0_1)_:
+1 flow(electricityBus_storage_non_convex_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_1_2)_:
+1 flow(electricityBus_storage_non_convex_1_2)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_1_3)_:
+1 flow(electricityBus_storage_non_convex_1_3)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_2_4)_:
+1 flow(electricityBus_storage_non_convex_2_4)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_2_5)_:
+1 flow(electricityBus_storage_non_convex_2_5)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_0_0)_:
+1 flow(storage_non_convex_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_0_1)_:
+1 flow(storage_non_convex_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_1_2)_:
+1 flow(storage_non_convex_electricityBus_1_2)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_1_3)_:
+1 flow(storage_non_convex_electricityBus_1_3)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_2_4)_:
+1 flow(storage_non_convex_electricityBus_2_4)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_2_5)_:
+1 flow(storage_non_convex_electricityBus_2_5)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_non_convex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_non_convex_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_1)
-1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_total(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_old(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_non_convex_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_2)
-1 GenericInvestmentStorageBlock_total(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_total(storage_non_convex_2)
+1 GenericInvestmentStorageBlock_old(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_non_convex_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_non_convex_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_non_convex_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_non_convex_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_non_convex_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_non_convex_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_non_convex_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_old(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_non_convex_1)_:
+1 GenericInvestmentStorageBlock_old(storage_non_convex_1)
-1 GenericInvestmentStorageBlock_old_end(storage_non_convex_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_non_convex_2)_:
+1 GenericInvestmentStorageBlock_old(storage_non_convex_2)
-1 GenericInvestmentStorageBlock_old_end(storage_non_convex_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage_non_convex_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_0_1)_:
-0.97 flow(electricityBus_storage_non_convex_0_1)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_1)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_1_2)_:
-0.97 flow(electricityBus_storage_non_convex_1_2)
+1.1627906976744187 flow(storage_non_convex_electricityBus_1_2)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_1_3)_:
-0.97 flow(electricityBus_storage_non_convex_1_3)
+1.1627906976744187 flow(storage_non_convex_electricityBus_1_3)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_2_4)_:
-0.97 flow(electricityBus_storage_non_convex_2_4)
+1.1627906976744187 flow(storage_non_convex_electricityBus_2_4)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_2_5)_:
-0.97 flow(electricityBus_storage_non_convex_2_5)
+1.1627906976744187 flow(storage_non_convex_electricityBus_2_5)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_1)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_1)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_2)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_2)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_1)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_1)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_2)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_2)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_0_0)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_0_1)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_1_2)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_1_3)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_2_4)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_2_5)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_5)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_0_0)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_0_1)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_1_2)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_1_3)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_3)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_2_4)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_4)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_2_5)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_5)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_non_convex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+244 GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_non_convex_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_1)
+244 GenericInvestmentStorageBlock_invest_status(storage_non_convex_1)
>= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_non_convex_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_2)
+244 GenericInvestmentStorageBlock_invest_status(storage_non_convex_2)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_non_convex_0)_:
+1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
-12 GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_non_convex_1)_:
+1 GenericInvestmentStorageBlock_invest(storage_non_convex_1)
-12 GenericInvestmentStorageBlock_invest_status(storage_non_convex_1)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_non_convex_2)_:
+1 GenericInvestmentStorageBlock_invest(storage_non_convex_2)
-12 GenericInvestmentStorageBlock_invest_status(storage_non_convex_2)
>= 0

bounds
   0 <= flow(electricityBus_storage_non_convex_0_0) <= +inf
   0 <= flow(electricityBus_storage_non_convex_0_1) <= +inf
   0 <= flow(electricityBus_storage_non_convex_1_2) <= +inf
   0 <= flow(electricityBus_storage_non_convex_1_3) <= +inf
   0 <= flow(electricityBus_storage_non_convex_2_4) <= +inf
   0 <= flow(electricityBus_storage_non_convex_2_5) <= +inf
   0 <= flow(storage_non_convex_electricityBus_0_0) <= +inf
   0 <= flow(storage_non_convex_electricityBus_0_1) <= +inf
   0 <= flow(storage_non_convex_electricityBus_1_2) <= +inf
   0 <= flow(storage_non_convex_electricityBus_1_3) <= +inf
   0 <= flow(storage_non_convex_electricityBus_2_4) <= +inf
   0 <= flow(storage_non_convex_electricityBus_2_5) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_non_convex_0) <= 244
   0 <= GenericInvestmentStorageBlock_invest(storage_non_convex_1) <= 244
   0 <= GenericInvestmentStorageBlock_invest(storage_non_convex_2) <= 244
   0 <= InvestmentFlowBlock_total(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage_non_convex_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage_non_convex_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage_non_convex_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage_non_convex_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage_non_convex_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage_non_convex_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_non_convex_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_non_convex_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_non_convex_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_non_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_non_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_non_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage_non_convex_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_non_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage_non_convex_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_non_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_non_convex_electricityBus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_5) <= +inf
   0 <= GenericInvestmentStorageBlock_invest_status(storage_non_convex_0) <= 1
   0 <= GenericInvestmentStorageBlock_invest_status(storage_non_convex_1) <= 1
   0 <= GenericInvestmentStorageBlock_invest_status(storage_non_convex_2) <= 1
binary
  GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
  GenericInvestmentStorageBlock_invest_status(storage_non_convex_1)
  GenericInvestmentStorageBlock_invest_status(storage_non_convex_2)
end
