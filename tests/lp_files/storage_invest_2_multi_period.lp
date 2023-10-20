\* Source Pyomo model name=Model *\

min 
objective:
+1.5873195277040417 InvestmentFlowBlock_invest(storage2_electricityBus_0)
+1.0477014265985347 InvestmentFlowBlock_invest(storage2_electricityBus_1)
+0.5186640725735326 InvestmentFlowBlock_invest(storage2_electricityBus_2)
+17.46051480474446 InvestmentFlowBlock_invest(electricityBus_storage2_0)
+11.524715692583884 InvestmentFlowBlock_invest(electricityBus_storage2_1)
+5.705304798308859 InvestmentFlowBlock_invest(electricityBus_storage2_2)
+25.57348127967623 GenericInvestmentStorageBlock_invest(storage2_0)
+16.879634095198618 GenericInvestmentStorageBlock_invest(storage2_1)
+8.35625450257358 GenericInvestmentStorageBlock_invest(storage2_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage2_electricityBus_0_0)
-1 flow(electricityBus_storage2_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 flow(electricityBus_storage2_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(storage2_electricityBus_1_2)
-1 flow(electricityBus_storage2_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(storage2_electricityBus_1_3)
-1 flow(electricityBus_storage2_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(storage2_electricityBus_2_4)
-1 flow(electricityBus_storage2_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(storage2_electricityBus_2_5)
-1 flow(electricityBus_storage2_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(storage2_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(storage2_electricityBus_0)
+1 InvestmentFlowBlock_total(storage2_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage2_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(storage2_electricityBus_1)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
+1 InvestmentFlowBlock_total(storage2_electricityBus_1)
+1 InvestmentFlowBlock_old(storage2_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage2_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(storage2_electricityBus_2)
-1 InvestmentFlowBlock_total(storage2_electricityBus_1)
+1 InvestmentFlowBlock_total(storage2_electricityBus_2)
+1 InvestmentFlowBlock_old(storage2_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage2_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage2_0)
+1 InvestmentFlowBlock_total(electricityBus_storage2_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage2_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage2_1)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
+1 InvestmentFlowBlock_total(electricityBus_storage2_1)
+1 InvestmentFlowBlock_old(electricityBus_storage2_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage2_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage2_2)
-1 InvestmentFlowBlock_total(electricityBus_storage2_1)
+1 InvestmentFlowBlock_total(electricityBus_storage2_2)
+1 InvestmentFlowBlock_old(electricityBus_storage2_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage2_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(storage2_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage2_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(storage2_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage2_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(storage2_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage2_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage2_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage2_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage2_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage2_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage2_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage2_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(storage2_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage2_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(storage2_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage2_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(storage2_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage2_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage2_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage2_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage2_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage2_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage2_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage2_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(storage2_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(storage2_electricityBus_0)
+1 InvestmentFlowBlock_old(storage2_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage2_electricityBus_1)_:
+1 InvestmentFlowBlock_old(storage2_electricityBus_1)
-1 InvestmentFlowBlock_old_end(storage2_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(storage2_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage2_electricityBus_2)_:
+1 InvestmentFlowBlock_old(storage2_electricityBus_2)
-1 InvestmentFlowBlock_old_end(storage2_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(storage2_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage2_0)_:
-1 InvestmentFlowBlock_old_end(electricityBus_storage2_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage2_0)
+1 InvestmentFlowBlock_old(electricityBus_storage2_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage2_1)_:
+1 InvestmentFlowBlock_old(electricityBus_storage2_1)
-1 InvestmentFlowBlock_old_end(electricityBus_storage2_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage2_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage2_2)_:
+1 InvestmentFlowBlock_old(electricityBus_storage2_2)
-1 InvestmentFlowBlock_old_end(electricityBus_storage2_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage2_2)
= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_0_0)_:
+1 flow(storage2_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_1_2)_:
+1 flow(storage2_electricityBus_1_2)
-1 InvestmentFlowBlock_total(storage2_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_1_3)_:
+1 flow(storage2_electricityBus_1_3)
-1 InvestmentFlowBlock_total(storage2_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_2_4)_:
+1 flow(storage2_electricityBus_2_4)
-1 InvestmentFlowBlock_total(storage2_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_2_5)_:
+1 flow(storage2_electricityBus_2_5)
-1 InvestmentFlowBlock_total(storage2_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_0_0)_:
+1 flow(electricityBus_storage2_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_0_1)_:
+1 flow(electricityBus_storage2_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_1_2)_:
+1 flow(electricityBus_storage2_1_2)
-1 InvestmentFlowBlock_total(electricityBus_storage2_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_1_3)_:
+1 flow(electricityBus_storage2_1_3)
-1 InvestmentFlowBlock_total(electricityBus_storage2_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_2_4)_:
+1 flow(electricityBus_storage2_2_4)
-1 InvestmentFlowBlock_total(electricityBus_storage2_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_2_5)_:
+1 flow(electricityBus_storage2_2_5)
-1 InvestmentFlowBlock_total(electricityBus_storage2_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage2_0)_:
-1 GenericInvestmentStorageBlock_invest(storage2_0)
+1 GenericInvestmentStorageBlock_total(storage2_0)
= 20

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage2_1)_:
-1 GenericInvestmentStorageBlock_invest(storage2_1)
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_total(storage2_1)
+1 GenericInvestmentStorageBlock_old(storage2_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage2_2)_:
-1 GenericInvestmentStorageBlock_invest(storage2_2)
-1 GenericInvestmentStorageBlock_total(storage2_1)
+1 GenericInvestmentStorageBlock_total(storage2_2)
+1 GenericInvestmentStorageBlock_old(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage2_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage2_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage2_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage2_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage2_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage2_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage2_1)
= 20

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage2_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage2_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage2_0)
-1 GenericInvestmentStorageBlock_old_exo(storage2_0)
+1 GenericInvestmentStorageBlock_old(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage2_1)_:
+1 GenericInvestmentStorageBlock_old(storage2_1)
-1 GenericInvestmentStorageBlock_old_end(storage2_1)
-1 GenericInvestmentStorageBlock_old_exo(storage2_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage2_2)_:
+1 GenericInvestmentStorageBlock_old(storage2_2)
-1 GenericInvestmentStorageBlock_old_end(storage2_2)
-1 GenericInvestmentStorageBlock_old_exo(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage2_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 flow(electricityBus_storage2_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_1_2)_:
+1 flow(storage2_electricityBus_1_2)
-1 flow(electricityBus_storage2_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage2_1)
+1 GenericInvestmentStorageBlock_storage_content(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_1_3)_:
+1 flow(storage2_electricityBus_1_3)
-1 flow(electricityBus_storage2_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage2_2)
+1 GenericInvestmentStorageBlock_storage_content(storage2_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_2_4)_:
+1 flow(storage2_electricityBus_2_4)
-1 flow(electricityBus_storage2_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage2_3)
+1 GenericInvestmentStorageBlock_storage_content(storage2_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_2_5)_:
+1 flow(storage2_electricityBus_2_5)
-1 flow(electricityBus_storage2_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage2_4)
+1 GenericInvestmentStorageBlock_storage_content(storage2_5)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage2_1)
+1 GenericInvestmentStorageBlock_storage_content(storage2_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage2_1)
+1 GenericInvestmentStorageBlock_storage_content(storage2_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage2_2)
+1 GenericInvestmentStorageBlock_storage_content(storage2_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage2_2)
+1 GenericInvestmentStorageBlock_storage_content(storage2_5)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(storage2_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage2_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage2_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage2_2) <= +inf
   0 <= flow(storage2_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage2_0_0) <= +inf
   0 <= flow(storage2_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage2_0_1) <= +inf
   0 <= flow(storage2_electricityBus_1_2) <= +inf
   0 <= flow(electricityBus_storage2_1_2) <= +inf
   0 <= flow(storage2_electricityBus_1_3) <= +inf
   0 <= flow(electricityBus_storage2_1_3) <= +inf
   0 <= flow(storage2_electricityBus_2_4) <= +inf
   0 <= flow(electricityBus_storage2_2_4) <= +inf
   0 <= flow(storage2_electricityBus_2_5) <= +inf
   0 <= flow(electricityBus_storage2_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(storage2_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage2_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage2_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage2_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage2_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage2_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage2_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage2_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage2_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage2_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage2_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage2_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage2_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage2_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage2_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage2_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_5) <= +inf
end
