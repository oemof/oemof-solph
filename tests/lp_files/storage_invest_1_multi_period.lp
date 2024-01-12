\* Source Pyomo model name=Model *\

min 
objective:
+56 flow(electricityBus_storage1_0_0)
+56 flow(electricityBus_storage1_0_1)
+54.90196078431372 flow(electricityBus_storage1_1_2)
+54.90196078431372 flow(electricityBus_storage1_1_3)
+53.82545174932718 flow(electricityBus_storage1_2_4)
+53.82545174932718 flow(electricityBus_storage1_2_5)
+24 flow(storage1_electricityBus_0_0)
+24 flow(storage1_electricityBus_0_1)
+23.52941176470588 flow(storage1_electricityBus_1_2)
+23.52941176470588 flow(storage1_electricityBus_1_3)
+23.06805074971165 flow(storage1_electricityBus_2_4)
+23.06805074971165 flow(storage1_electricityBus_2_5)
+31.685467778602654 GenericInvestmentStorageBlock_invest(storage1_0)
+21.210358847924045 GenericInvestmentStorageBlock_invest(storage1_1)
+10.650825820334894 GenericInvestmentStorageBlock_invest(storage1_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage1_0_0)
+1 flow(storage1_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage1_0_1)
+1 flow(storage1_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage1_1_2)
+1 flow(storage1_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage1_1_3)
+1 flow(storage1_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage1_2_4)
+1 flow(storage1_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage1_2_5)
+1 flow(storage1_electricityBus_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage1_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_0)
-1 InvestmentFlowBlock_invest(electricityBus_storage1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage1_1)_:
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
+1 InvestmentFlowBlock_total(electricityBus_storage1_1)
-1 InvestmentFlowBlock_invest(electricityBus_storage1_1)
+1 InvestmentFlowBlock_old(electricityBus_storage1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage1_2)_:
-1 InvestmentFlowBlock_total(electricityBus_storage1_1)
+1 InvestmentFlowBlock_total(electricityBus_storage1_2)
-1 InvestmentFlowBlock_invest(electricityBus_storage1_2)
+1 InvestmentFlowBlock_old(electricityBus_storage1_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage1_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage1_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage1_electricityBus_1)_:
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
+1 InvestmentFlowBlock_total(storage1_electricityBus_1)
-1 InvestmentFlowBlock_invest(storage1_electricityBus_1)
+1 InvestmentFlowBlock_old(storage1_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage1_electricityBus_2)_:
-1 InvestmentFlowBlock_total(storage1_electricityBus_1)
+1 InvestmentFlowBlock_total(storage1_electricityBus_2)
-1 InvestmentFlowBlock_invest(storage1_electricityBus_2)
+1 InvestmentFlowBlock_old(storage1_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage1_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage1_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage1_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage1_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(storage1_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage1_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(storage1_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage1_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(storage1_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage1_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage1_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage1_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage1_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(storage1_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage1_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(storage1_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage1_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(storage1_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage1_0)_:
-1 InvestmentFlowBlock_old_end(electricityBus_storage1_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage1_0)
+1 InvestmentFlowBlock_old(electricityBus_storage1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage1_1)_:
+1 InvestmentFlowBlock_old(electricityBus_storage1_1)
-1 InvestmentFlowBlock_old_end(electricityBus_storage1_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage1_2)_:
+1 InvestmentFlowBlock_old(electricityBus_storage1_2)
-1 InvestmentFlowBlock_old_end(electricityBus_storage1_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage1_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(storage1_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(storage1_electricityBus_0)
+1 InvestmentFlowBlock_old(storage1_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage1_electricityBus_1)_:
+1 InvestmentFlowBlock_old(storage1_electricityBus_1)
-1 InvestmentFlowBlock_old_end(storage1_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(storage1_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage1_electricityBus_2)_:
+1 InvestmentFlowBlock_old(storage1_electricityBus_2)
-1 InvestmentFlowBlock_old_end(storage1_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(storage1_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_0_0)_:
+1 flow(electricityBus_storage1_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_0_1)_:
+1 flow(electricityBus_storage1_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_1_2)_:
+1 flow(electricityBus_storage1_1_2)
-1 InvestmentFlowBlock_total(electricityBus_storage1_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_1_3)_:
+1 flow(electricityBus_storage1_1_3)
-1 InvestmentFlowBlock_total(electricityBus_storage1_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_2_4)_:
+1 flow(electricityBus_storage1_2_4)
-1 InvestmentFlowBlock_total(electricityBus_storage1_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_2_5)_:
+1 flow(electricityBus_storage1_2_5)
-1 InvestmentFlowBlock_total(electricityBus_storage1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_0_0)_:
+1 flow(storage1_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_1_2)_:
+1 flow(storage1_electricityBus_1_2)
-1 InvestmentFlowBlock_total(storage1_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_1_3)_:
+1 flow(storage1_electricityBus_1_3)
-1 InvestmentFlowBlock_total(storage1_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_2_4)_:
+1 flow(storage1_electricityBus_2_4)
-1 InvestmentFlowBlock_total(storage1_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_2_5)_:
+1 flow(storage1_electricityBus_2_5)
-1 InvestmentFlowBlock_total(storage1_electricityBus_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_invest(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_1)_:
-1 GenericInvestmentStorageBlock_invest(storage1_1)
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_old(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_2)_:
-1 GenericInvestmentStorageBlock_invest(storage1_2)
-1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_old(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage1_0)
-1 GenericInvestmentStorageBlock_old_exo(storage1_0)
+1 GenericInvestmentStorageBlock_old(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_1)_:
+1 GenericInvestmentStorageBlock_old(storage1_1)
-1 GenericInvestmentStorageBlock_old_end(storage1_1)
-1 GenericInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_2)_:
+1 GenericInvestmentStorageBlock_old(storage1_2)
-1 GenericInvestmentStorageBlock_old_end(storage1_2)
-1 GenericInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage1_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_0_1)_:
-0.97 flow(electricityBus_storage1_0_1)
+1.1627906976744187 flow(storage1_electricityBus_0_1)
-0.87 GenericInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_2)_:
-0.97 flow(electricityBus_storage1_1_2)
+1.1627906976744187 flow(storage1_electricityBus_1_2)
-0.87 GenericInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_3)_:
-0.97 flow(electricityBus_storage1_1_3)
+1.1627906976744187 flow(storage1_electricityBus_1_3)
-0.87 GenericInvestmentStorageBlock_storage_content(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_4)_:
-0.97 flow(electricityBus_storage1_2_4)
+1.1627906976744187 flow(storage1_electricityBus_2_4)
-0.87 GenericInvestmentStorageBlock_storage_content(storage1_3)
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_5)_:
-0.97 flow(electricityBus_storage1_2_5)
+1.1627906976744187 flow(storage1_electricityBus_2_5)
-0.87 GenericInvestmentStorageBlock_storage_content(storage1_4)
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage1_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage1_1)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_1)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage1_2)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_2)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage1_0)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage1_1)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_1)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage1_2)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_2)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage1_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_0)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_1)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_2)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_3)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_4)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_5)_:
-0.9 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_0_0)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_0)
-1 GenericInvestmentStorageBlock_storage_content(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_0_1)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_0)
-1 GenericInvestmentStorageBlock_storage_content(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_1_2)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_1)
-1 GenericInvestmentStorageBlock_storage_content(storage1_2)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_1_3)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_1)
-1 GenericInvestmentStorageBlock_storage_content(storage1_3)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_2_4)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage1_4)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage1_2_5)_:
+0.1 GenericInvestmentStorageBlock_total(storage1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage1_5)
<= 0

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_0)_:
+1 GenericInvestmentStorageBlock_total(storage1_0)
<= 1000

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_1)_:
+1 GenericInvestmentStorageBlock_total(storage1_1)
<= 1000

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_2)_:
+1 GenericInvestmentStorageBlock_total(storage1_2)
<= 1000

