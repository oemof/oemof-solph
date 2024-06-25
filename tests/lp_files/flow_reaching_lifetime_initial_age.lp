\* Source Pyomo model name=Model *\

min 
objective:
+25 flow(electricityBus_excess_0)
+25 flow(electricityBus_excess_1)
+24.509803921568626 flow(electricityBus_excess_2)
+24.509803921568626 flow(electricityBus_excess_3)
+24.029219530949632 flow(electricityBus_excess_4)
+24.029219530949632 flow(electricityBus_excess_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(electricityBus_excess_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(electricityBus_excess_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(electricityBus_excess_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(electricityBus_excess_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(electricityBus_excess_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(electricityBus_excess_5)
= 0

c_e_SimpleFlowBlock_lifetime_age_output(electricityBus_excess_1_2)_:
+1 flow(electricityBus_excess_2)
= 0

c_e_SimpleFlowBlock_lifetime_age_output(electricityBus_excess_1_3)_:
+1 flow(electricityBus_excess_3)
= 0

c_e_SimpleFlowBlock_lifetime_age_output(electricityBus_excess_2_4)_:
+1 flow(electricityBus_excess_4)
= 0

c_e_SimpleFlowBlock_lifetime_age_output(electricityBus_excess_2_5)_:
+1 flow(electricityBus_excess_5)
= 0

bounds
   0 <= flow(electricityBus_excess_0) <= 8.0
   0 <= flow(electricityBus_excess_1) <= 8.0
   0 <= flow(electricityBus_excess_2) <= 8.0
   0 <= flow(electricityBus_excess_3) <= 8.0
   0 <= flow(electricityBus_excess_4) <= 8.0
   0 <= flow(electricityBus_excess_5) <= 8.0
end
