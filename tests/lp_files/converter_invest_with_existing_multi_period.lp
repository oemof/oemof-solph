\* Source Pyomo model name=Model *\

min 
objective:
+20.0 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0)
+19.6078431372549 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_1)
+9.706853038245011 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_2)
+50 flow(powerplant_gas_coal_electricityBus_0)
+50 flow(powerplant_gas_coal_electricityBus_1)
+49.01960784313725 flow(powerplant_gas_coal_electricityBus_2)
+49.01960784313725 flow(powerplant_gas_coal_electricityBus_3)
+48.058439061899264 flow(powerplant_gas_coal_electricityBus_4)
+48.058439061899264 flow(powerplant_gas_coal_electricityBus_5)
+20 flow(powerplant_gas_coal_thermalBus_0)
+20 flow(powerplant_gas_coal_thermalBus_1)
+19.6078431372549 flow(powerplant_gas_coal_thermalBus_2)
+19.6078431372549 flow(powerplant_gas_coal_thermalBus_3)
+19.223375624759708 flow(powerplant_gas_coal_thermalBus_4)
+19.223375624759708 flow(powerplant_gas_coal_thermalBus_5)

s.t.

c_e_BusBlock_balance(coalBus_0)_:
+1 flow(coalBus_powerplant_gas_coal_0)
= 0

c_e_BusBlock_balance(coalBus_1)_:
+1 flow(coalBus_powerplant_gas_coal_1)
= 0

c_e_BusBlock_balance(coalBus_2)_:
+1 flow(coalBus_powerplant_gas_coal_2)
= 0

c_e_BusBlock_balance(coalBus_3)_:
+1 flow(coalBus_powerplant_gas_coal_3)
= 0

c_e_BusBlock_balance(coalBus_4)_:
+1 flow(coalBus_powerplant_gas_coal_4)
= 0

c_e_BusBlock_balance(coalBus_5)_:
+1 flow(coalBus_powerplant_gas_coal_5)
= 0

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(powerplant_gas_coal_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(powerplant_gas_coal_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(powerplant_gas_coal_electricityBus_5)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_powerplant_gas_coal_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_powerplant_gas_coal_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_powerplant_gas_coal_2)
= 0

c_e_BusBlock_balance(gasBus_3)_:
+1 flow(gasBus_powerplant_gas_coal_3)
= 0

c_e_BusBlock_balance(gasBus_4)_:
+1 flow(gasBus_powerplant_gas_coal_4)
= 0

c_e_BusBlock_balance(gasBus_5)_:
+1 flow(gasBus_powerplant_gas_coal_5)
= 0

c_e_BusBlock_balance(thermalBus_0)_:
+1 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_BusBlock_balance(thermalBus_1)_:
+1 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_BusBlock_balance(thermalBus_2)_:
+1 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_BusBlock_balance(thermalBus_3)_:
+1 flow(powerplant_gas_coal_thermalBus_3)
= 0

c_e_BusBlock_balance(thermalBus_4)_:
+1 flow(powerplant_gas_coal_thermalBus_4)
= 0

c_e_BusBlock_balance(thermalBus_5)_:
+1 flow(powerplant_gas_coal_thermalBus_5)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_0)_:
+0.3 flow(coalBus_powerplant_gas_coal_0)
-0.2 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_0)_:
+0.3 flow(gasBus_powerplant_gas_coal_0)
-0.58 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_0)_:
+0.5 flow(coalBus_powerplant_gas_coal_0)
-0.2 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_0)_:
+0.5 flow(gasBus_powerplant_gas_coal_0)
-0.58 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_1)_:
+0.3 flow(coalBus_powerplant_gas_coal_1)
-0.2 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_1)_:
+0.3 flow(gasBus_powerplant_gas_coal_1)
-0.58 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_1)_:
+0.5 flow(coalBus_powerplant_gas_coal_1)
-0.2 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_1)_:
+0.5 flow(gasBus_powerplant_gas_coal_1)
-0.58 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_2)_:
+0.3 flow(coalBus_powerplant_gas_coal_2)
-0.2 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_2)_:
+0.3 flow(gasBus_powerplant_gas_coal_2)
-0.58 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_2)_:
+0.5 flow(coalBus_powerplant_gas_coal_2)
-0.2 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_2)_:
+0.5 flow(gasBus_powerplant_gas_coal_2)
-0.58 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_3)_:
+0.3 flow(coalBus_powerplant_gas_coal_3)
-0.2 flow(powerplant_gas_coal_electricityBus_3)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_3)_:
+0.3 flow(gasBus_powerplant_gas_coal_3)
-0.58 flow(powerplant_gas_coal_electricityBus_3)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_3)_:
+0.5 flow(coalBus_powerplant_gas_coal_3)
-0.2 flow(powerplant_gas_coal_thermalBus_3)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_3)_:
+0.5 flow(gasBus_powerplant_gas_coal_3)
-0.58 flow(powerplant_gas_coal_thermalBus_3)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_4)_:
+0.3 flow(coalBus_powerplant_gas_coal_4)
-0.2 flow(powerplant_gas_coal_electricityBus_4)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_4)_:
+0.3 flow(gasBus_powerplant_gas_coal_4)
-0.58 flow(powerplant_gas_coal_electricityBus_4)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_4)_:
+0.5 flow(coalBus_powerplant_gas_coal_4)
-0.2 flow(powerplant_gas_coal_thermalBus_4)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_4)_:
+0.5 flow(gasBus_powerplant_gas_coal_4)
-0.58 flow(powerplant_gas_coal_thermalBus_4)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_5)_:
+0.3 flow(coalBus_powerplant_gas_coal_5)
-0.2 flow(powerplant_gas_coal_electricityBus_5)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_5)_:
+0.3 flow(gasBus_powerplant_gas_coal_5)
-0.58 flow(powerplant_gas_coal_electricityBus_5)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_5)_:
+0.5 flow(coalBus_powerplant_gas_coal_5)
-0.2 flow(powerplant_gas_coal_thermalBus_5)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_5)_:
+0.5 flow(gasBus_powerplant_gas_coal_5)
-0.58 flow(powerplant_gas_coal_thermalBus_5)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_coal_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0)
+1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
= 200

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_coal_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_1)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
+1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_1)
+1 InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_coal_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_2)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_1)
+1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_2)
+1 InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_coal_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_coal_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(powerplant_gas_coal_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0)
+1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_coal_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_coal_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_1)
= 200

c_e_InvestmentFlowBlock_old_rule_exo(powerplant_gas_coal_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_coal_electricityBus_0)_:
+1 InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_0)
-1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_coal_electricityBus_1)_:
+1 InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_1)
-1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(powerplant_gas_coal_electricityBus_2)_:
+1 InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_2)
-1 InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_0_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_0_1)_:
+1 flow(powerplant_gas_coal_electricityBus_1)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_1_2)_:
+1 flow(powerplant_gas_coal_electricityBus_2)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_1_3)_:
+1 flow(powerplant_gas_coal_electricityBus_3)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_2_4)_:
+1 flow(powerplant_gas_coal_electricityBus_4)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_2_5)_:
+1 flow(powerplant_gas_coal_electricityBus_5)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0) <= 1000
   0 <= InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_1) <= 1000
   0 <= InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_2) <= 1000
   0 <= flow(gasBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_3) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_4) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_5) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_3) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_4) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_5) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_3) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_4) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_5) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_0) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_1) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_2) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_3) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_4) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_5) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(powerplant_gas_coal_electricityBus_2) <= +inf
end
