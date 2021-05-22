\* Source Pyomo model name=Model *\

min 
objective:
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+23 flow(powerplant_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
+1 flow(powerplant_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(powerplant_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(powerplant_electricityBus_2)
= 0

c_e_Bus_balance(gasBus_0)_:
+1 flow(gasBus_powerplant_0)
= 0

c_e_Bus_balance(gasBus_1)_:
+1 flow(gasBus_powerplant_1)
= 0

c_e_Bus_balance(gasBus_2)_:
+1 flow(gasBus_powerplant_2)
= 0

c_e_Transformer_relation(powerplant_gasBus_electricityBus_0)_:
+1 flow(gasBus_powerplant_0)
-1 flow(powerplant_electricityBus_0)
= 0

c_e_Transformer_relation(powerplant_gasBus_electricityBus_1)_:
+1 flow(gasBus_powerplant_1)
-1 flow(powerplant_electricityBus_1)
= 0

c_e_Transformer_relation(powerplant_gasBus_electricityBus_2)_:
+1 flow(gasBus_powerplant_2)
-1 flow(powerplant_electricityBus_2)
= 0

c_u_InvestmentFlow_max(powerplant_electricityBus_0)_:
-1 InvestmentFlow_invest(powerplant_electricityBus)
+1 flow(powerplant_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(powerplant_electricityBus_1)_:
-1 InvestmentFlow_invest(powerplant_electricityBus)
+1 flow(powerplant_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(powerplant_electricityBus_2)_:
-1 InvestmentFlow_invest(powerplant_electricityBus)
+1 flow(powerplant_electricityBus_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gasBus_powerplant_0) <= +inf
   0 <= flow(gasBus_powerplant_1) <= +inf
   0 <= flow(gasBus_powerplant_2) <= +inf
   0 <= flow(powerplant_electricityBus_0) <= +inf
   0 <= flow(powerplant_electricityBus_1) <= +inf
   0 <= flow(powerplant_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(powerplant_electricityBus) <= +inf
end
