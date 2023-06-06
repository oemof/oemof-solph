\* Source Pyomo model name=Model *\

min 
objective:
+56 flow(electricityBus_storage_non_convex_0_0)
+56 flow(electricityBus_storage_non_convex_0_1)
+56 flow(electricityBus_storage_non_convex_0_2)
+24 flow(storage_non_convex_electricityBus_0_0)
+24 flow(storage_non_convex_electricityBus_0_1)
+24 flow(storage_non_convex_electricityBus_0_2)
+141 GenericInvestmentStorageBlock_invest(storage_non_convex_0)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage_non_convex_0_0)
+1 flow(storage_non_convex_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage_non_convex_0_1)
+1 flow(storage_non_convex_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
-1 flow(electricityBus_storage_non_convex_0_2)
+1 flow(storage_non_convex_electricityBus_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_non_convex_electricityBus_0)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
-1 InvestmentFlowBlock_invest(storage_non_convex_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
-1 InvestmentFlowBlock_invest(electricityBus_storage_non_convex_0)
= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_0_0)_:
+1 flow(storage_non_convex_electricityBus_0_0)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_0_1)_:
+1 flow(storage_non_convex_electricityBus_0_1)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_non_convex_electricityBus_0_2)_:
+1 flow(storage_non_convex_electricityBus_0_2)
-1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_0_0)_:
+1 flow(electricityBus_storage_non_convex_0_0)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_0_1)_:
+1 flow(electricityBus_storage_non_convex_0_1)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_storage_non_convex_0_2)_:
+1 flow(electricityBus_storage_non_convex_0_2)
-1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_non_convex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage_non_convex)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_init_content(storage_non_convex)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage_non_convex)_:
-0.97 flow(electricityBus_storage_non_convex_0_0)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_0)
-0.87 GenericInvestmentStorageBlock_init_content(storage_non_convex)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_0_1)_:
-0.97 flow(electricityBus_storage_non_convex_0_1)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_1)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_non_convex_0_2)_:
-0.97 flow(electricityBus_storage_non_convex_0_2)
+1.1627906976744187 flow(storage_non_convex_electricityBus_0_2)
-0.87 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage_non_convex)_:
-1 GenericInvestmentStorageBlock_init_content(storage_non_convex)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(electricityBus_storage_non_convex_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_non_convex_0)_:
+1 InvestmentFlowBlock_total(storage_non_convex_electricityBus_0)
-0.16666666666666666 GenericInvestmentStorageBlock_total(storage_non_convex_0)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_0_0)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_0_1)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_non_convex_0_2)_:
-0.9 GenericInvestmentStorageBlock_total(storage_non_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_0_0)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_0_1)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storage_non_convex_0_2)_:
+0.1 GenericInvestmentStorageBlock_total(storage_non_convex_0)
-1 GenericInvestmentStorageBlock_storage_content(storage_non_convex_2)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_non_convex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
+244 GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_non_convex_0)_:
+1 GenericInvestmentStorageBlock_invest(storage_non_convex_0)
-12 GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
>= 0

bounds
   0 <= flow(electricityBus_storage_non_convex_0_0) <= +inf
   0 <= flow(electricityBus_storage_non_convex_0_1) <= +inf
   0 <= flow(electricityBus_storage_non_convex_0_2) <= +inf
   0 <= flow(storage_non_convex_electricityBus_0_0) <= +inf
   0 <= flow(storage_non_convex_electricityBus_0_1) <= +inf
   0 <= flow(storage_non_convex_electricityBus_0_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_non_convex_0) <= 244
   0 <= InvestmentFlowBlock_total(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_non_convex_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_storage_non_convex_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricityBus_storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage_non_convex) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_non_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest_status(storage_non_convex_0) <= 1
binary
  GenericInvestmentStorageBlock_invest_status(storage_non_convex_0)
end
