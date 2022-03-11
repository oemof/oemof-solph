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

c_l_NonConvexFlowBlock_min(powerplant_electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
>= 0

c_l_NonConvexFlowBlock_min(powerplant_electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
>= 0

c_l_NonConvexFlowBlock_min(powerplant_electricityBus_0_2)_:
+1 flow(powerplant_electricityBus_0_2)
>= 0

c_u_NonConvexFlowBlock_max(powerplant_electricityBus_0_0)_:
-999 NonConvexFlowBlock_status(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_0_0)
<= 0

c_u_NonConvexFlowBlock_max(powerplant_electricityBus_0_1)_:
-999 NonConvexFlowBlock_status(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_0_1)
<= 0

c_u_NonConvexFlowBlock_max(powerplant_electricityBus_0_2)_:
-999 NonConvexFlowBlock_status(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_0_2)
<= 0

c_e_NonConvexFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_0)_:
+1 NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_0)
= 0

c_u_NonConvexFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_1)_:
-1 NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_1)
+ [
-1 NonConvexFlowBlock_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0_0)
+1 NonConvexFlowBlock_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
]
<= 0

c_u_NonConvexFlowBlock_positive_gradient_constr(powerplant_electricityBus_0_2)_:
-1 NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_2)
+ [
-1 NonConvexFlowBlock_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
+1 NonConvexFlowBlock_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_0_2)
]
<= 0

c_e_NonConvexFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_0)_:
+1 NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_0)
= 0

c_u_NonConvexFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_1)_:
-1 NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_1)
+ [
+1 NonConvexFlowBlock_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0_0)
-1 NonConvexFlowBlock_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
]
<= 0

c_u_NonConvexFlowBlock_negative_gradient_constr(powerplant_electricityBus_0_2)_:
-1 NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_2)
+ [
+1 NonConvexFlowBlock_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
-1 NonConvexFlowBlock_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_0_2)
]
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0_0) <= 999
   0 <= flow(powerplant_electricityBus_0_1) <= 999
   0 <= flow(powerplant_electricityBus_0_2) <= 999
   0 <= NonConvexFlowBlock_status(powerplant_electricityBus_0) <= 1
   0 <= NonConvexFlowBlock_status(powerplant_electricityBus_1) <= 1
   0 <= NonConvexFlowBlock_status(powerplant_electricityBus_2) <= 1
   0 <= NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_0) <= 29.969999999999999
   0 <= NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_1) <= 29.969999999999999
   0 <= NonConvexFlowBlock_positive_gradient(powerplant_electricityBus_2) <= 29.969999999999999
   0 <= NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_0) <= 49.950000000000003
   0 <= NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_1) <= 49.950000000000003
   0 <= NonConvexFlowBlock_negative_gradient(powerplant_electricityBus_2) <= 49.950000000000003
binary
  NonConvexFlowBlock_status(powerplant_electricityBus_0)
  NonConvexFlowBlock_status(powerplant_electricityBus_1)
  NonConvexFlowBlock_status(powerplant_electricityBus_2)
end
