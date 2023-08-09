\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+0.5 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_0)
+0.5 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_0)
+0.5 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_1)
+0.5 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_1)
+0.5 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_2)
+0.5 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_2)
+100 SinkDSMOemofInvestmentBlock_invest(sink_dsm_oemof_0)

s.t.

c_u_investment_limit_:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+100 SinkDSMOemofInvestmentBlock_invest(sink_dsm_oemof_0)
<= 900

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_sink_dsm_oemof_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_sink_dsm_oemof_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
-1 flow(Bus1_sink_dsm_oemof_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Source_Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
-1 InvestmentFlowBlock_total(Source_Bus1_0)
<= 0

c_e_SinkDSMOemofInvestmentBlock_total_dsm_rule(sink_dsm_oemof_0)_:
-1 SinkDSMOemofInvestmentBlock_invest(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
= 50

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(sink_dsm_oemof_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(sink_dsm_oemof_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(sink_dsm_oemof_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(sink_dsm_oemof_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_0)
-1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_0)
+1 flow(Bus1_sink_dsm_oemof_0_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_0)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(sink_dsm_oemof_0_1)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_1)
+1 flow(Bus1_sink_dsm_oemof_0_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_1)
= 1

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(sink_dsm_oemof_0_2)_:
-1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_2)
+1 flow(Bus1_sink_dsm_oemof_0_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_2)
= 1

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(sink_dsm_oemof_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_0)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(sink_dsm_oemof_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_1)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(sink_dsm_oemof_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_2)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(sink_dsm_oemof_0_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_0)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_0)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(sink_dsm_oemof_0_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_1)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_1)
<= 0

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(sink_dsm_oemof_0_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_2)
-0.5 SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_2)
<= 0

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(sink_dsm_oemof_0)_:
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_1)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_1)
= 0

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(sink_dsm_oemof_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(sink_dsm_oemof_2) <= +inf
   33 <= SinkDSMOemofInvestmentBlock_invest(sink_dsm_oemof_0) <= 100
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_sink_dsm_oemof_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_sink_dsm_oemof_0_1) <= +inf
   0 <= flow(Source_Bus1_0_2) <= +inf
   0 <= flow(Bus1_sink_dsm_oemof_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_total(sink_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(sink_dsm_oemof_2) <= +inf
end
