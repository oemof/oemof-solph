\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+61.15671812529034 MultiPeriodInvestmentFlow_invest(source_0_bus_1_0)
+59.957566789500333 MultiPeriodInvestmentFlow_invest(source_0_bus_1_1)
+58.781928225000321 MultiPeriodInvestmentFlow_invest(source_0_bus_1_2)
+122.31343625058068 MultiPeriodInvestmentFlow_invest(source_1_bus_1_0)
+119.91513357900067 MultiPeriodInvestmentFlow_invest(source_1_bus_1_1)
+117.56385645000064 MultiPeriodInvestmentFlow_invest(source_1_bus_1_2)
+91.735077187935516 MultiPeriodInvestmentFlow_invest(source_2_bus_1_0)
+89.9363501842505 MultiPeriodInvestmentFlow_invest(source_2_bus_1_1)
+88.172892337500485 MultiPeriodInvestmentFlow_invest(source_2_bus_1_2)

s.t.

c_u_add_limit(0)_:
+4 MultiPeriodInvestmentFlow_invest(source_0_bus_1_0)
+1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_0)
<= 20

c_u_add_limit(1)_:
+4 MultiPeriodInvestmentFlow_invest(source_0_bus_1_1)
+1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_1)
<= 20

c_u_add_limit(2)_:
+4 MultiPeriodInvestmentFlow_invest(source_0_bus_1_2)
+1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_2)
<= 20

c_e_MultiPeriodBus_balance(bus_1_0_0)_:
+1 flow(source_0_bus_1_0_0)
+1 flow(source_1_bus_1_0_0)
+1 flow(source_2_bus_1_0_0)
= 0

c_e_MultiPeriodBus_balance(bus_1_0_1)_:
+1 flow(source_0_bus_1_0_1)
+1 flow(source_1_bus_1_0_1)
+1 flow(source_2_bus_1_0_1)
= 0

c_e_MultiPeriodBus_balance(bus_1_1_2)_:
+1 flow(source_0_bus_1_1_2)
+1 flow(source_1_bus_1_1_2)
+1 flow(source_2_bus_1_1_2)
= 0

c_e_MultiPeriodBus_balance(bus_1_1_3)_:
+1 flow(source_0_bus_1_1_3)
+1 flow(source_1_bus_1_1_3)
+1 flow(source_2_bus_1_1_3)
= 0

c_e_MultiPeriodBus_balance(bus_1_2_4)_:
+1 flow(source_0_bus_1_2_4)
+1 flow(source_1_bus_1_2_4)
+1 flow(source_2_bus_1_2_4)
= 0

c_e_MultiPeriodBus_balance(bus_1_2_5)_:
+1 flow(source_0_bus_1_2_5)
+1 flow(source_1_bus_1_2_5)
+1 flow(source_2_bus_1_2_5)
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

c_e_MultiPeriodInvestmentFlow_total_rule(source_1_bus_1_0)_:
-1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_1_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_1_bus_1_1)_:
-1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_1)
+1 MultiPeriodInvestmentFlow_old(source_1_bus_1_1)
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_1_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_1_bus_1_2)_:
-1 MultiPeriodInvestmentFlow_invest(source_1_bus_1_2)
+1 MultiPeriodInvestmentFlow_old(source_1_bus_1_2)
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_1)
+1 MultiPeriodInvestmentFlow_total(source_1_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_2_bus_1_0)_:
-1 MultiPeriodInvestmentFlow_invest(source_2_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_2_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_2_bus_1_1)_:
-1 MultiPeriodInvestmentFlow_invest(source_2_bus_1_1)
+1 MultiPeriodInvestmentFlow_old(source_2_bus_1_1)
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_0)
+1 MultiPeriodInvestmentFlow_total(source_2_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(source_2_bus_1_2)_:
-1 MultiPeriodInvestmentFlow_invest(source_2_bus_1_2)
+1 MultiPeriodInvestmentFlow_old(source_2_bus_1_2)
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_1)
+1 MultiPeriodInvestmentFlow_total(source_2_bus_1_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_1_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_1_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_1_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_2_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_2_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(source_2_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_1_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_1_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_1_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_2_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_2_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(source_2_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_2)
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

c_e_MultiPeriodInvestmentFlow_old_rule(source_1_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old(source_1_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_1_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old(source_1_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_1_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old(source_1_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_end(source_1_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_2_bus_1_0)_:
+1 MultiPeriodInvestmentFlow_old(source_2_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_0)
-1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_2_bus_1_1)_:
+1 MultiPeriodInvestmentFlow_old(source_2_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_1)
-1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(source_2_bus_1_2)_:
+1 MultiPeriodInvestmentFlow_old(source_2_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_end(source_2_bus_1_2)
-1 MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_2)
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

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_0)
+1 flow(source_1_bus_1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_0)
+1 flow(source_1_bus_1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_1)
+1 flow(source_1_bus_1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_1)
+1 flow(source_1_bus_1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_2)
+1 flow(source_1_bus_1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_1_bus_1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(source_1_bus_1_2)
+1 flow(source_1_bus_1_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_0_0)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_0)
+1 flow(source_2_bus_1_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_0_1)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_0)
+1 flow(source_2_bus_1_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_1_2)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_1)
+1 flow(source_2_bus_1_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_1_3)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_1)
+1 flow(source_2_bus_1_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_2_4)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_2)
+1 flow(source_2_bus_1_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(source_2_bus_1_2_5)_:
-1 MultiPeriodInvestmentFlow_total(source_2_bus_1_2)
+1 flow(source_2_bus_1_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source_0_bus_1_0_0) <= +inf
   0 <= flow(source_0_bus_1_0_1) <= +inf
   0 <= flow(source_0_bus_1_1_2) <= +inf
   0 <= flow(source_0_bus_1_1_3) <= +inf
   0 <= flow(source_0_bus_1_2_4) <= +inf
   0 <= flow(source_0_bus_1_2_5) <= +inf
   0 <= flow(source_1_bus_1_0_0) <= +inf
   0 <= flow(source_1_bus_1_0_1) <= +inf
   0 <= flow(source_1_bus_1_1_2) <= +inf
   0 <= flow(source_1_bus_1_1_3) <= +inf
   0 <= flow(source_1_bus_1_2_4) <= +inf
   0 <= flow(source_1_bus_1_2_5) <= +inf
   0 <= flow(source_2_bus_1_0_0) <= +inf
   0 <= flow(source_2_bus_1_0_1) <= +inf
   0 <= flow(source_2_bus_1_1_2) <= +inf
   0 <= flow(source_2_bus_1_1_3) <= +inf
   0 <= flow(source_2_bus_1_2_4) <= +inf
   0 <= flow(source_2_bus_1_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_1_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_1_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_1_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_2_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_2_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(source_2_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_1_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_1_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_1_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_2_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_2_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(source_2_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_1_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_1_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_1_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_2_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_2_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(source_2_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_1_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_1_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_1_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_2_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_2_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(source_2_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_0_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_1_bus_1_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(source_2_bus_1_2) <= +inf
end
