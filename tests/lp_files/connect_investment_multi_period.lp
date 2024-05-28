\* Source Pyomo model name=Model *\

min 
objective:
+499.99999999999994 InvestmentFlowBlock_invest(Bus1_Sink_0)
+330.02221931773533 InvestmentFlowBlock_invest(Bus1_Sink_1)
+163.37733629590875 InvestmentFlowBlock_invest(Bus1_Sink_2)
+123.0 InvestmentFlowBlock_invest(Source_Bus1_0)
+81.1854659521629 InvestmentFlowBlock_invest(Source_Bus1_1)
+40.19082472879356 InvestmentFlowBlock_invest(Source_Bus1_2)
+144.99999999999997 GenericInvestmentStorageBlock_invest(storage_0)
+95.70644360214325 GenericInvestmentStorageBlock_invest(storage_1)
+47.37942752581354 GenericInvestmentStorageBlock_invest(storage_2)

s.t.

c_e__equate_InvestmentFlowBlock_invest(Source_Bus1_0)_InvestmentFlowBlock_invest(Bus1_Sink_0)__:
-1 InvestmentFlowBlock_invest(Bus1_Sink_0)
+2 InvestmentFlowBlock_invest(Source_Bus1_0)
= 0

c_e__equate_InvestmentFlowBlock_invest(Source_Bus1_0)_GenericInvestmentStorageBlock_invest(storage_0)__:
+1 InvestmentFlowBlock_invest(Source_Bus1_0)
-1 GenericInvestmentStorageBlock_invest(storage_0)
= 0

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(storage_Bus1_0_0)
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_storage_0_0)
-1 flow(Bus1_Sink_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(storage_Bus1_0_1)
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_storage_0_1)
-1 flow(Bus1_Sink_0_1)
= 0

c_e_BusBlock_balance(Bus1_1_2)_:
+1 flow(storage_Bus1_1_2)
+1 flow(Source_Bus1_1_2)
-1 flow(Bus1_storage_1_2)
-1 flow(Bus1_Sink_1_2)
= 0

c_e_BusBlock_balance(Bus1_1_3)_:
+1 flow(storage_Bus1_1_3)
+1 flow(Source_Bus1_1_3)
-1 flow(Bus1_storage_1_3)
-1 flow(Bus1_Sink_1_3)
= 0

c_e_BusBlock_balance(Bus1_2_4)_:
+1 flow(storage_Bus1_2_4)
+1 flow(Source_Bus1_2_4)
-1 flow(Bus1_storage_2_4)
-1 flow(Bus1_Sink_2_4)
= 0

