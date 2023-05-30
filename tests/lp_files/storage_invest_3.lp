\* Source Pyomo model name=Model *\

min 
objective:
+9 InvestmentFlowBlock_invest(storage3_electricityBus_0)
+99 InvestmentFlowBlock_invest(electricityBus_storage3_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage3_electricityBus_0_0)
-1 flow(electricityBus_storage3_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage3_electricityBus_0_1)
-1 flow(electricityBus_storage3_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage3_electricityBus_0_2)
-1 flow(electricityBus_storage3_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage3_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(storage3_electricityBus_0)
+1 InvestmentFlowBlock_total(storage3_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage3_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage3_0)
+1 InvestmentFlowBlock_total(electricityBus_storage3_0)
= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_0_0)_:
+1 flow(storage3_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_0_1)_:
+1 flow(storage3_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage3_electricityBus_0_2)_:
+1 flow(storage3_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage3_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_0_0)_:
+1 flow(electricityBus_storage3_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_0_1)_:
+1 flow(electricityBus_storage3_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage3_0_2)_:
+1 flow(electricityBus_storage3_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage3_0)
<= 0

c_e_GenericStorageBlock_balance(storage3_0_0)_:
+1 flow(storage3_electricityBus_0_0)
-1 flow(electricityBus_storage3_0_0)
+1 GenericStorageBlock_storage_content(storage3_1)
-1 GenericStorageBlock_storage_content(storage3_0)
= 0

c_e_GenericStorageBlock_balance(storage3_0_1)_:
+1 flow(storage3_electricityBus_0_1)
-1 flow(electricityBus_storage3_0_1)
-1 GenericStorageBlock_storage_content(storage3_1)
+1 GenericStorageBlock_storage_content(storage3_2)
= 0

c_e_GenericStorageBlock_balance(storage3_0_2)_:
+1 flow(storage3_electricityBus_0_2)
-1 flow(electricityBus_storage3_0_2)
-1 GenericStorageBlock_storage_content(storage3_2)
+1 GenericStorageBlock_storage_content(storage3_3)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage3)_:
-1 GenericStorageBlock_storage_content(storage3_0)
+1 GenericStorageBlock_storage_content(storage3_3)
= 0

bounds
   0 <= InvestmentFlowBlock_invest(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage3_0) <= +inf
   0 <= flow(storage3_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage3_0_0) <= +inf
   0 <= flow(storage3_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage3_0_1) <= +inf
   0 <= flow(storage3_electricityBus_0_2) <= +inf
   0 <= flow(electricityBus_storage3_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage3_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage3_0) <= +inf
   0 <= GenericStorageBlock_storage_content(storage3_1) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_0) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_2) <= 5000
   0 <= GenericStorageBlock_storage_content(storage3_3) <= 5000
end
