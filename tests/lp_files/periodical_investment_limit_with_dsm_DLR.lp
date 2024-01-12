\* Source Pyomo model name=Model *\

min 
objective:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+0.5 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+0.49019607843137253 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
+0.48058439061899266 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
+99.99999999999999 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
+98.03921568627449 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_1)
+48.534265191225046 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_2)

s.t.

c_u_investment_limit_per_period(0)_:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+99.99999999999999 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
<= 400

c_u_investment_limit_per_period(1)_:
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+98.03921568627449 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_1)
<= 300

c_u_investment_limit_per_period(2)_:
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+48.534265191225046 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_2)
<= 200

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_sink_dsm_DLR_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_sink_dsm_DLR_0_1)
= 0

c_e_BusBlock_balance(Bus1_1_2)_:
+1 flow(Source_Bus1_1_2)
-1 flow(Bus1_sink_dsm_DLR_1_2)
= 0

c_e_BusBlock_balance(Bus1_1_3)_:
+1 flow(Source_Bus1_1_3)
-1 flow(Bus1_sink_dsm_DLR_1_3)
= 0

c_e_BusBlock_balance(Bus1_2_4)_:
+1 flow(Source_Bus1_2_4)
-1 flow(Bus1_sink_dsm_DLR_2_4)
= 0

c_e_BusBlock_balance(Bus1_2_5)_:
+1 flow(Source_Bus1_2_5)
-1 flow(Bus1_sink_dsm_DLR_2_5)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_1)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 InvestmentFlowBlock_old(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_2)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_2)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
+1 InvestmentFlowBlock_total(Source_Bus1_2)
+1 InvestmentFlowBlock_old(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_0)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old_end(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_0)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old_exo(Source_Bus1_2)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_old_end(Source_Bus1_0)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_0)
+1 InvestmentFlowBlock_old(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_1)_:
+1 InvestmentFlowBlock_old(Source_Bus1_1)
-1 InvestmentFlowBlock_old_end(Source_Bus1_1)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_1)
= 0

c_e_InvestmentFlowBlock_old_rule(Source_Bus1_2)_:
+1 InvestmentFlowBlock_old(Source_Bus1_2)
-1 InvestmentFlowBlock_old_end(Source_Bus1_2)
-1 InvestmentFlowBlock_old_exo(Source_Bus1_2)
= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_2)_:
+1 flow(Source_Bus1_1_2)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_1_3)_:
+1 flow(Source_Bus1_1_3)
-1 InvestmentFlowBlock_total(Source_Bus1_1)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_4)_:
+1 flow(Source_Bus1_2_4)
-1 InvestmentFlowBlock_total(Source_Bus1_2)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_2_5)_:
+1 flow(Source_Bus1_2_5)
-1 InvestmentFlowBlock_total(Source_Bus1_2)
<= 0

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(sink_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
= 50

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(sink_dsm_DLR_1)_:
-1 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(sink_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_2)
-1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_end(sink_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_end(sink_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_end(sink_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_exo(sink_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_exo(sink_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_1)
= 50

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule_exo(sink_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule(sink_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule(sink_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_old_dsm_rule(sink_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_2)
-1 SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_2)
-1 SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_3)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_3)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_4)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_4)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_5)
= 0

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
+1 flow(Bus1_sink_dsm_DLR_0_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_0_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
+1 flow(Bus1_sink_dsm_DLR_0_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_1_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
+1 flow(Bus1_sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_1_3)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
+1 flow(Bus1_sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_3)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_2_4)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
+1 flow(Bus1_sink_dsm_DLR_2_4)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_4)
= 1

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_2_5)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
+1 flow(Bus1_sink_dsm_DLR_2_5)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_5)
= 1

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_3)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_4)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(sink_dsm_DLR_1_5)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_1)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_3)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_4)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(sink_dsm_DLR_1_5)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(sink_dsm_DLR_1_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(sink_dsm_DLR_1_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_1_3)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_3)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_2_4)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_4)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_2_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_5)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_1_3)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_2_4)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_2_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
<= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_3)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_3)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_4)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_3)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_4)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(sink_dsm_DLR_5)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_4)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_5)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_3)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_3)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_4)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_3)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_4)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(sink_dsm_DLR_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_4)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_5)
= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_1_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_1_3)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_3)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_2_4)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_4)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_2_5)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_5)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_1_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_1_3)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_3)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_2_4)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_4)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_2_5)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_5)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_0_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_0_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_1_3)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_3)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_2_4)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_4)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_2_5)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_5)
<= 0

c_u_SinkDSMDLRInvestmentBlock_overall_dsm_maximum(sink_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
<= 1000

c_u_SinkDSMDLRInvestmentBlock_overall_dsm_maximum(sink_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1)
<= 1000

c_u_SinkDSMDLRInvestmentBlock_overall_dsm_maximum(sink_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
<= 1000

c_l_SinkDSMDLRInvestmentBlock_overall_minimum(sink_dsm_DLR)_:
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2)
>= 200

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_5) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_5) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_5) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_5) <= +inf
   33 <= SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0) <= 100
   33 <= SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_1) <= 100
   33 <= SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_2) <= 100
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_0_1) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_1_2) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_1_3) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_2_4) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(Source_Bus1_2) <= +inf
   0 <= InvestmentFlowBlock_old(Source_Bus1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_end(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old_exo(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_old(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_5) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_5) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_3) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_4) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_5) <= +inf
end
