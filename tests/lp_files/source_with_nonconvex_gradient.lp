\* Source Pyomo model name=Model *\

min 
objective:
+8 NonConvexFlow_negative_gradient(powerplant_electricityBus_0)
+8 NonConvexFlow_negative_gradient(powerplant_electricityBus_1)
+8 NonConvexFlow_negative_gradient(powerplant_electricityBus_2)
+7 NonConvexFlow_positive_gradient(powerplant_electricityBus_0)
+7 NonConvexFlow_positive_gradient(powerplant_electricityBus_1)
+7 NonConvexFlow_positive_gradient(powerplant_electricityBus_2)
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+23 flow(powerplant_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
+1 flow(powerplant_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(powerplant_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(powerplant_electricityBus_2)
= 0

c_l_NonConvexFlow_min(powerplant_electricityBus_0)_:
+1 flow(powerplant_electricityBus_0)
>= 0

c_l_NonConvexFlow_min(powerplant_electricityBus_1)_:
+1 flow(powerplant_electricityBus_1)
>= 0

c_l_NonConvexFlow_min(powerplant_electricityBus_2)_:
+1 flow(powerplant_electricityBus_2)
>= 0

c_u_NonConvexFlow_max(powerplant_electricityBus_0)_:
-999 NonConvexFlow_status(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_0)
<= 0

c_u_NonConvexFlow_max(powerplant_electricityBus_1)_:
-999 NonConvexFlow_status(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_1)
<= 0

c_u_NonConvexFlow_max(powerplant_electricityBus_2)_:
-999 NonConvexFlow_status(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_2)
<= 0

c_u_NonConvexFlow_positive_gradient_constr(powerplant_electricityBus_1)_:
-1 NonConvexFlow_positive_gradient(powerplant_electricityBus_1)
+ [
-1 NonConvexFlow_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0)
+1 NonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_1)
]
<= 0

c_u_NonConvexFlow_positive_gradient_constr(powerplant_electricityBus_2)_:
-1 NonConvexFlow_positive_gradient(powerplant_electricityBus_2)
+ [
-1 NonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_1)
+1 NonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_2)
]
<= 0

c_u_NonConvexFlow_negative_gradient_constr(powerplant_electricityBus_1)_:
-1 NonConvexFlow_negative_gradient(powerplant_electricityBus_1)
+ [
+1 NonConvexFlow_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0)
-1 NonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_1)
]
<= 0

c_u_NonConvexFlow_negative_gradient_constr(powerplant_electricityBus_2)_:
-1 NonConvexFlow_negative_gradient(powerplant_electricityBus_2)
+ [
+1 NonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_1)
-1 NonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_2)
]
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0) <= 999
   0 <= flow(powerplant_electricityBus_1) <= 999
   0 <= flow(powerplant_electricityBus_2) <= 999
   0 <= NonConvexFlow_status(powerplant_electricityBus_0) <= 1
   0 <= NonConvexFlow_status(powerplant_electricityBus_1) <= 1
   0 <= NonConvexFlow_status(powerplant_electricityBus_2) <= 1
    -inf <= NonConvexFlow_positive_gradient(powerplant_electricityBus_0) <= +inf
    -inf <= NonConvexFlow_positive_gradient(powerplant_electricityBus_1) <= +inf
    -inf <= NonConvexFlow_positive_gradient(powerplant_electricityBus_2) <= +inf
    -inf <= NonConvexFlow_negative_gradient(powerplant_electricityBus_0) <= +inf
    -inf <= NonConvexFlow_negative_gradient(powerplant_electricityBus_1) <= +inf
    -inf <= NonConvexFlow_negative_gradient(powerplant_electricityBus_2) <= +inf
binary
  NonConvexFlow_status(powerplant_electricityBus_0)
  NonConvexFlow_status(powerplant_electricityBus_1)
  NonConvexFlow_status(powerplant_electricityBus_2)
end
