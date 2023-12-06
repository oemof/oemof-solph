\* Source Pyomo model name=Model *\

min 
objective:
+2941.5609381007307 ONE_VAR_CONSTANT
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+100 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+100 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
+0.9803921568627451 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
+0.9803921568627451 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+98.0392156862745 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
+0.9803921568627451 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_3)
+0.9803921568627451 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_3)
+98.0392156862745 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_3)
+0.9611687812379853 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_4)
+0.9611687812379853 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_4)
+96.11687812379853 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_4)
+0.9611687812379853 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_5)
+0.9611687812379853 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_5)
+96.11687812379853 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_5)
+76.46810240317063 SinkDSMOemofInvestmentBlock_invest(demand_dsm_0)
+50.47234572422055 SinkDSMOemofInvestmentBlock_invest(demand_dsm_1)
+24.986309764465627 SinkDSMOemofInvestmentBlock_invest(demand_dsm_2)

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

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
= 50

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(demand_dsm_1)_:
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_old(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(demand_dsm_2)_:
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_old(demand_dsm_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_end(demand_dsm_0)_:
+1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_end(demand_dsm_1)_:
+1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_end(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_exo(demand_dsm_0)_:
+1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_exo(demand_dsm_1)_:
+1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule_exo(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_old(demand_dsm_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule(demand_dsm_1)_:
+1 SinkDSMOemofInvestmentBlock_old(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_old_dsm_rule(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_old(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_old_end(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_1_2)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
= 2

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_1_3)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_3)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_3)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
= 2

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_2_4)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_4)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_4)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
= 3

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_2_5)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_5)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
= 3

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
-0.4 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_1_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_1_3)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_3)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_2_4)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_4)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_2_5)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_5)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
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

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_1_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2)
-0.5 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_1_3)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_3)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_3)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_2_4)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_4)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_4)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_2_5)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_5)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_5)
-0.3 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
<= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_3)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_3)
= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_4)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_4)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_4)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_5)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_5)
= 0

c_u_SinkDSMOemofInvestmentBlock_overall_dsm_maximum(demand_dsm_0)_:
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_0)
<= 1000

c_u_SinkDSMOemofInvestmentBlock_overall_dsm_maximum(demand_dsm_1)_:
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_1)
<= 1000

c_u_SinkDSMOemofInvestmentBlock_overall_dsm_maximum(demand_dsm_2)_:
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
<= 1000

c_l_SinkDSMOemofInvestmentBlock_overall_minimum(demand_dsm)_:
+1 SinkDSMOemofInvestmentBlock_total(demand_dsm_2)
>= 5

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_3) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_4) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_5) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_5) <= +inf
   33 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_0) <= 100
   33 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_1) <= 100
   33 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_2) <= 100
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_end(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_end(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_end(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old_exo(demand_dsm_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_old(demand_dsm_0) <= +inf
end
