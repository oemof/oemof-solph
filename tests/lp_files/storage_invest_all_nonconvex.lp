\* Source Pyomo model name=Model *\

min 
objective:
+10 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+15 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
+10 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+10 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
+20 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+30 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)

s.t.

c_e_BusBlock_balance(bus1_0_0)_:
+1 flow(storage_all_nonconvex_bus1_0_0)
-1 flow(bus1_storage_all_nonconvex_0_0)
= 0

c_e_BusBlock_balance(bus1_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 flow(bus1_storage_all_nonconvex_0_1)
= 0

c_e_BusBlock_balance(bus1_0_2)_:
+1 flow(storage_all_nonconvex_bus1_0_2)
-1 flow(bus1_storage_all_nonconvex_0_2)
= 0

c_u_InvestmentFlowBlock_minimum_rule(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+8 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+5 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(storage_all_nonconvex_bus1_0)_:
+1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
-20 InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(bus1_storage_all_nonconvex_0)_:
+1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
-30 InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
<= 0

c_e_InvestmentFlowBlock_total_rule(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0)
+1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0)
+1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_0_0)_:
+1 flow(storage_all_nonconvex_bus1_0_0)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_all_nonconvex_bus1_0_2)_:
+1 flow(storage_all_nonconvex_bus1_0_2)
-1 InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_0_0)_:
+1 flow(bus1_storage_all_nonconvex_0_0)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_0_1)_:
+1 flow(bus1_storage_all_nonconvex_0_1)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlowBlock_max(bus1_storage_all_nonconvex_0_2)_:
+1 flow(bus1_storage_all_nonconvex_0_2)
-1 InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage_all_nonconvex)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage_all_nonconvex)_:
+1 flow(storage_all_nonconvex_bus1_0_0)
-1 flow(bus1_storage_all_nonconvex_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_0_1)_:
+1 flow(storage_all_nonconvex_bus1_0_1)
-1 flow(bus1_storage_all_nonconvex_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_0_2)_:
+1 flow(storage_all_nonconvex_bus1_0_2)
-1 flow(bus1_storage_all_nonconvex_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage_all_nonconvex)_:
-1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
+100 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_all_nonconvex_0)_:
+1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0)
-20 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
>= 0

bounds
   0 <= InvestmentFlowBlock_invest(storage_all_nonconvex_bus1_0) <= 20
   0 <= InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0) <= 1
   0 <= InvestmentFlowBlock_invest(bus1_storage_all_nonconvex_0) <= 30
   0 <= InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0) <= 1
   0 <= GenericInvestmentStorageBlock_invest(storage_all_nonconvex_0) <= 100
   0 <= GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0) <= 1
   0 <= flow(storage_all_nonconvex_bus1_0_0) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_0) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0_1) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_1) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0_2) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_all_nonconvex_bus1_0) <= +inf
   0 <= InvestmentFlowBlock_total(bus1_storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage_all_nonconvex) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2) <= +inf
binary
  InvestmentFlowBlock_invest_status(storage_all_nonconvex_bus1_0)
  InvestmentFlowBlock_invest_status(bus1_storage_all_nonconvex_0)
  GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex_0)
end
