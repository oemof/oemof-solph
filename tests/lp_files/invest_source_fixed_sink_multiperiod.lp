\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+150.44552658821425 MultiPeriodInvestmentFlow_invest(pv_electricityBus_0)
+147.49561430217082 MultiPeriodInvestmentFlow_invest(pv_electricityBus_1)
+144.60354343350082 MultiPeriodInvestmentFlow_invest(pv_electricityBus_2)
+13 flow(pv_electricityBus_0_0)
+13 flow(pv_electricityBus_0_1)
+12.745098039215685 flow(pv_electricityBus_1_2)
+12.745098039215685 flow(pv_electricityBus_1_3)
+12.49519415609381 flow(pv_electricityBus_2_4)
+12.49519415609381 flow(pv_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
= 50000

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
= 80000

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(pv_electricityBus_1_2)
= 30000

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(pv_electricityBus_1_3)
= 50000

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(pv_electricityBus_2_4)
= 80000

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(pv_electricityBus_2_5)
= 30000

c_e_MultiPeriodInvestmentFlow_total_rule(pv_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(pv_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(pv_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(pv_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(pv_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(pv_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(pv_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(pv_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(pv_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(pv_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(pv_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(pv_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(pv_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(pv_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(pv_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(pv_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(pv_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(pv_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(pv_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(pv_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(pv_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(pv_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(pv_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(pv_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(pv_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(pv_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_0_0)_:
-45 MultiPeriodInvestmentFlow_total(pv_electricityBus_0)
+1 flow(pv_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_0_1)_:
-83 MultiPeriodInvestmentFlow_total(pv_electricityBus_0)
+1 flow(pv_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_1_2)_:
-65 MultiPeriodInvestmentFlow_total(pv_electricityBus_1)
+1 flow(pv_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_1_3)_:
-45 MultiPeriodInvestmentFlow_total(pv_electricityBus_1)
+1 flow(pv_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_2_4)_:
-83 MultiPeriodInvestmentFlow_total(pv_electricityBus_2)
+1 flow(pv_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(pv_electricityBus_2_5)_:
-65 MultiPeriodInvestmentFlow_total(pv_electricityBus_2)
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
   0 <= MultiPeriodInvestmentFlow_invest(pv_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(pv_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(pv_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(pv_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(pv_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(pv_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(pv_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(pv_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(pv_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(pv_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(pv_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(pv_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(pv_electricityBus_2) <= +inf
end
