\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+123 InvestmentFlow_invest(Source_Bus1)

s.t.

c_u_investment_limit_:
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+123 InvestmentFlow_invest(Source_Bus1)
<= 900

c_e_Bus_balance(Bus1_0)_:
-1 flow(Bus1_storage_invest_limit_0)
+1 flow(Source_Bus1_0)
+1 flow(storage_invest_limit_Bus1_0)
= 0

c_e_Bus_balance(Bus1_1)_:
-1 flow(Bus1_storage_invest_limit_1)
+1 flow(Source_Bus1_1)
+1 flow(storage_invest_limit_Bus1_1)
= 0

c_e_Bus_balance(Bus1_2)_:
-1 flow(Bus1_storage_invest_limit_2)
+1 flow(Source_Bus1_2)
+1 flow(storage_invest_limit_Bus1_2)
= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_0)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_1)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_1)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_2)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_2)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_0)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_0)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_1)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_1)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_2)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_2)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_0)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_1)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_1)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_2)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_2)
<= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_2)
-1 flow(Bus1_storage_invest_limit_0)
+1 flow(storage_invest_limit_Bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_1)
-1 flow(Bus1_storage_invest_limit_1)
+1 flow(storage_invest_limit_Bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_2)
-1 flow(Bus1_storage_invest_limit_2)
+1 flow(storage_invest_limit_Bus1_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 InvestmentFlow_invest(Bus1_storage_invest_limit)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 InvestmentFlow_invest(storage_invest_limit_Bus1)
= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_invest_limit_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_0)
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_invest_limit_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_1)
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_invest_limit_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage_invest_limit_2)
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_storage_invest_limit_0) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2) <= +inf
   0 <= flow(Source_Bus1_0) <= +inf
   0 <= flow(Source_Bus1_1) <= +inf
   0 <= flow(Source_Bus1_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlow_invest(Bus1_storage_invest_limit) <= +inf
   0 <= InvestmentFlow_invest(Source_Bus1) <= +inf
   0 <= InvestmentFlow_invest(storage_invest_limit_Bus1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit) <= +inf
end
