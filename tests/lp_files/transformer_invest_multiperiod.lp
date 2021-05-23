\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+24.462687250116133 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_0)
+23.983026715800129 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_1)
+23.512771290000128 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_2)
+50 flow(powerplant_gas_coal_electricityBus_0_0)
+50 flow(powerplant_gas_coal_electricityBus_0_1)
+49.019607843137251 flow(powerplant_gas_coal_electricityBus_1_2)
+49.019607843137251 flow(powerplant_gas_coal_electricityBus_1_3)
+48.058439061899264 flow(powerplant_gas_coal_electricityBus_2_4)
+48.058439061899264 flow(powerplant_gas_coal_electricityBus_2_5)
+20 flow(powerplant_gas_coal_thermalBus_0_0)
+20 flow(powerplant_gas_coal_thermalBus_0_1)
+19.6078431372549 flow(powerplant_gas_coal_thermalBus_1_2)
+19.6078431372549 flow(powerplant_gas_coal_thermalBus_1_3)
+19.223375624759708 flow(powerplant_gas_coal_thermalBus_2_4)
+19.223375624759708 flow(powerplant_gas_coal_thermalBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(coalBus_0_0)_:
+1 flow(coalBus_powerplant_gas_coal_0_0)
= 0

c_e_MultiPeriodBus_balance(coalBus_0_1)_:
+1 flow(coalBus_powerplant_gas_coal_0_1)
= 0

c_e_MultiPeriodBus_balance(coalBus_1_2)_:
+1 flow(coalBus_powerplant_gas_coal_1_2)
= 0

c_e_MultiPeriodBus_balance(coalBus_1_3)_:
+1 flow(coalBus_powerplant_gas_coal_1_3)
= 0

c_e_MultiPeriodBus_balance(coalBus_2_4)_:
+1 flow(coalBus_powerplant_gas_coal_2_4)
= 0

c_e_MultiPeriodBus_balance(coalBus_2_5)_:
+1 flow(coalBus_powerplant_gas_coal_2_5)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(powerplant_gas_coal_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(powerplant_gas_coal_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(powerplant_gas_coal_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(powerplant_gas_coal_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(powerplant_gas_coal_electricityBus_2_5)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_0)_:
+1 flow(gasBus_powerplant_gas_coal_0_0)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_1)_:
+1 flow(gasBus_powerplant_gas_coal_0_1)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_2)_:
+1 flow(gasBus_powerplant_gas_coal_1_2)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_3)_:
+1 flow(gasBus_powerplant_gas_coal_1_3)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_4)_:
+1 flow(gasBus_powerplant_gas_coal_2_4)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_5)_:
+1 flow(gasBus_powerplant_gas_coal_2_5)
= 0

c_e_MultiPeriodBus_balance(thermalBus_0_0)_:
+1 flow(powerplant_gas_coal_thermalBus_0_0)
= 0

c_e_MultiPeriodBus_balance(thermalBus_0_1)_:
+1 flow(powerplant_gas_coal_thermalBus_0_1)
= 0

c_e_MultiPeriodBus_balance(thermalBus_1_2)_:
+1 flow(powerplant_gas_coal_thermalBus_1_2)
= 0

c_e_MultiPeriodBus_balance(thermalBus_1_3)_:
+1 flow(powerplant_gas_coal_thermalBus_1_3)
= 0

c_e_MultiPeriodBus_balance(thermalBus_2_4)_:
+1 flow(powerplant_gas_coal_thermalBus_2_4)
= 0

c_e_MultiPeriodBus_balance(thermalBus_2_5)_:
+1 flow(powerplant_gas_coal_thermalBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_0_0)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_0_0)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_0_1)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_0_1)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_1_2)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_1_2)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_1_3)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_1_3)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_2_4)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_2_4)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_electricityBus_2_5)_:
+0.29999999999999999 flow(coalBus_powerplant_gas_coal_2_5)
-0.20000000000000001 flow(powerplant_gas_coal_electricityBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_0_0)_:
+0.5 flow(coalBus_powerplant_gas_coal_0_0)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_0_1)_:
+0.5 flow(coalBus_powerplant_gas_coal_0_1)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_1_2)_:
+0.5 flow(coalBus_powerplant_gas_coal_1_2)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_1_3)_:
+0.5 flow(coalBus_powerplant_gas_coal_1_3)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_2_4)_:
+0.5 flow(coalBus_powerplant_gas_coal_2_4)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_coalBus_thermalBus_2_5)_:
+0.5 flow(coalBus_powerplant_gas_coal_2_5)
-0.20000000000000001 flow(powerplant_gas_coal_thermalBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_0_0)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_0_0)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_0_1)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_0_1)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_1_2)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_1_2)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_1_3)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_1_3)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_2_4)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_2_4)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_electricityBus_2_5)_:
+0.29999999999999999 flow(gasBus_powerplant_gas_coal_2_5)
-0.57999999999999996 flow(powerplant_gas_coal_electricityBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_0_0)_:
+0.5 flow(gasBus_powerplant_gas_coal_0_0)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_0_1)_:
+0.5 flow(gasBus_powerplant_gas_coal_0_1)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_1_2)_:
+0.5 flow(gasBus_powerplant_gas_coal_1_2)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_1_3)_:
+0.5 flow(gasBus_powerplant_gas_coal_1_3)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_2_4)_:
+0.5 flow(gasBus_powerplant_gas_coal_2_4)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplant_gas_coal_gasBus_thermalBus_2_5)_:
+0.5 flow(gasBus_powerplant_gas_coal_2_5)
-0.57999999999999996 flow(powerplant_gas_coal_thermalBus_2_5)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_coal_electricityBus_0)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_coal_electricityBus_1)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_1)
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_1)
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_0)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(powerplant_gas_coal_electricityBus_2)_:
-1 MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_2)
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_2)
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_1)
+1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_coal_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_coal_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(powerplant_gas_coal_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_coal_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_coal_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(powerplant_gas_coal_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_coal_electricityBus_0)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_0)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_coal_electricityBus_1)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_1)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(powerplant_gas_coal_electricityBus_2)_:
+1 MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_2)
-1 MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_0_0)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_0)
+1 flow(powerplant_gas_coal_electricityBus_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_0_1)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_0)
+1 flow(powerplant_gas_coal_electricityBus_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_1_2)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_1)
+1 flow(powerplant_gas_coal_electricityBus_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_1_3)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_1)
+1 flow(powerplant_gas_coal_electricityBus_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_2_4)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_2)
+1 flow(powerplant_gas_coal_electricityBus_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(powerplant_gas_coal_electricityBus_2_5)_:
-1 MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_2)
+1 flow(powerplant_gas_coal_electricityBus_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(coalBus_powerplant_gas_coal_0_0) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_0_1) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_1_2) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_1_3) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_2_4) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_2_5) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_0_0) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_0_1) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_1_2) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_1_3) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_2_4) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_2_5) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_0_0) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_0_1) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_1_2) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_1_3) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_2_4) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_2_5) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_0_0) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_0_1) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_1_2) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_1_3) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_2_4) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_0) <= 1000
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_1) <= 1000
   0 <= MultiPeriodInvestmentFlow_invest(powerplant_gas_coal_electricityBus_2) <= 1000
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(powerplant_gas_coal_electricityBus_2) <= +inf
end
