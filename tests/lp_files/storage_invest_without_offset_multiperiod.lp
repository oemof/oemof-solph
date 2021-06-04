\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+517.38583533995632 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_0)
+507.24101503917279 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_1)
+497.29511278350276 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_2)
+56 flow(electricityBus_storage_non_convex_0_0)
+56 flow(electricityBus_storage_non_convex_0_1)
+54.901960784313722 flow(electricityBus_storage_non_convex_1_2)
+54.901960784313722 flow(electricityBus_storage_non_convex_1_3)
+53.825451749327179 flow(electricityBus_storage_non_convex_2_4)
+53.825451749327179 flow(electricityBus_storage_non_convex_2_5)
+24 flow(storage_non_convex_electricityBus_0_0)
+24 flow(storage_non_convex_electricityBus_0_1)
+23.52941176470588 flow(storage_non_convex_electricityBus_1_2)
+23.52941176470588 flow(storage_non_convex_electricityBus_1_3)
+23.068050749711649 flow(storage_non_convex_electricityBus_2_4)
+23.068050749711649 flow(storage_non_convex_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage_non_convex_0_0)
+1 flow(storage_non_convex_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage_non_convex_0_1)
+1 flow(storage_non_convex_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage_non_convex_1_2)
+1 flow(storage_non_convex_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage_non_convex_1_3)
+1 flow(storage_non_convex_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage_non_convex_2_4)
+1 flow(storage_non_convex_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage_non_convex_2_5)
+1 flow(storage_non_convex_electricityBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage_non_convex_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage_non_convex_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_1)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_1)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage_non_convex_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_2)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_2)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_non_convex_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_non_convex_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_non_convex_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage_non_convex_0)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage_non_convex_1)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage_non_convex_2)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_non_convex_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_non_convex_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_non_convex_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage_non_convex_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage_non_convex_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage_non_convex_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_non_convex_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_non_convex_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_non_convex_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage_non_convex_0)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_0)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_0)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage_non_convex_1)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_1)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_1)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage_non_convex_2)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_2)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_2)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_non_convex_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_non_convex_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_non_convex_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_0_0)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0)
+1 flow(electricityBus_storage_non_convex_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_0_1)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0)
+1 flow(electricityBus_storage_non_convex_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_1_2)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1)
+1 flow(electricityBus_storage_non_convex_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_1_3)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1)
+1 flow(electricityBus_storage_non_convex_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_2_4)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_2)
+1 flow(electricityBus_storage_non_convex_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage_non_convex_2_5)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_2)
+1 flow(electricityBus_storage_non_convex_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0)
+1 flow(storage_non_convex_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0)
+1 flow(storage_non_convex_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1)
+1 flow(storage_non_convex_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1)
+1 flow(storage_non_convex_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_2)
+1 flow(storage_non_convex_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_non_convex_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_2)
+1 flow(storage_non_convex_electricityBus_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_non_convex_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_non_convex_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_non_convex_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_non_convex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_non_convex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_non_convex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_non_convex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_non_convex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_non_convex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_non_convex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_non_convex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_non_convex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_non_convex_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage_non_convex)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0)
-0.96999999999999997 flow(electricityBus_storage_non_convex_0_0)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_non_convex_0_1)_:
-0.87 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1)
-0.96999999999999997 flow(electricityBus_storage_non_convex_0_1)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_non_convex_1_2)_:
-0.87 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2)
-0.96999999999999997 flow(electricityBus_storage_non_convex_1_2)
+1.1627906976744187 flow(storage_non_convex_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_non_convex_1_3)_:
-0.87 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3)
-0.96999999999999997 flow(electricityBus_storage_non_convex_1_3)
+1.1627906976744187 flow(storage_non_convex_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_non_convex_2_4)_:
-0.87 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4)
-0.96999999999999997 flow(electricityBus_storage_non_convex_2_4)
+1.1627906976744187 flow(storage_non_convex_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_non_convex_2_5)_:
-0.87 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_5)
-0.96999999999999997 flow(electricityBus_storage_non_convex_2_5)
+1.1627906976744187 flow(storage_non_convex_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_0)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_1)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_2)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_0)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_1)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_2)_:
-0.16666666666666666 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
+1 MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_non_convex_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_5)
-0.90000000000000002 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_0_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_min_storage_content(storage_non_convex_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_5)
+0.10000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2)
<= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_non_convex_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_0)
+244 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_non_convex_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_1)
+244 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_1)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_non_convex_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_2)
+244 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_2)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_non_convex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_0)
-12 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_non_convex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_1)
-12 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_1)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_non_convex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_2)
-12 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_2)
>= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

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
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage_non_convex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_non_convex_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage_non_convex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_non_convex_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage_non_convex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_non_convex_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage_non_convex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_non_convex_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage_non_convex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_non_convex_electricityBus_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_non_convex_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_0) <= 244
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_1) <= 244
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_non_convex_2) <= 244
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_non_convex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_non_convex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_non_convex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_non_convex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_0) <= 1
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_1) <= 1
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_2) <= 1
binary
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_0)
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_1)
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_non_convex_2)
end
