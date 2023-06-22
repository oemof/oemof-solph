\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage1_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage1_electricityBus_0_0)
-1 flow(electricityBus_storage1_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 flow(electricityBus_storage1_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage1_electricityBus_0_2)
-1 flow(electricityBus_storage1_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage1_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_0)
-1 InvestmentFlowBlock_invest(electricityBus_storage1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage1_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage1_electricityBus_0)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_0_0)_:
+1 flow(electricityBus_storage1_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_0_1)_:
+1 flow(electricityBus_storage1_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage1_0_2)_:
+1 flow(electricityBus_storage1_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_0_0)_:
+1 flow(storage1_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage1_electricityBus_0_2)_:
+1 flow(storage1_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage1_electricityBus_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_invest(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(storage1)_:
-0.5 GenericInvestmentStorageBlock_invest(storage1_0)
+1 GenericInvestmentStorageBlock_init_content(storage1)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage1)_:
+1 flow(storage1_electricityBus_0_0)
-1 flow(electricityBus_storage1_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 flow(electricityBus_storage1_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_0_2)_:
+1 flow(storage1_electricityBus_0_2)
-1 flow(electricityBus_storage1_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage1_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage1_0)
-1 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage1_0)_:
+1 InvestmentFlowBlock_total(storage1_electricityBus_0)
-1 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
<= 0

bounds
   0 <= GenericInvestmentStorageBlock_invest(storage1_0) <= +inf
   0 <= flow(storage1_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage1_0_0) <= +inf
   0 <= flow(storage1_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage1_0_1) <= +inf
   0 <= flow(storage1_electricityBus_0_2) <= +inf
   0 <= flow(electricityBus_storage1_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage1_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage1_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage1_electricityBus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_2) <= +inf
end
