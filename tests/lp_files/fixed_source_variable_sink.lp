\* Source Pyomo model name=Model *\

min 
objective:
+40 flow(electricityBus_excess_0_0)
+40 flow(electricityBus_excess_0_1)
+40 flow(electricityBus_excess_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_excess_0_0)
= -430000.0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_excess_0_1)
= -720000.0

c_e_BusBlock_balance(electricityBus_0_2)_:
-1 flow(electricityBus_excess_0_2)
= -290000.0

bounds
   0 <= flow(electricityBus_excess_0_0) <= +inf
   0 <= flow(electricityBus_excess_0_1) <= +inf
   0 <= flow(electricityBus_excess_0_2) <= +inf
end
