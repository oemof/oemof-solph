\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_2)
+150.44552658821425 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
+147.49561430217082 MultiPeriodInvestmentFlow_invest(Source_Bus1_1)
+144.60354343350082 MultiPeriodInvestmentFlow_invest(Source_Bus1_2)

s.t.

c_u_multiperiodinvestment_limit_:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_2)
+150.44552658821425 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
+147.49561430217082 MultiPeriodInvestmentFlow_invest(Source_Bus1_1)
+144.60354343350082 MultiPeriodInvestmentFlow_invest(Source_Bus1_2)
<= 900

c_e_MultiPeriodBus_balance(Bus1_0_0)_:
-1 flow(Bus1_storage_invest_limit_0_0)
+1 flow(Source_Bus1_0_0)
+1 flow(storage_invest_limit_Bus1_0_0)
= 0

c_e_MultiPeriodBus_balance(Bus1_0_1)_:
-1 flow(Bus1_storage_invest_limit_0_1)
+1 flow(Source_Bus1_0_1)
+1 flow(storage_invest_limit_Bus1_0_1)
= 0

c_e_MultiPeriodBus_balance(Bus1_1_2)_:
-1 flow(Bus1_storage_invest_limit_1_2)
+1 flow(Source_Bus1_1_2)
+1 flow(storage_invest_limit_Bus1_1_2)
= 0

c_e_MultiPeriodBus_balance(Bus1_1_3)_:
-1 flow(Bus1_storage_invest_limit_1_3)
+1 flow(Source_Bus1_1_3)
+1 flow(storage_invest_limit_Bus1_1_3)
= 0

c_e_MultiPeriodBus_balance(Bus1_2_4)_:
-1 flow(Bus1_storage_invest_limit_2_4)
+1 flow(Source_Bus1_2_4)
+1 flow(storage_invest_limit_Bus1_2_4)
= 0

c_e_MultiPeriodBus_balance(Bus1_2_5)_:
-1 flow(Bus1_storage_invest_limit_2_5)
+1 flow(Source_Bus1_2_5)
+1 flow(storage_invest_limit_Bus1_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Source_Bus1_0)_:
-1 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
+1 MultiPeriodInvestmentFlow_total(Source_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Source_Bus1_1)_:
-1 MultiPeriodInvestmentFlow_invest(Source_Bus1_1)
+1 MultiPeriodInvestmentFlow_old(Source_Bus1_1)
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_0)
+1 MultiPeriodInvestmentFlow_total(Source_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Source_Bus1_2)_:
-1 MultiPeriodInvestmentFlow_invest(Source_Bus1_2)
+1 MultiPeriodInvestmentFlow_old(Source_Bus1_2)
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_1)
+1 MultiPeriodInvestmentFlow_total(Source_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Source_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Source_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Source_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Source_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Source_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Source_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Source_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old(Source_Bus1_0)
-1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_0)
-1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Source_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old(Source_Bus1_1)
-1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_1)
-1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Source_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old(Source_Bus1_2)
-1 MultiPeriodInvestmentFlow_old_end(Source_Bus1_2)
-1 MultiPeriodInvestmentFlow_old_exo(Source_Bus1_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_0)
+1 flow(Source_Bus1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_0)
+1 flow(Source_Bus1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_1)
+1 flow(Source_Bus1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_1)
+1 flow(Source_Bus1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_2)
+1 flow(Source_Bus1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Source_Bus1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(Source_Bus1_2)
+1 flow(Source_Bus1_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_invest_limit_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_invest_limit_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_invest_limit_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_invest_limit_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_invest_limit_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_invest_limit_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_invest_limit_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_invest_limit_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_invest_limit_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_invest_limit_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_invest_limit_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_invest_limit_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_invest_limit_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage_invest_limit)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_0)
-1 flow(Bus1_storage_invest_limit_0_0)
+1 flow(storage_invest_limit_Bus1_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_invest_limit_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 flow(Bus1_storage_invest_limit_0_1)
+1 flow(storage_invest_limit_Bus1_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_invest_limit_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 flow(Bus1_storage_invest_limit_1_2)
+1 flow(storage_invest_limit_Bus1_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_invest_limit_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_3)
-1 flow(Bus1_storage_invest_limit_1_3)
+1 flow(storage_invest_limit_Bus1_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_invest_limit_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_4)
-1 flow(Bus1_storage_invest_limit_2_4)
+1 flow(storage_invest_limit_Bus1_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_invest_limit_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_5)
-1 flow(Bus1_storage_invest_limit_2_5)
+1 flow(storage_invest_limit_Bus1_2_5)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_storage_invest_limit_0_0) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_1) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1_2) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1_3) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2_4) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2_5) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_0) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_1) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1_3) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2_4) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_invest_limit_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_invest_limit_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_invest_limit_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_invest_limit_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_invest_limit_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_invest_limit_2) <= +inf
end
