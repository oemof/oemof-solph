\* Source Pyomo model name=Model *\

min 
objective:
+100 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+100 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+98.039215686274503 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+98.039215686274503 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
+96.116878123798529 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
+96.116878123798529 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
+0.98039215686274506 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4)
+0.96116878123798533 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5)
+455.88267648036174 SinkDSMDIWInvestmentBlock_invest(demand_dsm_0)
+440.5314736691401 SinkDSMDIWInvestmentBlock_invest(demand_dsm_1)
+425.73027329942335 SinkDSMDIWInvestmentBlock_invest(demand_dsm_2)
+15992.031251718836 ONE_VAR_CONSTANT

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

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(demand_dsm_0)_:
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
= 50

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(demand_dsm_1)_:
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_old(demand_dsm_1)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(demand_dsm_2)_:
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_old(demand_dsm_2)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_old(demand_dsm_0)
-1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_0)
-1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_old(demand_dsm_1)
-1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_1)
-1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_old(demand_dsm_2)
-1 SinkDSMDIWInvestmentBlock_old_end(demand_dsm_2)
-1 SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0_0)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_0_1)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_1_2)
= 2

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3)
+1 flow(bus_elec_demand_dsm_1_3)
= 2

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4)
+1 flow(bus_elec_demand_dsm_2_4)
= 3

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5)
+1 flow(bus_elec_demand_dsm_2_5)
= 3

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
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_3)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_4)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_5)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5)
= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5)
-0.5 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_shed_limit_constraint(demand_dsm_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5)
-1 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(demand_dsm_0)_:
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_0)
<= 1000

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(demand_dsm_1)_:
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_1)
<= 1000

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(demand_dsm_2)_:
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
<= 1000

c_l_SinkDSMDIWInvestmentBlock_overall_minimum(demand_dsm)_:
+1 SinkDSMDIWInvestmentBlock_total(demand_dsm_2)
>= 5

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_0_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_2) <= +inf
   0 <= flow(bus_elec_demand_dsm_1_3) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_4) <= +inf
   0 <= flow(bus_elec_demand_dsm_2_5) <= +inf
   33 <= SinkDSMDIWInvestmentBlock_invest(demand_dsm_0) <= 100
   33 <= SinkDSMDIWInvestmentBlock_invest(demand_dsm_1) <= 100
   33 <= SinkDSMDIWInvestmentBlock_invest(demand_dsm_2) <= 100
   0 <= SinkDSMDIWInvestmentBlock_total(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_total(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_total(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_0_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_1_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_2_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_3_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_4_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_5_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_5) <= +inf
end
