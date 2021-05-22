\* Source Pyomo model name=Model *\

min 
objective:
+8 Flow_negative_gradient(powerplant_electricityBus_0)
+8 Flow_negative_gradient(powerplant_electricityBus_1)
+8 Flow_negative_gradient(powerplant_electricityBus_2)
+7 Flow_positive_gradient(powerplant_electricityBus_0)
+7 Flow_positive_gradient(powerplant_electricityBus_1)
+7 Flow_positive_gradient(powerplant_electricityBus_2)
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+23 flow(powerplant_electricityBus_2)

s.t.

c_u_Flow_positive_gradient_constr(powerplant_electricityBus_1)_:
-1 Flow_positive_gradient(powerplant_electricityBus_1)
-1 flow(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_1)
<= 0

c_u_Flow_positive_gradient_constr(powerplant_electricityBus_2)_:
-1 Flow_positive_gradient(powerplant_electricityBus_2)
-1 flow(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_2)
<= 0

c_u_Flow_negative_gradient_constr(powerplant_electricityBus_1)_:
-1 Flow_negative_gradient(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_0)
-1 flow(powerplant_electricityBus_1)
<= 0

c_u_Flow_negative_gradient_constr(powerplant_electricityBus_2)_:
-1 Flow_negative_gradient(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_1)
-1 flow(powerplant_electricityBus_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0) <= 999
   0 <= flow(powerplant_electricityBus_1) <= 999
   0 <= flow(powerplant_electricityBus_2) <= 999
    -inf <= Flow_positive_gradient(powerplant_electricityBus_0) <= 29.969999999999999
    -inf <= Flow_positive_gradient(powerplant_electricityBus_1) <= 29.969999999999999
    -inf <= Flow_positive_gradient(powerplant_electricityBus_2) <= 29.969999999999999
    -inf <= Flow_negative_gradient(powerplant_electricityBus_0) <= 49.950000000000003
    -inf <= Flow_negative_gradient(powerplant_electricityBus_1) <= 49.950000000000003
    -inf <= Flow_negative_gradient(powerplant_electricityBus_2) <= 49.950000000000003
end
