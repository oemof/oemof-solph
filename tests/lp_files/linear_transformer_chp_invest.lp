\* Source Pyomo model name=Model *\

min 
objective:
+20 InvestmentFlow_invest(gasBus_chp_powerplant_gas)
+50 flow(gasBus_chp_powerplant_gas_0)
+50 flow(gasBus_chp_powerplant_gas_1)
+50 flow(gasBus_chp_powerplant_gas_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
+1 flow(chp_powerplant_gas_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(chp_powerplant_gas_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(chp_powerplant_gas_electricityBus_2)
= 0

c_e_Bus_balance(gasBus_0)_:
+1 flow(gasBus_chp_powerplant_gas_0)
= 0

c_e_Bus_balance(gasBus_1)_:
+1 flow(gasBus_chp_powerplant_gas_1)
= 0

c_e_Bus_balance(gasBus_2)_:
+1 flow(gasBus_chp_powerplant_gas_2)
= 0

c_e_Bus_balance(heatBus_0)_:
+1 flow(chp_powerplant_gas_heatBus_0)
= 0

c_e_Bus_balance(heatBus_1)_:
+1 flow(chp_powerplant_gas_heatBus_1)
= 0

c_e_Bus_balance(heatBus_2)_:
+1 flow(chp_powerplant_gas_heatBus_2)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_electricityBus_0)_:
-2.5 flow(chp_powerplant_gas_electricityBus_0)
+1 flow(gasBus_chp_powerplant_gas_0)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_electricityBus_1)_:
-2.5 flow(chp_powerplant_gas_electricityBus_1)
+1 flow(gasBus_chp_powerplant_gas_1)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_electricityBus_2)_:
-2.5 flow(chp_powerplant_gas_electricityBus_2)
+1 flow(gasBus_chp_powerplant_gas_2)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_heatBus_0)_:
-2 flow(chp_powerplant_gas_heatBus_0)
+1 flow(gasBus_chp_powerplant_gas_0)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_heatBus_1)_:
-2 flow(chp_powerplant_gas_heatBus_1)
+1 flow(gasBus_chp_powerplant_gas_1)
= 0

c_e_Transformer_relation(chp_powerplant_gas_gasBus_heatBus_2)_:
-2 flow(chp_powerplant_gas_heatBus_2)
+1 flow(gasBus_chp_powerplant_gas_2)
= 0

c_u_InvestmentFlow_max(gasBus_chp_powerplant_gas_0)_:
-1 InvestmentFlow_invest(gasBus_chp_powerplant_gas)
+1 flow(gasBus_chp_powerplant_gas_0)
<= 0

c_u_InvestmentFlow_max(gasBus_chp_powerplant_gas_1)_:
-1 InvestmentFlow_invest(gasBus_chp_powerplant_gas)
+1 flow(gasBus_chp_powerplant_gas_1)
<= 0

c_u_InvestmentFlow_max(gasBus_chp_powerplant_gas_2)_:
-1 InvestmentFlow_invest(gasBus_chp_powerplant_gas)
+1 flow(gasBus_chp_powerplant_gas_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(chp_powerplant_gas_electricityBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_electricityBus_2) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_0) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_1) <= +inf
   0 <= flow(chp_powerplant_gas_heatBus_2) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_0) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_1) <= +inf
   0 <= flow(gasBus_chp_powerplant_gas_2) <= +inf
   0 <= InvestmentFlow_invest(gasBus_chp_powerplant_gas) <= 1000
end
