\* Source Pyomo model name=Model *\

min 
objective:
+212.02333722461535 GenericInvestmentStorageBlock_invest(storage1_0)
+207.86601688687779 GenericInvestmentStorageBlock_invest(storage1_1)
+203.79021263419389 GenericInvestmentStorageBlock_invest(storage1_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage1_0_0)
+1 flow(storage1_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage1_0_1)
+1 flow(storage1_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage1_1_2)
+1 flow(storage1_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage1_1_3)
+1 flow(storage1_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage1_2_4)
+1 flow(storage1_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage1_2_5)
+1 flow(storage1_electricityBus_2_5)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_invest(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_1)_:
-1 GenericInvestmentStorageBlock_invest(storage1_1)
+1 GenericInvestmentStorageBlock_old(storage1_1)
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_2)_:
-1 GenericInvestmentStorageBlock_invest(storage1_2)
+1 GenericInvestmentStorageBlock_old(storage1_2)
-1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_total(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_1)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage1_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_0)_:
+1 GenericInvestmentStorageBlock_old(storage1_0)
-1 GenericInvestmentStorageBlock_old_end(storage1_0)
-1 GenericInvestmentStorageBlock_old_exo(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_1)_:
+1 GenericInvestmentStorageBlock_old(storage1_1)
-1 GenericInvestmentStorageBlock_old_end(storage1_1)
-1 GenericInvestmentStorageBlock_old_exo(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_2)_:
+1 GenericInvestmentStorageBlock_old(storage1_2)
-1 GenericInvestmentStorageBlock_old_end(storage1_2)
-1 GenericInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_0_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
-1 flow(electricityBus_storage1_0_1)
+1 flow(storage1_electricityBus_0_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
-1 flow(electricityBus_storage1_1_2)
+1 flow(storage1_electricityBus_1_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_3)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
-1 flow(electricityBus_storage1_1_3)
+1 flow(storage1_electricityBus_1_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_4)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_3)
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
-1 flow(electricityBus_storage1_2_4)
+1 flow(storage1_electricityBus_2_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_5)_:
-1 GenericInvestmentStorageBlock_storage_content(storage1_4)
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
-1 flow(electricityBus_storage1_2_5)
+1 flow(storage1_electricityBus_2_5)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
-1 GenericInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_1)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
-1 GenericInvestmentStorageBlock_total(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_2)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
-1 GenericInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_3)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
-1 GenericInvestmentStorageBlock_total(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_4)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
-1 GenericInvestmentStorageBlock_total(storage1_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_5)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
-1 GenericInvestmentStorageBlock_total(storage1_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage1_0_0) <= +inf
   0 <= flow(electricityBus_storage1_0_1) <= +inf
   0 <= flow(electricityBus_storage1_1_2) <= +inf
   0 <= flow(electricityBus_storage1_1_3) <= +inf
   0 <= flow(electricityBus_storage1_2_4) <= +inf
   0 <= flow(electricityBus_storage1_2_5) <= +inf
   0 <= flow(storage1_electricityBus_0_0) <= +inf
   0 <= flow(storage1_electricityBus_0_1) <= +inf
   0 <= flow(storage1_electricityBus_1_2) <= +inf
   0 <= flow(storage1_electricityBus_1_3) <= +inf
   0 <= flow(storage1_electricityBus_2_4) <= +inf
   0 <= flow(storage1_electricityBus_2_5) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_5) <= +inf
   100 <= GenericInvestmentStorageBlock_invest(storage1_0) <= 200
   100 <= GenericInvestmentStorageBlock_invest(storage1_1) <= 200
   100 <= GenericInvestmentStorageBlock_invest(storage1_2) <= 200
   0 <= GenericInvestmentStorageBlock_total(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_2) <= +inf
end