\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_2)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage1_0_0)
+1 flow(storage1_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage1_0_1)
+1 flow(storage1_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage1_1_2)
+1 flow(storage1_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage1_1_3)
+1 flow(storage1_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage1_2_4)
+1 flow(storage1_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage1_2_5)
+1 flow(storage1_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage1_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage1_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage1_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage1_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage1_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage1_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage1_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage1_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage1_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage1_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage1_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage1_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage1_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage1_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage1_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_0)
-1 flow(electricityBus_storage1_0_0)
+1 flow(storage1_electricityBus_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage1_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_1)
-1 flow(electricityBus_storage1_0_1)
+1 flow(storage1_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage1_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_2)
-1 flow(electricityBus_storage1_1_2)
+1 flow(storage1_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage1_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_3)
-1 flow(electricityBus_storage1_1_3)
+1 flow(storage1_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage1_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_4)
-1 flow(electricityBus_storage1_2_4)
+1 flow(storage1_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage1_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_5)
-1 flow(electricityBus_storage1_2_5)
+1 flow(storage1_electricityBus_2_5)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage1_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage1_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

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
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage1_5) <= +inf
   100 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage1_0) <= 200
   100 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage1_1) <= 200
   100 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage1_2) <= 200
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage1_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage1_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage1_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage1_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage1_2) <= +inf
end
