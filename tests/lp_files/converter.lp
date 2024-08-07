\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGasBiomass_electricityBus_0)
+50 flow(powerplantGasBiomass_electricityBus_1)
+50 flow(powerplantGasBiomass_electricityBus_2)
+20 flow(powerplantGasBiomass_thermalBus_0)
+20 flow(powerplantGasBiomass_thermalBus_1)
+20 flow(powerplantGasBiomass_thermalBus_2)

s.t.

c_e_BusBlock_balance(biomassBus_0)_:
+1 flow(biomassBus_powerplantGasBiomass_0)
= 0

c_e_BusBlock_balance(biomassBus_1)_:
+1 flow(biomassBus_powerplantGasBiomass_1)
= 0

c_e_BusBlock_balance(biomassBus_2)_:
+1 flow(biomassBus_powerplantGasBiomass_2)
= 0

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(powerplantGasBiomass_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(powerplantGasBiomass_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(powerplantGasBiomass_electricityBus_2)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_powerplantGasBiomass_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_powerplantGasBiomass_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_powerplantGasBiomass_2)
= 0

c_e_BusBlock_balance(thermalBus_0)_:
+1 flow(powerplantGasBiomass_thermalBus_0)
= 0

c_e_BusBlock_balance(thermalBus_1)_:
+1 flow(powerplantGasBiomass_thermalBus_1)
= 0

c_e_BusBlock_balance(thermalBus_2)_:
+1 flow(powerplantGasBiomass_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_0)_:
+0.3 flow(gasBus_powerplantGasBiomass_0)
-0.4 flow(powerplantGasBiomass_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_0)_:
+0.3 flow(biomassBus_powerplantGasBiomass_0)
-0.1 flow(powerplantGasBiomass_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_0)_:
+0.5 flow(gasBus_powerplantGasBiomass_0)
-0.4 flow(powerplantGasBiomass_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_0)_:
+0.5 flow(biomassBus_powerplantGasBiomass_0)
-0.1 flow(powerplantGasBiomass_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_1)_:
+0.3 flow(gasBus_powerplantGasBiomass_1)
-0.4 flow(powerplantGasBiomass_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_1)_:
+0.3 flow(biomassBus_powerplantGasBiomass_1)
-0.1 flow(powerplantGasBiomass_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_1)_:
+0.5 flow(gasBus_powerplantGasBiomass_1)
-0.4 flow(powerplantGasBiomass_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_1)_:
+0.5 flow(biomassBus_powerplantGasBiomass_1)
-0.1 flow(powerplantGasBiomass_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_2)_:
+0.3 flow(gasBus_powerplantGasBiomass_2)
-0.4 flow(powerplantGasBiomass_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_2)_:
+0.3 flow(biomassBus_powerplantGasBiomass_2)
-0.1 flow(powerplantGasBiomass_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_2)_:
+0.5 flow(gasBus_powerplantGasBiomass_2)
-0.4 flow(powerplantGasBiomass_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_2)_:
+0.5 flow(biomassBus_powerplantGasBiomass_2)
-0.1 flow(powerplantGasBiomass_thermalBus_2)
= 0

bounds
   0 <= flow(gasBus_powerplantGasBiomass_0) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_1) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_2) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_0) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_1) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_2) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_0) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_1) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_2) <= +inf
   0.0 <= flow(powerplantGasBiomass_thermalBus_0) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_1) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_2) <= 50000000000.0
end
