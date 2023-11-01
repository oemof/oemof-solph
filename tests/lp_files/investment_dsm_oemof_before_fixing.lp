\* Source Pyomo model name=Model *\

min 
objective:
+50 flow(powerplant_gas_electricity_0_0)
+50 flow(powerplant_gas_electricity_0_1)
+50 flow(powerplant_gas_electricity_0_2)
+0.01 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+0.01 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+0.01 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+0.01 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+0.01 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
+0.01 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+10 SinkDSMOemofInvestmentBlock_invest(demand_dsm_0)

s.t.

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

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 flow(electricity_demand_dsm_0_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
= 20

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 flow(electricity_demand_dsm_0_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
= 20

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_2)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 flow(electricity_demand_dsm_0_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
= 20

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
-10 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
<= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
= 0

bounds
   0 <= flow(powerplant_gas_electricity_0_0) <= 110
   0 <= flow(powerplant_gas_electricity_0_1) <= 110
   0 <= flow(powerplant_gas_electricity_0_2) <= 110
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_0) <= 20
   0 <= flow(electricity_demand_dsm_0_0) <= +inf
   0 <= flow(electricity_demand_dsm_0_1) <= +inf
   0 <= flow(electricity_demand_dsm_0_2) <= +inf
   0 <= flow(gas_source_gas_0_0) <= +inf
   0 <= flow(gas_powerplant_gas_0_0) <= +inf
   0 <= flow(gas_source_gas_0_1) <= +inf
   0 <= flow(gas_powerplant_gas_0_1) <= +inf
   0 <= flow(gas_source_gas_0_2) <= +inf
   0 <= flow(gas_powerplant_gas_0_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
end
