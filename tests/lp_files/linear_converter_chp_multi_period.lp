\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(gasBus_CHPpowerplantGas_0_0)
+50 flow(gasBus_CHPpowerplantGas_0_1)
+49.01960784313725 flow(gasBus_CHPpowerplantGas_1_2)
+49.01960784313725 flow(gasBus_CHPpowerplantGas_1_3)
+48.058439061899264 flow(gasBus_CHPpowerplantGas_2_4)
+48.058439061899264 flow(gasBus_CHPpowerplantGas_2_5)

s.t.

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_CHPpowerplantGas_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_CHPpowerplantGas_0_1)
= 0

c_e_BusBlock_balance(gasBus_1_2)_:
+1 flow(gasBus_CHPpowerplantGas_1_2)
= 0

c_e_BusBlock_balance(gasBus_1_3)_:
+1 flow(gasBus_CHPpowerplantGas_1_3)
= 0

c_e_BusBlock_balance(gasBus_2_4)_:
+1 flow(gasBus_CHPpowerplantGas_2_4)
= 0

c_e_BusBlock_balance(gasBus_2_5)_:
+1 flow(gasBus_CHPpowerplantGas_2_5)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(CHPpowerplantGas_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(CHPpowerplantGas_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(CHPpowerplantGas_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(CHPpowerplantGas_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(CHPpowerplantGas_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(CHPpowerplantGas_electricityBus_2_5)
= 0

c_e_BusBlock_balance(heatBus_0_0)_:
+1 flow(CHPpowerplantGas_heatBus_0_0)
= 0

c_e_BusBlock_balance(heatBus_0_1)_:
+1 flow(CHPpowerplantGas_heatBus_0_1)
= 0

c_e_BusBlock_balance(heatBus_1_2)_:
+1 flow(CHPpowerplantGas_heatBus_1_2)
= 0

c_e_BusBlock_balance(heatBus_1_3)_:
+1 flow(CHPpowerplantGas_heatBus_1_3)
= 0

c_e_BusBlock_balance(heatBus_2_4)_:
+1 flow(CHPpowerplantGas_heatBus_2_4)
= 0

c_e_BusBlock_balance(heatBus_2_5)_:
+1 flow(CHPpowerplantGas_heatBus_2_5)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_0_0)_:
+0.4 flow(gasBus_CHPpowerplantGas_0_0)
-1 flow(CHPpowerplantGas_electricityBus_0_0)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_0_0)_:
+0.5 flow(gasBus_CHPpowerplantGas_0_0)
-1 flow(CHPpowerplantGas_heatBus_0_0)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_0_1)_:
+0.4 flow(gasBus_CHPpowerplantGas_0_1)
-1 flow(CHPpowerplantGas_electricityBus_0_1)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_0_1)_:
+0.5 flow(gasBus_CHPpowerplantGas_0_1)
-1 flow(CHPpowerplantGas_heatBus_0_1)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_1_2)_:
+0.4 flow(gasBus_CHPpowerplantGas_1_2)
-1 flow(CHPpowerplantGas_electricityBus_1_2)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_1_2)_:
+0.5 flow(gasBus_CHPpowerplantGas_1_2)
-1 flow(CHPpowerplantGas_heatBus_1_2)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_1_3)_:
+0.4 flow(gasBus_CHPpowerplantGas_1_3)
-1 flow(CHPpowerplantGas_electricityBus_1_3)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_1_3)_:
+0.5 flow(gasBus_CHPpowerplantGas_1_3)
-1 flow(CHPpowerplantGas_heatBus_1_3)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_2_4)_:
+0.4 flow(gasBus_CHPpowerplantGas_2_4)
-1 flow(CHPpowerplantGas_electricityBus_2_4)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_2_4)_:
+0.5 flow(gasBus_CHPpowerplantGas_2_4)
-1 flow(CHPpowerplantGas_heatBus_2_4)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_2_5)_:
+0.4 flow(gasBus_CHPpowerplantGas_2_5)
-1 flow(CHPpowerplantGas_electricityBus_2_5)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_2_5)_:
+0.5 flow(gasBus_CHPpowerplantGas_2_5)
-1 flow(CHPpowerplantGas_heatBus_2_5)
= 0

bounds
   0.0 <= flow(gasBus_CHPpowerplantGas_0_0) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_0_1) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_1_2) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_1_3) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_2_4) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_2_5) <= 100000000000.0
   0 <= flow(CHPpowerplantGas_electricityBus_0_0) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_0_1) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_1_2) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_1_3) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_2_4) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_2_5) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0_0) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0_1) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_1_2) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_1_3) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_2_4) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_2_5) <= +inf
end
