\* Source Pyomo model name=Model *\

min 
objective:
+500 InvestmentFlowBlock_invest(Bus1_Sink_0)
+123 InvestmentFlowBlock_invest(Source_Bus1_0)
+145 GenericInvestmentStorageBlock_invest(storage_0)

s.t.

c_e__equate_InvestmentFlowBlock_invest(Source_Bus1_0)_InvestmentFlowBlock_invest(Bus1_Sink_0)__:
-1 InvestmentFlowBlock_invest(Bus1_Sink_0)
+2 InvestmentFlowBlock_invest(Source_Bus1_0)
= 0

c_e__equate_InvestmentFlowBlock_invest(Source_Bus1_0)_GenericInvestmentStorageBlock_invest(storage_0)__:
+1 InvestmentFlowBlock_invest(Source_Bus1_0)
-1 GenericInvestmentStorageBlock_invest(storage_0)
= 0

c_e_BusBlock_balance(Bus1_0_0)_:
+1 flow(Source_Bus1_0_0)
+1 flow(storage_Bus1_0_0)
-1 flow(Bus1_storage_0_0)
-1 flow(Bus1_Sink_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
+1 flow(Source_Bus1_0_1)
+1 flow(storage_Bus1_0_1)
-1 flow(Bus1_storage_0_1)
-1 flow(Bus1_Sink_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
+1 flow(Source_Bus1_0_2)
+1 flow(storage_Bus1_0_2)
-1 flow(Bus1_storage_0_2)
-1 flow(Bus1_Sink_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_Bus1_0)_:
+1 InvestmentFlowBlock_total(storage_Bus1_0)
-1 InvestmentFlowBlock_invest(storage_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_Sink_0)_:
-1 InvestmentFlowBlock_invest(Bus1_Sink_0)
+1 InvestmentFlowBlock_total(Bus1_Sink_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Source_Bus1_0)_:
-1 InvestmentFlowBlock_invest(Source_Bus1_0)
+1 InvestmentFlowBlock_total(Source_Bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(Bus1_storage_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_0)
-1 InvestmentFlowBlock_invest(Bus1_storage_0)
= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_0_0)_:
+1 flow(storage_Bus1_0_0)
-1 InvestmentFlowBlock_total(storage_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_0_1)_:
+1 flow(storage_Bus1_0_1)
-1 InvestmentFlowBlock_total(storage_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_Bus1_0_2)_:
+1 flow(storage_Bus1_0_2)
-1 InvestmentFlowBlock_total(storage_Bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_0_0)_:
+1 flow(Bus1_Sink_0_0)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_0_1)_:
+1 flow(Bus1_Sink_0_1)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_Sink_0_2)_:
+1 flow(Bus1_Sink_0_2)
-1 InvestmentFlowBlock_total(Bus1_Sink_0)
<= 0

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

c_u_InvestmentFlowBlock_max(Bus1_storage_0_0)_:
+1 flow(Bus1_storage_0_0)
-1 InvestmentFlowBlock_total(Bus1_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_0_1)_:
+1 flow(Bus1_storage_0_1)
-1 InvestmentFlowBlock_total(Bus1_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(Bus1_storage_0_2)_:
+1 flow(Bus1_storage_0_2)
-1 InvestmentFlowBlock_total(Bus1_storage_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_init_content(storage)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage)_:
+1 flow(storage_Bus1_0_0)
-1 flow(Bus1_storage_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_Bus1_0_1)
-1 flow(Bus1_storage_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
+1 flow(storage_Bus1_0_2)
-1 flow(Bus1_storage_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage)_:
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_0)_:
+1 InvestmentFlowBlock_total(Bus1_storage_0)
-0.2 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_0)_:
+1 InvestmentFlowBlock_total(storage_Bus1_0)
-0.2 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Source_Bus1_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= +inf
   0 <= flow(Source_Bus1_0_0) <= +inf
   0 <= flow(storage_Bus1_0_0) <= +inf
   0 <= flow(Bus1_storage_0_0) <= +inf
   0 <= flow(Bus1_Sink_0_0) <= +inf
   0 <= flow(Source_Bus1_0_1) <= +inf
   0 <= flow(storage_Bus1_0_1) <= +inf
   0 <= flow(Bus1_storage_0_1) <= +inf
   0 <= flow(Bus1_Sink_0_1) <= +inf
   0 <= flow(Source_Bus1_0_2) <= +inf
   0 <= flow(storage_Bus1_0_2) <= +inf
   0 <= flow(Bus1_storage_0_2) <= +inf
   0 <= flow(Bus1_Sink_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_Sink_0) <= +inf
   0 <= InvestmentFlowBlock_total(Source_Bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(Bus1_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(Bus1_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
end
