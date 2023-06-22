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

c_u_SimpleFlowBlock_full_load_time_max_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0_0)
+1 flow(electricityBus_excess_0_1)
+1 flow(electricityBus_excess_1_2)
+1 flow(electricityBus_excess_1_3)
+1 flow(electricityBus_excess_2_4)
+1 flow(electricityBus_excess_2_5)
<= 1000

c_l_SimpleFlowBlock_full_load_time_min_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0_0)
+1 flow(electricityBus_excess_0_1)
+1 flow(electricityBus_excess_1_2)
+1 flow(electricityBus_excess_1_3)
+1 flow(electricityBus_excess_2_4)
+1 flow(electricityBus_excess_2_5)
>= 30

bounds
   0 <= flow(electricityBus_excess_0_0) <= 8.0
   0 <= flow(electricityBus_excess_0_1) <= 8.0
   0 <= flow(electricityBus_excess_1_2) <= 8.0
   0 <= flow(electricityBus_excess_1_3) <= 8.0
   0 <= flow(electricityBus_excess_2_4) <= 8.0
   0 <= flow(electricityBus_excess_2_5) <= 8.0
end
