\* Source Pyomo model name=Model *\

min 
objective:
+25 flow(electricityBus_excess_0_0)
+25 flow(electricityBus_excess_0_1)
+24.509803921568626 flow(electricityBus_excess_1_2)
+24.509803921568626 flow(electricityBus_excess_1_3)
+24.029219530949632 flow(electricityBus_excess_2_4)
+24.029219530949632 flow(electricityBus_excess_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(electricityBus_excess_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(electricityBus_excess_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(electricityBus_excess_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(electricityBus_excess_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(electricityBus_excess_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(electricityBus_excess_2_5)
= 0

c_e_SimpleFlowBlock_lifetime_output(electricityBus_excess_2_4)_:
+1 flow(electricityBus_excess_2_4)
= 0

c_e_SimpleFlowBlock_lifetime_output(electricityBus_excess_2_5)_:
+1 flow(electricityBus_excess_2_5)
= 0

bounds
   0 <= flow(electricityBus_excess_0_0) <= 8.0
   0 <= flow(electricityBus_excess_0_1) <= 8.0
   0 <= flow(electricityBus_excess_1_2) <= 8.0
   0 <= flow(electricityBus_excess_1_3) <= 8.0
   0 <= flow(electricityBus_excess_2_4) <= 8.0
   0 <= flow(electricityBus_excess_2_5) <= 8.0
end
