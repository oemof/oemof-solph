\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGas_electricity_0_0)
+50 flow(powerplantGas_electricity_0_1)
+49.01960784313725 flow(powerplantGas_electricity_1_2)
+49.01960784313725 flow(powerplantGas_electricity_1_3)
+48.058439061899264 flow(powerplantGas_electricity_2_4)
+48.058439061899264 flow(powerplantGas_electricity_2_5)

s.t.

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_powerplantGas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_powerplantGas_0_1)
= 0

c_e_BusBlock_balance(gas_1_2)_:
+1 flow(gas_powerplantGas_1_2)
= 0

c_e_BusBlock_balance(gas_1_3)_:
+1 flow(gas_powerplantGas_1_3)
= 0

c_e_BusBlock_balance(gas_2_4)_:
+1 flow(gas_powerplantGas_2_4)
= 0

c_e_BusBlock_balance(gas_2_5)_:
+1 flow(gas_powerplantGas_2_5)
= 0

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(powerplantGas_electricity_0_0)
= 0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(powerplantGas_electricity_0_1)
= 0

c_e_BusBlock_balance(electricity_1_2)_:
+1 flow(powerplantGas_electricity_1_2)
= 0

c_e_BusBlock_balance(electricity_1_3)_:
+1 flow(powerplantGas_electricity_1_3)
= 0

c_e_BusBlock_balance(electricity_2_4)_:
+1 flow(powerplantGas_electricity_2_4)
= 0

c_e_BusBlock_balance(electricity_2_5)_:
+1 flow(powerplantGas_electricity_2_5)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_0_0)_:
-1 flow(powerplantGas_electricity_0_0)
+0.58 flow(gas_powerplantGas_0_0)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_0_1)_:
-1 flow(powerplantGas_electricity_0_1)
+0.58 flow(gas_powerplantGas_0_1)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_1_2)_:
-1 flow(powerplantGas_electricity_1_2)
+0.58 flow(gas_powerplantGas_1_2)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_1_3)_:
-1 flow(powerplantGas_electricity_1_3)
+0.58 flow(gas_powerplantGas_1_3)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_2_4)_:
-1 flow(powerplantGas_electricity_2_4)
+0.58 flow(gas_powerplantGas_2_4)
= 0

c_e_ConverterBlock_relation(powerplantGas_gas_electricity_2_5)_:
-1 flow(powerplantGas_electricity_2_5)
+0.58 flow(gas_powerplantGas_2_5)
= 0

bounds
   0.0 <= flow(powerplantGas_electricity_0_0) <= 100000000000.0
   0.0 <= flow(powerplantGas_electricity_0_1) <= 100000000000.0
   0.0 <= flow(powerplantGas_electricity_1_2) <= 100000000000.0
   0.0 <= flow(powerplantGas_electricity_1_3) <= 100000000000.0
   0.0 <= flow(powerplantGas_electricity_2_4) <= 100000000000.0
   0.0 <= flow(powerplantGas_electricity_2_5) <= 100000000000.0
   0 <= flow(gas_powerplantGas_0_0) <= +inf
   0 <= flow(gas_powerplantGas_0_1) <= +inf
   0 <= flow(gas_powerplantGas_1_2) <= +inf
   0 <= flow(gas_powerplantGas_1_3) <= +inf
   0 <= flow(gas_powerplantGas_2_4) <= +inf
   0 <= flow(gas_powerplantGas_2_5) <= +inf
end
