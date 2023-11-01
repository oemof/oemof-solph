\* Source Pyomo model name=Model *\

min 
objective:
+10.0 ONE_VAR_CONSTANT
+50 flow(powerplant_gas_electricity_0_0)
+50 flow(powerplant_gas_electricity_0_1)
+50 flow(powerplant_gas_electricity_0_2)
+0.01 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+0.01 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+0.01 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+0.01 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+0.01 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+0.01 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+0.01 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)

s.t.

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_source_gas_0_0)
-1 flow(gas_powerplant_gas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_source_gas_0_1)
-1 flow(gas_powerplant_gas_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_source_gas_0_2)
-1 flow(gas_powerplant_gas_0_2)
= 0

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0_0)
-1 flow(electricity_demand_dsm_0_0)
= 90.0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(powerplant_gas_electricity_0_1)
-1 flow(electricity_demand_dsm_0_1)
= 100.0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(powerplant_gas_electricity_0_2)
-1 flow(electricity_demand_dsm_0_2)
= 80.0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_0)_:
-1 flow(powerplant_gas_electricity_0_0)
+0.58 flow(gas_powerplant_gas_0_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_1)_:
-1 flow(powerplant_gas_electricity_0_1)
+0.58 flow(gas_powerplant_gas_0_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_2)_:
-1 flow(powerplant_gas_electricity_0_2)
+0.58 flow(gas_powerplant_gas_0_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_1_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_1_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+1 flow(electricity_demand_dsm_0_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
= 20

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 flow(electricity_demand_dsm_0_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
= 20

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_0_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 flow(electricity_demand_dsm_0_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
= 20

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

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
<= 10.0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1)
<= 10.0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2)
<= 10.0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(powerplant_gas_electricity_0_0) <= 110
   0 <= flow(powerplant_gas_electricity_0_1) <= 110
   0 <= flow(powerplant_gas_electricity_0_2) <= 110
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_1_2) <= +inf
   0 <= flow(gas_source_gas_0_0) <= +inf
   0 <= flow(gas_powerplant_gas_0_0) <= +inf
   0 <= flow(gas_source_gas_0_1) <= +inf
   0 <= flow(gas_powerplant_gas_0_1) <= +inf
   0 <= flow(gas_source_gas_0_2) <= +inf
   0 <= flow(gas_powerplant_gas_0_2) <= +inf
   0 <= flow(electricity_demand_dsm_0_0) <= +inf
   0 <= flow(electricity_demand_dsm_0_1) <= +inf
   0 <= flow(electricity_demand_dsm_0_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_2) <= +inf
end
