\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGas_electricity_0)
+50 flow(powerplantGas_electricity_1)
+50 flow(powerplantGas_electricity_2)

s.t.

c_e_Bus_balance(electricity_0)_:
+1 flow(powerplantGas_electricity_0)
= 0

c_e_Bus_balance(electricity_1)_:
+1 flow(powerplantGas_electricity_1)
= 0

c_e_Bus_balance(electricity_2)_:
+1 flow(powerplantGas_electricity_2)
= 0

c_e_Bus_balance(gas_0)_:
+1 flow(gas_powerplantGas_0)
= 0

c_e_Bus_balance(gas_1)_:
+1 flow(gas_powerplantGas_1)
= 0

c_e_Bus_balance(gas_2)_:
+1 flow(gas_powerplantGas_2)
= 0

c_e_Transformer_relation(powerplantGas_gas_electricity_0)_:
+1 flow(gas_powerplantGas_0)
-1.7241379310344829 flow(powerplantGas_electricity_0)
= 0

c_e_Transformer_relation(powerplantGas_gas_electricity_1)_:
+1 flow(gas_powerplantGas_1)
-1.7241379310344829 flow(powerplantGas_electricity_1)
= 0

c_e_Transformer_relation(powerplantGas_gas_electricity_2)_:
+1 flow(gas_powerplantGas_2)
-1.7241379310344829 flow(powerplantGas_electricity_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gas_powerplantGas_0) <= +inf
   0 <= flow(gas_powerplantGas_1) <= +inf
   0 <= flow(gas_powerplantGas_2) <= +inf
   0 <= flow(powerplantGas_electricity_0) <= 100000000000
   0 <= flow(powerplantGas_electricity_1) <= 100000000000
   0 <= flow(powerplantGas_electricity_2) <= 100000000000
end
