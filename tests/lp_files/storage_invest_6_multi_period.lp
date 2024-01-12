\* Source Pyomo model name=Model *\

min 
objective:
+17.46051480474446 InvestmentFlowBlock_invest(electricityBus_storage6_0)
+11.524715692583884 InvestmentFlowBlock_invest(electricityBus_storage6_1)
+5.705304798308859 InvestmentFlowBlock_invest(electricityBus_storage6_2)
+25.57348127967623 GenericInvestmentStorageBlock_invest(storage6_0)
+16.879634095198618 GenericInvestmentStorageBlock_invest(storage6_1)
+8.35625450257358 GenericInvestmentStorageBlock_invest(storage6_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage6_electricityBus_0_0)
-1 flow(electricityBus_storage6_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 flow(electricityBus_storage6_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(storage6_electricityBus_1_2)
-1 flow(electricityBus_storage6_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(storage6_electricityBus_1_3)
-1 flow(electricityBus_storage6_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(storage6_electricityBus_2_4)
-1 flow(electricityBus_storage6_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(storage6_electricityBus_2_5)
-1 flow(electricityBus_storage6_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(storage6_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage6_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage6_electricityBus_0)
= 100

c_e_InvestmentFlowBlock_total_rule(storage6_electricityBus_1)_:
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
+1 InvestmentFlowBlock_total(storage6_electricityBus_1)
-1 InvestmentFlowBlock_invest(storage6_electricityBus_1)
+1 InvestmentFlowBlock_old(storage6_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage6_electricityBus_2)_:
-1 InvestmentFlowBlock_total(storage6_electricityBus_1)
+1 InvestmentFlowBlock_total(storage6_electricityBus_2)
-1 InvestmentFlowBlock_invest(storage6_electricityBus_2)
+1 InvestmentFlowBlock_old(storage6_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage6_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage6_0)
+1 InvestmentFlowBlock_total(electricityBus_storage6_0)
= 110

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage6_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage6_1)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
+1 InvestmentFlowBlock_total(electricityBus_storage6_1)
+1 InvestmentFlowBlock_old(electricityBus_storage6_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage6_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage6_2)
-1 InvestmentFlowBlock_total(electricityBus_storage6_1)
+1 InvestmentFlowBlock_total(electricityBus_storage6_2)
+1 InvestmentFlowBlock_old(electricityBus_storage6_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage6_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(storage6_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage6_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(storage6_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage6_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(storage6_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage6_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage6_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage6_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage6_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage6_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage6_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage6_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(storage6_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage6_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(storage6_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage6_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(storage6_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage6_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage6_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage6_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage6_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage6_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage6_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage6_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(storage6_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(storage6_electricityBus_0)
+1 InvestmentFlowBlock_old(storage6_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage6_electricityBus_1)_:
+1 InvestmentFlowBlock_old(storage6_electricityBus_1)
-1 InvestmentFlowBlock_old_end(storage6_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(storage6_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage6_electricityBus_2)_:
+1 InvestmentFlowBlock_old(storage6_electricityBus_2)
-1 InvestmentFlowBlock_old_end(storage6_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(storage6_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage6_0)_:
-1 InvestmentFlowBlock_old_end(electricityBus_storage6_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage6_0)
+1 InvestmentFlowBlock_old(electricityBus_storage6_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage6_1)_:
+1 InvestmentFlowBlock_old(electricityBus_storage6_1)
-1 InvestmentFlowBlock_old_end(electricityBus_storage6_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage6_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage6_2)_:
+1 InvestmentFlowBlock_old(electricityBus_storage6_2)
-1 InvestmentFlowBlock_old_end(electricityBus_storage6_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage6_2)
= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_0_0)_:
+1 flow(storage6_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_1_2)_:
+1 flow(storage6_electricityBus_1_2)
-1 InvestmentFlowBlock_total(storage6_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_1_3)_:
+1 flow(storage6_electricityBus_1_3)
-1 InvestmentFlowBlock_total(storage6_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_2_4)_:
+1 flow(storage6_electricityBus_2_4)
-1 InvestmentFlowBlock_total(storage6_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_2_5)_:
+1 flow(storage6_electricityBus_2_5)
-1 InvestmentFlowBlock_total(storage6_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_0_0)_:
+1 flow(electricityBus_storage6_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_0_1)_:
+1 flow(electricityBus_storage6_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_1_2)_:
+1 flow(electricityBus_storage6_1_2)
-1 InvestmentFlowBlock_total(electricityBus_storage6_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_1_3)_:
+1 flow(electricityBus_storage6_1_3)
-1 InvestmentFlowBlock_total(electricityBus_storage6_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_2_4)_:
+1 flow(electricityBus_storage6_2_4)
-1 InvestmentFlowBlock_total(electricityBus_storage6_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_2_5)_:
+1 flow(electricityBus_storage6_2_5)
-1 InvestmentFlowBlock_total(electricityBus_storage6_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage6_0)_:
-1 GenericInvestmentStorageBlock_invest(storage6_0)
+1 GenericInvestmentStorageBlock_total(storage6_0)
= 1000

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage6_1)_:
-1 GenericInvestmentStorageBlock_invest(storage6_1)
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_total(storage6_1)
+1 GenericInvestmentStorageBlock_old(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage6_2)_:
-1 GenericInvestmentStorageBlock_invest(storage6_2)
-1 GenericInvestmentStorageBlock_total(storage6_1)
+1 GenericInvestmentStorageBlock_total(storage6_2)
+1 GenericInvestmentStorageBlock_old(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage6_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage6_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage6_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage6_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage6_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage6_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage6_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage6_0)
-1 GenericInvestmentStorageBlock_old_exo(storage6_0)
+1 GenericInvestmentStorageBlock_old(storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage6_1)_:
+1 GenericInvestmentStorageBlock_old(storage6_1)
-1 GenericInvestmentStorageBlock_old_end(storage6_1)
-1 GenericInvestmentStorageBlock_old_exo(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage6_2)_:
+1 GenericInvestmentStorageBlock_old(storage6_2)
-1 GenericInvestmentStorageBlock_old_end(storage6_2)
-1 GenericInvestmentStorageBlock_old_exo(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage6_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 flow(electricityBus_storage6_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_1_2)_:
+1 flow(storage6_electricityBus_1_2)
-1 flow(electricityBus_storage6_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage6_1)
+1 GenericInvestmentStorageBlock_storage_content(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_1_3)_:
+1 flow(storage6_electricityBus_1_3)
-1 flow(electricityBus_storage6_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage6_2)
+1 GenericInvestmentStorageBlock_storage_content(storage6_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_2_4)_:
+1 flow(storage6_electricityBus_2_4)
-1 flow(electricityBus_storage6_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage6_3)
+1 GenericInvestmentStorageBlock_storage_content(storage6_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_2_5)_:
+1 flow(storage6_electricityBus_2_5)
-1 flow(electricityBus_storage6_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage6_4)
+1 GenericInvestmentStorageBlock_storage_content(storage6_5)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage6_0)_:
+1.1 InvestmentFlowBlock_total(storage6_electricityBus_0)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage6_1)_:
+1.1 InvestmentFlowBlock_total(storage6_electricityBus_1)
-1 InvestmentFlowBlock_total(electricityBus_storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage6_2)_:
+1.1 InvestmentFlowBlock_total(storage6_electricityBus_2)
-1 InvestmentFlowBlock_total(electricityBus_storage6_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage6_1)
+1 GenericInvestmentStorageBlock_storage_content(storage6_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage6_1)
+1 GenericInvestmentStorageBlock_storage_content(storage6_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage6_2)
+1 GenericInvestmentStorageBlock_storage_content(storage6_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage6_2)
+1 GenericInvestmentStorageBlock_storage_content(storage6_5)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_storage6_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage6_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage6_2) <= +inf
   0 <= flow(storage6_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage6_0_0) <= +inf
   0 <= flow(storage6_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage6_0_1) <= +inf
   0 <= flow(storage6_electricityBus_1_2) <= +inf
   0 <= flow(electricityBus_storage6_1_2) <= +inf
   0 <= flow(storage6_electricityBus_1_3) <= +inf
   0 <= flow(electricityBus_storage6_1_3) <= +inf
   0 <= flow(storage6_electricityBus_2_4) <= +inf
   0 <= flow(electricityBus_storage6_2_4) <= +inf
   0 <= flow(storage6_electricityBus_2_5) <= +inf
   0 <= flow(electricityBus_storage6_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage6_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage6_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage6_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage6_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage6_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage6_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage6_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage6_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage6_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage6_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage6_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage6_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage6_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage6_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage6_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage6_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_5) <= +inf
end
