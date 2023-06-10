\* Source Pyomo model name=Model *\

min 
objective:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_0)
+100 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_1)
+100 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+0.9803921568627451 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_2)
+98.0392156862745 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+0.9803921568627451 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3)
+0.9803921568627451 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_3)
+98.0392156862745 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
+0.9611687812379853 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4)
+96.11687812379853 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
+0.9611687812379853 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5)
+0.9611687812379853 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5)
+96.11687812379853 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)

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

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 0.9

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_1_2)_:
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
= 0.8

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_1_3)_:
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
= 0.7

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_2_4)_:
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
= 0.7

c_e_SinkDSMDIWBlock_input_output_relation(demand_dsm_2_5)_:
-1 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
= 0.7

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_0)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_1)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_2)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_3)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_4)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5)
= 0

c_e_SinkDSMDIWBlock_dsm_updo_constraint(demand_dsm_5)_:
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4)
+0.99 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
-1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5)
= 0

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
<= 0.4

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_3)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_4)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_up_constraint(demand_dsm_5)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
<= 0.4

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_3)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_4)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
<= 0.3

c_u_SinkDSMDIWBlock_dsm_do_constraint(demand_dsm_5)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)
<= 0.3

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
<= 0.4

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
<= 0.5

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_3)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
<= 0.3

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_4)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
<= 0.3

c_u_SinkDSMDIWBlock_C2_constraint(demand_dsm_5)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)
<= 0.3

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
<= 0.5

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
<= 0.4

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
<= 0.5

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_3)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_3)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
<= 0.3

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_4)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_4)
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
<= 0.3

c_u_SinkDSMDIWBlock_recovery_constraint(demand_dsm_5)_:
+1 SinkDSMDIWBlock_dsm_up(demand_dsm_5)
<= 0.3

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_0)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
<= 0.6

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_1)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
<= 0.6

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_2)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
<= 0.8

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_3)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
<= 0.6

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_4)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)
<= 0.6

c_u_SinkDSMDIWBlock_shed_limit_constraint(demand_dsm_5)_:
+1 SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5)
<= 0.6

bounds
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_3) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_4) <= +inf
   0 <= SinkDSMDIWBlock_dsm_up(demand_dsm_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_0_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_1_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_2_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_3_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_4_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shift(demand_dsm_5_5) <= +inf
   0 <= SinkDSMDIWBlock_dsm_do_shed(demand_dsm_5) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
end
