\* Source Pyomo model name=OperationalModel *\

min 
objective:
+20 InvestmentFlow_invest(powerplant_gas_coal_electricityBus)
+50 flow(powerplant_gas_coal_electricityBus_0)
+50 flow(powerplant_gas_coal_electricityBus_1)
+50 flow(powerplant_gas_coal_electricityBus_2)

s.t.

c_e_Bus_balance(coalBus_0)_:
+1 flow(coalBus_powerplant_gas_coal_0)
= 0

c_e_Bus_balance(coalBus_1)_:
+1 flow(coalBus_powerplant_gas_coal_1)
= 0

c_e_Bus_balance(coalBus_2)_:
+1 flow(coalBus_powerplant_gas_coal_2)
= 0

c_e_Bus_balance(electricityBus_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_Bus_balance(gasBus_0)_:
+1 flow(gasBus_powerplant_gas_coal_0)
= 0

c_e_Bus_balance(gasBus_1)_:
+1 flow(gasBus_powerplant_gas_coal_1)
= 0

c_e_Bus_balance(gasBus_2)_:
+1 flow(gasBus_powerplant_gas_coal_2)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_coalBus_0)_:
-0.20000000000000001 flow(coalBus_powerplant_gas_coal_0)
+1 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_coalBus_1)_:
-0.20000000000000001 flow(coalBus_powerplant_gas_coal_1)
+1 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_coalBus_2)_:
-0.20000000000000001 flow(coalBus_powerplant_gas_coal_2)
+1 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_gasBus_0)_:
-0.57999999999999996 flow(gasBus_powerplant_gas_coal_0)
+1 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_gasBus_1)_:
-0.57999999999999996 flow(gasBus_powerplant_gas_coal_1)
+1 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_LinearN1Transformer_relation(powerplant_gas_coal_gasBus_2)_:
-0.57999999999999996 flow(gasBus_powerplant_gas_coal_2)
+1 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_u_InvestmentFlow_max(powerplant_gas_coal_electricityBus_0)_:
-1 InvestmentFlow_invest(powerplant_gas_coal_electricityBus)
+1 flow(powerplant_gas_coal_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(powerplant_gas_coal_electricityBus_1)_:
-1 InvestmentFlow_invest(powerplant_gas_coal_electricityBus)
+1 flow(powerplant_gas_coal_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(powerplant_gas_coal_electricityBus_2)_:
-1 InvestmentFlow_invest(powerplant_gas_coal_electricityBus)
+1 flow(powerplant_gas_coal_electricityBus_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(coalBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(powerplant_gas_coal_electricityBus) <= 1000
end
