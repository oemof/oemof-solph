\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)

s.t.

c_u_investment_limit_:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
<= 900

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
+1 flow(storage_invest_limit_Bus1_0_0)
-1 flow(Bus1_storage_invest_limit_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
+1 flow(storage_invest_limit_Bus1_0_1)
-1 flow(Bus1_storage_invest_limit_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
+1 flow(storage_invest_limit_Bus1_0_2)
-1 flow(Bus1_storage_invest_limit_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
-1 InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_invest_limit_Bus1_0)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
-1 InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_0)_:
+1 flow(Bus1_storage_invest_limit_0_0)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_1)_:
+1 flow(Bus1_storage_invest_limit_0_1)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_invest_limit_0_2)_:
+1 flow(Bus1_storage_invest_limit_0_2)
-1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_0)_:
+1 flow(storage_invest_limit_Bus1_0_0)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_1)_:
+1 flow(storage_invest_limit_Bus1_0_1)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_invest_limit_Bus1_0_2)_:
+1 flow(storage_invest_limit_Bus1_0_2)
-1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_invest_limit_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage_invest_limit)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage_invest_limit)_:
+1 flow(storage_invest_limit_Bus1_0_0)
-1 flow(Bus1_storage_invest_limit_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_0_1)_:
+1 flow(storage_invest_limit_Bus1_0_1)
-1 flow(Bus1_storage_invest_limit_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_0_2)_:
+1 flow(storage_invest_limit_Bus1_0_2)
-1 flow(Bus1_storage_invest_limit_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage_invest_limit)_:
-1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_invest_limit_0)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit_0)_:
+1 InvestmentFlowBlock_total(storage_invest_limit_Bus1_0)
-0.2 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit_0) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_0) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_1) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_1) <= +inf
   0 <= flow(Source_Bus1_0_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0_2) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_invest_limit_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_invest_limit_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage_invest_limit) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2) <= +inf
end
