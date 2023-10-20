\* Source Pyomo model name=Model *\

min 
objective:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_1)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_2)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3)
+0.49019607843137253 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_3)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5)
+0.48058439061899266 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5)
+99.99999999999999 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
+98.03921568627449 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_1)
+48.534265191225046 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_2)

s.t.

c_u_investment_limit_per_period(0)_:
+8.230422488026955 InvestmentFlowBlock_invest(Source_Bus1_0)
+99.99999999999999 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
<= 400

c_u_investment_limit_per_period(1)_:
+5.432444590842506 InvestmentFlowBlock_invest(Source_Bus1_1)
+98.03921568627449 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_1)
<= 300

c_u_investment_limit_per_period(2)_:
+2.6893290053675805 InvestmentFlowBlock_invest(Source_Bus1_2)
+48.534265191225046 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_2)
<= 200

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_sink_dsm_DIW_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_sink_dsm_DIW_0_1)
= 0

c_e_BusBlock_balance(Bus1_1_2)_:
+1 flow(Source_Bus1_1_2)
-1 flow(Bus1_sink_dsm_DIW_1_2)
= 0

c_e_BusBlock_balance(Bus1_1_3)_:
+1 flow(Source_Bus1_1_3)
-1 flow(Bus1_sink_dsm_DIW_1_3)
= 0

c_e_BusBlock_balance(Bus1_2_4)_:
+1 flow(Source_Bus1_2_4)
-1 flow(Bus1_sink_dsm_DIW_2_4)
= 0

c_e_BusBlock_balance(Bus1_2_5)_:
+1 flow(Source_Bus1_2_5)
-1 flow(Bus1_sink_dsm_DIW_2_5)
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

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(sink_dsm_DIW_0)_:
-1 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
= 50

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(sink_dsm_DIW_1)_:
-1 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_1)
-1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(sink_dsm_DIW_2)_:
-1 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_2)
-1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(sink_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_end(sink_dsm_DIW_2)_:
-1 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(sink_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_1)
= 50

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule_exo(sink_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(sink_dsm_DIW_0)_:
-1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_0)
-1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_1)
-1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_1)
-1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_old_dsm_rule(sink_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_2)
-1 SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_2)
-1 SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_3)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_4)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_5)
= 0

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
+1 flow(Bus1_sink_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_0_1)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
+1 flow(Bus1_sink_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_1_2)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2)
+1 flow(Bus1_sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_1_3)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3)
+1 flow(Bus1_sink_dsm_DIW_1_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_3)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_2_4)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4)
+1 flow(Bus1_sink_dsm_DIW_2_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_4)
= 1

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_2_5)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5)
+1 flow(Bus1_sink_dsm_DIW_2_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_5)
= 1

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_0)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_1)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_2)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_3)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_4)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(sink_dsm_DIW_5)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5)
= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_3)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_4)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_5)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_1_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_1_3)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_3)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_2_4)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_4)
<= 0

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_2_5)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_5)
<= 0

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(sink_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
<= 1000

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1)
<= 1000

c_u_SinkDSMDIWInvestmentBlock_overall_dsm_maximum(sink_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
<= 1000

c_l_SinkDSMDIWInvestmentBlock_overall_minimum(sink_dsm_DIW)_:
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2)
>= 200

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_1) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_3_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_4_5) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_5_5) <= +inf
   33 <= SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0) <= 100
   33 <= SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_1) <= 100
   33 <= SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_2) <= 100
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_0_1) <= +inf
   0 <= flow(Source_Bus1_1_2) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_1_2) <= +inf
   0 <= flow(Source_Bus1_1_3) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_1_3) <= +inf
   0 <= flow(Source_Bus1_2_4) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_2_4) <= +inf
   0 <= flow(Source_Bus1_2_5) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_2_5) <= +inf
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
   0 <= SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_end(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old_exo(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_old(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_3) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_4) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_5) <= +inf
end
