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

c_u_SimpleFlowBlock_full_load_time_max_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0)
+1 flow(electricityBus_excess_1)
+1 flow(electricityBus_excess_2)
+1 flow(electricityBus_excess_3)
+1 flow(electricityBus_excess_4)
+1 flow(electricityBus_excess_5)
<= 1000

c_l_SimpleFlowBlock_full_load_time_min_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0)
+1 flow(electricityBus_excess_1)
+1 flow(electricityBus_excess_2)
+1 flow(electricityBus_excess_3)
+1 flow(electricityBus_excess_4)
+1 flow(electricityBus_excess_5)
>= 30

bounds
   0 <= flow(electricityBus_excess_0) <= 8.0
   0 <= flow(electricityBus_excess_1) <= 8.0
   0 <= flow(electricityBus_excess_2) <= 8.0
   0 <= flow(electricityBus_excess_3) <= 8.0
   0 <= flow(electricityBus_excess_4) <= 8.0
   0 <= flow(electricityBus_excess_5) <= 8.0
end
