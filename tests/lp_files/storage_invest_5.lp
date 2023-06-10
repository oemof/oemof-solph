\* Source Pyomo model name=Model *\

min 
objective:
+99 InvestmentFlowBlock_invest(electricityBus_storage5_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage5_electricityBus_0_0)
-1 flow(electricityBus_storage5_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage5_electricityBus_0_1)
-1 flow(electricityBus_storage5_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage5_electricityBus_0_2)
-1 flow(electricityBus_storage5_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage5_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage5_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage5_electricityBus_0)
= 100

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage5_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_storage5_0)
+1 InvestmentFlowBlock_total(electricityBus_storage5_0)
= 110

c_u_InvestmentFlowBlock_max(storage5_electricityBus_0_0)_:
+1 flow(storage5_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage5_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage5_electricityBus_0_1)_:
+1 flow(storage5_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage5_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage5_electricityBus_0_2)_:
+1 flow(storage5_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage5_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage5_0_0)_:
+1 flow(electricityBus_storage5_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage5_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage5_0_1)_:
+1 flow(electricityBus_storage5_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage5_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage5_0_2)_:
+1 flow(electricityBus_storage5_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage5_0)
<= 0

c_e_GenericStorageBlock_balance(storage5_0_0)_:
+1 flow(storage5_electricityBus_0_0)
-1 flow(electricityBus_storage5_0_0)
+1 GenericStorageBlock_storage_content(storage5_1)
-1 GenericStorageBlock_storage_content(storage5_0)
= 0

c_e_GenericStorageBlock_balance(storage5_0_1)_:
+1 flow(storage5_electricityBus_0_1)
-1 flow(electricityBus_storage5_0_1)
-1 GenericStorageBlock_storage_content(storage5_1)
+1 GenericStorageBlock_storage_content(storage5_2)
= 0

c_e_GenericStorageBlock_balance(storage5_0_2)_:
+1 flow(storage5_electricityBus_0_2)
-1 flow(electricityBus_storage5_0_2)
-1 GenericStorageBlock_storage_content(storage5_2)
+1 GenericStorageBlock_storage_content(storage5_3)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage5)_:
-1 GenericStorageBlock_storage_content(storage5_0)
+1 GenericStorageBlock_storage_content(storage5_3)
= 0

c_e_GenericStorageBlock_power_coupled(storage5_0)_:
+1.1 InvestmentFlowBlock_total(storage5_electricityBus_0)
-1 InvestmentFlowBlock_total(electricityBus_storage5_0)
= 0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_storage5_0) <= +inf
   0 <= flow(storage5_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage5_0_0) <= +inf
   0 <= flow(storage5_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage5_0_1) <= +inf
   0 <= flow(storage5_electricityBus_0_2) <= +inf
   0 <= flow(electricityBus_storage5_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage5_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage5_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage5_0) <= +inf
   0 <= GenericStorageBlock_storage_content(storage5_1) <= 10000
   0 <= GenericStorageBlock_storage_content(storage5_0) <= 10000
   0 <= GenericStorageBlock_storage_content(storage5_2) <= 10000
   0 <= GenericStorageBlock_storage_content(storage5_3) <= 10000
end
