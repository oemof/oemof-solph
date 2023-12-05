\* Source Pyomo model name=Model *\

min 
objective:
+250.0 ONE_VAR_CONSTANT
+29.994068581329355 GenericInvestmentStorageBlock_invest(storage1_0)
+19.797418159157367 GenericInvestmentStorageBlock_invest(storage1_1)
+9.8007020589888 GenericInvestmentStorageBlock_invest(storage1_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(storage1_electricityBus_0_0)
-1 flow(electricityBus_storage1_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 flow(electricityBus_storage1_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(storage1_electricityBus_1_2)
-1 flow(electricityBus_storage1_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(storage1_electricityBus_1_3)
-1 flow(electricityBus_storage1_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(storage1_electricityBus_2_4)
-1 flow(electricityBus_storage1_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(storage1_electricityBus_2_5)
-1 flow(electricityBus_storage1_2_5)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_invest(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_0)
= 50

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_1)_:
-1 GenericInvestmentStorageBlock_invest(storage1_1)
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_old(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage1_2)_:
-1 GenericInvestmentStorageBlock_invest(storage1_2)
-1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_old(storage1_2)
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
= 50

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage1_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage1_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage1_0)
-1 GenericInvestmentStorageBlock_old_exo(storage1_0)
+1 GenericInvestmentStorageBlock_old(storage1_0)
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

c_e_GenericInvestmentStorageBlock_initially_empty(storage1_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_0_1)_:
+1 flow(storage1_electricityBus_0_1)
-1 flow(electricityBus_storage1_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_2)_:
+1 flow(storage1_electricityBus_1_2)
-1 flow(electricityBus_storage1_1_2)
-1 GenericInvestmentStorageBlock_storage_content(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_1_3)_:
+1 flow(storage1_electricityBus_1_3)
-1 flow(electricityBus_storage1_1_3)
-1 GenericInvestmentStorageBlock_storage_content(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_4)_:
+1 flow(storage1_electricityBus_2_4)
-1 flow(electricityBus_storage1_2_4)
-1 GenericInvestmentStorageBlock_storage_content(storage1_3)
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage1_2_5)_:
+1 flow(storage1_electricityBus_2_5)
-1 flow(electricityBus_storage1_2_5)
-1 GenericInvestmentStorageBlock_storage_content(storage1_4)
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage1_0)
+1 GenericInvestmentStorageBlock_storage_content(storage1_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_2)_:
-1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_1_3)_:
-1 GenericInvestmentStorageBlock_total(storage1_1)
+1 GenericInvestmentStorageBlock_storage_content(storage1_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_4)_:
-1 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage1_2_5)_:
-1 GenericInvestmentStorageBlock_total(storage1_2)
+1 GenericInvestmentStorageBlock_storage_content(storage1_5)
<= 0

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_0)_:
+1 GenericInvestmentStorageBlock_total(storage1_0)
<= 500

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_1)_:
+1 GenericInvestmentStorageBlock_total(storage1_1)
<= 500

c_u_GenericInvestmentStorageBlock_overall_storage_maximum(storage1_2)_:
+1 GenericInvestmentStorageBlock_total(storage1_2)
<= 500

c_l_GenericInvestmentStorageBlock_overall_minimum(storage1)_:
+1 GenericInvestmentStorageBlock_total(storage1_2)
>= 10

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   100 <= GenericInvestmentStorageBlock_invest(storage1_0) <= 200
   100 <= GenericInvestmentStorageBlock_invest(storage1_1) <= 200
   100 <= GenericInvestmentStorageBlock_invest(storage1_2) <= 200
   0 <= flow(storage1_electricityBus_0_0) <= +inf
   0 <= flow(electricityBus_storage1_0_0) <= +inf
   0 <= flow(storage1_electricityBus_0_1) <= +inf
   0 <= flow(electricityBus_storage1_0_1) <= +inf
   0 <= flow(storage1_electricityBus_1_2) <= +inf
   0 <= flow(electricityBus_storage1_1_2) <= +inf
   0 <= flow(storage1_electricityBus_1_3) <= +inf
   0 <= flow(electricityBus_storage1_1_3) <= +inf
   0 <= flow(storage1_electricityBus_2_4) <= +inf
   0 <= flow(electricityBus_storage1_2_4) <= +inf
   0 <= flow(storage1_electricityBus_2_5) <= +inf
   0 <= flow(electricityBus_storage1_2_5) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage1_5) <= +inf
end
