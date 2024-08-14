\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGasBiomass_electricityBus_0)
+50 flow(powerplantGasBiomass_electricityBus_1)
+49.01960784313725 flow(powerplantGasBiomass_electricityBus_2)
+49.01960784313725 flow(powerplantGasBiomass_electricityBus_3)
+48.058439061899264 flow(powerplantGasBiomass_electricityBus_4)
+48.058439061899264 flow(powerplantGasBiomass_electricityBus_5)
+20 flow(powerplantGasBiomass_thermalBus_0)
+20 flow(powerplantGasBiomass_thermalBus_1)
+19.6078431372549 flow(powerplantGasBiomass_thermalBus_2)
+19.6078431372549 flow(powerplantGasBiomass_thermalBus_3)
+19.223375624759708 flow(powerplantGasBiomass_thermalBus_4)
+19.223375624759708 flow(powerplantGasBiomass_thermalBus_5)

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

c_e_BusBlock_balance(biomassBus_3)_:
+1 flow(biomassBus_powerplantGasBiomass_3)
= 0

c_e_BusBlock_balance(biomassBus_4)_:
+1 flow(biomassBus_powerplantGasBiomass_4)
= 0

c_e_BusBlock_balance(biomassBus_5)_:
+1 flow(biomassBus_powerplantGasBiomass_5)
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

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(powerplantGasBiomass_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(powerplantGasBiomass_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(powerplantGasBiomass_electricityBus_5)
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

c_e_BusBlock_balance(gasBus_3)_:
+1 flow(gasBus_powerplantGasBiomass_3)
= 0

c_e_BusBlock_balance(gasBus_4)_:
+1 flow(gasBus_powerplantGasBiomass_4)
= 0

c_e_BusBlock_balance(gasBus_5)_:
+1 flow(gasBus_powerplantGasBiomass_5)
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

c_e_BusBlock_balance(thermalBus_3)_:
+1 flow(powerplantGasBiomass_thermalBus_3)
= 0

c_e_BusBlock_balance(thermalBus_4)_:
+1 flow(powerplantGasBiomass_thermalBus_4)
= 0

c_e_BusBlock_balance(thermalBus_5)_:
+1 flow(powerplantGasBiomass_thermalBus_5)
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

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_3)_:
+0.3 flow(gasBus_powerplantGasBiomass_3)
-0.4 flow(powerplantGasBiomass_electricityBus_3)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_3)_:
+0.3 flow(biomassBus_powerplantGasBiomass_3)
-0.1 flow(powerplantGasBiomass_electricityBus_3)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_3)_:
+0.5 flow(gasBus_powerplantGasBiomass_3)
-0.4 flow(powerplantGasBiomass_thermalBus_3)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_3)_:
+0.5 flow(biomassBus_powerplantGasBiomass_3)
-0.1 flow(powerplantGasBiomass_thermalBus_3)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_4)_:
+0.3 flow(gasBus_powerplantGasBiomass_4)
-0.4 flow(powerplantGasBiomass_electricityBus_4)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_4)_:
+0.3 flow(biomassBus_powerplantGasBiomass_4)
-0.1 flow(powerplantGasBiomass_electricityBus_4)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_4)_:
+0.5 flow(gasBus_powerplantGasBiomass_4)
-0.4 flow(powerplantGasBiomass_thermalBus_4)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_4)_:
+0.5 flow(biomassBus_powerplantGasBiomass_4)
-0.1 flow(powerplantGasBiomass_thermalBus_4)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_electricityBus_5)_:
+0.3 flow(gasBus_powerplantGasBiomass_5)
-0.4 flow(powerplantGasBiomass_electricityBus_5)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_5)_:
+0.3 flow(biomassBus_powerplantGasBiomass_5)
-0.1 flow(powerplantGasBiomass_electricityBus_5)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_gasBus_thermalBus_5)_:
+0.5 flow(gasBus_powerplantGasBiomass_5)
-0.4 flow(powerplantGasBiomass_thermalBus_5)
= 0

c_e_ConverterBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_5)_:
+0.5 flow(biomassBus_powerplantGasBiomass_5)
-0.1 flow(powerplantGasBiomass_thermalBus_5)
= 0

bounds
   0 <= flow(gasBus_powerplantGasBiomass_0) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_1) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_2) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_3) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_4) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_5) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_0) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_1) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_2) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_3) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_4) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_5) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_0) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_1) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_2) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_3) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_4) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_5) <= +inf
   0.0 <= flow(powerplantGasBiomass_thermalBus_0) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_1) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_2) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_3) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_4) <= 50000000000.0
   0.0 <= flow(powerplantGasBiomass_thermalBus_5) <= 50000000000.0
end
