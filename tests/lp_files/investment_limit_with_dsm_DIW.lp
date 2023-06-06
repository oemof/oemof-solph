\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
+0.5 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1)
+0.5 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_2)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+0.5 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+100 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)

s.t.

c_u_investment_limit_:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+100 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
<= 900

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_sink_dsm_DIW_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_sink_dsm_DIW_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
-1 flow(Bus1_sink_dsm_DIW_0_2)
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

c_e_SinkDSMDIWInvestmentBlock_total_dsm_rule(sink_dsm_DIW_0)_:
-1 SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
= 50

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(sink_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
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

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(sink_dsm_DIW_0_2)_:
-1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
+1 flow(Bus1_sink_dsm_DIW_0_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
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
= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_0_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_0_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
<= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(sink_dsm_DIW_0_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
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

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(sink_dsm_DIW_0_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
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

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(sink_dsm_DIW_0_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2)
-0.5 SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(sink_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_0_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(sink_dsm_DIW_2_2) <= +inf
   33 <= SinkDSMDIWInvestmentBlock_invest(sink_dsm_DIW_0) <= 100
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_0_1) <= +inf
   0 <= flow(Source_Bus1_0_2) <= +inf
   0 <= flow(Bus1_sink_dsm_DIW_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_total(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(sink_dsm_DIW_2) <= +inf
end
