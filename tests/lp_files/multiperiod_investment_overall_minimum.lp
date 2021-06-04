\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+61.15671812529034 MultiPeriodInvestmentFlow_invest(source_0_bus_1_0)
+59.957566789500333 MultiPeriodInvestmentFlow_invest(source_0_bus_1_1)
+58.781928225000321 MultiPeriodInvestmentFlow_invest(source_0_bus_1_2)

s.t.

c_e_MultiPeriodBus_balance(bus_1_0_0)_:
+1 flow(source_0_bus_1_0_0)
= 0

c_e_MultiPeriodBus_balance(bus_1_0_1)_:
+1 flow(source_0_bus_1_0_1)
= 0

c_e_MultiPeriodBus_balance(bus_1_1_2)_:
+1 flow(source_0_bus_1_1_2)
= 0

c_e_MultiPeriodBus_balance(bus_1_1_3)_:
+1 flow(source_0_bus_1_1_3)
= 0

c_e_MultiPeriodBus_balance(bus_1_2_4)_:
+1 flow(source_0_bus_1_2_4)
= 0

c_e_MultiPeriodBus_balance(bus_1_2_5)_:
+1 flow(source_0_bus_1_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_0_bus_1_0)_:
-1 MultiPeriodInvestmentFlow_invest(source_0_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_0_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_0_bus_1_1)_:
-1 MultiPeriodInvestmentFlow_invest(source_0_bus_1_1)
+1 MultiPeriodInvestmentFlow_old(source_0_bus_1_1)
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_0_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_0_bus_1_2)_:
-1 MultiPeriodInvestmentFlow_invest(source_0_bus_1_2)
+1 MultiPeriodInvestmentFlow_old(source_0_bus_1_2)
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_1)
+1 MultiPeriodInvestmentFlow_total(source_0_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_0_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_0_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_0_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_0_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_0_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_0_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_0_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old(source_0_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_0_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old(source_0_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_0_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old(source_0_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_end(source_0_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_0)
+1 flow(source_0_bus_1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_0)
+1 flow(source_0_bus_1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_1)
+1 flow(source_0_bus_1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_1)
+1 flow(source_0_bus_1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_2)
+1 flow(source_0_bus_1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_0_bus_1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(source_0_bus_1_2)
+1 flow(source_0_bus_1_2_5)
<= 0

c_l_MultiPeriodInvestmentFlow_overall_minimum(source_0_bus_1)_:
+1 MultiPeriodInvestmentFlow_total(source_0_bus_1_2)
>= 100

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source_0_bus_1_0_0) <= +inf
   0 <= flow(source_0_bus_1_0_1) <= +inf
   0 <= flow(source_0_bus_1_1_2) <= +inf
   0 <= flow(source_0_bus_1_1_3) <= +inf
   0 <= flow(source_0_bus_1_2_4) <= +inf
   0 <= flow(source_0_bus_1_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_2) <= +inf
end
