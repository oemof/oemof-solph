\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+50 flow(powerplantGasCoal_electricityBus_0_0)
+50 flow(powerplantGasCoal_electricityBus_0_1)
+49.019607843137251 flow(powerplantGasCoal_electricityBus_1_2)
+49.019607843137251 flow(powerplantGasCoal_electricityBus_1_3)
+48.058439061899264 flow(powerplantGasCoal_electricityBus_2_4)
+48.058439061899264 flow(powerplantGasCoal_electricityBus_2_5)
+20 flow(powerplantGasCoal_thermalBus_0_0)
+20 flow(powerplantGasCoal_thermalBus_0_1)
+19.6078431372549 flow(powerplantGasCoal_thermalBus_1_2)
+19.6078431372549 flow(powerplantGasCoal_thermalBus_1_3)
+19.223375624759708 flow(powerplantGasCoal_thermalBus_2_4)
+19.223375624759708 flow(powerplantGasCoal_thermalBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(biomassBus_0_0)_:
+1 flow(biomassBus_powerplantGasCoal_0_0)
= 0

c_e_MultiPeriodBus_balance(biomassBus_0_1)_:
+1 flow(biomassBus_powerplantGasCoal_0_1)
= 0

c_e_MultiPeriodBus_balance(biomassBus_1_2)_:
+1 flow(biomassBus_powerplantGasCoal_1_2)
= 0

c_e_MultiPeriodBus_balance(biomassBus_1_3)_:
+1 flow(biomassBus_powerplantGasCoal_1_3)
= 0

c_e_MultiPeriodBus_balance(biomassBus_2_4)_:
+1 flow(biomassBus_powerplantGasCoal_2_4)
= 0

c_e_MultiPeriodBus_balance(biomassBus_2_5)_:
+1 flow(biomassBus_powerplantGasCoal_2_5)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(powerplantGasCoal_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(powerplantGasCoal_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(powerplantGasCoal_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(powerplantGasCoal_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(powerplantGasCoal_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(powerplantGasCoal_electricityBus_2_5)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_0)_:
+1 flow(gasBus_powerplantGasCoal_0_0)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_1)_:
+1 flow(gasBus_powerplantGasCoal_0_1)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_2)_:
+1 flow(gasBus_powerplantGasCoal_1_2)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_3)_:
+1 flow(gasBus_powerplantGasCoal_1_3)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_4)_:
+1 flow(gasBus_powerplantGasCoal_2_4)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_5)_:
+1 flow(gasBus_powerplantGasCoal_2_5)
= 0

c_e_MultiPeriodBus_balance(thermalBus_0_0)_:
+1 flow(powerplantGasCoal_thermalBus_0_0)
= 0

c_e_MultiPeriodBus_balance(thermalBus_0_1)_:
+1 flow(powerplantGasCoal_thermalBus_0_1)
= 0

c_e_MultiPeriodBus_balance(thermalBus_1_2)_:
+1 flow(powerplantGasCoal_thermalBus_1_2)
= 0

c_e_MultiPeriodBus_balance(thermalBus_1_3)_:
+1 flow(powerplantGasCoal_thermalBus_1_3)
= 0

c_e_MultiPeriodBus_balance(thermalBus_2_4)_:
+1 flow(powerplantGasCoal_thermalBus_2_4)
= 0

c_e_MultiPeriodBus_balance(thermalBus_2_5)_:
+1 flow(powerplantGasCoal_thermalBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_0_0)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_0_0)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_0_1)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_0_1)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_1_2)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_1_2)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_1_3)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_1_3)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_2_4)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_2_4)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_electricityBus_2_5)_:
+0.29999999999999999 flow(biomassBus_powerplantGasCoal_2_5)
-0.10000000000000001 flow(powerplantGasCoal_electricityBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_0_0)_:
+0.5 flow(biomassBus_powerplantGasCoal_0_0)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_0_1)_:
+0.5 flow(biomassBus_powerplantGasCoal_0_1)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_1_2)_:
+0.5 flow(biomassBus_powerplantGasCoal_1_2)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_1_3)_:
+0.5 flow(biomassBus_powerplantGasCoal_1_3)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_2_4)_:
+0.5 flow(biomassBus_powerplantGasCoal_2_4)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_biomassBus_thermalBus_2_5)_:
+0.5 flow(biomassBus_powerplantGasCoal_2_5)
-0.10000000000000001 flow(powerplantGasCoal_thermalBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_0_0)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_0_0)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_0_1)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_0_1)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_1_2)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_1_2)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_1_3)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_1_3)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_2_4)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_2_4)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_electricityBus_2_5)_:
+0.29999999999999999 flow(gasBus_powerplantGasCoal_2_5)
-0.40000000000000002 flow(powerplantGasCoal_electricityBus_2_5)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_0_0)_:
+0.5 flow(gasBus_powerplantGasCoal_0_0)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_0_0)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_0_1)_:
+0.5 flow(gasBus_powerplantGasCoal_0_1)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_0_1)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_1_2)_:
+0.5 flow(gasBus_powerplantGasCoal_1_2)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_1_2)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_1_3)_:
+0.5 flow(gasBus_powerplantGasCoal_1_3)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_1_3)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_2_4)_:
+0.5 flow(gasBus_powerplantGasCoal_2_4)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_2_4)
= 0

c_e_MultiPeriodTransformer_relation(powerplantGasCoal_gasBus_thermalBus_2_5)_:
+0.5 flow(gasBus_powerplantGasCoal_2_5)
-0.40000000000000002 flow(powerplantGasCoal_thermalBus_2_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(biomassBus_powerplantGasCoal_0_0) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_0_1) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_1_2) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_1_3) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_2_4) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_2_5) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_0_0) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_0_1) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_1_2) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_1_3) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_2_4) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_2_5) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_0_0) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_0_1) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_1_2) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_1_3) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_2_4) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_2_5) <= +inf
   0 <= flow(powerplantGasCoal_thermalBus_0_0) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_0_1) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_1_2) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_1_3) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_2_4) <= 50000000000
   0 <= flow(powerplantGasCoal_thermalBus_2_5) <= 50000000000
end
