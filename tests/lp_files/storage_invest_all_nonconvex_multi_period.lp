\* Source Pyomo model name=Model *\

min 
objective:
+1.7636883641156018 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+15 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
+1.164112696220594 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_1)
+14.705882352941176 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_1)
+0.5762934139705919 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_2)
+14.41753171856978 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_2)
+1.7636883641156018 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+10 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
+1.164112696220594 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_1)
+9.80392156862745 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_1)
+0.5762934139705919 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_2)
+9.611687812379854 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_2)
+3.5273767282312036 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+30 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
+2.328225392441188 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_1)
+29.41176470588235 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
+1.1525868279411837 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_2)
+28.83506343713956 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)

s.t.

c_e_BusBlock_balance(bus1_0_0)_:
+1 flow(storage_all_nonconvex_bus1_0_0)
-1 flow(bus1_storage_all_nonconvex_0_0)
= 0

c_e_BusBlock_balance(bus1_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 flow(bus1_storage_all_nonconvex_0_1)
= 0

c_e_BusBlock_balance(bus1_1_2)_:
+1 flow(storage_all_nonconvex_bus1_1_2)
-1 flow(bus1_storage_all_nonconvex_1_2)
= 0

c_e_BusBlock_balance(bus1_1_3)_:
+1 flow(storage_all_nonconvex_bus1_1_3)
-1 flow(bus1_storage_all_nonconvex_1_3)
= 0

c_e_BusBlock_balance(bus1_2_4)_:
+1 flow(storage_all_nonconvex_bus1_2_4)
-1 flow(bus1_storage_all_nonconvex_2_4)
= 0

c_e_BusBlock_balance(bus1_2_5)_:
+1 flow(storage_all_nonconvex_bus1_2_5)
-1 flow(bus1_storage_all_nonconvex_2_5)
= 0

c_u_InvestmentFlowBlock_minimum_rule(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+8 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(storage_all_nonconvex_bus1_1)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_1)
+8 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_1)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(storage_all_nonconvex_bus1_2)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_2)
+8 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_2)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+5 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(bus1_storage_all_nonconvex_1)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_1)
+5 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_1)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(bus1_storage_all_nonconvex_2)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_2)
+5 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_2)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(storage_all_nonconvex_bus1_0)_:
+1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
-20 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(storage_all_nonconvex_bus1_1)_:
+1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_1)
-20 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_1)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(storage_all_nonconvex_bus1_2)_:
+1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_2)
-20 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_2)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(bus1_storage_all_nonconvex_0)_:
+1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
-30 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(bus1_storage_all_nonconvex_1)_:
+1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_1)
-30 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_1)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(bus1_storage_all_nonconvex_2)_:
+1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_2)
-30 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_2)
<= 0

c_e_InvestmentFlowBlock_total_rule(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_all_nonconvex_bus1_1)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_1)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
+1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_1)
+1 InvestmentFlowBlock_old(storage_all_nonconvex_bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_all_nonconvex_bus1_2)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_2)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_1)
+1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_2)
+1 InvestmentFlowBlock_old(storage_all_nonconvex_bus1_2)
= 0

c_e_InvestmentFlowBlock_total_rule(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
= 0

c_e_InvestmentFlowBlock_total_rule(bus1_storage_all_nonconvex_1)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_1)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
+1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_1)
+1 InvestmentFlowBlock_old(bus1_storage_all_nonconvex_1)
= 0

c_e_InvestmentFlowBlock_total_rule(bus1_storage_all_nonconvex_2)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_2)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_1)
+1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_2)
+1 InvestmentFlowBlock_old(bus1_storage_all_nonconvex_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_all_nonconvex_bus1_0)_:
+1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_all_nonconvex_bus1_1)_:
+1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_all_nonconvex_bus1_2)_:
+1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus1_storage_all_nonconvex_0)_:
+1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus1_storage_all_nonconvex_1)_:
+1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(bus1_storage_all_nonconvex_2)_:
+1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_all_nonconvex_bus1_0)_:
+1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_all_nonconvex_bus1_1)_:
+1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_all_nonconvex_bus1_2)_:
+1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus1_storage_all_nonconvex_0)_:
+1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus1_storage_all_nonconvex_1)_:
+1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(bus1_storage_all_nonconvex_2)_:
+1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_0)
-1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_0)
+1 InvestmentFlowBlock_old(storage_all_nonconvex_bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_all_nonconvex_bus1_1)_:
+1 InvestmentFlowBlock_old(storage_all_nonconvex_bus1_1)
-1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_1)
-1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_all_nonconvex_bus1_2)_:
+1 InvestmentFlowBlock_old(storage_all_nonconvex_bus1_2)
-1 InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_2)
-1 InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_0)
-1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_0)
+1 InvestmentFlowBlock_old(bus1_storage_all_nonconvex_0)
= 0

