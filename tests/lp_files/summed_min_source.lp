\* Source Pyomo model name=Model *\

min 
objective:
+25 flow(electricityBus_excess_0)
+25 flow(electricityBus_excess_1)
+25 flow(electricityBus_excess_2)

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

c_u_SimpleFlowBlock_full_load_time_max_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0)
+1 flow(electricityBus_excess_1)
+1 flow(electricityBus_excess_2)
<= 1000

c_l_SimpleFlowBlock_full_load_time_min_constr(electricityBus_excess)_:
+1 flow(electricityBus_excess_0)
+1 flow(electricityBus_excess_1)
+1 flow(electricityBus_excess_2)
>= 30

bounds
   0 <= flow(electricityBus_excess_0) <= 8.0
   0 <= flow(electricityBus_excess_1) <= 8.0
   0 <= flow(electricityBus_excess_2) <= 8.0
end
