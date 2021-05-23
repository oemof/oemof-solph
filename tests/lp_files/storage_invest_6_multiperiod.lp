\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+212.02333722461535 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_0)
+207.86601688687779 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_1)
+203.79021263419389 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_2)
+121.09030188807486 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_0)
+118.71598224321065 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_1)
+116.38821788550062 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_2)
+11.00820926255226 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_0)
+10.792362022110058 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_1)
+10.580747080500057 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_2)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage6_0_0)
+1 flow(storage6_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage6_0_1)
+1 flow(storage6_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage6_1_2)
+1 flow(storage6_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage6_1_3)
+1 flow(storage6_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage6_2_4)
+1 flow(storage6_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage6_2_5)
+1 flow(storage6_electricityBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage6_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_0)
= 110

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage6_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_1)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage6_1)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_storage6_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_storage6_2)
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage6_2)
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage6_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_0)
= 100

c_e_MultiPeriodInvestmentFlow_total_rule(storage6_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(storage6_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage6_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage6_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(storage6_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage6_0)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage6_1)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_storage6_2)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage6_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage6_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage6_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage6_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage6_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_storage6_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_2)
= 110

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage6_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage6_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage6_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_2)
= 100

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage6_0)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage6_0)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_0)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage6_1)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage6_1)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_1)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_storage6_2)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_storage6_2)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_2)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage6_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(storage6_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage6_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(storage6_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage6_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(storage6_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_0_0)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_0)
+1 flow(electricityBus_storage6_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_0_1)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_0)
+1 flow(electricityBus_storage6_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_1_2)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_1)
+1 flow(electricityBus_storage6_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_1_3)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_1)
+1 flow(electricityBus_storage6_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_2_4)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_2)
+1 flow(electricityBus_storage6_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_storage6_2_5)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_2)
+1 flow(electricityBus_storage6_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_0)
+1 flow(storage6_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_0)
+1 flow(storage6_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_1)
+1 flow(storage6_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_1)
+1 flow(storage6_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_2)
+1 flow(storage6_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage6_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage6_electricityBus_2)
+1 flow(storage6_electricityBus_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage6_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
= 10000

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage6_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage6_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage6_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage6_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage6_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage6_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage6_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage6_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage6_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage6_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_1)
= 10000

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage6_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage6_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage6_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage6_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage6_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage6_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage6_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage6_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage6)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_0)
-1 flow(electricityBus_storage6_0_0)
+1 flow(storage6_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage6_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_1)
-1 flow(electricityBus_storage6_0_1)
+1 flow(storage6_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage6_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2)
-1 flow(electricityBus_storage6_1_2)
+1 flow(storage6_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage6_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3)
-1 flow(electricityBus_storage6_1_3)
+1 flow(storage6_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage6_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4)
-1 flow(electricityBus_storage6_2_4)
+1 flow(storage6_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage6_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_5)
-1 flow(electricityBus_storage6_2_5)
+1 flow(storage6_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balanced_cstr(storage6_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balanced_cstr(storage6_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balanced_cstr(storage6_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balanced_cstr(storage6_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_power_coupled(storage6_0)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_0)
+1.1000000000000001 MultiPeriodInvestmentFlow_total(storage6_electricityBus_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_power_coupled(storage6_1)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_1)
+1.1000000000000001 MultiPeriodInvestmentFlow_total(storage6_electricityBus_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_power_coupled(storage6_2)_:
-1 MultiPeriodInvestmentFlow_total(electricityBus_storage6_2)
+1.1000000000000001 MultiPeriodInvestmentFlow_total(storage6_electricityBus_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage6_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage6_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage6_0_0) <= +inf
   0 <= flow(electricityBus_storage6_0_1) <= +inf
   0 <= flow(electricityBus_storage6_1_2) <= +inf
   0 <= flow(electricityBus_storage6_1_3) <= +inf
   0 <= flow(electricityBus_storage6_2_4) <= +inf
   0 <= flow(electricityBus_storage6_2_5) <= +inf
   0 <= flow(storage6_electricityBus_0_0) <= +inf
   0 <= flow(storage6_electricityBus_0_1) <= +inf
   0 <= flow(storage6_electricityBus_1_2) <= +inf
   0 <= flow(storage6_electricityBus_1_3) <= +inf
   0 <= flow(storage6_electricityBus_2_4) <= +inf
   0 <= flow(storage6_electricityBus_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage6_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage6_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_storage6_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage6_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage6_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage6_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage6_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage6_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_storage6_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage6_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage6_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage6_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage6_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage6_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_storage6_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage6_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage6_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage6_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_storage6_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage6_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_storage6_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage6_electricityBus_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage6_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage6_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage6_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage6_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage6_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage6_2) <= +inf
end
