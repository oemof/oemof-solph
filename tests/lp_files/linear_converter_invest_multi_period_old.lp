\* Source Pyomo model name=Model *\

min 
objective:
+20.0 InvestmentFlowBlock_invest(powerplant_gas_electricity_0)
+19.6078431372549 InvestmentFlowBlock_invest(powerplant_gas_electricity_1)
+9.706853038245011 InvestmentFlowBlock_invest(powerplant_gas_electricity_2)
+50 flow(powerplant_gas_electricity_0_0)
+50 flow(powerplant_gas_electricity_0_1)
+49.01960784313725 flow(powerplant_gas_electricity_1_2)
+49.01960784313725 flow(powerplant_gas_electricity_1_3)
+48.058439061899264 flow(powerplant_gas_electricity_2_4)
+48.058439061899264 flow(powerplant_gas_electricity_2_5)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(powerplant_gas_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_1_2)_:
+1 flow(powerplant_gas_electricity_1_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(powerplant_gas_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_2_4)_:
+1 flow(powerplant_gas_electricity_2_4)
= 0

c_e_BusBlock_balance(electricity_2_5)_:
+1 flow(powerplant_gas_electricity_2_5)
= 0

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_powerplant_gas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_powerplant_gas_0_1)
= 0

c_e_BusBlock_balance(gas_1_2)_:
+1 flow(gas_powerplant_gas_1_2)
= 0

c_e_BusBlock_balance(gas_1_3)_:
+1 flow(gas_powerplant_gas_1_3)
= 0

c_e_BusBlock_balance(gas_2_4)_:
+1 flow(gas_powerplant_gas_2_4)
= 0

c_e_BusBlock_balance(gas_2_5)_:
+1 flow(gas_powerplant_gas_2_5)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_0)_:
-1 flow(powerplant_gas_electricity_0_0)
+0.58 flow(gas_powerplant_gas_0_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_1)_:
-1 flow(powerplant_gas_electricity_0_1)
+0.58 flow(gas_powerplant_gas_0_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_1_2)_:
-1 flow(powerplant_gas_electricity_1_2)
+0.58 flow(gas_powerplant_gas_1_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_1_3)_:
-1 flow(powerplant_gas_electricity_1_3)
+0.58 flow(gas_powerplant_gas_1_3)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_2_4)_:
-1 flow(powerplant_gas_electricity_2_4)
+0.58 flow(gas_powerplant_gas_2_4)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_2_5)_:
-1 flow(powerplant_gas_electricity_2_5)
+0.58 flow(gas_powerplant_gas_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_electricity_0)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity_0)
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
= 50

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_electricity_1)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity_1)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_1)
+1 InvestmentFlowBlock_old(powerplant_gas_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_electricity_2)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity_2)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_1)
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_2)
+1 InvestmentFlowBlock_old(powerplant_gas_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_electricity_0)_:
+1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_electricity_1)_:
+1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_electricity_2)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity_0)
+1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_1)
= 50

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_electricity_0)_:
-1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_0)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_0)
+1 InvestmentFlowBlock_old(powerplant_gas_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_electricity_1)_:
+1 InvestmentFlowBlock_old(powerplant_gas_electricity_1)
-1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_1)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_electricity_2)_:
+1 InvestmentFlowBlock_old(powerplant_gas_electricity_2)
-1 InvestmentFlowBlock_old_end(powerplant_gas_electricity_2)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0_0)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0_1)_:
+1 flow(powerplant_gas_electricity_0_1)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_1_2)_:
+1 flow(powerplant_gas_electricity_1_2)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_1_3)_:
+1 flow(powerplant_gas_electricity_1_3)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_2_4)_:
+1 flow(powerplant_gas_electricity_2_4)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_2_5)_:
+1 flow(powerplant_gas_electricity_2_5)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_2)
<= 0

c_u_InvestmentFlowBlock_overall_maximum(powerplant_gas_electricity_0)_:
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 10000

c_u_InvestmentFlowBlock_overall_maximum(powerplant_gas_electricity_1)_:
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_1)
<= 10000

c_u_InvestmentFlowBlock_overall_maximum(powerplant_gas_electricity_2)_:
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_2)
<= 10000

c_l_InvestmentFlowBlock_overall_minimum(powerplant_gas_electricity)_:
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_2)
>= 200

bounds
   0 <= InvestmentFlowBlock_invest(powerplant_gas_electricity_0) <= 1000
   0 <= InvestmentFlowBlock_invest(powerplant_gas_electricity_1) <= 1000
   0 <= InvestmentFlowBlock_invest(powerplant_gas_electricity_2) <= 1000
   0 <= flow(powerplant_gas_electricity_0_0) <= +inf
   0 <= flow(powerplant_gas_electricity_0_1) <= +inf
   0 <= flow(powerplant_gas_electricity_1_2) <= +inf
   0 <= flow(powerplant_gas_electricity_1_3) <= +inf
   0 <= flow(powerplant_gas_electricity_2_4) <= +inf
   0 <= flow(powerplant_gas_electricity_2_5) <= +inf
   0 <= flow(gas_powerplant_gas_0_0) <= +inf
   0 <= flow(gas_powerplant_gas_0_1) <= +inf
   0 <= flow(gas_powerplant_gas_1_2) <= +inf
   0 <= flow(gas_powerplant_gas_1_3) <= +inf
   0 <= flow(gas_powerplant_gas_2_4) <= +inf
   0 <= flow(gas_powerplant_gas_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_electricity_0) <= +inf
end
