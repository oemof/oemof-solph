\* Source Pyomo model name=Model *\

min 
objective:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+100 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
+100 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
+100 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)

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

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_0)
= 50

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_1)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_2)
= 1

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
-0.4 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
-0.4 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
= 0

bounds
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(demand_dsm_0) <= +inf
   33 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_0) <= 100
end
