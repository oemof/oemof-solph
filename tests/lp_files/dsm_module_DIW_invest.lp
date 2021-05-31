\* Source Pyomo model name=Model *\

min 
objective:
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_2)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)

s.t.

c_e_Bus_balance(bus_elec_0)_:
+1 flow(bus_elec_demand_dsm_0)
= 0

c_e_Bus_balance(bus_elec_1)_:
+1 flow(bus_elec_demand_dsm_1)
= 0

c_e_Bus_balance(bus_elec_2)_:
+1 flow(bus_elec_demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
+1 flow(bus_elec_demand_dsm_0)
= 50

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
+1 flow(bus_elec_demand_dsm_1)
= 50

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
+1 flow(bus_elec_demand_dsm_2)
= 50

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_0)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_1)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_2)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm)
<= 25

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   33 <= SinkDSMDIWInvestmentBlock_invest(demand_dsm) <= 100
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2) <= +inf
end
