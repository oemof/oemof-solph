\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage)
+123 InvestmentFlow_invest(Source_Bus1)

s.t.

c_u_investment_limit_:
+145 GenericInvestmentStorageBlock_invest(storage)
+123 InvestmentFlow_invest(Source_Bus1)
<= 900

c_e_Bus_balance(Bus1_0)_:
-1 flow(Bus1_storage_0)
+1 flow(Source_Bus1_0)
+1 flow(storage_Bus1_0)
= 0

c_e_Bus_balance(Bus1_1)_:
-1 flow(Bus1_storage_1)
+1 flow(Source_Bus1_1)
+1 flow(storage_Bus1_1)
= 0

c_e_Bus_balance(Bus1_2)_:
-1 flow(Bus1_storage_2)
+1 flow(Source_Bus1_2)
+1 flow(storage_Bus1_2)
= 0

c_u_InvestmentFlow_max(Bus1_storage_0)_:
-1 InvestmentFlow_invest(Bus1_storage)
+1 flow(Bus1_storage_0)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_1)_:
-1 InvestmentFlow_invest(Bus1_storage)
+1 flow(Bus1_storage_1)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_2)_:
-1 InvestmentFlow_invest(Bus1_storage)
+1 flow(Bus1_storage_2)
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

c_u_InvestmentFlow_max(storage_Bus1_0)_:
-1 InvestmentFlow_invest(storage_Bus1)
+1 flow(storage_Bus1_0)
<= 0

c_u_InvestmentFlow_max(storage_Bus1_1)_:
-1 InvestmentFlow_invest(storage_Bus1)
+1 flow(storage_Bus1_1)
<= 0

c_u_InvestmentFlow_max(storage_Bus1_2)_:
-1 InvestmentFlow_invest(storage_Bus1)
+1 flow(storage_Bus1_2)
<= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_0)
-1 GenericInvestmentStorageBlock_capacity(storage_2)
-1 flow(Bus1_storage_0)
+1 flow(storage_Bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage_0)
+1 GenericInvestmentStorageBlock_capacity(storage_1)
-1 flow(Bus1_storage_1)
+1 flow(storage_Bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage_1)
+1 GenericInvestmentStorageBlock_capacity(storage_2)
-1 flow(Bus1_storage_2)
+1 flow(storage_Bus1_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage)
+1 InvestmentFlow_invest(Bus1_storage)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage)
+1 InvestmentFlow_invest(storage_Bus1)
= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_0)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage_1)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage_2)
-1 GenericInvestmentStorageBlock_invest(storage)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_storage_0) <= +inf
   0 <= flow(Bus1_storage_1) <= +inf
   0 <= flow(Bus1_storage_2) <= +inf
   0 <= flow(Source_Bus1_0) <= +inf
   0 <= flow(Source_Bus1_1) <= +inf
   0 <= flow(Source_Bus1_2) <= +inf
   0 <= flow(storage_Bus1_0) <= +inf
   0 <= flow(storage_Bus1_1) <= +inf
   0 <= flow(storage_Bus1_2) <= +inf
   0 <= InvestmentFlow_invest(Bus1_storage) <= +inf
   0 <= InvestmentFlow_invest(Source_Bus1) <= +inf
   0 <= InvestmentFlow_invest(storage_Bus1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage) <= +inf
end
