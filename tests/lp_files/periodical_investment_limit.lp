\* Source Pyomo model name=Model *\

min 
objective:
+194.22716197630274 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+190.4187862512772 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
+186.68508456007567 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)
+285.39374551281168 InvestmentFlowBlock_invest(Source_Bus1_0)
+279.7977897184428 InvestmentFlowBlock_invest(Source_Bus1_1)
+274.31155854749295 InvestmentFlowBlock_invest(Source_Bus1_2)

s.t.

c_u_investment_limit_per_period(0)_:
+194.22716197630274 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+285.39374551281168 InvestmentFlowBlock_invest(Source_Bus1_0)
<= 500

c_u_investment_limit_per_period(1)_:
+190.4187862512772 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
+279.7977897184428 InvestmentFlowBlock_invest(Source_Bus1_1)
<= 400

c_u_investment_limit_per_period(2)_:
+186.68508456007567 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)
+274.31155854749295 InvestmentFlowBlock_invest(Source_Bus1_2)
<= 300

c_e_BusBlock_balance(Bus1_0_0)_:
-1 flow(Bus1_storage_invest_limit_0_0)
+1 flow(Source_Bus1_0_0)
+1 flow(storage_invest_limit_Bus1_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
-1 flow(Bus1_storage_invest_limit_0_1)
+1 flow(Source_Bus1_0_1)
+1 flow(storage_invest_limit_Bus1_0_1)
= 0

c_e_BusBlock_balance(Bus1_1_2)_:
-1 flow(Bus1_storage_invest_limit_1_2)
+1 flow(Source_Bus1_1_2)
+1 flow(storage_invest_limit_Bus1_1_2)
= 0

c_e_BusBlock_balance(Bus1_1_3)_:
-1 flow(Bus1_storage_invest_limit_1_3)
+1 flow(Source_Bus1_1_3)
+1 flow(storage_invest_limit_Bus1_1_3)
= 0

c_e_BusBlock_balance(Bus1_2_4)_:
-1 flow(Bus1_storage_invest_limit_2_4)
+1 flow(Source_Bus1_2_4)
+1 flow(storage_invest_limit_Bus1_2_4)
= 0

c_e_BusBlock_balance(Bus1_2_5)_:
-1 flow(Bus1_storage_invest_limit_2_5)
+1 flow(Source_Bus1_2_5)
+1 flow(storage_invest_limit_Bus1_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_0)_:
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_1)_:
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_1)
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_1)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_2)_:
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_2)
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_2)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_1)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_1)
+1 InvestmentFlowBlock_old(Source_Bus1_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_2)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_2)
+1 InvestmentFlowBlock_old(Source_Bus1_2)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 InvestmentFlowBlock_total(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_0)_:
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_1)_:
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_1)
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_1)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_2)_:
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_2)
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_2)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_invest_limit_0)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_invest_limit_1)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Bus1_storage_invest_limit_2)_:
+1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_2)
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

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_1)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_2)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_invest_limit_0)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_invest_limit_1)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Bus1_storage_invest_limit_2)_:
+1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_2)
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

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_1)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_2)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_invest_limit_0)_:
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_0)
-1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_0)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_invest_limit_1)_:
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_1)
-1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_1)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_1)
= 0

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_invest_limit_2)_:
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_2)
-1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_2)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_0)_:
+1 InvestmentFlowBlock_old(Source_Bus1_0)
-1 InvestmentFlowBlock_old_end(Source_Bus1_0)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_0)
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

c_e_InvestmentFlowBlock_old_rule(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_0)
-1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0)
-1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_invest_limit_Bus1_1)_:
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_1)
-1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_1)
-1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_invest_limit_Bus1_2)_:
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_2)
-1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_2)
-1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_2)
= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_0)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
+1 flow(Bus1_storage_invest_limit_0_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_1)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
+1 flow(Bus1_storage_invest_limit_0_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_1_2)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
+1 flow(Bus1_storage_invest_limit_1_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_1_3)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
+1 flow(Bus1_storage_invest_limit_1_3)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_2_4)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
+1 flow(Bus1_storage_invest_limit_2_4)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_2_5)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
+1 flow(Bus1_storage_invest_limit_2_5)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_0)_:
-1 InvestmentFlowBlock_total(Source_Bus1_0)
+1 flow(Source_Bus1_0_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_1)_:
-1 InvestmentFlowBlock_total(Source_Bus1_0)
+1 flow(Source_Bus1_0_1)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_2)_:
-1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 flow(Source_Bus1_1_2)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_3)_:
-1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 flow(Source_Bus1_1_3)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_4)_:
-1 InvestmentFlowBlock_total(Source_Bus1_2)
+1 flow(Source_Bus1_2_4)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_5)_:
-1 InvestmentFlowBlock_total(Source_Bus1_2)
+1 flow(Source_Bus1_2_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_0)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
+1 flow(storage_invest_limit_Bus1_0_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_1)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
+1 flow(storage_invest_limit_Bus1_0_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_1_2)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
+1 flow(storage_invest_limit_Bus1_1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_1_3)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
+1 flow(storage_invest_limit_Bus1_1_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_2_4)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
+1 flow(storage_invest_limit_Bus1_2_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_2_5)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
+1 flow(storage_invest_limit_Bus1_2_5)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_invest_limit_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_invest_limit_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_invest_limit_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_invest_limit_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_invest_limit_1)_:
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_invest_limit_2)_:
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_0_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 flow(Bus1_storage_invest_limit_0_1)
+1 flow(storage_invest_limit_Bus1_0_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 flow(Bus1_storage_invest_limit_1_2)
+1 flow(storage_invest_limit_Bus1_1_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1_3)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
-1 flow(Bus1_storage_invest_limit_1_3)
+1 flow(storage_invest_limit_Bus1_1_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2_4)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
-1 flow(Bus1_storage_invest_limit_2_4)
+1 flow(storage_invest_limit_Bus1_2_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2_5)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5)
-1 flow(Bus1_storage_invest_limit_2_5)
+1 flow(storage_invest_limit_Bus1_2_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_0)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_1)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_2)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_0)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_1)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_2)_:
-0.20000000000000001 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_1)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_2)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_3)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_4)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_5)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
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
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_2) <= +inf
end