\* Source Pyomo model name=Model *\

min 
objective:
+1 flow(gasBus_pwltf_0_0)
+1 flow(gasBus_pwltf_0_1)
+0.9803921568627451 flow(gasBus_pwltf_1_2)
+0.9803921568627451 flow(gasBus_pwltf_1_3)
+0.9611687812379853 flow(gasBus_pwltf_2_4)
+0.9611687812379853 flow(gasBus_pwltf_2_5)

s.t.

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_pwltf_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_pwltf_0_1)
= 0

c_e_BusBlock_balance(gasBus_1_2)_:
+1 flow(gasBus_pwltf_1_2)
= 0

c_e_BusBlock_balance(gasBus_1_3)_:
+1 flow(gasBus_pwltf_1_3)
= 0

c_e_BusBlock_balance(gasBus_2_4)_:
+1 flow(gasBus_pwltf_2_4)
= 0

c_e_BusBlock_balance(gasBus_2_5)_:
+1 flow(gasBus_pwltf_2_5)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(pwltf_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(pwltf_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(pwltf_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(pwltf_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(pwltf_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(pwltf_electricityBus_2_5)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_0_0)_:
-1 flow(gasBus_pwltf_0_0)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_0)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_0_1)_:
-1 flow(gasBus_pwltf_0_1)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_1)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_1_2)_:
-1 flow(gasBus_pwltf_1_2)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_2)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_1_3)_:
-1 flow(gasBus_pwltf_1_3)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_3)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_2_4)_:
-1 flow(gasBus_pwltf_2_4)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_4)
= 0

c_e_PiecewiseLinearConverterBlock_equate_in(pwltf_2_5)_:
-1 flow(gasBus_pwltf_2_5)
+1 PiecewiseLinearConverterBlock_inflow(pwltf_5)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_0_0)_:
-1 flow(pwltf_electricityBus_0_0)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_0)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_0_1)_:
-1 flow(pwltf_electricityBus_0_1)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_1)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_1_2)_:
-1 flow(pwltf_electricityBus_1_2)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_2)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_1_3)_:
-1 flow(pwltf_electricityBus_1_3)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_3)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_2_4)_:
-1 flow(pwltf_electricityBus_2_4)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_4)
= 0

c_e_PiecewiseLinearConverterBlock_equate_out(pwltf_2_5)_:
-1 flow(pwltf_electricityBus_2_5)
+1 PiecewiseLinearConverterBlock_outflow(pwltf_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_0)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_0)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_1)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_1)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_3)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_3)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_4)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_4)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(4)
= 1

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint1_:
+1 PiecewiseLinearConverterBlock_inflow(pwltf_5)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_2)
-25 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_2)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_3)
-50 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_3)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_4)
-75 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_4)
-100 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint2_:
+1 PiecewiseLinearConverterBlock_outflow(pwltf_5)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_2)
-625 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_2)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_3)
-2500 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_3)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_4)
-5625 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_4)
-10000 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_5)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint3(1)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(1)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_1)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint3(2)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_2)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(2)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint3(3)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_3)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_4)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(3)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint3(4)_:
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_4)
-1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_5)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(4)
= 0

c_e_PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_constraint4_:
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(1)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(2)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(3)
+1 PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(4)
= 1

bounds
   0 <= flow(gasBus_pwltf_0_0) <= 100
   0 <= flow(gasBus_pwltf_0_1) <= 100
   0 <= flow(gasBus_pwltf_1_2) <= 100
   0 <= flow(gasBus_pwltf_1_3) <= 100
   0 <= flow(gasBus_pwltf_2_4) <= 100
   0 <= flow(gasBus_pwltf_2_5) <= 100
   0 <= flow(pwltf_electricityBus_0_0) <= +inf
   0 <= flow(pwltf_electricityBus_0_1) <= +inf
   0 <= flow(pwltf_electricityBus_1_2) <= +inf
   0 <= flow(pwltf_electricityBus_1_3) <= +inf
   0 <= flow(pwltf_electricityBus_2_4) <= +inf
   0 <= flow(pwltf_electricityBus_2_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_0) <= 100
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_1) <= 100
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_2) <= 100
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_3) <= 100
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_4) <= 100
   0 <= PiecewiseLinearConverterBlock_inflow(pwltf_5) <= 100
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_0) <= 10000
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_1) <= 10000
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_2) <= 10000
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_3) <= 10000
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_4) <= 10000
   0 <= PiecewiseLinearConverterBlock_outflow(pwltf_5) <= 10000
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(4) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_2) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(2_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_3) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(3_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_4) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(4_5) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(1) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_lambda(1_1) <= +inf
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(2) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(3) <= 1
   0 <= PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(4) <= 1
binary
  PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_0)_DCC_bin_y(4)
  PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_1)_DCC_bin_y(4)
  PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_2)_DCC_bin_y(4)
  PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_3)_DCC_bin_y(4)
  PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_4)_DCC_bin_y(4)
  PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(1)
  PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(2)
  PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(3)
  PiecewiseLinearConverterBlock_piecewise(pwltf_5)_DCC_bin_y(4)
end
