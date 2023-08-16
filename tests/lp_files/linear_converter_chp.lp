\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(gasBus_CHPpowerplantGas_0_0)
+50 flow(gasBus_CHPpowerplantGas_0_1)
+50 flow(gasBus_CHPpowerplantGas_0_2)

s.t.

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_CHPpowerplantGas_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_CHPpowerplantGas_0_1)
= 0

c_e_BusBlock_balance(gasBus_0_2)_:
+1 flow(gasBus_CHPpowerplantGas_0_2)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(CHPpowerplantGas_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(CHPpowerplantGas_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(CHPpowerplantGas_electricityBus_0_2)
= 0

c_e_BusBlock_balance(heatBus_0_0)_:
+1 flow(CHPpowerplantGas_heatBus_0_0)
= 0

c_e_BusBlock_balance(heatBus_0_1)_:
+1 flow(CHPpowerplantGas_heatBus_0_1)
= 0

c_e_BusBlock_balance(heatBus_0_2)_:
+1 flow(CHPpowerplantGas_heatBus_0_2)
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

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_electricityBus_0_2)_:
+0.4 flow(gasBus_CHPpowerplantGas_0_2)
-1 flow(CHPpowerplantGas_electricityBus_0_2)
= 0

c_e_ConverterBlock_relation(CHPpowerplantGas_gasBus_heatBus_0_2)_:
+0.5 flow(gasBus_CHPpowerplantGas_0_2)
-1 flow(CHPpowerplantGas_heatBus_0_2)
= 0

bounds
   0.0 <= flow(gasBus_CHPpowerplantGas_0_0) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_0_1) <= 100000000000.0
   0.0 <= flow(gasBus_CHPpowerplantGas_0_2) <= 100000000000.0
   0 <= flow(CHPpowerplantGas_electricityBus_0_0) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_0_1) <= +inf
   0 <= flow(CHPpowerplantGas_electricityBus_0_2) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0_0) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0_1) <= +inf
   0 <= flow(CHPpowerplantGas_heatBus_0_2) <= +inf
end
