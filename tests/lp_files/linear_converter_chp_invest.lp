\* Source Pyomo model name=Model *\

min 
objective:
+20 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0)
+50 flow(gasBus_chp_powerplant_gas_0)
+50 flow(gasBus_chp_powerplant_gas_1)
+50 flow(gasBus_chp_powerplant_gas_2)

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

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_chp_powerplant_gas_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_chp_powerplant_gas_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_chp_powerplant_gas_2)
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

c_e_InvestmentFlowBlock_total_rule(gasBus_chp_powerplant_gas_0)_:
-1 InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0)
+1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_0_0)_:
+1 flow(gasBus_chp_powerplant_gas_0)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_0_1)_:
+1 flow(gasBus_chp_powerplant_gas_1)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
<= 0

c_u_InvestmentFlowBlock_max(gasBus_chp_powerplant_gas_0_2)_:
+1 flow(gasBus_chp_powerplant_gas_2)
-1 InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(gasBus_chp_powerplant_gas_0) <= 1000
   0 <= flow(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_2) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(gasBus_chp_powerplant_gas_0) <= +inf
end
