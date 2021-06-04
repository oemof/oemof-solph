\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+177.35448256334197 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_0)
+173.87694368955096 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_1)
+170.46759185250093 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_2)
+1160.1371768813483 MultiPeriodInvestmentFlow_invest(Bus1_Sink_0)
+1137.3893890993611 MultiPeriodInvestmentFlow_invest(Bus1_Sink_1)
+1115.0876363719226 MultiPeriodInvestmentFlow_invest(Bus1_Sink_2)
+157.50284813348861 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
+154.41455699361629 MultiPeriodInvestmentFlow_invest(Source_Bus1_1)
+151.38682058197674 MultiPeriodInvestmentFlow_invest(Source_Bus1_2)

s.t.

c_e_equate_MultiPeriodInvestmentFlow_invest(Source_Bus1_0)_MultiPeriodInvestmentFlow_invest(Bus1_Sink_0)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_Sink_0)
+2 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
= 0

c_e_equate_MultiPeriodInvestmentFlow_invest(Source_Bus1_0)_GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_0)
+1 MultiPeriodInvestmentFlow_invest(Source_Bus1_0)
= 0

c_e_MultiPeriodBus_balance(Bus1_0_0)_:
-1 flow(Bus1_Sink_0_0)
-1 flow(Bus1_storage_constraint_0_0)
+1 flow(Source_Bus1_0_0)
+1 flow(storage_constraint_Bus1_0_0)
= 0

c_e_MultiPeriodBus_balance(Bus1_0_1)_:
-1 flow(Bus1_Sink_0_1)
-1 flow(Bus1_storage_constraint_0_1)
+1 flow(Source_Bus1_0_1)
+1 flow(storage_constraint_Bus1_0_1)
= 0

c_e_MultiPeriodBus_balance(Bus1_1_2)_:
-1 flow(Bus1_Sink_1_2)
-1 flow(Bus1_storage_constraint_1_2)
+1 flow(Source_Bus1_1_2)
+1 flow(storage_constraint_Bus1_1_2)
= 0

c_e_MultiPeriodBus_balance(Bus1_1_3)_:
-1 flow(Bus1_Sink_1_3)
-1 flow(Bus1_storage_constraint_1_3)
+1 flow(Source_Bus1_1_3)
+1 flow(storage_constraint_Bus1_1_3)
= 0

c_e_MultiPeriodBus_balance(Bus1_2_4)_:
-1 flow(Bus1_Sink_2_4)
-1 flow(Bus1_storage_constraint_2_4)
+1 flow(Source_Bus1_2_4)
+1 flow(storage_constraint_Bus1_2_4)
= 0

c_e_MultiPeriodBus_balance(Bus1_2_5)_:
-1 flow(Bus1_Sink_2_5)
-1 flow(Bus1_storage_constraint_2_5)
+1 flow(Source_Bus1_2_5)
+1 flow(storage_constraint_Bus1_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_Sink_0)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_Sink_0)
+1 MultiPeriodInvestmentFlow_total(Bus1_Sink_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_Sink_1)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_Sink_1)
+1 MultiPeriodInvestmentFlow_old(Bus1_Sink_1)
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_0)
+1 MultiPeriodInvestmentFlow_total(Bus1_Sink_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_Sink_2)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_Sink_2)
+1 MultiPeriodInvestmentFlow_old(Bus1_Sink_2)
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_1)
+1 MultiPeriodInvestmentFlow_total(Bus1_Sink_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_storage_constraint_0)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_0)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_storage_constraint_1)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_1)
+1 MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_1)
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(Bus1_storage_constraint_2)_:
-1 MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_2)
+1 MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_2)
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_2)
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

