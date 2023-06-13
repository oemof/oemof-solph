\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage4_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage4_electricityBus_0_0)
-1 flow(electricityBus_storage4_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage4_electricityBus_0_1)
-1 flow(electricityBus_storage4_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(storage4_electricityBus_0_2)
-1 flow(electricityBus_storage4_0_2)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage4_0)_:
-1 GenericInvestmentStorageBlock_invest(storage4_0)
+1 GenericInvestmentStorageBlock_total(storage4_0)
= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage4)_:
-1 GenericInvestmentStorageBlock_invest(storage4_0)
+1 GenericInvestmentStorageBlock_init_content(storage4)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage4)_:
+1 flow(storage4_electricityBus_0_0)
-1 flow(electricityBus_storage4_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage4)
+1 GenericInvestmentStorageBlock_storage_content(storage4_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage4_0_1)_:
+1 flow(storage4_electricityBus_0_1)
-1 flow(electricityBus_storage4_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage4_0)
+1 GenericInvestmentStorageBlock_storage_content(storage4_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage4_0_2)_:
+1 flow(storage4_electricityBus_0_2)
-1 flow(electricityBus_storage4_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage4_1)
+1 GenericInvestmentStorageBlock_storage_content(storage4_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage4)_:
-1 GenericInvestmentStorageBlock_init_content(storage4)
+1 GenericInvestmentStorageBlock_storage_content(storage4_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage4_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage4_0)
+1 GenericInvestmentStorageBlock_storage_content(storage4_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage4_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage4_0)
+1 GenericInvestmentStorageBlock_storage_content(storage4_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage4_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage4_0)
+1 GenericInvestmentStorageBlock_storage_content(storage4_2)
<= 0

bounds
   0 <= GenericInvestmentStorageBlock_invest(storage4_0) <= 500
   0 <= flow(storage4_electricityBus_0_0) <= 100
   0 <= flow(electricityBus_storage4_0_0) <= 80
   0 <= flow(storage4_electricityBus_0_1) <= 100
   0 <= flow(electricityBus_storage4_0_1) <= 80
   0 <= flow(storage4_electricityBus_0_2) <= 100
   0 <= flow(electricityBus_storage4_0_2) <= 80
   0 <= GenericInvestmentStorageBlock_total(storage4_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage4_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage4_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage4_2) <= +inf
end
