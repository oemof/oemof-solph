\* Source Pyomo model name=Model *\

min 
objective:
+40 flow(electricityBus_excess_0_0)
+40 flow(electricityBus_excess_0_1)
+39.2156862745098 flow(electricityBus_excess_1_2)
+39.2156862745098 flow(electricityBus_excess_1_3)
+38.446751249519416 flow(electricityBus_excess_2_4)
+38.446751249519416 flow(electricityBus_excess_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_excess_0_0)
= -430000.0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_excess_0_1)
= -720000.0

c_e_BusBlock_balance(electricityBus_1_2)_:
-1 flow(electricityBus_excess_1_2)
= -290000.0

c_e_BusBlock_balance(electricityBus_1_3)_:
-1 flow(electricityBus_excess_1_3)
= -330000.0

c_e_BusBlock_balance(electricityBus_2_4)_:
-1 flow(electricityBus_excess_2_4)
= -330000.0

c_e_BusBlock_balance(electricityBus_2_5)_:
-1 flow(electricityBus_excess_2_5)
= -330000.0

bounds
   0 <= flow(electricityBus_excess_0_0) <= +inf
   0 <= flow(electricityBus_excess_0_1) <= +inf
   0 <= flow(electricityBus_excess_1_2) <= +inf
   0 <= flow(electricityBus_excess_1_3) <= +inf
   0 <= flow(electricityBus_excess_2_4) <= +inf
   0 <= flow(electricityBus_excess_2_5) <= +inf
end
