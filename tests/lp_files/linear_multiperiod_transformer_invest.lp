\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+611567.18125290342 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_0)
+599575.66789500334 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_1)
+587819.28225000331 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_2)
+50 flow(powerplant_gas_electricity_0_0)
+50 flow(powerplant_gas_electricity_0_1)
+49.019607843137251 flow(powerplant_gas_electricity_1_2)
+49.019607843137251 flow(powerplant_gas_electricity_1_3)
+48.058439061899264 flow(powerplant_gas_electricity_2_4)
+48.058439061899264 flow(powerplant_gas_electricity_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0_0)
= 0

c_e_MultiPeriodBus_balance(electricity_0_1)_:
+1 flow(powerplant_gas_electricity_0_1)
= 0

c_e_MultiPeriodBus_balance(electricity_1_2)_:
+1 flow(powerplant_gas_electricity_1_2)
= 0

c_e_MultiPeriodBus_balance(electricity_1_3)_:
+1 flow(powerplant_gas_electricity_1_3)
= 0

c_e_MultiPeriodBus_balance(electricity_2_4)_:
+1 flow(powerplant_gas_electricity_2_4)
= 0

c_e_MultiPeriodBus_balance(electricity_2_5)_:
+1 flow(powerplant_gas_electricity_2_5)
= 0

c_e_MultiPeriodBus_balance(gas_0_0)_:
+1 flow(gas_powerplant_gas_0_0)
= 0

c_e_MultiPeriodBus_balance(gas_0_1)_:
+1 flow(gas_powerplant_gas_0_1)
= 0

c_e_MultiPeriodBus_balance(gas_1_2)_:
+1 flow(gas_powerplant_gas_1_2)
= 0

c_e_MultiPeriodBus_balance(gas_1_3)_:
+1 flow(gas_powerplant_gas_1_3)
= 0

c_e_MultiPeriodBus_balance(gas_2_4)_:
+1 flow(gas_powerplant_gas_2_4)
= 0

c_e_MultiPeriodBus_balance(gas_2_5)_:
+1 flow(gas_powerplant_gas_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_0_0)_:
+0.57999999999999996 flow(gas_powerplant_gas_0_0)
-1 flow(powerplant_gas_electricity_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_0_1)_:
+0.57999999999999996 flow(gas_powerplant_gas_0_1)
-1 flow(powerplant_gas_electricity_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_1_2)_:
+0.57999999999999996 flow(gas_powerplant_gas_1_2)
-1 flow(powerplant_gas_electricity_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_1_3)_:
+0.57999999999999996 flow(gas_powerplant_gas_1_3)
-1 flow(powerplant_gas_electricity_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_2_4)_:
+0.57999999999999996 flow(gas_powerplant_gas_2_4)
-1 flow(powerplant_gas_electricity_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_gas_electricity_2_5)_:
+0.57999999999999996 flow(gas_powerplant_gas_2_5)
-1 flow(powerplant_gas_electricity_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_electricity_0)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_electricity_1)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_1)
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_1)
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_electricity_2)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_2)
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_2)
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_1)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_electricity_0)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_electricity_1)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_electricity_2)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_electricity_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_electricity_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_electricity_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_electricity_0)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_0)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_0)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_electricity_1)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_1)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_1)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_electricity_2)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_2)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_2)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_0_0)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_0)
+1 flow(powerplant_gas_electricity_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_0_1)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_0)
+1 flow(powerplant_gas_electricity_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_1_2)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_1)
+1 flow(powerplant_gas_electricity_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_1_3)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_1)
+1 flow(powerplant_gas_electricity_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_2_4)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_2)
+1 flow(powerplant_gas_electricity_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_electricity_2_5)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_2)
+1 flow(powerplant_gas_electricity_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gas_powerplant_gas_0_0) <= +inf
   0 <= flow(gas_powerplant_gas_0_1) <= +inf
   0 <= flow(gas_powerplant_gas_1_2) <= +inf
   0 <= flow(gas_powerplant_gas_1_3) <= +inf
   0 <= flow(gas_powerplant_gas_2_4) <= +inf
   0 <= flow(gas_powerplant_gas_2_5) <= +inf
   0 <= flow(powerplant_gas_electricity_0_0) <= +inf
   0 <= flow(powerplant_gas_electricity_0_1) <= +inf
   0 <= flow(powerplant_gas_electricity_1_2) <= +inf
   0 <= flow(powerplant_gas_electricity_1_3) <= +inf
   0 <= flow(powerplant_gas_electricity_2_4) <= +inf
   0 <= flow(powerplant_gas_electricity_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_0) <= 1000
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_1) <= 1000
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_electricity_2) <= 1000
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_electricity_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_electricity_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_electricity_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_electricity_2) <= +inf
end
