\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage6)
+99 InvestmentFlow_invest(electricityBus_storage6)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storage6_0)
+1 flow(storage6_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storage6_1)
+1 flow(storage6_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storage6_2)
+1 flow(storage6_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_storage6_0)_:
-1 InvestmentFlow_invest(electricityBus_storage6)
+1 flow(electricityBus_storage6_0)
<= 110

c_u_InvestmentFlow_max(electricityBus_storage6_1)_:
-1 InvestmentFlow_invest(electricityBus_storage6)
+1 flow(electricityBus_storage6_1)
<= 110

c_u_InvestmentFlow_max(electricityBus_storage6_2)_:
-1 InvestmentFlow_invest(electricityBus_storage6)
+1 flow(electricityBus_storage6_2)
<= 110

c_u_InvestmentFlow_max(storage6_electricityBus_0)_:
-1 InvestmentFlow_invest(storage6_electricityBus)
+1 flow(storage6_electricityBus_0)
<= 100

c_u_InvestmentFlow_max(storage6_electricityBus_1)_:
-1 InvestmentFlow_invest(storage6_electricityBus)
+1 flow(storage6_electricityBus_1)
<= 100

c_u_InvestmentFlow_max(storage6_electricityBus_2)_:
-1 InvestmentFlow_invest(storage6_electricityBus)
+1 flow(storage6_electricityBus_2)
<= 100

c_e_GenericInvestmentStorageBlock_balance(storage6_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage6_0)
-1 GenericInvestmentStorageBlock_capacity(storage6_2)
-1 flow(electricityBus_storage6_0)
+1 flow(storage6_electricityBus_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage6_0)
+1 GenericInvestmentStorageBlock_capacity(storage6_1)
-1 flow(electricityBus_storage6_1)
+1 flow(storage6_electricityBus_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage6_1)
+1 GenericInvestmentStorageBlock_capacity(storage6_2)
-1 flow(electricityBus_storage6_2)
+1 flow(storage6_electricityBus_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage6)_:
-1 InvestmentFlow_invest(electricityBus_storage6)
+1.1000000000000001 InvestmentFlow_invest(storage6_electricityBus)
= -1.4210854715202004e-14

c_u_GenericInvestmentStorageBlock_max_capacity(storage6_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage6_0)
-1 GenericInvestmentStorageBlock_invest(storage6)
<= 10000

c_u_GenericInvestmentStorageBlock_max_capacity(storage6_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage6_1)
-1 GenericInvestmentStorageBlock_invest(storage6)
<= 10000

c_u_GenericInvestmentStorageBlock_max_capacity(storage6_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage6_2)
-1 GenericInvestmentStorageBlock_invest(storage6)
<= 10000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage6_0) <= +inf
   0 <= flow(electricityBus_storage6_1) <= +inf
   0 <= flow(electricityBus_storage6_2) <= +inf
   0 <= flow(storage6_electricityBus_0) <= +inf
   0 <= flow(storage6_electricityBus_1) <= +inf
   0 <= flow(storage6_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_storage6) <= +inf
   0 <= InvestmentFlow_invest(storage6_electricityBus) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage6_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage6) <= +inf
end
