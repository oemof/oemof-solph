\* Source Pyomo model name=Model *\

min 
objective:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+18.670948783910358 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+12.323655908867737 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
+6.1008197568652225 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)

s.t.

c_u_investment_limit_per_period(0)_:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+18.670948783910358 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
<= 500

c_u_investment_limit_per_period(1)_:
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+12.323655908867737 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
<= 400

c_u_investment_limit_per_period(2)_:
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+6.1008197568652225 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)
<= 300

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(storage_invest_limit_Bus1_0_0)
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_storage_invest_limit_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(storage_invest_limit_Bus1_0_1)
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_storage_invest_limit_0_1)
= 0

c_e_BusBlock_balance(Bus1_1_2)_:
+1 flow(storage_invest_limit_Bus1_1_2)
+1 flow(Source_Bus1_1_2)
-1 flow(Bus1_storage_invest_limit_1_2)
= 0

c_e_BusBlock_balance(Bus1_1_3)_:
+1 flow(storage_invest_limit_Bus1_1_3)
+1 flow(Source_Bus1_1_3)
-1 flow(Bus1_storage_invest_limit_1_3)
= 0

c_e_BusBlock_balance(Bus1_2_4)_:
+1 flow(storage_invest_limit_Bus1_2_4)
+1 flow(Source_Bus1_2_4)
-1 flow(Bus1_storage_invest_limit_2_4)
= 0

c_e_BusBlock_balance(Bus1_2_5)_:
+1 flow(storage_invest_limit_Bus1_2_5)
+1 flow(Source_Bus1_2_5)
-1 flow(Bus1_storage_invest_limit_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_1)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_1)
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_2)_:
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_2)
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_1)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_1)
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_2)_:
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_2)
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_2)
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

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_1)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_invest_limit_Bus1_2)_:
+1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_2)
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

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_1)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_invest_limit_Bus1_2)_:
+1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_2)
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

c_e_InvestmentFlowBlock_old_rule(storage_invest_limit_Bus1_0)_:
-1 InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0)
-1 InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0)
+1 InvestmentFlowBlock_old(storage_invest_limit_Bus1_0)
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

c_e_InvestmentFlowBlock_old_rule(Bus1_storage_invest_limit_0)_:
-1 InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_0)
-1 InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_0)
+1 InvestmentFlowBlock_old(Bus1_storage_invest_limit_0)
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

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_0)_:
+1 flow(storage_invest_limit_Bus1_0_0)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_1)_:
+1 flow(storage_invest_limit_Bus1_0_1)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_1_2)_:
+1 flow(storage_invest_limit_Bus1_1_2)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_1_3)_:
+1 flow(storage_invest_limit_Bus1_1_3)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_2_4)_:
+1 flow(storage_invest_limit_Bus1_2_4)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_2_5)_:
+1 flow(storage_invest_limit_Bus1_2_5)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_0)_:
+1 flow(Bus1_storage_invest_limit_0_0)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_1)_:
+1 flow(Bus1_storage_invest_limit_0_1)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_1_2)_:
+1 flow(Bus1_storage_invest_limit_1_2)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_1_3)_:
+1 flow(Bus1_storage_invest_limit_1_3)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_2_4)_:
+1 flow(Bus1_storage_invest_limit_2_4)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_2_5)_:
+1 flow(Bus1_storage_invest_limit_2_5)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
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

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_2)
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
-1 GenericInvestmentStorageBlock_old_end(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_old(storage_invest_limit_0)
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

c_e_GenericInvestmentStorageBlock_initially_empty(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_0_1)_:
+1 flow(storage_invest_limit_Bus1_0_1)
-1 flow(Bus1_storage_invest_limit_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1_2)_:
+1 flow(storage_invest_limit_Bus1_1_2)
-1 flow(Bus1_storage_invest_limit_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1_3)_:
+1 flow(storage_invest_limit_Bus1_1_3)
-1 flow(Bus1_storage_invest_limit_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2_4)_:
+1 flow(storage_invest_limit_Bus1_2_4)
-1 flow(Bus1_storage_invest_limit_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2_5)_:
+1 flow(storage_invest_limit_Bus1_2_5)
-1 flow(Bus1_storage_invest_limit_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_1)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_1)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_2)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_2)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_1)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_1)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_2)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_2)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_0) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_0) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_1) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_1) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1_2) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1_3) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1_3) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2_4) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2_4) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2_5) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Bus1_storage_invest_limit_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_5) <= +inf
end
