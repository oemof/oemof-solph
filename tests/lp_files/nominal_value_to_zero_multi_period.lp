\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(s1_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(s1_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(s1_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(s1_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(s1_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(s1_electricityBus_2_5)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(s1_electricityBus_0_0) <= 0
   0 <= flow(s1_electricityBus_0_1) <= 0
   0 <= flow(s1_electricityBus_1_2) <= 0
   0 <= flow(s1_electricityBus_1_3) <= 0
   0 <= flow(s1_electricityBus_2_4) <= 0
   0 <= flow(s1_electricityBus_2_5) <= 0
end
