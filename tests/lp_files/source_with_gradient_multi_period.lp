\* Source Pyomo model name=Model *\

min 
objective:
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+22.549019607843135 flow(powerplant_electricityBus_2)
+22.549019607843135 flow(powerplant_electricityBus_3)
+22.10688196847366 flow(powerplant_electricityBus_4)
+22.10688196847366 flow(powerplant_electricityBus_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(powerplant_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(powerplant_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(powerplant_electricityBus_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
+1 flow(powerplant_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
+1 flow(powerplant_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
+1 flow(powerplant_electricityBus_5)
= 0

c_e_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_0)_:
+1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_0)
= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_1)_:
-1 flow(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_1)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_1)
<= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_2)_:
-1 flow(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_2)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_2)
<= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_3)_:
-1 flow(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_3)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_3)
<= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_4)_:
-1 flow(powerplant_electricityBus_3)
+1 flow(powerplant_electricityBus_4)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_4)
<= 0

c_u_SimpleFlowBlock_positive_gradient_constr(powerplant_electricityBus_5)_:
-1 flow(powerplant_electricityBus_4)
+1 flow(powerplant_electricityBus_5)
-1 SimpleFlowBlock_positive_gradient(powerplant_electricityBus_5)
<= 0

c_e_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_0)_:
+1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_0)
= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_1)_:
+1 flow(powerplant_electricityBus_0)
-1 flow(powerplant_electricityBus_1)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_1)
<= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_2)_:
+1 flow(powerplant_electricityBus_1)
-1 flow(powerplant_electricityBus_2)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_2)
<= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_3)_:
+1 flow(powerplant_electricityBus_2)
-1 flow(powerplant_electricityBus_3)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_3)
<= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_4)_:
+1 flow(powerplant_electricityBus_3)
-1 flow(powerplant_electricityBus_4)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_4)
<= 0

c_u_SimpleFlowBlock_negative_gradient_constr(powerplant_electricityBus_5)_:
+1 flow(powerplant_electricityBus_4)
-1 flow(powerplant_electricityBus_5)
-1 SimpleFlowBlock_negative_gradient(powerplant_electricityBus_5)
<= 0

bounds
   0 <= flow(powerplant_electricityBus_0) <= 999
   0 <= flow(powerplant_electricityBus_1) <= 999
   0 <= flow(powerplant_electricityBus_2) <= 999
   0 <= flow(powerplant_electricityBus_3) <= 999
   0 <= flow(powerplant_electricityBus_4) <= 999
   0 <= flow(powerplant_electricityBus_5) <= 999
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_0) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_1) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_2) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_3) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_4) <= 29.97
   0 <= SimpleFlowBlock_positive_gradient(powerplant_electricityBus_5) <= 29.97
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_0) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_1) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_2) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_3) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_4) <= 49.95
   0 <= SimpleFlowBlock_negative_gradient(powerplant_electricityBus_5) <= 49.95
end
