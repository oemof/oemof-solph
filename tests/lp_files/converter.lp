\* Source Pyomo model name=Model *\

min
objective:
+50 flow(powerplantGasCoal_electricityBus_0)
+50 flow(powerplantGasCoal_electricityBus_1)
+50 flow(powerplantGasCoal_electricityBus_2)
+20 flow(powerplantGasCoal_thermalBus_0)
+20 flow(powerplantGasCoal_thermalBus_1)
+20 flow(powerplantGasCoal_thermalBus_2)

s.t.

c_e_BusBlock_balance(biomassBus_0)_:
+1 flow(biomassBus_powerplantGasCoal_0)
= 0

c_e_BusBlock_balance(biomassBus_1)_:
+1 flow(biomassBus_powerplantGasCoal_1)
= 0

c_e_BusBlock_balance(biomassBus_2)_:
+1 flow(biomassBus_powerplantGasCoal_2)
= 0

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_powerplantGasCoal_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_powerplantGasCoal_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_powerplantGasCoal_2)
= 0

c_e_BusBlock_balance(thermalBus_0)_:
+1 flow(powerplantGasCoal_thermalBus_0)
= 0

c_e_BusBlock_balance(thermalBus_1)_:
+1 flow(powerplantGasCoal_thermalBus_1)
= 0

c_e_BusBlock_balance(thermalBus_2)_:
+1 flow(powerplantGasCoal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_electricityBus_0)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_0)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_electricityBus_1)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_1)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_electricityBus_2)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_2)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_thermalBus_0)_:
+0.5 flow(biomassBus_powerplantGasCoal_0)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_thermalBus_1)_:
+0.5 flow(biomassBus_powerplantGasCoal_1)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_biomassBus_thermalBus_2)_:
+0.5 flow(biomassBus_powerplantGasCoal_2)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_electricityBus_0)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_0)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_electricityBus_1)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_1)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_electricityBus_2)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_2)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_thermalBus_0)_:
+0.5 flow(gasBus_powerplantGasCoal_0)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_thermalBus_1)_:
+0.5 flow(gasBus_powerplantGasCoal_1)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasCoal_gasBus_thermalBus_2)_:
+0.5 flow(gasBus_powerplantGasCoal_2)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(biomassBus_powerplantGasCoal_0) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_1) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_2) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_0) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_1) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_2) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_0) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_1) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_2) <= +inf
   0 <= flow(powerplantGasCoal_thermalBus_0) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_1) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_2) <= 50000000000
end