c_e_BusBlock_balance(Bus1_2_5)_:
+1 flow(storage_Bus1_2_5)
+1 flow(Source_Bus1_2_5)
-1 flow(Bus1_storage_2_5)
-1 flow(Bus1_Sink_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_Sink_0)_:
-1 InvestmentFlowBlock_invest(Bus1_Sink_0)
+1 InvestmentFlowBlock_total(Bus1_Sink_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_Sink_1)_:
-1 InvestmentFlowBlock_invest(Bus1_Sink_1)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
+1 InvestmentFlowBlock_total(Bus1_Sink_1)
+1 InvestmentFlowBlock_old(Bus1_Sink_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_Sink_2)_:
-1 InvestmentFlowBlock_invest(Bus1_Sink_2)
-1 InvestmentFlowBlock_total(Bus1_Sink_1)
+1 InvestmentFlowBlock_total(Bus1_Sink_2)
+1 InvestmentFlowBlock_old(Bus1_Sink_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_0)
-1 InvestmentFlowBlock_invest(Bus1_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_1)_:
-1 InvestmentFlowBlock_total(Bus1_storage_0)
+1 InvestmentFlowBlock_total(Bus1_storage_1)
-1 InvestmentFlowBlock_invest(Bus1_storage_1)
+1 InvestmentFlowBlock_old(Bus1_storage_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_2)_:
-1 InvestmentFlowBlock_total(Bus1_storage_1)
+1 InvestmentFlowBlock_total(Bus1_storage_2)
-1 InvestmentFlowBlock_invest(Bus1_storage_2)
+1 InvestmentFlowBlock_old(Bus1_storage_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_1)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 InvestmentFlowBlock_old(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_2)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_2)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 InvestmentFlowBlock_total(Source_Bus1_2)
+1 InvestmentFlowBlock_old(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_Bus1_0)_:
+1 InvestmentFlowBlock_total(storage_Bus1_0)
-1 InvestmentFlowBlock_invest(storage_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_Bus1_1)_:
-1 InvestmentFlowBlock_total(storage_Bus1_0)
+1 InvestmentFlowBlock_total(storage_Bus1_1)
-1 InvestmentFlowBlock_invest(storage_Bus1_1)
+1 InvestmentFlowBlock_old(storage_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_Bus1_2)_:
-1 InvestmentFlowBlock_total(storage_Bus1_1)
+1 InvestmentFlowBlock_total(storage_Bus1_2)
-1 InvestmentFlowBlock_invest(storage_Bus1_2)
+1 InvestmentFlowBlock_old(storage_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_Sink_0)_:
+1 InvestmentFlowBlock_old_end(Bus1_Sink_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_Sink_1)_:
+1 InvestmentFlowBlock_old_end(Bus1_Sink_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_Sink_2)_:
+1 InvestmentFlowBlock_old_end(Bus1_Sink_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_0)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_1)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_2)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_0)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_Bus1_0)_:
+1 InvestmentFlowBlock_old_end(storage_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_Bus1_1)_:
+1 InvestmentFlowBlock_old_end(storage_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_Bus1_2)_:
+1 InvestmentFlowBlock_old_end(storage_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_Sink_0)_:
+1 InvestmentFlowBlock_old_exo(Bus1_Sink_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_Sink_1)_:
+1 InvestmentFlowBlock_old_exo(Bus1_Sink_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_Sink_2)_:
+1 InvestmentFlowBlock_old_exo(Bus1_Sink_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_0)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_1)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_2)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_0)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_Bus1_0)_:
+1 InvestmentFlowBlock_old_exo(storage_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_Bus1_1)_:
+1 InvestmentFlowBlock_old_exo(storage_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_Bus1_2)_:
+1 InvestmentFlowBlock_old_exo(storage_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_Sink_0)_:
-1 InvestmentFlowBlock_old_end(Bus1_Sink_0)
-1 InvestmentFlowBlock_old_exo(Bus1_Sink_0)
+1 InvestmentFlowBlock_old(Bus1_Sink_0)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_Sink_1)_:
+1 InvestmentFlowBlock_old(Bus1_Sink_1)
-1 InvestmentFlowBlock_old_end(Bus1_Sink_1)
-1 InvestmentFlowBlock_old_exo(Bus1_Sink_1)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_Sink_2)_:
+1 InvestmentFlowBlock_old(Bus1_Sink_2)
-1 InvestmentFlowBlock_old_end(Bus1_Sink_2)
-1 InvestmentFlowBlock_old_exo(Bus1_Sink_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_0)_:
-1 InvestmentFlowBlock_old_end(Bus1_storage_0)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_0)
+1 InvestmentFlowBlock_old(Bus1_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_1)_:
+1 InvestmentFlowBlock_old(Bus1_storage_1)
-1 InvestmentFlowBlock_old_end(Bus1_storage_1)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_2)_:
+1 InvestmentFlowBlock_old(Bus1_storage_2)
-1 InvestmentFlowBlock_old_end(Bus1_storage_2)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_old_end(Source_Bus1_0)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_0)
+1 InvestmentFlowBlock_old(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old(Source_Bus1_1)
-1 InvestmentFlowBlock_old_end(Source_Bus1_1)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old(Source_Bus1_2)
-1 InvestmentFlowBlock_old_end(Source_Bus1_2)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_Bus1_0)_:
-1 InvestmentFlowBlock_old_end(storage_Bus1_0)
-1 InvestmentFlowBlock_old_exo(storage_Bus1_0)
+1 InvestmentFlowBlock_old(storage_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_Bus1_1)_:
+1 InvestmentFlowBlock_old(storage_Bus1_1)
-1 InvestmentFlowBlock_old_end(storage_Bus1_1)
-1 InvestmentFlowBlock_old_exo(storage_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_Bus1_2)_:
+1 InvestmentFlowBlock_old(storage_Bus1_2)
-1 InvestmentFlowBlock_old_end(storage_Bus1_2)
-1 InvestmentFlowBlock_old_exo(storage_Bus1_2)
= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_0_0)_:
+1 flow(Bus1_Sink_0_0)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_0_1)_:
+1 flow(Bus1_Sink_0_1)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_1_2)_:
+1 flow(Bus1_Sink_1_2)
-1 InvestmentFlowBlock_total(Bus1_Sink_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_1_3)_:
+1 flow(Bus1_Sink_1_3)
-1 InvestmentFlowBlock_total(Bus1_Sink_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_2_4)_:
+1 flow(Bus1_Sink_2_4)
-1 InvestmentFlowBlock_total(Bus1_Sink_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_2_5)_:
+1 flow(Bus1_Sink_2_5)
-1 InvestmentFlowBlock_total(Bus1_Sink_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_0_0)_:
+1 flow(Bus1_storage_0_0)
-1 InvestmentFlowBlock_total(Bus1_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_0_1)_:
+1 flow(Bus1_storage_0_1)
-1 InvestmentFlowBlock_total(Bus1_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_1_2)_:
+1 flow(Bus1_storage_1_2)
-1 InvestmentFlowBlock_total(Bus1_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_1_3)_:
+1 flow(Bus1_storage_1_3)
-1 InvestmentFlowBlock_total(Bus1_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_2_4)_:
+1 flow(Bus1_storage_2_4)
-1 InvestmentFlowBlock_total(Bus1_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_2_5)_:
+1 flow(Bus1_storage_2_5)
-1 InvestmentFlowBlock_total(Bus1_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_2)_:
+1 flow(Source_Bus1_1_2)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_3)_:
+1 flow(Source_Bus1_1_3)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_4)_:
+1 flow(Source_Bus1_2_4)
-1 InvestmentFlowBlock_total(Source_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_5)_:
+1 flow(Source_Bus1_2_5)
-1 InvestmentFlowBlock_total(Source_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_0_0)_:
+1 flow(storage_Bus1_0_0)
-1 InvestmentFlowBlock_total(storage_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_0_1)_:
+1 flow(storage_Bus1_0_1)
-1 InvestmentFlowBlock_total(storage_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_1_2)_:
+1 flow(storage_Bus1_1_2)
-1 InvestmentFlowBlock_total(storage_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_1_3)_:
+1 flow(storage_Bus1_1_3)
-1 InvestmentFlowBlock_total(storage_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_2_4)_:
+1 flow(storage_Bus1_2_4)
-1 InvestmentFlowBlock_total(storage_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_2_5)_:
+1 flow(storage_Bus1_2_5)
-1 InvestmentFlowBlock_total(storage_Bus1_2)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_1)
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_old(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_2)
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_old(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_0)
+1 GenericInvestmentStorageBlock_old(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_1)_:
+1 GenericInvestmentStorageBlock_old(storage_1)
-1 GenericInvestmentStorageBlock_old_end(storage_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_2)_:
+1 GenericInvestmentStorageBlock_old(storage_2)
-1 GenericInvestmentStorageBlock_old_end(storage_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_initially_empty(storage_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_Bus1_0_1)
-1 flow(Bus1_storage_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_2)_:
+1 flow(storage_Bus1_1_2)
-1 flow(Bus1_storage_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_3)_:
+1 flow(storage_Bus1_1_3)
-1 flow(Bus1_storage_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_4)_:
+1 flow(storage_Bus1_2_4)
-1 flow(Bus1_storage_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_5)_:
+1 flow(storage_Bus1_2_5)
-1 flow(Bus1_storage_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_0)
-0.2 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_1)_:
+1 InvestmentFlowBlock_total(Bus1_storage_1)
-0.2 GenericInvestmentStorageBlock_total(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_2)_:
+1 InvestmentFlowBlock_total(Bus1_storage_2)
-0.2 GenericInvestmentStorageBlock_total(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_0)_:
+1 InvestmentFlowBlock_total(storage_Bus1_0)
-0.2 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_1)_:
+1 InvestmentFlowBlock_total(storage_Bus1_1)
-0.2 GenericInvestmentStorageBlock_total(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_2)_:
+1 InvestmentFlowBlock_total(storage_Bus1_2)
-0.2 GenericInvestmentStorageBlock_total(storage_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_Sink_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_Sink_2) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_2) <= +inf
   0 <= flow(storage_Bus1_0_0) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_storage_0_0) <= +inf
   0 <= flow(Bus1_Sink_0_0) <= +inf
   0 <= flow(storage_Bus1_0_1) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_storage_0_1) <= +inf
   0 <= flow(Bus1_Sink_0_1) <= +inf
   0 <= flow(storage_Bus1_1_2) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Bus1_storage_1_2) <= +inf
   0 <= flow(Bus1_Sink_1_2) <= +inf
   0 <= flow(storage_Bus1_1_3) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Bus1_storage_1_3) <= +inf
   0 <= flow(Bus1_Sink_1_3) <= +inf
   0 <= flow(storage_Bus1_2_4) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Bus1_storage_2_4) <= +inf
   0 <= flow(Bus1_Sink_2_4) <= +inf
   0 <= flow(storage_Bus1_2_5) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(Bus1_storage_2_5) <= +inf
   0 <= flow(Bus1_Sink_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_Sink_1) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_Sink_1) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_Sink_2) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_Sink_2) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_1) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_2) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_Sink_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_Sink_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_Sink_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_Sink_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_Bus1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_5) <= +inf
end
