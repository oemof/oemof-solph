\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+73.388061750348399 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+71.949080147400394 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_1)
+70.53831387000038 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_2)
+90 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
+88.235294117647058 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
+86.505190311418687 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
+12.231343625058066 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_0)
+11.991513357900065 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_1)
+11.756385645000064 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_2)
+12.231343625058066 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_0)
+11.991513357900065 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_1)
+11.756385645000064 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_2)
+10 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_0)
+9.8039215686274499 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_1)
+9.6116878123798539 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_2)
+15 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_0)
+14.705882352941176 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_1)
+14.41753171856978 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_2)

s.t.

c_e_MultiPeriodBus_balance(bus1_0_0)_:
-1 flow(bus1_storage_all_nonconvex_0_0)
+1 flow(storage_all_nonconvex_bus1_0_0)
= 0

c_e_MultiPeriodBus_balance(bus1_0_1)_:
-1 flow(bus1_storage_all_nonconvex_0_1)
+1 flow(storage_all_nonconvex_bus1_0_1)
= 0

c_e_MultiPeriodBus_balance(bus1_1_2)_:
-1 flow(bus1_storage_all_nonconvex_1_2)
+1 flow(storage_all_nonconvex_bus1_1_2)
= 0

c_e_MultiPeriodBus_balance(bus1_1_3)_:
-1 flow(bus1_storage_all_nonconvex_1_3)
+1 flow(storage_all_nonconvex_bus1_1_3)
= 0

c_e_MultiPeriodBus_balance(bus1_2_4)_:
-1 flow(bus1_storage_all_nonconvex_2_4)
+1 flow(storage_all_nonconvex_bus1_2_4)
= 0

c_e_MultiPeriodBus_balance(bus1_2_5)_:
-1 flow(bus1_storage_all_nonconvex_2_5)
+1 flow(storage_all_nonconvex_bus1_2_5)
= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(bus1_storage_all_nonconvex_0)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_0)
+5 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(bus1_storage_all_nonconvex_1)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_1)
+5 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_1)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(bus1_storage_all_nonconvex_2)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_2)
+5 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_2)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(storage_all_nonconvex_bus1_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_0)
+8 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(storage_all_nonconvex_bus1_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_1)
+8 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_1)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(storage_all_nonconvex_bus1_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_2)
+8 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(bus1_storage_all_nonconvex_0)_:
+1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_0)
-30 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(bus1_storage_all_nonconvex_1)_:
+1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_1)
-30 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_1)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(bus1_storage_all_nonconvex_2)_:
+1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_2)
-30 MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_2)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(storage_all_nonconvex_bus1_0)_:
+1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_0)
-20 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(storage_all_nonconvex_bus1_1)_:
+1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_1)
-20 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_1)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(storage_all_nonconvex_bus1_2)_:
+1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_2)
-20 MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_2)
<= 0

