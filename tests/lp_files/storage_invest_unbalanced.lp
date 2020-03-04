\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage1)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storage1_0)
+1 flow(storage1_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storage1_1)
+1 flow(storage1_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storage1_2)
+1 flow(storage1_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_storage1_0)_:
-1 InvestmentFlow_invest(electricityBus_storage1)
+1 flow(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage1_1)_:
-1 InvestmentFlow_invest(electricityBus_storage1)
+1 flow(electricityBus_storage1_1)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage1_2)_:
-1 InvestmentFlow_invest(electricityBus_storage1)
+1 flow(electricityBus_storage1_2)
<= 0

c_u_InvestmentFlow_max(storage1_electricityBus_0)_:
-1 InvestmentFlow_invest(storage1_electricityBus)
+1 flow(storage1_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(storage1_electricityBus_1)_:
-1 InvestmentFlow_invest(storage1_electricityBus)
+1 flow(storage1_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(storage1_electricityBus_2)_:
-1 InvestmentFlow_invest(storage1_electricityBus)
+1 flow(storage1_electricityBus_2)
<= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(storage1)_:
+1 GenericInvestmentStorageBlock_init_content(storage1)
-0.5 GenericInvestmentStorageBlock_invest(storage1)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage1)_:
-1 GenericInvestmentStorageBlock_init_content(storage1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
-1 flow(electricityBus_storage1_0)
+1 flow(storage1_electricityBus_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
-1 flow(electricityBus_storage1_1)
+1 flow(storage1_electricityBus_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
-1 flow(electricityBus_storage1_2)
+1 flow(storage1_electricityBus_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage1)_:
-1 GenericInvestmentStorageBlock_invest(storage1)
+1 InvestmentFlow_invest(electricityBus_storage1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage1)_:
-1 GenericInvestmentStorageBlock_invest(storage1)
+1 InvestmentFlow_invest(storage1_electricityBus)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0)_:
-1 GenericInvestmentStorageBlock_invest(storage1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1)_:
-1 GenericInvestmentStorageBlock_invest(storage1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2)_:
-1 GenericInvestmentStorageBlock_invest(storage1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage1_0) <= +inf
   0 <= flow(electricityBus_storage1_1) <= +inf
   0 <= flow(electricityBus_storage1_2) <= +inf
   0 <= flow(storage1_electricityBus_0) <= +inf
   0 <= flow(storage1_electricityBus_1) <= +inf
   0 <= flow(storage1_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_storage1) <= +inf
   0 <= InvestmentFlow_invest(storage1_electricityBus) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage1) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage1) <= +inf
end
