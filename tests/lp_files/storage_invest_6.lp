\* Source Pyomo model name=Model *\

min 
objective:
+99 InvestmentFlowBlock_invest(electricityBus_storage6_0)
+145 GenericInvestmentStorageBlock_invest(storage6_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage6_electricityBus_0_0)
-1 flow(electricityBus_storage6_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 flow(electricityBus_storage6_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage6_electricityBus_0_2)
-1 flow(electricityBus_storage6_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage6_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage6_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage6_electricityBus_0)
= 100

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage6_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage6_0)
+1 InvestmentFlowBlock_total(electricityBus_storage6_0)
= 110

c_u_InvestmentFlowBlock_max(storage6_electricityBus_0_0)_:
+1 flow(storage6_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage6_electricityBus_0_2)_:
+1 flow(storage6_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage6_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_0_0)_:
+1 flow(electricityBus_storage6_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_0_1)_:
+1 flow(electricityBus_storage6_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage6_0_2)_:
+1 flow(electricityBus_storage6_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage6_0)_:
-1 GenericInvestmentStorageBlock_invest(storage6_0)
+1 GenericInvestmentStorageBlock_total(storage6_0)
= 10000

c_u_GenericInvestmentStorageBlock_init_content_limit(storage6)_:
-1 GenericInvestmentStorageBlock_invest(storage6_0)
+1 GenericInvestmentStorageBlock_init_content(storage6)
<= 10000

c_e_GenericInvestmentStorageBlock_balance_first(storage6)_:
+1 flow(storage6_electricityBus_0_0)
-1 flow(electricityBus_storage6_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage6)
+1 GenericInvestmentStorageBlock_storage_content(storage6_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_0_1)_:
+1 flow(storage6_electricityBus_0_1)
-1 flow(electricityBus_storage6_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage6_0_2)_:
+1 flow(storage6_electricityBus_0_2)
-1 flow(electricityBus_storage6_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage6_1)
+1 GenericInvestmentStorageBlock_storage_content(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage6)_:
-1 GenericInvestmentStorageBlock_init_content(storage6)
+1 GenericInvestmentStorageBlock_storage_content(storage6_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage6_0)_:
+1.1 InvestmentFlowBlock_total(storage6_electricityBus_0)
-1 InvestmentFlowBlock_total(electricityBus_storage6_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage6_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage6_0)
+1 GenericInvestmentStorageBlock_storage_content(storage6_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage6_0) <= +inf
   0 <= flow(storage6_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage6_0_0) <= +inf
   0 <= flow(storage6_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage6_0_1) <= +inf
   0 <= flow(storage6_electricityBus_0_2) <= +inf
   0 <= flow(electricityBus_storage6_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage6_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage6) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage6_2) <= +inf
end
