\* Source Pyomo model name=Model *\

min 
objective:
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+23 flow(powerplant_electricityBus_2)

s.t.

c_u_Flow_summed_max(powerplant_electricityBus)_:
+1 flow(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_2)
<= 99900

c_l_Flow_summed_min(powerplant_electricityBus)_:
+1 flow(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_2)
>= 999

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0) <= 999
   0 <= flow(powerplant_electricityBus_1) <= 999
   0 <= flow(powerplant_electricityBus_2) <= 999
end
