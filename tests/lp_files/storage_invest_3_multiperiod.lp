\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+121.09030188807486 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_0)
+118.71598224321065 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_1)
+116.38821788550062 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_2)
+11.00820926255226 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_0)
+10.792362022110058 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_1)
+10.580747080500057 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_2)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage3_0_0)
+1 flow(storage3_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage3_0_1)
+1 flow(storage3_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage3_1_2)
+1 flow(storage3_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage3_1_3)
+1 flow(storage3_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage3_2_4)
+1 flow(storage3_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage3_2_5)
+1 flow(storage3_electricityBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage3_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage3_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_1)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage3_1)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage3_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage3_2)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage3_2)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage3_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage3_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(storage3_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage3_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage3_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(storage3_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage3_0)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage3_1)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage3_2)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage3_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage3_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage3_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage3_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage3_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage3_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage3_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage3_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage3_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage3_0)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage3_0)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_0)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage3_1)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage3_1)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_1)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage3_2)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage3_2)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_2)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage3_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(storage3_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage3_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(storage3_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage3_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(storage3_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_0_0)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_0)
+1 flow(electricityBus_storage3_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_0_1)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_0)
+1 flow(electricityBus_storage3_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_1_2)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_1)
+1 flow(electricityBus_storage3_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_1_3)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_1)
+1 flow(electricityBus_storage3_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_2_4)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_2)
+1 flow(electricityBus_storage3_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage3_2_5)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage3_2)
+1 flow(electricityBus_storage3_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_0)
+1 flow(storage3_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_0)
+1 flow(storage3_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_1)
+1 flow(storage3_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_1)
+1 flow(storage3_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_2)
+1 flow(storage3_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage3_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage3_electricityBus_2)
+1 flow(storage3_electricityBus_2_5)
<= 0

c_e_GenericMultiPeriodStorageBlock_balance_first(storage3)_:
-1 GenericMultiPeriodStorageBlock_init_content(storage3)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_0)
-1 flow(electricityBus_storage3_0_0)
+1 flow(storage3_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage3_0_1)_:
-1 GenericMultiPeriodStorageBlock_storage_content(storage3_0)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_1)
-1 flow(electricityBus_storage3_0_1)
+1 flow(storage3_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage3_1_2)_:
-1 GenericMultiPeriodStorageBlock_storage_content(storage3_1)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_2)
-1 flow(electricityBus_storage3_1_2)
+1 flow(storage3_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage3_1_3)_:
-1 GenericMultiPeriodStorageBlock_storage_content(storage3_2)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_3)
-1 flow(electricityBus_storage3_1_3)
+1 flow(storage3_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage3_2_4)_:
-1 GenericMultiPeriodStorageBlock_storage_content(storage3_3)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_4)
-1 flow(electricityBus_storage3_2_4)
+1 flow(storage3_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage3_2_5)_:
-1 GenericMultiPeriodStorageBlock_storage_content(storage3_4)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_5)
-1 flow(electricityBus_storage3_2_5)
+1 flow(storage3_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodStorageBlock_balanced_cstr(storage3)_:
-1 GenericMultiPeriodStorageBlock_init_content(storage3)
+1 GenericMultiPeriodStorageBlock_storage_content(storage3_5)
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
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage3_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage3_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage3_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage3_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage3_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage3_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage3_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage3_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage3_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage3_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage3_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage3_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage3_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage3_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage3_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage3_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage3_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage3_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage3_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage3_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage3_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage3_electricityBus_2) <= +inf
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_0) <= 5000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_1) <= 5000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_2) <= 5000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_3) <= 5000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_4) <= 5000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage3_5) <= 5000
   0 <= GenericMultiPeriodStorageBlock_init_content(storage3) <= 5000
end
