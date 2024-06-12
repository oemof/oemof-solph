\* Source Pyomo model name=Model *\

min 
objective:
+1.8354884429290608 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0)
+1.2115039389350062 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_1)
+0.5997544252153503 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_2)
+50 flow(gasBus_chp_powerplant_gas_0)
+50 flow(gasBus_chp_powerplant_gas_1)
+49.01960784313725 flow(gasBus_chp_powerplant_gas_2)
+49.01960784313725 flow(gasBus_chp_powerplant_gas_3)
+48.058439061899264 flow(gasBus_chp_powerplant_gas_4)
+48.058439061899264 flow(gasBus_chp_powerplant_gas_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(chp_powerplant_gas_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(chp_powerplant_gas_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(chp_powerplant_gas_electricityBus_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(chp_powerplant_gas_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(chp_powerplant_gas_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(chp_powerplant_gas_electricityBus_5)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_chp_powerplant_gas_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_chp_powerplant_gas_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_chp_powerplant_gas_2)
= 0

c_e_BusBlock_balance(gasBus_3)_:
+1 flow(gasBus_chp_powerplant_gas_3)
= 0

c_e_BusBlock_balance(gasBus_4)_:
+1 flow(gasBus_chp_powerplant_gas_4)
= 0

c_e_BusBlock_balance(gasBus_5)_:
+1 flow(gasBus_chp_powerplant_gas_5)
= 0

c_e_BusBlock_balance(heatBus_0)_:
+1 flow(chp_powerplant_gas_heatBus_0)
= 0

c_e_BusBlock_balance(heatBus_1)_:
+1 flow(chp_powerplant_gas_heatBus_1)
= 0

c_e_BusBlock_balance(heatBus_2)_:
+1 flow(chp_powerplant_gas_heatBus_2)
= 0

c_e_BusBlock_balance(heatBus_3)_:
+1 flow(chp_powerplant_gas_heatBus_3)
= 0

c_e_BusBlock_balance(heatBus_4)_:
+1 flow(chp_powerplant_gas_heatBus_4)
= 0

c_e_BusBlock_balance(heatBus_5)_:
+1 flow(chp_powerplant_gas_heatBus_5)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_0)_:
+0.4 flow(gasBus_chp_powerplant_gas_0)
-1 flow(chp_powerplant_gas_electricityBus_0)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_0)_:
+0.5 flow(gasBus_chp_powerplant_gas_0)
-1 flow(chp_powerplant_gas_heatBus_0)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_1)_:
+0.4 flow(gasBus_chp_powerplant_gas_1)
-1 flow(chp_powerplant_gas_electricityBus_1)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_1)_:
+0.5 flow(gasBus_chp_powerplant_gas_1)
-1 flow(chp_powerplant_gas_heatBus_1)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_2)_:
+0.4 flow(gasBus_chp_powerplant_gas_2)
-1 flow(chp_powerplant_gas_electricityBus_2)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_2)_:
+0.5 flow(gasBus_chp_powerplant_gas_2)
-1 flow(chp_powerplant_gas_heatBus_2)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_3)_:
+0.4 flow(gasBus_chp_powerplant_gas_3)
-1 flow(chp_powerplant_gas_electricityBus_3)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_3)_:
+0.5 flow(gasBus_chp_powerplant_gas_3)
-1 flow(chp_powerplant_gas_heatBus_3)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_4)_:
+0.4 flow(gasBus_chp_powerplant_gas_4)
-1 flow(chp_powerplant_gas_electricityBus_4)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_4)_:
+0.5 flow(gasBus_chp_powerplant_gas_4)
-1 flow(chp_powerplant_gas_heatBus_4)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_electricityBus_5)_:
+0.4 flow(gasBus_chp_powerplant_gas_5)
-1 flow(chp_powerplant_gas_electricityBus_5)
= 0

c_e_ConverterBlock_relation(chp_powerplant_gas_gasBus_heatBus_5)_:
+0.5 flow(gasBus_chp_powerplant_gas_5)
-1 flow(chp_powerplant_gas_heatBus_5)
= 0

c_e_InvestmentFlowBlock_total_rule(gasBus_chp_powerplant_gas_0)_:
-1 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0)
+1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
= 0

c_e_InvestmentFlowBlock_total_rule(gasBus_chp_powerplant_gas_1)_:
-1 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_1)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
+1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_1)
+1 InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_1)
= 0

c_e_InvestmentFlowBlock_total_rule(gasBus_chp_powerplant_gas_2)_:
-1 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_2)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_1)
+1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_2)
+1 InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gasBus_chp_powerplant_gas_0)_:
+1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gasBus_chp_powerplant_gas_1)_:
+1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(gasBus_chp_powerplant_gas_2)_:
+1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gasBus_chp_powerplant_gas_0)_:
+1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gasBus_chp_powerplant_gas_1)_:
+1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(gasBus_chp_powerplant_gas_2)_:
+1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_2)
= 0

c_e_InvestmentFlowBlock_old_rule(gasBus_chp_powerplant_gas_0)_:
+1 InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_0)
-1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_0)
-1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_0)
= 0

c_e_InvestmentFlowBlock_old_rule(gasBus_chp_powerplant_gas_1)_:
+1 InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_1)
-1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_1)
-1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_1)
= 0

c_e_InvestmentFlowBlock_old_rule(gasBus_chp_powerplant_gas_2)_:
+1 InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_2)
-1 InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_2)
-1 InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_2)
= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_0_0)_:
+1 flow(gasBus_chp_powerplant_gas_0)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_0_1)_:
+1 flow(gasBus_chp_powerplant_gas_1)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_1_2)_:
+1 flow(gasBus_chp_powerplant_gas_2)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_1)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_1_3)_:
+1 flow(gasBus_chp_powerplant_gas_3)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_1)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_2_4)_:
+1 flow(gasBus_chp_powerplant_gas_4)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_2)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_2_5)_:
+1 flow(gasBus_chp_powerplant_gas_5)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0) <= 1000
   0 <= InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_1) <= 1000
   0 <= InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_2) <= 1000
   0 <= flow(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_3) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_4) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_5) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_2) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_3) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_4) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_5) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_2) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_3) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_4) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_5) <= +inf
   0 <= InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= InvestmentFlowBlock_old(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(gasBus_chp_powerplant_gas_2) <= +inf
end
