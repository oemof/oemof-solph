\* Source Pyomo model name=Model *\

min 
objective:
+157.50284813348861 InvestmentFlowBlock_invest(pv_electricityBus_0)
+154.41455699361629 InvestmentFlowBlock_invest(pv_electricityBus_1)
+151.38682058197674 InvestmentFlowBlock_invest(pv_electricityBus_2)
+13 flow(pv_electricityBus_0_0)
+13 flow(pv_electricityBus_0_1)
+12.745098039215685 flow(pv_electricityBus_1_2)
+12.745098039215685 flow(pv_electricityBus_1_3)
+12.49519415609381 flow(pv_electricityBus_2_4)
+12.49519415609381 flow(pv_electricityBus_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
= 50000

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
= 80000

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(pv_electricityBus_1_2)
= 30000

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(pv_electricityBus_1_3)
= 60000

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(pv_electricityBus_2_4)
= 70000

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(pv_electricityBus_2_5)
= 20000

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_0)
+1 InvestmentFlowBlock_total(pv_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_1)
+1 InvestmentFlowBlock_old(pv_electricityBus_1)
-1 InvestmentFlowBlock_total(pv_electricityBus_0)
+1 InvestmentFlowBlock_total(pv_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_2)
+1 InvestmentFlowBlock_old(pv_electricityBus_2)
-1 InvestmentFlowBlock_total(pv_electricityBus_1)
+1 InvestmentFlowBlock_total(pv_electricityBus_2)
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
+1 InvestmentFlowBlock_old(pv_electricityBus_0)
-1 InvestmentFlowBlock_old_end(pv_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(pv_electricityBus_0)
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
-45 InvestmentFlowBlock_total(pv_electricityBus_0)
+1 flow(pv_electricityBus_0_0)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_1)_:
-83 InvestmentFlowBlock_total(pv_electricityBus_0)
+1 flow(pv_electricityBus_0_1)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_1_2)_:
-65 InvestmentFlowBlock_total(pv_electricityBus_1)
+1 flow(pv_electricityBus_1_2)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_1_3)_:
-67 InvestmentFlowBlock_total(pv_electricityBus_1)
+1 flow(pv_electricityBus_1_3)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_2_4)_:
-33 InvestmentFlowBlock_total(pv_electricityBus_2)
+1 flow(pv_electricityBus_2_4)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_2_5)_:
-96 InvestmentFlowBlock_total(pv_electricityBus_2)
+1 flow(pv_electricityBus_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(pv_electricityBus_0_0) <= +inf
   0 <= flow(pv_electricityBus_0_1) <= +inf
   0 <= flow(pv_electricityBus_1_2) <= +inf
   0 <= flow(pv_electricityBus_1_3) <= +inf
   0 <= flow(pv_electricityBus_2_4) <= +inf
   0 <= flow(pv_electricityBus_2_5) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricityBus_2) <= +inf
end