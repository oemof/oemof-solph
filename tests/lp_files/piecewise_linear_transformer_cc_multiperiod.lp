\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+1 flow(gasBus_pwltf_0_0)
+1 flow(gasBus_pwltf_0_1)
+0.98039215686274506 flow(gasBus_pwltf_1_2)
+0.98039215686274506 flow(gasBus_pwltf_1_3)
+0.96116878123798533 flow(gasBus_pwltf_2_4)
+0.96116878123798533 flow(gasBus_pwltf_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(pwltf_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(pwltf_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(pwltf_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(pwltf_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(pwltf_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(pwltf_electricityBus_2_5)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_0)_:
+1 flow(gasBus_pwltf_0_0)
= 0

c_e_MultiPeriodBus_balance(gasBus_0_1)_:
+1 flow(gasBus_pwltf_0_1)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_2)_:
+1 flow(gasBus_pwltf_1_2)
= 0

c_e_MultiPeriodBus_balance(gasBus_1_3)_:
+1 flow(gasBus_pwltf_1_3)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_4)_:
+1 flow(gasBus_pwltf_2_4)
= 0

c_e_MultiPeriodBus_balance(gasBus_2_5)_:
+1 flow(gasBus_pwltf_2_5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_0_0)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_0)
-1 flow(gasBus_pwltf_0_0)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_0_1)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_1)
-1 flow(gasBus_pwltf_0_1)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_1_2)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_2)
-1 flow(gasBus_pwltf_1_2)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_1_3)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_3)
-1 flow(gasBus_pwltf_1_3)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_2_4)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_4)
-1 flow(gasBus_pwltf_2_4)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_in(pwltf_2_5)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_5)
-1 flow(gasBus_pwltf_2_5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_0_0)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_0)
-1 flow(pwltf_electricityBus_0_0)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_0_1)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_1)
-1 flow(pwltf_electricityBus_0_1)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_1_2)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_2)
-1 flow(pwltf_electricityBus_1_2)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_1_3)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_3)
-1 flow(pwltf_electricityBus_1_3)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_2_4)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_4)
-1 flow(pwltf_electricityBus_2_4)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_equate_out(pwltf_2_5)_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_5)
-1 flow(pwltf_electricityBus_2_5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_0)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_0)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_1)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_1)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_2)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_2)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_3)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_3)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_4)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_4)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(4)
= 1

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint1_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_5)
-25 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(2)
-50 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(3)
-75 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(4)
-100 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint2_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_5)
-625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(2)
-2500 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(3)
-5625 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(4)
-10000 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(5)
= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint3_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(5)
= 1

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint4(1)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(1)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint4(2)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(1)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(2)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint4(3)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(2)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(3)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint4(4)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(3)
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(4)
<= 0

c_u_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint4(5)_:
-1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(4)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(5)
<= 0

c_e_PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_constraint5_:
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(1)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(2)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(3)
+1 PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(4)
= 1

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

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
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_0) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_1) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_2) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_3) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_4) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_inflow(pwltf_5) <= 100
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_0) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_1) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_2) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_3) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_4) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_outflow(pwltf_5) <= 10000
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(4) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(1) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(2) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(3) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(4) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_lambda(5) <= +inf
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(1) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(2) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(3) <= 1
   0 <= PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(4) <= 1
binary
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_0)_CC_bin_y(4)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_1)_CC_bin_y(4)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_2)_CC_bin_y(4)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_3)_CC_bin_y(4)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_4)_CC_bin_y(4)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(1)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(2)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(3)
  PiecewiseLinearTransformerMultiPeriodBlock_piecewise(pwltf_5)_CC_bin_y(4)
end
