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

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_0)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_0)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint3(1)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint3(2)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint3(3)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint3(4)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_constraint4_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_1)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_1)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint3(1)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint3(2)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint3(3)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint3(4)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_constraint4_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint1_:
+1 PiecewiseLinearTransformerBlock_inflow(pwltf_2)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
-25 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
-50 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
-75 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-100 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint2_:
+1 PiecewiseLinearTransformerBlock_outflow(pwltf_2)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
-625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
-2500 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
-5625 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-10000 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint3(1)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(1)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint3(2)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint3(3)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint3(4)_:
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_constraint4_:
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(1)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(2)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(3)
+1 PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(4)
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
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(4) <= 1
binary
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_0)_DCC_bin_y(4)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_1)_DCC_bin_y(4)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(1)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(2)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(3)
  PiecewiseLinearTransformerBlock_piecewise(pwltf_2)_DCC_bin_y(4)
end
