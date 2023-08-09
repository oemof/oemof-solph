\* Source Pyomo model name=Model *\

min 
objective:
+2 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+2 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1.9607843137254901 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1.9607843137254901 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+1.9223375624759707 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+1.9223375624759707 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)

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

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_0)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
= 0

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
= 0

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
= 0

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_3)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
= 0

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_4)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
= 0

c_e_SinkDSMOemofBlock_shift_shed_vars(demand_dsm_5)_:
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
= 0

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_2)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_3)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_4)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_5)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
= 1

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
<= 0.4

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_3)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_4)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_up_constraint(demand_dsm_5)_:
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_0)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
<= 0.4

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
<= 0.5

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_3)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_4)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_5)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
<= 0.3

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
= 0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_2)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
= 0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_4)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
= 0

bounds
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
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
