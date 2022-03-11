\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplantGasBiomass_electricityBus_0_0)
+50 flow(powerplantGasBiomass_electricityBus_0_1)
+50 flow(powerplantGasBiomass_electricityBus_0_2)
+20 flow(powerplantGasBiomass_thermalBus_0_0)
+20 flow(powerplantGasBiomass_thermalBus_0_1)
+20 flow(powerplantGasBiomass_thermalBus_0_2)

s.t.

c_e_BusBlock_balance(biomassBus_0_0)_:
+1 flow(biomassBus_powerplantGasBiomass_0_0)
= 0

c_e_BusBlock_balance(biomassBus_0_1)_:
+1 flow(biomassBus_powerplantGasBiomass_0_1)
= 0

c_e_BusBlock_balance(biomassBus_0_2)_:
+1 flow(biomassBus_powerplantGasBiomass_0_2)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(powerplantGasBiomass_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(powerplantGasBiomass_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(powerplantGasBiomass_electricityBus_0_2)
= 0

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_powerplantGasBiomass_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_powerplantGasBiomass_0_1)
= 0

c_e_BusBlock_balance(gasBus_0_2)_:
+1 flow(gasBus_powerplantGasBiomass_0_2)
= 0

c_e_BusBlock_balance(thermalBus_0_0)_:
+1 flow(powerplantGasBiomass_thermalBus_0_0)
= 0

c_e_BusBlock_balance(thermalBus_0_1)_:
+1 flow(powerplantGasBiomass_thermalBus_0_1)
= 0

c_e_BusBlock_balance(thermalBus_0_2)_:
+1 flow(powerplantGasBiomass_thermalBus_0_2)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_0_0)_:
+0.29999999999999999 flow(biomassBus_powerplantGasBiomass_0_0)
-0.10000000000000001 flow(powerplantGasBiomass_electricityBus_0_0)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_0_1)_:
+0.29999999999999999 flow(biomassBus_powerplantGasBiomass_0_1)
-0.10000000000000001 flow(powerplantGasBiomass_electricityBus_0_1)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_electricityBus_0_2)_:
+0.29999999999999999 flow(biomassBus_powerplantGasBiomass_0_2)
-0.10000000000000001 flow(powerplantGasBiomass_electricityBus_0_2)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_0_0)_:
+0.5 flow(biomassBus_powerplantGasBiomass_0_0)
-0.10000000000000001 flow(powerplantGasBiomass_thermalBus_0_0)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_0_1)_:
+0.5 flow(biomassBus_powerplantGasBiomass_0_1)
-0.10000000000000001 flow(powerplantGasBiomass_thermalBus_0_1)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_biomassBus_thermalBus_0_2)_:
+0.5 flow(biomassBus_powerplantGasBiomass_0_2)
-0.10000000000000001 flow(powerplantGasBiomass_thermalBus_0_2)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_electricityBus_0_0)_:
+0.29999999999999999 flow(gasBus_powerplantGasBiomass_0_0)
-0.40000000000000002 flow(powerplantGasBiomass_electricityBus_0_0)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_electricityBus_0_1)_:
+0.29999999999999999 flow(gasBus_powerplantGasBiomass_0_1)
-0.40000000000000002 flow(powerplantGasBiomass_electricityBus_0_1)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_electricityBus_0_2)_:
+0.29999999999999999 flow(gasBus_powerplantGasBiomass_0_2)
-0.40000000000000002 flow(powerplantGasBiomass_electricityBus_0_2)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_thermalBus_0_0)_:
+0.5 flow(gasBus_powerplantGasBiomass_0_0)
-0.40000000000000002 flow(powerplantGasBiomass_thermalBus_0_0)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_thermalBus_0_1)_:
+0.5 flow(gasBus_powerplantGasBiomass_0_1)
-0.40000000000000002 flow(powerplantGasBiomass_thermalBus_0_1)
= 0

c_e_TransformerBlock_relation(powerplantGasBiomass_gasBus_thermalBus_0_2)_:
+0.5 flow(gasBus_powerplantGasBiomass_0_2)
-0.40000000000000002 flow(powerplantGasBiomass_thermalBus_0_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(biomassBus_powerplantGasBiomass_0_0) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_0_1) <= +inf
   0 <= flow(biomassBus_powerplantGasBiomass_0_2) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_0_0) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_0_1) <= +inf
   0 <= flow(gasBus_powerplantGasBiomass_0_2) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_0_0) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_0_1) <= +inf
   0 <= flow(powerplantGasBiomass_electricityBus_0_2) <= +inf
   0 <= flow(powerplantGasBiomass_thermalBus_0_0) <= 50000000000
   0 <= flow(powerplantGasBiomass_thermalBus_0_1) <= 50000000000
   0 <= flow(powerplantGasBiomass_thermalBus_0_2) <= 50000000000
end
