\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+8 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_0)
+8 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_1)
+7.8431372549019605 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_2)
+7.8431372549019605 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_3)
+7.6893502499038826 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_4)
+7.6893502499038826 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_5)
+7 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_0)
+7 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_1)
+6.8627450980392153 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_2)
+6.8627450980392153 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_3)
+6.7281814686658974 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_4)
+6.7281814686658974 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_5)
+23 flow(powerplant_electricityBus_0_0)
+23 flow(powerplant_electricityBus_0_1)
+22.549019607843135 flow(powerplant_electricityBus_1_2)
+22.549019607843135 flow(powerplant_electricityBus_1_3)
+22.106881968473662 flow(powerplant_electricityBus_2_4)
+22.106881968473662 flow(powerplant_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(powerplant_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(powerplant_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(powerplant_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(powerplant_electricityBus_2_5)
= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_0_0)_:
+1 flow(powerplant_electricityBus_0_0)
>= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_0_1)_:
+1 flow(powerplant_electricityBus_0_1)
>= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_1_2)_:
+1 flow(powerplant_electricityBus_1_2)
>= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_1_3)_:
+1 flow(powerplant_electricityBus_1_3)
>= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_2_4)_:
+1 flow(powerplant_electricityBus_2_4)
>= 0

c_l_MultiPeriodNonConvexFlow_min(powerplant_electricityBus_2_5)_:
+1 flow(powerplant_electricityBus_2_5)
>= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_0_0)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_0)
+1 flow(powerplant_electricityBus_0_0)
<= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_0_1)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1)
+1 flow(powerplant_electricityBus_0_1)
<= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_1_2)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2)
+1 flow(powerplant_electricityBus_1_2)
<= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_1_3)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3)
+1 flow(powerplant_electricityBus_1_3)
<= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_2_4)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4)
+1 flow(powerplant_electricityBus_2_4)
<= 0

c_u_MultiPeriodNonConvexFlow_max(powerplant_electricityBus_2_5)_:
-999 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_5)
+1 flow(powerplant_electricityBus_2_5)
<= 0

c_u_MultiPeriodNonConvexFlow_positive_gradient_constr(powerplant_electricityBus_0_1)_:
-1 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_1)
+ [
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0_0)
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
]
<= 0

c_u_MultiPeriodNonConvexFlow_positive_gradient_constr(powerplant_electricityBus_1_2)_:
-1 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_2)
+ [
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_1_2)
]
<= 0

c_u_MultiPeriodNonConvexFlow_positive_gradient_constr(powerplant_electricityBus_1_3)_:
-1 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_3)
+ [
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_1_2)
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3) * flow(powerplant_electricityBus_1_3)
]
<= 0

c_u_MultiPeriodNonConvexFlow_positive_gradient_constr(powerplant_electricityBus_2_4)_:
-1 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_4)
+ [
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3) * flow(powerplant_electricityBus_1_3)
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4) * flow(powerplant_electricityBus_2_4)
]
<= 0

c_u_MultiPeriodNonConvexFlow_positive_gradient_constr(powerplant_electricityBus_2_5)_:
-1 MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_5)
+ [
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4) * flow(powerplant_electricityBus_2_4)
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_5) * flow(powerplant_electricityBus_2_5)
]
<= 0

c_u_MultiPeriodNonConvexFlow_negative_gradient_constr(powerplant_electricityBus_0_1)_:
-1 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_1)
+ [
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_0) * flow(powerplant_electricityBus_0_0)
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
]
<= 0

c_u_MultiPeriodNonConvexFlow_negative_gradient_constr(powerplant_electricityBus_1_2)_:
-1 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_2)
+ [
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1) * flow(powerplant_electricityBus_0_1)
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_1_2)
]
<= 0

c_u_MultiPeriodNonConvexFlow_negative_gradient_constr(powerplant_electricityBus_1_3)_:
-1 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_3)
+ [
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2) * flow(powerplant_electricityBus_1_2)
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3) * flow(powerplant_electricityBus_1_3)
]
<= 0

c_u_MultiPeriodNonConvexFlow_negative_gradient_constr(powerplant_electricityBus_2_4)_:
-1 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_4)
+ [
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3) * flow(powerplant_electricityBus_1_3)
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4) * flow(powerplant_electricityBus_2_4)
]
<= 0

c_u_MultiPeriodNonConvexFlow_negative_gradient_constr(powerplant_electricityBus_2_5)_:
-1 MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_5)
+ [
+1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4) * flow(powerplant_electricityBus_2_4)
-1 MultiPeriodNonConvexFlow_status(powerplant_electricityBus_5) * flow(powerplant_electricityBus_2_5)
]
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0_0) <= 999
   0 <= flow(powerplant_electricityBus_0_1) <= 999
   0 <= flow(powerplant_electricityBus_1_2) <= 999
   0 <= flow(powerplant_electricityBus_1_3) <= 999
   0 <= flow(powerplant_electricityBus_2_4) <= 999
   0 <= flow(powerplant_electricityBus_2_5) <= 999
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_0) <= 1
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1) <= 1
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2) <= 1
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3) <= 1
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4) <= 1
   0 <= MultiPeriodNonConvexFlow_status(powerplant_electricityBus_5) <= 1
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_0) <= +inf
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_1) <= +inf
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_2) <= +inf
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_3) <= +inf
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_4) <= +inf
    -inf <= MultiPeriodNonConvexFlow_positive_gradient(powerplant_electricityBus_5) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_0) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_1) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_2) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_3) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_4) <= +inf
    -inf <= MultiPeriodNonConvexFlow_negative_gradient(powerplant_electricityBus_5) <= +inf
binary
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_0)
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_1)
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_2)
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_3)
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_4)
  MultiPeriodNonConvexFlow_status(powerplant_electricityBus_5)
end
