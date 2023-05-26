\* Source Pyomo model name=Model *\

min 
objective:
+101.97980198019803 InvestmentFlowBlock_invest(electricityBus_storage3_0)
+99.980198019801989 InvestmentFlowBlock_invest(electricityBus_storage3_1)
+98.019801980198025 InvestmentFlowBlock_invest(electricityBus_storage3_2)
+11.00820926255226 InvestmentFlowBlock_invest(storage3_electricityBus_0)
+10.792362022110058 InvestmentFlowBlock_invest(storage3_electricityBus_1)
+10.580747080500057 InvestmentFlowBlock_invest(storage3_electricityBus_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage3_0_0)
+1 flow(storage3_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage3_0_1)
+1 flow(storage3_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage3_1_2)
+1 flow(storage3_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage3_1_3)
+1 flow(storage3_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage3_2_4)
+1 flow(storage3_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage3_2_5)
+1 flow(storage3_electricityBus_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage3_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage3_0)
+1 InvestmentFlowBlock_total(electricityBus_storage3_0)
= 10

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage3_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage3_1)
+1 InvestmentFlowBlock_old(electricityBus_storage3_1)
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
+1 InvestmentFlowBlock_total(electricityBus_storage3_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage3_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage3_2)
+1 InvestmentFlowBlock_old(electricityBus_storage3_2)
-1 InvestmentFlowBlock_total(electricityBus_storage3_1)
+1 InvestmentFlowBlock_total(electricityBus_storage3_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage3_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(storage3_electricityBus_0)
+1 InvestmentFlowBlock_total(storage3_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage3_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(storage3_electricityBus_1)
+1 InvestmentFlowBlock_old(storage3_electricityBus_1)
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
+1 InvestmentFlowBlock_total(storage3_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage3_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(storage3_electricityBus_2)
+1 InvestmentFlowBlock_old(storage3_electricityBus_2)
-1 InvestmentFlowBlock_total(storage3_electricityBus_1)
+1 InvestmentFlowBlock_total(storage3_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage3_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage3_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage3_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_storage3_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_storage3_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage3_0)
+1 InvestmentFlowBlock_old_end(electricityBus_storage3_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage3_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(storage3_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage3_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(storage3_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage3_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(storage3_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage3_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage3_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage3_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage3_1)
= 10

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_storage3_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_storage3_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage3_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(storage3_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage3_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(storage3_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage3_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(storage3_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage3_0)_:
+1 InvestmentFlowBlock_old(electricityBus_storage3_0)
-1 InvestmentFlowBlock_old_end(electricityBus_storage3_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage3_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage3_1)_:
+1 InvestmentFlowBlock_old(electricityBus_storage3_1)
-1 InvestmentFlowBlock_old_end(electricityBus_storage3_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage3_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_storage3_2)_:
+1 InvestmentFlowBlock_old(electricityBus_storage3_2)
-1 InvestmentFlowBlock_old_end(electricityBus_storage3_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_storage3_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage3_electricityBus_0)_:
+1 InvestmentFlowBlock_old(storage3_electricityBus_0)
-1 InvestmentFlowBlock_old_end(storage3_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(storage3_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage3_electricityBus_1)_:
+1 InvestmentFlowBlock_old(storage3_electricityBus_1)
-1 InvestmentFlowBlock_old_end(storage3_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(storage3_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage3_electricityBus_2)_:
+1 InvestmentFlowBlock_old(storage3_electricityBus_2)
-1 InvestmentFlowBlock_old_end(storage3_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(storage3_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_0_0)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
+1 flow(electricityBus_storage3_0_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_0_1)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
+1 flow(electricityBus_storage3_0_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_1_2)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_1)
+1 flow(electricityBus_storage3_1_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_1_3)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_1)
+1 flow(electricityBus_storage3_1_3)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_2_4)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_2)
+1 flow(electricityBus_storage3_2_4)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_2_5)_:
-1 InvestmentFlowBlock_total(electricityBus_storage3_2)
+1 flow(electricityBus_storage3_2_5)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_0_0)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
+1 flow(storage3_electricityBus_0_0)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_0_1)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
+1 flow(storage3_electricityBus_0_1)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_1_2)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_1)
+1 flow(storage3_electricityBus_1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_1_3)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_1)
+1 flow(storage3_electricityBus_1_3)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_2_4)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_2)
+1 flow(storage3_electricityBus_2_4)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_2_5)_:
-1 InvestmentFlowBlock_total(storage3_electricityBus_2)
+1 flow(storage3_electricityBus_2_5)
<= 0

