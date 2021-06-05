\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+123 InvestmentFlow_invest(Source_Bus1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_2)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_0)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1)
+2 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2)
+100 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1)
+2 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
+2 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
+100 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
+2 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_0)
+2 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_1)
+2 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_2)
+100 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)

s.t.

c_u_investment_limit_:
+145 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+123 InvestmentFlow_invest(Source_Bus1)
+100 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
+100 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
+100 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 1000

c_e_Bus_balance(Bus1_0)_:
-1 flow(Bus1_demand_dsm_DIW_0)
-1 flow(Bus1_demand_dsm_DLR_0)
-1 flow(Bus1_demand_dsm_oemof_0)
-1 flow(Bus1_storage_invest_limit_0)
+1 flow(Source_Bus1_0)
+1 flow(storage_invest_limit_Bus1_0)
= 0

c_e_Bus_balance(Bus1_1)_:
-1 flow(Bus1_demand_dsm_DIW_1)
-1 flow(Bus1_demand_dsm_DLR_1)
-1 flow(Bus1_demand_dsm_oemof_1)
-1 flow(Bus1_storage_invest_limit_1)
+1 flow(Source_Bus1_1)
+1 flow(storage_invest_limit_Bus1_1)
= 0

c_e_Bus_balance(Bus1_2)_:
-1 flow(Bus1_demand_dsm_DIW_2)
-1 flow(Bus1_demand_dsm_DLR_2)
-1 flow(Bus1_demand_dsm_oemof_2)
-1 flow(Bus1_storage_invest_limit_2)
+1 flow(Source_Bus1_2)
+1 flow(storage_invest_limit_Bus1_2)
= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_0)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_0)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_1)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_1)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_invest_limit_2)_:
-1 InvestmentFlow_invest(Bus1_storage_invest_limit)
+1 flow(Bus1_storage_invest_limit_2)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_0)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_0)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_1)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_1)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_2)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_2)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_0)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_0)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_1)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_1)
<= 0

c_u_InvestmentFlow_max(storage_invest_limit_Bus1_2)_:
-1 InvestmentFlow_invest(storage_invest_limit_Bus1)
+1 flow(storage_invest_limit_Bus1_2)
<= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage_invest_limit)_:
+1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage_invest_limit)_:
-1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
-1 flow(Bus1_storage_invest_limit_0)
+1 flow(storage_invest_limit_Bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
-1 flow(Bus1_storage_invest_limit_1)
+1 flow(storage_invest_limit_Bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_invest_limit_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
-1 flow(Bus1_storage_invest_limit_2)
+1 flow(storage_invest_limit_Bus1_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage_invest_limit)_:
-1 GenericInvestmentStorageBlock_init_content(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_invest_limit)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 InvestmentFlow_invest(Bus1_storage_invest_limit)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_invest_limit)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 InvestmentFlow_invest(storage_invest_limit_Bus1)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_invest_limit_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_invest_limit)
+1 GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2)
<= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_shift_shed_vars(demand_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_2)
= 0

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_0)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
+1 flow(Bus1_demand_dsm_DIW_0)
= 50

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_1)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
+1 flow(Bus1_demand_dsm_DIW_1)
= 50

c_e_SinkDSMDIWInvestmentBlock_input_output_relation(demand_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2)
-1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_2)
-1 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
+1 flow(Bus1_demand_dsm_DIW_2)
= 50

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_DIW_0)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_0)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_DIW_1)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_1)
= 0

c_e_SinkDSMDIWInvestmentBlock_dsm_updo_constraint(demand_dsm_DIW_2)_:
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1)
-1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_2)
= 0

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_up_constraint(demand_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_dsm_do_constraint(demand_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_DIW_0)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_0)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_DIW_1)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_1)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_u_SinkDSMDIWInvestmentBlock_C2_constraint(demand_dsm_DIW_2)_:
+1 SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2)
+1 SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2)
+1 SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_2)
-0.5 SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW)
<= 25

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_1_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_2_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_2_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_shift_shed_vars(demand_dsm_DLR_2_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0)
-1 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
+1 flow(Bus1_demand_dsm_DLR_0)
= 50

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_DLR_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1)
-1 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
+1 flow(Bus1_demand_dsm_DLR_1)
= 50

c_e_SinkDSMDLRInvestmentBlock_input_output_relation(demand_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2)
-1 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
+1 flow(Bus1_demand_dsm_DLR_2)
= 50

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_DLR_1_1)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_DLR_2_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_red(demand_dsm_DLR_2_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_DLR_1_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_DLR_1_1)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_DLR_2_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_capacity_balance_inc(demand_dsm_DLR_2_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_DLR_2_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_red(demand_dsm_DLR_2_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_DLR_1_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_DLR_2_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_no_comp_inc(demand_dsm_DLR_2_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_availability_red(demand_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_availability_inc(demand_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_DLR_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_red(demand_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_DLR_0)_:
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_0)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_DLR_1)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_0)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_1)
= 0

c_e_SinkDSMDLRInvestmentBlock_dr_storage_inc(demand_dsm_DLR_2)_:
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
-1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_1)
-1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_2)
= 0

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_0)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_1)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_red(demand_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_2)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_0)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_1)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_storage_limit_inc(demand_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_2)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_DLR_0)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_DLR_1)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_u_SinkDSMDLRInvestmentBlock_dr_logical_constraint(demand_dsm_DLR_2)_:
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2)
+1 SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2)
-0.5 SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR)
<= 25

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_oemof_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_0)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_oemof_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_1)
= 0

