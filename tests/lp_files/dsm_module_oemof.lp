\* Source Pyomo model name=Model *\

min 
objective:
+2 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+2 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+2 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)

s.t.

c_e_BusBlock_balance(bus_elec_0)_:
+1 flow(bus_elec_demand_dsm_0)
= 0

c_e_BusBlock_balance(bus_elec_1)_:
+1 flow(bus_elec_demand_dsm_1)
= 0

c_e_BusBlock_balance(bus_elec_2)_:
+1 flow(bus_elec_demand_dsm_2)
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

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_2)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
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

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
= 0

bounds
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_2) <= +inf
end
