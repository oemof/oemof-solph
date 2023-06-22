\* Source Pyomo model name=Model *\

min 
objective:
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_0)
+100 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_1)
+100 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2)
+100 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_2)

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

c_e_SinkDSMDLRBlock_input_output_relation(demand_dsm_0_0)_:
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_0)
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMDLRBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1)
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_1)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 0.9

c_e_SinkDSMDLRBlock_input_output_relation(demand_dsm_0_2)_:
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2)
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_2)
-1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_0_2)
= 0.8

c_e_SinkDSMDLRBlock_capacity_balance_red(demand_dsm_1_0)_:
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_0)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_red(demand_dsm_1_1)_:
-1.0101010101010102 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_red(demand_dsm_1_2)_:
-1.0101010101010102 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_red(demand_dsm_2_0)_:
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_0)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_red(demand_dsm_2_2)_:
-1.0101010101010102 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_inc(demand_dsm_1_0)_:
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_0)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_inc(demand_dsm_1_1)_:
-0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_inc(demand_dsm_1_2)_:
-0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_inc(demand_dsm_2_0)_:
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_0)
= 0

c_e_SinkDSMDLRBlock_capacity_balance_inc(demand_dsm_2_2)_:
-0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2)
= 0

c_u_SinkDSMDLRBlock_availability_red(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_0)
<= 0.3

c_u_SinkDSMDLRBlock_availability_red(demand_dsm_1)_:
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_1)
<= 0.3

c_u_SinkDSMDLRBlock_availability_red(demand_dsm_2)_:
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_2)
<= 0.4

c_u_SinkDSMDLRBlock_availability_inc(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_0)
<= 0.5

c_u_SinkDSMDLRBlock_availability_inc(demand_dsm_1)_:
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_1)
<= 0.4

c_u_SinkDSMDLRBlock_availability_inc(demand_dsm_2)_:
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2)
<= 0.5

c_e_SinkDSMDLRBlock_dr_storage_red(demand_dsm_0)_:
-1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRBlock_dr_storage_red(demand_dsm_1)_:
-0.99 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1)
-0.99 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_0)
-1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRBlock_dr_storage_red(demand_dsm_2)_:
-0.99 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2)
-0.99 SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_1)
-1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_2)
= 0

c_e_SinkDSMDLRBlock_dr_storage_inc(demand_dsm_0)_:
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRBlock_dr_storage_inc(demand_dsm_1)_:
+0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
+0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_2_1)
-1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_0)
-1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRBlock_dr_storage_inc(demand_dsm_2)_:
+0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_1_2)
+0.99 SinkDSMDLRBlock_dsm_up(demand_dsm_2_2)
-1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_1)
-1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_2)
= 0

c_u_SinkDSMDLRBlock_dr_storage_limit_red(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_0)
<= 0.3333333333333333

c_u_SinkDSMDLRBlock_dr_storage_limit_red(demand_dsm_1)_:
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_1)
<= 0.3333333333333333

c_u_SinkDSMDLRBlock_dr_storage_limit_red(demand_dsm_2)_:
+1 SinkDSMDLRBlock_dsm_do_level(demand_dsm_2)
<= 0.3333333333333333

c_u_SinkDSMDLRBlock_dr_storage_limit_inc(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_0)
<= 0.4666666666666666

c_u_SinkDSMDLRBlock_dr_storage_limit_inc(demand_dsm_1)_:
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_1)
<= 0.4666666666666666

c_u_SinkDSMDLRBlock_dr_storage_limit_inc(demand_dsm_2)_:
+1 SinkDSMDLRBlock_dsm_up_level(demand_dsm_2)
<= 0.4666666666666666

c_u_SinkDSMDLRBlock_dr_yearly_limit_shed(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDLRBlock_dsm_do_shed(demand_dsm_2)
<= 33.33333333333333

c_u_SinkDSMDLRBlock_dr_yearly_limit_red(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2)
<= 33.33333333333333

c_u_SinkDSMDLRBlock_dr_yearly_limit_inc(demand_dsm_0)_:
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRBlock_dsm_up(demand_dsm_2_2)
<= 46.666666666666664

bounds
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_do(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRBlock_balance_dsm_up(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_do_level(demand_dsm_2) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRBlock_dsm_up_level(demand_dsm_2) <= +inf
end
