\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGas_electricity_0_0)
+50 flow(powerplantGas_electricity_0_1)
+50 flow(powerplantGas_electricity_0_2)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(powerplantGas_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(powerplantGas_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(powerplantGas_electricity_0_2)
= 0

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_powerplantGas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_powerplantGas_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_powerplantGas_0_2)
= 0

c_e_TransformerBlock_relation(powerplantGas_gas_electricity_0_0)_:
+0.57999999999999996 flow(gas_powerplantGas_0_0)
-1 flow(powerplantGas_electricity_0_0)
= 0

c_e_TransformerBlock_relation(powerplantGas_gas_electricity_0_1)_:
+0.57999999999999996 flow(gas_powerplantGas_0_1)
-1 flow(powerplantGas_electricity_0_1)
= 0

c_e_TransformerBlock_relation(powerplantGas_gas_electricity_0_2)_:
+0.57999999999999996 flow(gas_powerplantGas_0_2)
-1 flow(powerplantGas_electricity_0_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gas_powerplantGas_0_0) <= +inf
   0 <= flow(gas_powerplantGas_0_1) <= +inf
   0 <= flow(gas_powerplantGas_0_2) <= +inf
   0 <= flow(powerplantGas_electricity_0_0) <= 100000000000
   0 <= flow(powerplantGas_electricity_0_1) <= 100000000000
   0 <= flow(powerplantGas_electricity_0_2) <= 100000000000
end