c_e_InvestmentFlowBlock_old_rule(bus1_storage_all_nonconvex_1)_:
+1 InvestmentFlowBlock_old(bus1_storage_all_nonconvex_1)
-1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_1)
-1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_1)
= 0

c_e_InvestmentFlowBlock_old_rule(bus1_storage_all_nonconvex_2)_:
+1 InvestmentFlowBlock_old(bus1_storage_all_nonconvex_2)
-1 InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_2)
-1 InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_2)
= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_0_0)_:
+1 flow(storage_all_nonconvex_bus1_0_0)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_1_2)_:
+1 flow(storage_all_nonconvex_bus1_1_2)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_1_3)_:
+1 flow(storage_all_nonconvex_bus1_1_3)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_2_4)_:
+1 flow(storage_all_nonconvex_bus1_2_4)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_2_5)_:
+1 flow(storage_all_nonconvex_bus1_2_5)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_0_0)_:
+1 flow(bus1_storage_all_nonconvex_0_0)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_0_1)_:
+1 flow(bus1_storage_all_nonconvex_0_1)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_1_2)_:
+1 flow(bus1_storage_all_nonconvex_1_2)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_1)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_1_3)_:
+1 flow(bus1_storage_all_nonconvex_1_3)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_1)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_2_4)_:
+1 flow(bus1_storage_all_nonconvex_2_4)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_2)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_2_5)_:
+1 flow(bus1_storage_all_nonconvex_2_5)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_1)
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_old(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_2)
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_2)
+1 GenericInvestmentStorageBlock_old(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_all_nonconvex_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_all_nonconvex_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_old(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_all_nonconvex_1)_:
+1 GenericInvestmentStorageBlock_old(storage_all_nonconvex_1)
-1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_all_nonconvex_2)_:
+1 GenericInvestmentStorageBlock_old(storage_all_nonconvex_2)
-1 GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage_all_nonconvex_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 flow(bus1_storage_all_nonconvex_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_1_2)_:
+1 flow(storage_all_nonconvex_bus1_1_2)
-1 flow(bus1_storage_all_nonconvex_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_1_3)_:
+1 flow(storage_all_nonconvex_bus1_1_3)
-1 flow(bus1_storage_all_nonconvex_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_2_4)_:
+1 flow(storage_all_nonconvex_bus1_2_4)
-1 flow(bus1_storage_all_nonconvex_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_2_5)_:
+1 flow(storage_all_nonconvex_bus1_2_5)
-1 flow(bus1_storage_all_nonconvex_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_5)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_5)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+100 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_all_nonconvex_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_1)
+100 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
>= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_all_nonconvex_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_2)
+100 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_all_nonconvex_0)_:
+1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
-20 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_all_nonconvex_1)_:
+1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_1)
-20 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_all_nonconvex_2)_:
+1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_2)
-20 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
>= 0

bounds
   0 <= InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0) <= 20
   0 <= InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0) <= 1
   0 <= InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_1) <= 20
   0 <= InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_1) <= 1
   0 <= InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_2) <= 20
   0 <= InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_2) <= 1
   0 <= InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0) <= 30
   0 <= InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0) <= 1
   0 <= InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_1) <= 30
   0 <= InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_1) <= 1
   0 <= InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_2) <= 30
   0 <= InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_2) <= 1
   0 <= GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0) <= 100
   0 <= GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0) <= 1
   0 <= GenericInvestmentStorageBlock_invest(storage_all_nonconvex_1) <= 100
   0 <= GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_1) <= 1
   0 <= GenericInvestmentStorageBlock_invest(storage_all_nonconvex_2) <= 100
   0 <= GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_2) <= 1
   0 <= flow(storage_all_nonconvex_bus1_0_0) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_0) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0_1) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_1) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_1_2) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_1_2) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_1_3) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_1_3) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_2_4) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_2_4) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_2_5) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_all_nonconvex_bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_all_nonconvex_bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_all_nonconvex_bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_all_nonconvex_bus1_2) <= +inf
   0 <= InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0) <= +inf
   0 <= InvestmentFlowBlock_total(bus1_storage_all_nonconvex_1) <= +inf
   0 <= InvestmentFlowBlock_old(bus1_storage_all_nonconvex_1) <= +inf
   0 <= InvestmentFlowBlock_total(bus1_storage_all_nonconvex_2) <= +inf
   0 <= InvestmentFlowBlock_old(bus1_storage_all_nonconvex_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_all_nonconvex_bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(bus1_storage_all_nonconvex_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_all_nonconvex_bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(bus1_storage_all_nonconvex_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_all_nonconvex_bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old(bus1_storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_5) <= +inf
binary
  InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
  InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_1)
  InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_2)
  InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
  InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_1)
  InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_2)
  GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
  GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_1)
  GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_2)
end
