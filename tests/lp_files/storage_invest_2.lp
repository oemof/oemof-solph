\* Source Pyomo model name=Model *\

min 
objective:
+99 InvestmentFlowBlock_invest(electricityBus_storage2_0)
+9 InvestmentFlowBlock_invest(storage2_electricityBus_0)
+145 GenericInvestmentStorageBlock_invest(storage2_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage2_electricityBus_0_0)
-1 flow(electricityBus_storage2_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 flow(electricityBus_storage2_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage2_electricityBus_0_2)
-1 flow(electricityBus_storage2_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage2_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage2_0)
+1 InvestmentFlowBlock_total(electricityBus_storage2_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage2_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(storage2_electricityBus_0)
+1 InvestmentFlowBlock_total(storage2_electricityBus_0)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_0_0)_:
+1 flow(electricityBus_storage2_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_0_1)_:
+1 flow(electricityBus_storage2_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage2_0_2)_:
+1 flow(electricityBus_storage2_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage2_0)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_0_0)_:
+1 flow(storage2_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage2_electricityBus_0_2)_:
+1 flow(storage2_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage2_electricityBus_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage2_0)_:
-1 GenericInvestmentStorageBlock_invest(storage2_0)
+1 GenericInvestmentStorageBlock_total(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_init_content_fix(storage2)_:
-0.5 GenericInvestmentStorageBlock_invest(storage2_0)
+1 GenericInvestmentStorageBlock_init_content(storage2)
= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage2)_:
+1 flow(storage2_electricityBus_0_0)
-1 flow(electricityBus_storage2_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage2)
+1 GenericInvestmentStorageBlock_storage_content(storage2_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_0_1)_:
+1 flow(storage2_electricityBus_0_1)
-1 flow(electricityBus_storage2_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage2_0_2)_:
+1 flow(storage2_electricityBus_0_2)
-1 flow(electricityBus_storage2_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage2_1)
+1 GenericInvestmentStorageBlock_storage_content(storage2_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage2)_:
-1 GenericInvestmentStorageBlock_init_content(storage2)
+1 GenericInvestmentStorageBlock_storage_content(storage2_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage2_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage2_0)
+1 GenericInvestmentStorageBlock_storage_content(storage2_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage2_electricityBus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage2_0) <= +inf
   0 <= flow(storage2_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage2_0_0) <= +inf
   0 <= flow(storage2_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage2_0_1) <= +inf
   0 <= flow(storage2_electricityBus_0_2) <= +inf
   0 <= flow(electricityBus_storage2_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage2_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage2_electricityBus_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage2_2) <= +inf
end
