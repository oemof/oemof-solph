\* Source Pyomo model name=Model *\

min 
objective:
+40 flow(electricityBus_excess_0)
+40 flow(electricityBus_excess_1)
+39.2156862745098 flow(electricityBus_excess_2)
+39.2156862745098 flow(electricityBus_excess_3)
+38.446751249519416 flow(electricityBus_excess_4)
+38.446751249519416 flow(electricityBus_excess_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
-1 flow(electricityBus_excess_0)
= -430000.0

c_e_BusBlock_balance(electricityBus_1)_:
-1 flow(electricityBus_excess_1)
= -720000.0

c_e_BusBlock_balance(electricityBus_2)_:
-1 flow(electricityBus_excess_2)
= -290000.0

c_e_BusBlock_balance(electricityBus_3)_:
-1 flow(electricityBus_excess_3)
= -330000.0

c_e_BusBlock_balance(electricityBus_4)_:
-1 flow(electricityBus_excess_4)
= -330000.0

c_e_BusBlock_balance(electricityBus_5)_:
-1 flow(electricityBus_excess_5)
= -330000.0

bounds
   0 <= flow(electricityBus_excess_0) <= +inf
   0 <= flow(electricityBus_excess_1) <= +inf
   0 <= flow(electricityBus_excess_2) <= +inf
   0 <= flow(electricityBus_excess_3) <= +inf
   0 <= flow(electricityBus_excess_4) <= +inf
   0 <= flow(electricityBus_excess_5) <= +inf
end