c_e_SinkDSMOemofInvestmentBlock_shift_shed_vars(demand_dsm_oemof_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_2)
= 0

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_oemof_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_0)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_0)
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
+1 flow(Bus1_demand_dsm_oemof_0)
= 50

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_oemof_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_1)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_1)
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
+1 flow(Bus1_demand_dsm_oemof_1)
= 50

c_e_SinkDSMOemofInvestmentBlock_input_output_relation(demand_dsm_oemof_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_2)
-1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_2)
-1 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
+1 flow(Bus1_demand_dsm_oemof_2)
= 50

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_oemof_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_0)
-0.5 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 25

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_oemof_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_1)
-0.40000000000000002 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 20

c_u_SinkDSMOemofInvestmentBlock_dsm_up_constraint(demand_dsm_oemof_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_2)
-0.5 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 25

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_oemof_0)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_0)
-0.5 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 25

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_oemof_1)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_1)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_1)
-0.40000000000000002 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 20

c_u_SinkDSMOemofInvestmentBlock_dsm_down_constraint(demand_dsm_oemof_2)_:
+1 SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_2)
+1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_2)
-0.5 SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof)
<= 25

c_e_SinkDSMOemofInvestmentBlock_dsm_sum_constraint(demand_dsm_oemof_0)_:
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_0)
-1 SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_1)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_0)
+1 SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_1)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_demand_dsm_DIW_0) <= +inf
   0 <= flow(Bus1_demand_dsm_DIW_1) <= +inf
   0 <= flow(Bus1_demand_dsm_DIW_2) <= +inf
   0 <= flow(Bus1_demand_dsm_DLR_0) <= +inf
   0 <= flow(Bus1_demand_dsm_DLR_1) <= +inf
   0 <= flow(Bus1_demand_dsm_DLR_2) <= +inf
   0 <= flow(Bus1_demand_dsm_oemof_0) <= +inf
   0 <= flow(Bus1_demand_dsm_oemof_1) <= +inf
   0 <= flow(Bus1_demand_dsm_oemof_2) <= +inf
   0 <= flow(Bus1_storage_invest_limit_0) <= +inf
   0 <= flow(Bus1_storage_invest_limit_1) <= +inf
   0 <= flow(Bus1_storage_invest_limit_2) <= +inf
   0 <= flow(Source_Bus1_0) <= +inf
   0 <= flow(Source_Bus1_1) <= +inf
   0 <= flow(Source_Bus1_2) <= +inf
   0 <= flow(storage_invest_limit_Bus1_0) <= +inf
   0 <= flow(storage_invest_limit_Bus1_1) <= +inf
   0 <= flow(storage_invest_limit_Bus1_2) <= +inf
   0 <= InvestmentFlow_invest(Bus1_storage_invest_limit) <= +inf
   0 <= InvestmentFlow_invest(Source_Bus1) <= +inf
   0 <= InvestmentFlow_invest(storage_invest_limit_Bus1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_invest_limit_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_invest_limit) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage_invest_limit) <= +inf
   33 <= SinkDSMDIWInvestmentBlock_invest(demand_dsm_DIW) <= 100
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_0_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_1_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shift(demand_dsm_DIW_2_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_do_shed(demand_dsm_DIW_2) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_0) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_1) <= +inf
   0 <= SinkDSMDIWInvestmentBlock_dsm_up(demand_dsm_DIW_2) <= +inf
   33 <= SinkDSMDLRInvestmentBlock_invest(demand_dsm_DLR) <= 100
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shift(demand_dsm_DLR_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_shed(demand_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up(demand_dsm_DLR_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_do(demand_dsm_DLR_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_1_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_balance_dsm_up(demand_dsm_DLR_2_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_do_level(demand_dsm_DLR_2) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_0) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_1) <= +inf
   0 <= SinkDSMDLRInvestmentBlock_dsm_up_level(demand_dsm_DLR_2) <= +inf
   33 <= SinkDSMOemofInvestmentBlock_invest(demand_dsm_oemof) <= 100
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shift(demand_dsm_oemof_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_do_shed(demand_dsm_oemof_2) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_0) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_1) <= +inf
   0 <= SinkDSMOemofInvestmentBlock_dsm_up(demand_dsm_oemof_2) <= +inf
end