c_e_MultiPeriodInvestmentFlow_total_rule(bus1_storage_all_nonconvex_0)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_0)
+1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(bus1_storage_all_nonconvex_1)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_1)
+1 MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_1)
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_0)
+1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(bus1_storage_all_nonconvex_2)_:
-1 MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_2)
+1 MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_2)
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_1)
+1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_all_nonconvex_bus1_0)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_0)
+1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_all_nonconvex_bus1_1)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_1)
+1 MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_1)
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_0)
+1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(storage_all_nonconvex_bus1_2)_:
-1 MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_2)
+1 MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_2)
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_1)
+1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(bus1_storage_all_nonconvex_0)_:
+1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(bus1_storage_all_nonconvex_1)_:
+1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(bus1_storage_all_nonconvex_2)_:
+1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_all_nonconvex_bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_all_nonconvex_bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(storage_all_nonconvex_bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(bus1_storage_all_nonconvex_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(bus1_storage_all_nonconvex_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(bus1_storage_all_nonconvex_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_all_nonconvex_bus1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_all_nonconvex_bus1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(storage_all_nonconvex_bus1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(bus1_storage_all_nonconvex_0)_:
+1 MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_0)
-1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_0)
-1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(bus1_storage_all_nonconvex_1)_:
+1 MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_1)
-1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_1)
-1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(bus1_storage_all_nonconvex_2)_:
+1 MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_2)
-1 MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_2)
-1 MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_all_nonconvex_bus1_0)_:
+1 MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_0)
-1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_0)
-1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_all_nonconvex_bus1_1)_:
+1 MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_1)
-1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_1)
-1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(storage_all_nonconvex_bus1_2)_:
+1 MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_2)
-1 MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_2)
-1 MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_0_0)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_0)
+1 flow(bus1_storage_all_nonconvex_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_0_1)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_0)
+1 flow(bus1_storage_all_nonconvex_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_1_2)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_1)
+1 flow(bus1_storage_all_nonconvex_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_1_3)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_1)
+1 flow(bus1_storage_all_nonconvex_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_2_4)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_2)
+1 flow(bus1_storage_all_nonconvex_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(bus1_storage_all_nonconvex_2_5)_:
-1 MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_2)
+1 flow(bus1_storage_all_nonconvex_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_0)
+1 flow(storage_all_nonconvex_bus1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_0)
+1 flow(storage_all_nonconvex_bus1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_1)
+1 flow(storage_all_nonconvex_bus1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_1)
+1 flow(storage_all_nonconvex_bus1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_2)
+1 flow(storage_all_nonconvex_bus1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(storage_all_nonconvex_bus1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_2)
+1 flow(storage_all_nonconvex_bus1_2_5)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_2)
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_all_nonconvex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_all_nonconvex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_old_rule(storage_all_nonconvex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_2)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_storage_level_noinv_rule(storage_all_nonconvex_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2)
<= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance_first(storage_all_nonconvex)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
-1 flow(bus1_storage_all_nonconvex_0_0)
+1 flow(storage_all_nonconvex_bus1_0_0)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_all_nonconvex_0_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
-1 flow(bus1_storage_all_nonconvex_0_1)
+1 flow(storage_all_nonconvex_bus1_0_1)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_all_nonconvex_1_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
-1 flow(bus1_storage_all_nonconvex_1_2)
+1 flow(storage_all_nonconvex_bus1_1_2)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_all_nonconvex_1_3)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
-1 flow(bus1_storage_all_nonconvex_1_3)
+1 flow(storage_all_nonconvex_bus1_1_3)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_all_nonconvex_2_4)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
-1 flow(bus1_storage_all_nonconvex_2_4)
+1 flow(storage_all_nonconvex_bus1_2_4)
= 0

c_e_GenericMultiPeriodInvestmentStorageBlock_balance(storage_all_nonconvex_2_5)_:
-1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_5)
-1 flow(bus1_storage_all_nonconvex_2_5)
+1 flow(storage_all_nonconvex_bus1_2_5)
= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_1_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_1_3)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_2_4)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2)
<= 0

c_u_GenericMultiPeriodInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_2_5)_:
+1 GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_5)
-1 GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2)
<= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_all_nonconvex_0)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+100 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_all_nonconvex_1)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_1)
+100 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_max(storage_all_nonconvex_2)_:
-1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_2)
+100 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_all_nonconvex_0)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_0)
-20 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_all_nonconvex_1)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_1)
-20 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
>= 0

c_l_GenericMultiPeriodInvestmentStorageBlock_limit_min(storage_all_nonconvex_2)_:
+1 GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_2)
-20 GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
>= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus1_storage_all_nonconvex_0_0) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_1) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_1_2) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_1_3) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_2_4) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_2_5) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0_0) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0_1) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_1_2) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_1_3) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_2_4) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_0) <= 30
   0 <= MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_1) <= 30
   0 <= MultiPeriodInvestmentFlow_invest(bus1_storage_all_nonconvex_2) <= 30
   0 <= MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_0) <= 20
   0 <= MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_1) <= 20
   0 <= MultiPeriodInvestmentFlow_invest(storage_all_nonconvex_bus1_2) <= 20
   0 <= MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(bus1_storage_all_nonconvex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(storage_all_nonconvex_bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(bus1_storage_all_nonconvex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(storage_all_nonconvex_bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(bus1_storage_all_nonconvex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(storage_all_nonconvex_bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(bus1_storage_all_nonconvex_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(storage_all_nonconvex_bus1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_0) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_1) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_2) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_0) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_1) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_2) <= 1
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_3) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_4) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_storage_content(storage_all_nonconvex_5) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_0) <= 100
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_1) <= 100
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest(storage_all_nonconvex_2) <= 100
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_total(storage_all_nonconvex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old(storage_all_nonconvex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_end(storage_all_nonconvex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_0) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_1) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_old_exo(storage_all_nonconvex_2) <= +inf
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_0) <= 1
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_1) <= 1
   0 <= GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_2) <= 1
binary
  MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_0)
  MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_1)
  MultiPeriodInvestmentFlow_invest_status(bus1_storage_all_nonconvex_2)
  MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_0)
  MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_1)
  MultiPeriodInvestmentFlow_invest_status(storage_all_nonconvex_bus1_2)
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
  GenericMultiPeriodInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
end
