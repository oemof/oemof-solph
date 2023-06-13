\* Source Pyomo model name=Model *\

min 
objective:
+1 flow(gasBus_pwltf_0_0)
+1 flow(gasBus_pwltf_0_1)
+1 flow(gasBus_pwltf_0_2)

s.t.

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_pwltf_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_pwltf_0_1)
= 0

c_e_BusBlock_balance(gasBus_0_2)_:
+1 flow(gasBus_pwltf_0_2)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(pwltf_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(pwltf_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(pwltf_electricityBus_0_2)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_in(pwltf_0_0)_:
-1 flow(gasBus_pwltf_0_0)
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_0)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_in(pwltf_0_1)_:
-1 flow(gasBus_pwltf_0_1)
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_1)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_in(pwltf_0_2)_:
-1 flow(gasBus_pwltf_0_2)
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_2)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_out(pwltf_0_0)_:
-1 flow(pwltf_electricityBus_0_0)
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_0)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_out(pwltf_0_1)_:
-1 flow(pwltf_electricityBus_0_1)
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_1)
= 0

c_e_PiecewiseLinearTransformerBlock_equate_out(pwltf_0_2)_:
-1 flow(pwltf_electricityBus_0_2)
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_2)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_0)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_0)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint3_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(1)
= 1

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint4(1)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(1)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint4(2)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(2)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint4(3)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(3)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint4(4)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(4)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint4(5)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(5)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(4)
<= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_constraint5_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_1)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_1)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint3_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(1)
= 1

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint4(1)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(1)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint4(2)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(2)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint4(3)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(3)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint4(4)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(4)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint4(5)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(5)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(4)
<= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_constraint5_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_2)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_2)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint3_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(1)
= 1

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint4(1)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(1)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint4(2)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(2)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint4(3)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(3)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint4(4)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(4)
<= 0

c_u_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint4(5)_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(5)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(4)
<= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_constraint5_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(4)
= 1

bounds
   0 <= flow(gasBus_pwltf_0_0) <= 100
   0 <= flow(gasBus_pwltf_0_1) <= 100
   0 <= flow(gasBus_pwltf_0_2) <= 100
   0 <= flow(pwltf_electricityBus_0_0) <= +inf
   0 <= flow(pwltf_electricityBus_0_1) <= +inf
   0 <= flow(pwltf_electricityBus_0_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_inflow(pwltf_0) <= 100
   0 <= PiecewiseLinearTransformerBlock_inflow(pwltf_1) <= 100
   0 <= PiecewiseLinearTransformerBlock_inflow(pwltf_2) <= 100
   0 <= PiecewiseLinearTransformerBlock_outflow(pwltf_0) <= 10000
   0 <= PiecewiseLinearTransformerBlock_outflow(pwltf_1) <= 10000
   0 <= PiecewiseLinearTransformerBlock_outflow(pwltf_2) <= 10000
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(4) <= 1
binary
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_CC_bin_y(4)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_CC_bin_y(4)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_CC_bin_y(4)
end
