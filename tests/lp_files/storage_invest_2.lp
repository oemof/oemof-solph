\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage2)
+99 InvestmentFlow_invest(electricityBus_storage2)
+9 InvestmentFlow_invest(storage2_electricityBus)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storage2_0)
+1 flow(storage2_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storage2_1)
+1 flow(storage2_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storage2_2)
+1 flow(storage2_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_storage2_0)_:
-1 InvestmentFlow_invest(electricityBus_storage2)
+1 flow(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage2_1)_:
-1 InvestmentFlow_invest(electricityBus_storage2)
+1 flow(electricityBus_storage2_1)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage2_2)_:
-1 InvestmentFlow_invest(electricityBus_storage2)
+1 flow(electricityBus_storage2_2)
<= 0

c_u_InvestmentFlow_max(storage2_electricityBus_0)_:
-1 InvestmentFlow_invest(storage2_electricityBus)
+1 flow(storage2_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(storage2_electricityBus_1)_:
-1 InvestmentFlow_invest(storage2_electricityBus)
+1 flow(storage2_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(storage2_electricityBus_2)_:
-1 InvestmentFlow_invest(storage2_electricityBus)
+1 flow(storage2_electricityBus_2)
<= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage2_0)
-1 GenericInvestmentStorageBlock_capacity(storage2_2)
-1 flow(electricityBus_storage2_0)
+1 flow(storage2_electricityBus_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage2_0)
+1 GenericInvestmentStorageBlock_capacity(storage2_1)
-1 flow(electricityBus_storage2_1)
+1 flow(storage2_electricityBus_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage2_1)
+1 GenericInvestmentStorageBlock_capacity(storage2_2)
-1 flow(electricityBus_storage2_2)
+1 flow(storage2_electricityBus_2)
= 0

c_e_GenericInvestmentStorageBlock_initial_capacity(storage2)_:
+1 GenericInvestmentStorageBlock_capacity(storage2_2)
-0.5 GenericInvestmentStorageBlock_invest(storage2)
= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage2_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage2_0)
-1 GenericInvestmentStorageBlock_invest(storage2)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage2_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage2_1)
-1 GenericInvestmentStorageBlock_invest(storage2)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage2_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage2_2)
-1 GenericInvestmentStorageBlock_invest(storage2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage2_0) <= +inf
   0 <= flow(electricityBus_storage2_1) <= +inf
   0 <= flow(electricityBus_storage2_2) <= +inf
   0 <= flow(storage2_electricityBus_0) <= +inf
   0 <= flow(storage2_electricityBus_1) <= +inf
   0 <= flow(storage2_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_storage2) <= +inf
   0 <= InvestmentFlow_invest(storage2_electricityBus) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage2_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage2) <= +inf
end