c_l_GenericInvestmentStorageBlock_overall_minimum(storage1)_:
+1 GenericInvestmentStorageBlock_total(storage1_2)
>= 2

bounds
   0 <= flow(electricityBus_storage1_0_0) <= +inf
   0 <= flow(electricityBus_storage1_0_1) <= +inf
   0 <= flow(electricityBus_storage1_1_2) <= +inf
   0 <= flow(electricityBus_storage1_1_3) <= +inf
   0 <= flow(electricityBus_storage1_2_4) <= +inf
   0 <= flow(electricityBus_storage1_2_5) <= +inf
   0 <= flow(storage1_electricityBus_0_0) <= +inf
   0 <= flow(storage1_electricityBus_0_1) <= +inf
   0 <= flow(storage1_electricityBus_1_2) <= +inf
   0 <= flow(storage1_electricityBus_1_3) <= +inf
   0 <= flow(storage1_electricityBus_2_4) <= +inf
   0 <= flow(storage1_electricityBus_2_5) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage1_0) <= 234
   0 <= GenericInvestmentStorageBlock_invest(storage1_1) <= 234
   0 <= GenericInvestmentStorageBlock_invest(storage1_2) <= 234
   0 <= InvestmentFlowBlock_total(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage1_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage1_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage1_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage1_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage1_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage1_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage1_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage1_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage1_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage1_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage1_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage1_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage1_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage1_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage1_electricityBus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_5) <= +inf
end
