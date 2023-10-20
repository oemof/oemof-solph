\* Source Pyomo model name=Model *\

min 
objective:
+18.16879316506207 InvestmentFlowBlock_invest(pv_electricityBus_0)
+11.99221088531737 InvestmentFlowBlock_invest(pv_electricityBus_1)
+5.93673806203831 InvestmentFlowBlock_invest(pv_electricityBus_2)
+13 flow(pv_electricityBus_0_0)
+13 flow(pv_electricityBus_0_1)
+12.745098039215685 flow(pv_electricityBus_1_2)
+12.745098039215685 flow(pv_electricityBus_1_3)
+12.49519415609381 flow(pv_electricityBus_2_4)
+12.49519415609381 flow(pv_electricityBus_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
= 50000.0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
= 80000.0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(pv_electricityBus_1_2)
= 30000.0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(pv_electricityBus_1_3)
= 60000.0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(pv_electricityBus_2_4)
= 70000.0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(pv_electricityBus_2_5)
= 20000.0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_0)
+1 InvestmentFlowBlock_total(pv_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_1)
-1 InvestmentFlowBlock_total(pv_electricityBus_0)
+1 InvestmentFlowBlock_total(pv_electricityBus_1)
+1 InvestmentFlowBlock_old(pv_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_2)
-1 InvestmentFlowBlock_total(pv_electricityBus_1)
+1 InvestmentFlowBlock_total(pv_electricityBus_2)
+1 InvestmentFlowBlock_old(pv_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(pv_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(pv_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(pv_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(pv_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(pv_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(pv_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(pv_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(pv_electricityBus_0)
+1 InvestmentFlowBlock_old(pv_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricityBus_1)_:
+1 InvestmentFlowBlock_old(pv_electricityBus_1)
-1 InvestmentFlowBlock_old_end(pv_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(pv_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricityBus_2)_:
+1 InvestmentFlowBlock_old(pv_electricityBus_2)
-1 InvestmentFlowBlock_old_end(pv_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(pv_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
-45 InvestmentFlowBlock_total(pv_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
-83 InvestmentFlowBlock_total(pv_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_1_2)_:
+1 flow(pv_electricityBus_1_2)
-65 InvestmentFlowBlock_total(pv_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_1_3)_:
+1 flow(pv_electricityBus_1_3)
-67 InvestmentFlowBlock_total(pv_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_2_4)_:
+1 flow(pv_electricityBus_2_4)
-33 InvestmentFlowBlock_total(pv_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_2_5)_:
+1 flow(pv_electricityBus_2_5)
-96 InvestmentFlowBlock_total(pv_electricityBus_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_2) <= +inf
   0 <= flow(pv_electricityBus_0_0) <= +inf
   0 <= flow(pv_electricityBus_0_1) <= +inf
   0 <= flow(pv_electricityBus_1_2) <= +inf
   0 <= flow(pv_electricityBus_1_3) <= +inf
   0 <= flow(pv_electricityBus_2_4) <= +inf
   0 <= flow(pv_electricityBus_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_0) <= +inf
end
