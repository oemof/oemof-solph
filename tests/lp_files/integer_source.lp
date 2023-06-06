\* Source Pyomo model name=Model *\

min 
objective:
+25 flow(electricityBus_excess_0_0)
+25 flow(electricityBus_excess_0_1)
+25 flow(electricityBus_excess_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(electricityBus_excess_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(electricityBus_excess_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(electricityBus_excess_0_2)
= 0

c_e_SimpleFlowBlock_integer_flow_constr(electricityBus_excess_0_0)_:
-1 flow(electricityBus_excess_0_0)
+1 SimpleFlowBlock_integer_flow(electricityBus_excess_0)
= 0

c_e_SimpleFlowBlock_integer_flow_constr(electricityBus_excess_0_1)_:
-1 flow(electricityBus_excess_0_1)
+1 SimpleFlowBlock_integer_flow(electricityBus_excess_1)
= 0

c_e_SimpleFlowBlock_integer_flow_constr(electricityBus_excess_0_2)_:
-1 flow(electricityBus_excess_0_2)
+1 SimpleFlowBlock_integer_flow(electricityBus_excess_2)
= 0

bounds
   0 <= flow(electricityBus_excess_0_0) <= 10
   0 <= flow(electricityBus_excess_0_1) <= 10
   0 <= flow(electricityBus_excess_0_2) <= 10
   0 <= SimpleFlowBlock_integer_flow(electricityBus_excess_0) <= +inf
   0 <= SimpleFlowBlock_integer_flow(electricityBus_excess_1) <= +inf
   0 <= SimpleFlowBlock_integer_flow(electricityBus_excess_2) <= +inf
general
  SimpleFlowBlock_integer_flow(electricityBus_excess_0)
  SimpleFlowBlock_integer_flow(electricityBus_excess_1)
  SimpleFlowBlock_integer_flow(electricityBus_excess_2)
end
