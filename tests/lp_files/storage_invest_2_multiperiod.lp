\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_2)
+121.09030188807486 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_0)
+118.71598224321065 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_1)
+116.38821788550062 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_2)
+11.00820926255226 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_0)
+10.792362022110058 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_1)
+10.580747080500057 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_2)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage2_0_0)
+1 flow(storage2_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage2_0_1)
+1 flow(storage2_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage2_1_2)
+1 flow(storage2_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage2_1_3)
+1 flow(storage2_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage2_2_4)
+1 flow(storage2_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage2_2_5)
+1 flow(storage2_electricityBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage2_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage2_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_1)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage2_1)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage2_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage2_2)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage2_2)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage2_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage2_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(storage2_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage2_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage2_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(storage2_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage2_0)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage2_1)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage2_2)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage2_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage2_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage2_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage2_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage2_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage2_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage2_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage2_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage2_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage2_0)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage2_0)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_0)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage2_1)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage2_1)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_1)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage2_2)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage2_2)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_2)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage2_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(storage2_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage2_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(storage2_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage2_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(storage2_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_0_0)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_0)
+1 flow(electricityBus_storage2_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_0_1)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_0)
+1 flow(electricityBus_storage2_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_1_2)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_1)
+1 flow(electricityBus_storage2_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_1_3)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_1)
+1 flow(electricityBus_storage2_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_2_4)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_2)
+1 flow(electricityBus_storage2_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage2_2_5)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage2_2)
+1 flow(electricityBus_storage2_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_0)
+1 flow(storage2_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_0)
+1 flow(storage2_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_1)
+1 flow(storage2_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_1)
+1 flow(storage2_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_2)
+1 flow(storage2_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage2_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage2_electricityBus_2)
+1 flow(storage2_electricityBus_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage2_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage2_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage2_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage2_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage2_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage2_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage2_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage2_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage2_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage2_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage2_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage2_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage2_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage2_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage2_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage2_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage2_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage2_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage2_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_0)
-1 flow(electricityBus_storage2_0_0)
+1 flow(storage2_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage2_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_1)
-1 flow(electricityBus_storage2_0_1)
+1 flow(storage2_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage2_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_2)
-1 flow(electricityBus_storage2_1_2)
+1 flow(storage2_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage2_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_3)
-1 flow(electricityBus_storage2_1_3)
+1 flow(storage2_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage2_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_4)
-1 flow(electricityBus_storage2_2_4)
+1 flow(storage2_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage2_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_5)
-1 flow(electricityBus_storage2_2_5)
+1 flow(storage2_electricityBus_2_5)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage2_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage2_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage2_0_0) <= +inf
   0 <= flow(electricityBus_storage2_0_1) <= +inf
   0 <= flow(electricityBus_storage2_1_2) <= +inf
   0 <= flow(electricityBus_storage2_1_3) <= +inf
   0 <= flow(electricityBus_storage2_2_4) <= +inf
   0 <= flow(electricityBus_storage2_2_5) <= +inf
   0 <= flow(storage2_electricityBus_0_0) <= +inf
   0 <= flow(storage2_electricityBus_0_1) <= +inf
   0 <= flow(storage2_electricityBus_1_2) <= +inf
   0 <= flow(storage2_electricityBus_1_3) <= +inf
   0 <= flow(storage2_electricityBus_2_4) <= +inf
   0 <= flow(storage2_electricityBus_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage2_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage2_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage2_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage2_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage2_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage2_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage2_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage2_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage2_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage2_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage2_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage2_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage2_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage2_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage2_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage2_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage2_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage2_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage2_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage2_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage2_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage2_electricityBus_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage2_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage2_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage2_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage2_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage2_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage2_2) <= +inf
end
