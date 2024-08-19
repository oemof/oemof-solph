\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(gasBus_CHPpowerplantGas_0)
+50 flow(gasBus_CHPpowerplantGas_1)
+49.01960784313725 flow(gasBus_CHPpowerplantGas_2)
+49.01960784313725 flow(gasBus_CHPpowerplantGas_3)
+48.058439061899264 flow(gasBus_CHPpowerplantGas_4)
+48.058439061899264 flow(gasBus_CHPpowerplantGas_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(CHPpowerplantGas_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(CHPpowerplantGas_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(CHPpowerplantGas_electricityBus_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(CHPpowerplantGas_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(CHPpowerplantGas_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(CHPpowerplantGas_electricityBus_5)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_CHPpowerplantGas_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_CHPpowerplantGas_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_CHPpowerplantGas_2)
= 0

c_e_BusBlock_balance(gasBus_3)_:
+1 flow(gasBus_CHPpowerplantGas_3)
= 0

c_e_BusBlock_balance(gasBus_4)_:
+1 flow(gasBus_CHPpowerplantGas_4)
= 0

c_e_BusBlock_balance(gasBus_5)_:
+1 flow(gasBus_CHPpowerplantGas_5)
= 0

c_e_BusBlock_balance(heatBus_0)_:
+1 flow(CHPpowerplantGas_heatBus_0)
= 0

c_e_BusBlock_balance(heatBus_1)_:
+1 flow(CHPpowerplantGas_heatBus_1)
= 0

c_e_BusBlock_balance(heatBus_2)_:
+1 flow(CHPpowerplantGas_heatBus_2)
= 0

c_e_BusBlock_balance(heatBus_3)_:
+1 flow(CHPpowerplantGas_heatBus_3)
= 0

c_e_BusBlock_balance(heatBus_4)_:
+1 flow(CHPpowerplantGas_heatBus_4)
= 0

c_e_BusBlock_balance(heatBus_5)_:
+1 flow(CHPpowerplantGas_heatBus_5)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_0)_:
+0.4 flow(gasBus_CHPpowerplantGas_0)
-1 flow(CHPpowerplantGas_electricityBus_0)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_0)_:
+0.5 flow(gasBus_CHPpowerplantGas_0)
-1 flow(CHPpowerplantGas_heatBus_0)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_1)_:
+0.4 flow(gasBus_CHPpowerplantGas_1)
-1 flow(CHPpowerplantGas_electricityBus_1)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_1)_:
+0.5 flow(gasBus_CHPpowerplantGas_1)
-1 flow(CHPpowerplantGas_heatBus_1)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_2)_:
+0.4 flow(gasBus_CHPpowerplantGas_2)
-1 flow(CHPpowerplantGas_electricityBus_2)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_2)_:
+0.5 flow(gasBus_CHPpowerplantGas_2)
-1 flow(CHPpowerplantGas_heatBus_2)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_3)_:
+0.4 flow(gasBus_CHPpowerplantGas_3)
-1 flow(CHPpowerplantGas_electricityBus_3)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_3)_:
+0.5 flow(gasBus_CHPpowerplantGas_3)
-1 flow(CHPpowerplantGas_heatBus_3)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_4)_:
+0.4 flow(gasBus_CHPpowerplantGas_4)
-1 flow(CHPpowerplantGas_electricityBus_4)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_4)_:
+0.5 flow(gasBus_CHPpowerplantGas_4)
-1 flow(CHPpowerplantGas_heatBus_4)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_5)_:
+0.4 flow(gasBus_CHPpowerplantGas_5)
-1 flow(CHPpowerplantGas_electricityBus_5)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_5)_:
+0.5 flow(gasBus_CHPpowerplantGas_5)
-1 flow(CHPpowerplantGas_heatBus_5)
= 0

bounds
   0.0 <= flow(gasBus_CHPpowerplantGas_0) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_1) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_2) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_3) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_4) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_5) <= 100000000000.0
   0 <= flow(CHPpowerplantGas_electricityBus_0) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_1) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_2) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_3) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_4) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_5) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_1) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_2) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_3) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_4) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_5) <= +inf
end
