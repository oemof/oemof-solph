\* Source Pyomo model name=Model *\

min 
objective:
+20 InvestmentFlowBlock_invest(powerplant_gas_electricity_0)
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
+0.58 flow(gas_powerplant_gas_0)
-1 flow(powerplant_gas_electricity_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_1)_:
+0.58 flow(gas_powerplant_gas_1)
-1 flow(powerplant_gas_electricity_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_2)_:
+0.58 flow(gas_powerplant_gas_2)
-1 flow(powerplant_gas_electricity_2)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_electricity_0)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_electricity_0)
+1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0_1)_:
+1 flow(powerplant_gas_electricity_1)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_electricity_0_2)_:
+1 flow(powerplant_gas_electricity_2)
-1 InvestmentFlowBlock_total(powerplant_gas_electricity_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(powerplant_gas_electricity_0) <= 1000
   0 <= flow(gas_powerplant_gas_0) <= +inf
   0 <= flow(gas_powerplant_gas_1) <= +inf
   0 <= flow(gas_powerplant_gas_2) <= +inf
   0 <= flow(powerplant_gas_electricity_0) <= +inf
   0 <= flow(powerplant_gas_electricity_1) <= +inf
   0 <= flow(powerplant_gas_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_electricity_0) <= +inf
end