c_e_GenericStorageBlock_balance(storage3_0_0)_:
-1 GenericStorageBlock_storage_content(storage3_0)
+1 GenericStorageBlock_storage_content(storage3_1)
-1 flow(electricityBus_storage3_0_0)
+1 flow(storage3_electricityBus_0_0)
= 0

c_e_GenericStorageBlock_balance(storage3_0_1)_:
-1 GenericStorageBlock_storage_content(storage3_1)
+1 GenericStorageBlock_storage_content(storage3_2)
-1 flow(electricityBus_storage3_0_1)
+1 flow(storage3_electricityBus_0_1)
= 0

c_e_GenericStorageBlock_balance(storage3_1_2)_:
-1 GenericStorageBlock_storage_content(storage3_2)
+1 GenericStorageBlock_storage_content(storage3_3)
-1 flow(electricityBus_storage3_1_2)
+1 flow(storage3_electricityBus_1_2)
= 0

c_e_GenericStorageBlock_balance(storage3_1_3)_:
-1 GenericStorageBlock_storage_content(storage3_3)
+1 GenericStorageBlock_storage_content(storage3_4)
-1 flow(electricityBus_storage3_1_3)
+1 flow(storage3_electricityBus_1_3)
= 0

c_e_GenericStorageBlock_balance(storage3_2_4)_:
-1 GenericStorageBlock_storage_content(storage3_4)
+1 GenericStorageBlock_storage_content(storage3_5)
-1 flow(electricityBus_storage3_2_4)
+1 flow(storage3_electricityBus_2_4)
= 0

c_e_GenericStorageBlock_balance(storage3_2_5)_:
-1 GenericStorageBlock_storage_content(storage3_5)
+1 GenericStorageBlock_storage_content(storage3_6)
-1 flow(electricityBus_storage3_2_5)
+1 flow(storage3_electricityBus_2_5)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage3)_:
-1 GenericStorageBlock_storage_content(storage3_0)
+1 GenericStorageBlock_storage_content(storage3_6)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage3_0_0) <= +inf
   0 <= flow(electricityBus_storage3_0_1) <= +inf
   0 <= flow(electricityBus_storage3_1_2) <= +inf
   0 <= flow(electricityBus_storage3_1_3) <= +inf
   0 <= flow(electricityBus_storage3_2_4) <= +inf
   0 <= flow(electricityBus_storage3_2_5) <= +inf
   0 <= flow(storage3_electricityBus_0_0) <= +inf
   0 <= flow(storage3_electricityBus_0_1) <= +inf
   0 <= flow(storage3_electricityBus_1_2) <= +inf
   0 <= flow(storage3_electricityBus_1_3) <= +inf
   0 <= flow(storage3_electricityBus_2_4) <= +inf
   0 <= flow(storage3_electricityBus_2_5) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage3_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage3_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage3_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage3_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage3_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage3_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage3_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage3_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage3_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage3_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage3_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage3_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_storage3_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage3_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage3_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage3_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage3_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_storage3_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage3_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage3_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage3_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage3_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_storage3_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage3_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage3_electricityBus_2) <= +inf
   0 <= GenericStorageBlock_storage_content(storage3_0) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_1) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_2) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_3) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_4) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_5) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_6) <= 5000
end