c_e_MultiPeriodInvestmentFlow_total_rule(storage_constraint_Bus1_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_0)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_constraint_Bus1_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_1)
+1 MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_1)
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_constraint_Bus1_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_2)
+1 MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_2)
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_Sink_0)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_Sink_1)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_Sink_2)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_storage_constraint_0)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_storage_constraint_1)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(Bus1_storage_constraint_2)_:
+1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_constraint_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_constraint_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_constraint_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_Sink_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_Sink_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_Sink_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_storage_constraint_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_storage_constraint_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(Bus1_storage_constraint_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_constraint_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_constraint_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_constraint_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_Sink_0)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_Sink_0)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_0)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_Sink_1)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_Sink_1)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_1)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_Sink_2)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_Sink_2)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_Sink_2)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_storage_constraint_0)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_0)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_0)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_storage_constraint_1)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_1)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_1)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(Bus1_storage_constraint_2)_:
+1 MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_2)
-1 MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_2)
-1 MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule(storage_constraint_Bus1_0)_:
+1 MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_0)
-1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_constraint_Bus1_1)_:
+1 MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_1)
-1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_constraint_Bus1_2)_:
+1 MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_2)
-1 MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_0_0)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_0)
+1 flow(Bus1_Sink_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_0_1)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_0)
+1 flow(Bus1_Sink_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_1_2)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_1)
+1 flow(Bus1_Sink_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_1_3)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_1)
+1 flow(Bus1_Sink_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_2_4)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_2)
+1 flow(Bus1_Sink_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_Sink_2_5)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_Sink_2)
+1 flow(Bus1_Sink_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_0_0)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0)
+1 flow(Bus1_storage_constraint_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_0_1)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0)
+1 flow(Bus1_storage_constraint_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_1_2)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1)
+1 flow(Bus1_storage_constraint_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_1_3)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1)
+1 flow(Bus1_storage_constraint_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_2_4)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_2)
+1 flow(Bus1_storage_constraint_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(Bus1_storage_constraint_2_5)_:
-1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_2)
+1 flow(Bus1_storage_constraint_2_5)
<= 0

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

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0)
+1 flow(storage_constraint_Bus1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0)
+1 flow(storage_constraint_Bus1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1)
+1 flow(storage_constraint_Bus1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1)
+1 flow(storage_constraint_Bus1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_2)
+1 flow(storage_constraint_Bus1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_constraint_Bus1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_2)
+1 flow(storage_constraint_Bus1_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_constraint_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_constraint_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_constraint_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_constraint_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_constraint_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_constraint_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_constraint_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_constraint_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_constraint_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_constraint_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_constraint_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_constraint_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_constraint_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage_constraint)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_0)
-1 flow(Bus1_storage_constraint_0_0)
+1 flow(storage_constraint_Bus1_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_constraint_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_1)
-1 flow(Bus1_storage_constraint_0_1)
+1 flow(storage_constraint_Bus1_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_constraint_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_2)
-1 flow(Bus1_storage_constraint_1_2)
+1 flow(storage_constraint_Bus1_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_constraint_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_3)
-1 flow(Bus1_storage_constraint_1_3)
+1 flow(storage_constraint_Bus1_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_constraint_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_4)
-1 flow(Bus1_storage_constraint_2_4)
+1 flow(storage_constraint_Bus1_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_constraint_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_5)
-1 flow(Bus1_storage_constraint_2_5)
+1 flow(storage_constraint_Bus1_2_5)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_constraint_0)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_constraint_1)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_inflow(storage_constraint_2)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
+1 MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_constraint_0)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_constraint_1)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_storage_capacity_outflow(storage_constraint_2)_:
-0.20000000000000001 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
+1 MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_constraint_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_Sink_0_0) <= +inf
   0 <= flow(Bus1_Sink_0_1) <= +inf
   0 <= flow(Bus1_Sink_1_2) <= +inf
   0 <= flow(Bus1_Sink_1_3) <= +inf
   0 <= flow(Bus1_Sink_2_4) <= +inf
   0 <= flow(Bus1_Sink_2_5) <= +inf
   0 <= flow(Bus1_storage_constraint_0_0) <= +inf
   0 <= flow(Bus1_storage_constraint_0_1) <= +inf
   0 <= flow(Bus1_storage_constraint_1_2) <= +inf
   0 <= flow(Bus1_storage_constraint_1_3) <= +inf
   0 <= flow(Bus1_storage_constraint_2_4) <= +inf
   0 <= flow(Bus1_storage_constraint_2_5) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(storage_constraint_Bus1_0_0) <= +inf
   0 <= flow(storage_constraint_Bus1_0_1) <= +inf
   0 <= flow(storage_constraint_Bus1_1_2) <= +inf
   0 <= flow(storage_constraint_Bus1_1_3) <= +inf
   0 <= flow(storage_constraint_Bus1_2_4) <= +inf
   0 <= flow(storage_constraint_Bus1_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_Sink_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_Sink_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_Sink_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Bus1_storage_constraint_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(storage_constraint_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_Sink_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_Sink_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_Sink_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Bus1_storage_constraint_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_constraint_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_Sink_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_Sink_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_Sink_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Bus1_storage_constraint_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_constraint_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_Sink_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_Sink_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_Sink_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Bus1_storage_constraint_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_constraint_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_Sink_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Bus1_storage_constraint_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(Source_Bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_constraint_Bus1_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_constraint_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_constraint_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_constraint_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_constraint_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_constraint_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_constraint_2) <= +inf
end
