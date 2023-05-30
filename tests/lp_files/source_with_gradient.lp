\* Source Pyomo model name=Model *\

min 
objective:
+23 flow(powerplant_electricityBus_0_0)
+23 flow(powerplant_electricityBus_0_1)
+23 flow(powerplant_electricityBus_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(powerplant_electricityBus_0_2)
= 0

c_e_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_0)_:
+1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_0)
= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_1)_:
-1 flow(powerplant_electricityBus_0_0)
+1 flow(powerplant_electricityBus_0_1)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_1)
<= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_2)_:
-1 flow(powerplant_electricityBus_0_1)
+1 flow(powerplant_electricityBus_0_2)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_2)
<= 0

c_e_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_0)_:
+1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_0)
= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_0)
-1 flow(powerplant_electricityBus_0_1)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_1)
<= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_2)_:
+1 flow(powerplant_electricityBus_0_1)
-1 flow(powerplant_electricityBus_0_2)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_2)
<= 0

bounds
   0 <= flow(powerplant_electricityBus_0_0) <= 999
   0 <= flow(powerplant_electricityBus_0_1) <= 999
   0 <= flow(powerplant_electricityBus_0_2) <= 999
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_0) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_1) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_2) <= 29.97
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_0) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_1) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_2) <= 49.95
end
