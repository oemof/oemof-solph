\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+146.22299118938992 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_0)
+143.35587371508814 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_1)
+140.54497423047857 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_2)
+23 flow(powerplant_electricityBus_0_0)
+23 flow(powerplant_electricityBus_0_1)
+22.549019607843135 flow(powerplant_electricityBus_1_2)
+22.549019607843135 flow(powerplant_electricityBus_1_3)
+22.106881968473662 flow(powerplant_electricityBus_2_4)
+22.106881968473662 flow(powerplant_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(powerplant_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(powerplant_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(powerplant_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(powerplant_electricityBus_2_5)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_0)_:
+1 flow(gasBus_powerplant_0_0)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_1)_:
+1 flow(gasBus_powerplant_0_1)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_2)_:
+1 flow(gasBus_powerplant_1_2)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_3)_:
+1 flow(gasBus_powerplant_1_3)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_4)_:
+1 flow(gasBus_powerplant_2_4)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_5)_:
+1 flow(gasBus_powerplant_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_0_0)_:
+1 flow(gasBus_powerplant_0_0)
-1 flow(powerplant_electricityBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_0_1)_:
+1 flow(gasBus_powerplant_0_1)
-1 flow(powerplant_electricityBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_1_2)_:
+1 flow(gasBus_powerplant_1_2)
-1 flow(powerplant_electricityBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_1_3)_:
+1 flow(gasBus_powerplant_1_3)
-1 flow(powerplant_electricityBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_2_4)_:
+1 flow(gasBus_powerplant_2_4)
-1 flow(powerplant_electricityBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gasBus_electricityBus_2_5)_:
+1 flow(gasBus_powerplant_2_5)
-1 flow(powerplant_electricityBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(powerplant_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(powerplant_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_summed_min(powerplant_electricityBus)_:
+1000 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0)
+1000 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1)
+1000 MultiPeriodInvestmentFlow_total(powerplant_electricityBus_2)
-1 flow(powerplant_electricityBus_0_0)
-1 flow(powerplant_electricityBus_0_1)
-1 flow(powerplant_electricityBus_1_2)
-1 flow(powerplant_electricityBus_1_3)
-1 flow(powerplant_electricityBus_2_4)
-1 flow(powerplant_electricityBus_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gasBus_powerplant_0_0) <= +inf
   0 <= flow(gasBus_powerplant_0_1) <= +inf
   0 <= flow(gasBus_powerplant_1_2) <= +inf
   0 <= flow(gasBus_powerplant_1_3) <= +inf
   0 <= flow(gasBus_powerplant_2_4) <= +inf
   0 <= flow(gasBus_powerplant_2_5) <= +inf
   0 <= flow(powerplant_electricityBus_0_0) <= +inf
   0 <= flow(powerplant_electricityBus_0_1) <= +inf
   0 <= flow(powerplant_electricityBus_1_2) <= +inf
   0 <= flow(powerplant_electricityBus_1_3) <= +inf
   0 <= flow(powerplant_electricityBus_2_4) <= +inf
   0 <= flow(powerplant_electricityBus_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_electricityBus_2) <= +inf
end
