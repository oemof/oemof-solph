\* Source Pyomo model name=Model *\

min 
objective:
+100 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
+100 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
+98.039215686274503 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
+98.039215686274503 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
+96.116878123798529 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
+96.116878123798529 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+0.98039215686274506 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+0.98039215686274506 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+0.96116878123798533 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+0.96116878123798533 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
+0.98039215686274506 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+0.98039215686274506 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
+0.96116878123798533 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+0.96116878123798533 SinkDSMOemofBlock_dsm_up(demand_dsm_5)

s.t.

c_e_BusBlock_balance(bus_elec_0_0)_:
+1 flow(bus_elec_demand_dsm_0_0)
= 0

c_e_BusBlock_balance(bus_elec_0_1)_:
+1 flow(bus_elec_demand_dsm_0_1)
= 0

c_e_BusBlock_balance(bus_elec_1_2)_:
+1 flow(bus_elec_demand_dsm_1_2)
= 0

c_e_BusBlock_balance(bus_elec_1_3)_:
+1 flow(bus_elec_demand_dsm_1_3)
= 0

c_e_BusBlock_balance(bus_elec_2_4)_:
+1 flow(bus_elec_demand_dsm_2_4)
= 0

c_e_BusBlock_balance(bus_elec_2_5)_:
+1 flow(bus_elec_demand_dsm_2_5)
= 0

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 0.90000000000000002

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_2)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
= 0.80000000000000004

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_3)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
= 0.69999999999999996

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_4)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
= 0.69999999999999996

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_5)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
= 0.69999999999999996

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
<= 0.40000000000000002

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_3)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_4)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_5)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_0)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
<= 0.40000000000000002

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_3)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_4)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
<= 0.29999999999999999

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_5)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
<= 0.29999999999999999

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
= 0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_2)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
= 0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_4)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+0.98999999999999999 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_5) <= +inf
end
