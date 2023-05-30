\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+0.5 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_0)
+0.5 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_1)
+0.5 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+0.5 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+0.5 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
+100 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)

s.t.

c_u_investment_limit_:
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+100 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
<= 900

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
-1 flow(Bus1_sink_dsm_DLR_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
-1 flow(Bus1_sink_dsm_DLR_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
-1 flow(Bus1_sink_dsm_DLR_0_2)
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

c_e_SinkDSMDLRInvestmentBlock_total_dsm_rule(sink_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
= 50

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
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

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(sink_dsm_DLR_0_2)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
+1 flow(Bus1_sink_dsm_DLR_0_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
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

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(sink_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
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

c_u_SinkDSMDLRInvestmentBlock_availability_red(sink_dsm_DLR_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
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

c_u_SinkDSMDLRInvestmentBlock_availability_inc(sink_dsm_DLR_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
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

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(sink_dsm_DLR_0_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_0_0)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_0_1)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1)
<= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(sink_dsm_DLR_0_2)_:
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2)
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

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(sink_dsm_DLR_0_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(sink_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(sink_dsm_DLR_1_2)
-0.5 SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
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
   33 <= SinkDSMDLRInvestmentBlock_invest(sink_dsm_DLR_0) <= 100
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_0_1) <= +inf
   0 <= flow(Source_Bus1_0_2) <= +inf
   0 <= flow(Bus1_sink_dsm_DLR_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_total(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(sink_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(sink_dsm_DLR_2) <= +inf
end
