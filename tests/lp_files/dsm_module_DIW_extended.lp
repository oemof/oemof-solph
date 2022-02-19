\* Source Pyomo model name=Model *\

min 
objective:
+100 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+100 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+100 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)

s.t.

c_e_BusBlock_balance(bus_elec_0_0)_:
+1 flow(bus_elec_demand_dsm_0_0)
= 0

c_e_BusBlock_balance(bus_elec_0_1)_:
+1 flow(bus_elec_demand_dsm_0_1)
= 0

c_e_BusBlock_balance(bus_elec_0_2)_:
+1 flow(bus_elec_demand_dsm_0_2)
= 0

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 0.90000000000000002

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_0_2)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_0_2)
= 0.80000000000000004

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_0)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+0.98999999999999999 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_1)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+0.98999999999999999 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_2)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+0.98999999999999999 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
= 0

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
<= 0.40000000000000002

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
<= 0.29999999999999999

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
<= 0.29999999999999999

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
<= 0.40000000000000002

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
<= 0.40000000000000002

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
<= 0.5

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.40000000000000002

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
<= 0.59999999999999998

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
<= 0.59999999999999998

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
<= 0.80000000000000004

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_2) <= +inf
end
