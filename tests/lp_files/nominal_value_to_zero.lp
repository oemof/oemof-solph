\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(s1_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(s1_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(s1_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(s1_electricityBus_0) <= 0
   0 <= flow(s1_electricityBus_1) <= 0
   0 <= flow(s1_electricityBus_2) <= 0
end
