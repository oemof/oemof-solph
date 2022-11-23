\* Source Pyomo model name=Model *\

min
objective:
+20 InvestmentFlowBlock_invest(powerplant_gas_electricity)
+50 flow(powerplant_gas_electricity_0)
+50 flow(powerplant_gas_electricity_1)
+50 flow(powerplant_gas_electricity_2)

s.t.

c_e_BusBlock_balance(electricity_0)_:
+1 flow(powerplant_gas_electricity_0)
= 0

c_e_BusBlock_balance(electricity_1)_:
+1 flow(powerplant_gas_electricity_1)
= 0

c_e_BusBlock_balance(electricity_2)_:
+1 flow(powerplant_gas_electricity_2)
= 0

c_e_BusBlock_balance(gas_0)_:
+1 flow(gas_powerplant_gas_0)
= 0

c_e_BusBlock_balance(gas_1)_:
+1 flow(gas_powerplant_gas_1)
= 0

c_e_BusBlock_balance(gas_2)_:
+1 flow(gas_powerplant_gas_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0)_:
+0.57999999999999996 flow(gas_powerplant_gas_0)
-1 flow(powerplant_gas_electricity_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_1)_:
+0.57999999999999996 flow(gas_powerplant_gas_1)
-1 flow(powerplant_gas_electricity_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_2)_:
+0.57999999999999996 flow(gas_powerplant_gas_2)
-1 flow(powerplant_gas_electricity_2)
= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity)
+1 flow(powerplant_gas_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_1)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity)
+1 flow(powerplant_gas_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_2)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity)
+1 flow(powerplant_gas_electricity_2)
<= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gas_powerplant_gas_0) <= +inf
   0 <= flow(gas_powerplant_gas_1) <= +inf
   0 <= flow(gas_powerplant_gas_2) <= +inf
   0 <= flow(powerplant_gas_electricity_0) <= +inf
   0 <= flow(powerplant_gas_electricity_1) <= +inf
   0 <= flow(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(powerplant_gas_electricity) <= 1000
end