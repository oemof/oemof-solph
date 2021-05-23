\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_2)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage4_0_0)
+1 flow(storage4_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage4_0_1)
+1 flow(storage4_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage4_1_2)
+1 flow(storage4_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage4_1_3)
+1 flow(storage4_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage4_2_4)
+1 flow(storage4_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage4_2_5)
+1 flow(storage4_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage4_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage4_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage4_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage4_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage4_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage4_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage4_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage4_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage4_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage4_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage4_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage4_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage4_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage4_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage4_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage4_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage4_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage4_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage4_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_0)
-1 flow(electricityBus_storage4_0_0)
+1 flow(storage4_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage4_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_1)
-1 flow(electricityBus_storage4_0_1)
+1 flow(storage4_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage4_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_2)
-1 flow(electricityBus_storage4_1_2)
+1 flow(storage4_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage4_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_3)
-1 flow(electricityBus_storage4_1_3)
+1 flow(storage4_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage4_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_4)
-1 flow(electricityBus_storage4_2_4)
+1 flow(storage4_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage4_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_5)
-1 flow(electricityBus_storage4_2_5)
+1 flow(storage4_electricityBus_2_5)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage4_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage4_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage4_0_0) <= 80
   0 <= flow(electricityBus_storage4_0_1) <= 80
   0 <= flow(electricityBus_storage4_1_2) <= 80
   0 <= flow(electricityBus_storage4_1_3) <= 80
   0 <= flow(electricityBus_storage4_2_4) <= 80
   0 <= flow(electricityBus_storage4_2_5) <= 80
   0 <= flow(storage4_electricityBus_0_0) <= 100
   0 <= flow(storage4_electricityBus_0_1) <= 100
   0 <= flow(storage4_electricityBus_1_2) <= 100
   0 <= flow(storage4_electricityBus_1_3) <= 100
   0 <= flow(storage4_electricityBus_2_4) <= 100
   0 <= flow(storage4_electricityBus_2_5) <= 100
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage4_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage4_0) <= 500
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage4_1) <= 500
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage4_2) <= 500
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage4_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage4_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage4_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage4_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage4_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage4_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage4_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage4_2) <= +inf
end
