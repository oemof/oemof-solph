\* Source Pyomo model name=Model *\

min 
objective:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+100 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+100 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
+0.9803921568627451 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+0.9803921568627451 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+98.0392156862745 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
+0.9803921568627451 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
+0.9803921568627451 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+98.0392156862745 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
+0.9611687812379853 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+0.9611687812379853 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+96.11687812379853 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
+0.9611687812379853 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
+0.9611687812379853 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+96.11687812379853 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)

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
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 0.9

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_2)_:
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
= 0.8

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_1_3)_:
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
= 0.7

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_4)_:
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
= 0.7

c_e_SinkDSMOemofBlock_input_output_relation(demand_dsm_2_5)_:
-1 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
= 0.7

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
<= 0.3

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_1)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1)
<= 0.3

c_u_SinkDSMOemofBlock_dsm_down_constraint(demand_dsm_2)_:
+1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2)
<= 0.4

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
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_0)
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_1)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1)
= 0.0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_2)_:
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_2)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2)
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_3)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3)
= 0.0

c_e_SinkDSMOemofBlock_dsm_sum_constraint(demand_dsm_4)_:
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_4)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4)
+0.99 SinkDSMOemofBlock_dsm_up(demand_dsm_5)
-1 SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5)
= 0.0

bounds
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofBlock_dsm_up(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shift(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofBlock_dsm_do_shed(demand_dsm_5) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
end
