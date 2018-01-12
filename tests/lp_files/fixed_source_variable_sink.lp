\* Source Pyomo model name=Model *\

min 
objective:
+40 flow(electricityBus_excess_0)
+40 flow(electricityBus_excess_1)
+40 flow(electricityBus_excess_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_excess_0)
= -430000

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_excess_1)
= -720000

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_excess_2)
= -290000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_excess_0) <= +inf
   0 <= flow(electricityBus_excess_1) <= +inf
   0 <= flow(electricityBus_excess_2) <= +inf
end
