\* Source Pyomo model name=Model *\

min 
objective:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0)
+100 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1)
+100 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
+100 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)

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

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
+1 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
-1 SinkDSMDLRInvestmentBlock_invest(demand_dsm_0)
= 50

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_0_2)
= 1

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_1_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_1_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_2_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_2_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_1_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_1_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_2_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_2_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_2_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_2_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_2_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_2_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_yearly_limit_shed(demand_dsm_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
-50.0 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
-0.5 SinkDSMDLRInvestmentBlock_total(demand_dsm_0)
<= 0

bounds
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_total(demand_dsm_0) <= +inf
   33 <= SinkDSMDLRInvestmentBlock_invest(demand_dsm_0) <= 100
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2) <= +inf
end
