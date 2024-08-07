\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(gasBus_CHPpowerplantGas_0)
+50 flow(gasBus_CHPpowerplantGas_1)
+50 flow(gasBus_CHPpowerplantGas_2)

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

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_CHPpowerplantGas_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_CHPpowerplantGas_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_CHPpowerplantGas_2)
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

bounds
   0.0 <= flow(gasBus_CHPpowerplantGas_0) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_1) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_2) <= 100000000000.0
   0 <= flow(CHPpowerplantGas_electricityBus_0) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_1) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_2) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_1) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_2) <= +inf
end
