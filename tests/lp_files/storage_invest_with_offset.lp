\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storagenon_convex)
+5 GenericInvestmentStorageBlock_invest_status(storagenon_convex)
+56 flow(electricityBus_storagenon_convex_0)
+56 flow(electricityBus_storagenon_convex_1)
+56 flow(electricityBus_storagenon_convex_2)
+24 flow(storagenon_convex_electricityBus_0)
+24 flow(storagenon_convex_electricityBus_1)
+24 flow(storagenon_convex_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storagenon_convex_0)
+1 flow(storagenon_convex_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storagenon_convex_1)
+1 flow(storagenon_convex_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storagenon_convex_2)
+1 flow(storagenon_convex_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_storagenon_convex_0)_:
-1 InvestmentFlow_invest(electricityBus_storagenon_convex)
+1 flow(electricityBus_storagenon_convex_0)
<= 0

c_u_InvestmentFlow_max(electricityBus_storagenon_convex_1)_:
-1 InvestmentFlow_invest(electricityBus_storagenon_convex)
+1 flow(electricityBus_storagenon_convex_1)
<= 0

c_u_InvestmentFlow_max(electricityBus_storagenon_convex_2)_:
-1 InvestmentFlow_invest(electricityBus_storagenon_convex)
+1 flow(electricityBus_storagenon_convex_2)
<= 0

c_u_InvestmentFlow_max(storagenon_convex_electricityBus_0)_:
-1 InvestmentFlow_invest(storagenon_convex_electricityBus)
+1 flow(storagenon_convex_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(storagenon_convex_electricityBus_1)_:
-1 InvestmentFlow_invest(storagenon_convex_electricityBus)
+1 flow(storagenon_convex_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(storagenon_convex_electricityBus_2)_:
-1 InvestmentFlow_invest(storagenon_convex_electricityBus)
+1 flow(storagenon_convex_electricityBus_2)
<= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storagenon_convex)_:
+1 GenericInvestmentStorageBlock_init_content(storagenon_convex)
-1 GenericInvestmentStorageBlock_invest(storagenon_convex)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storagenon_convex)_:
-0.87 GenericInvestmentStorageBlock_init_content(storagenon_convex)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_0)
-0.96999999999999997 flow(electricityBus_storagenon_convex_0)
+1.1627906976744187 flow(storagenon_convex_electricityBus_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storagenon_convex_1)_:
-0.87 GenericInvestmentStorageBlock_storage_content(storagenon_convex_0)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_1)
-0.96999999999999997 flow(electricityBus_storagenon_convex_1)
+1.1627906976744187 flow(storagenon_convex_electricityBus_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storagenon_convex_2)_:
-0.87 GenericInvestmentStorageBlock_storage_content(storagenon_convex_1)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_2)
-0.96999999999999997 flow(electricityBus_storagenon_convex_2)
+1.1627906976744187 flow(storagenon_convex_electricityBus_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storagenon_convex)_:
-1 GenericInvestmentStorageBlock_init_content(storagenon_convex)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storagenon_convex)_:
-0.16666666666666666 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1 InvestmentFlow_invest(electricityBus_storagenon_convex)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storagenon_convex)_:
-0.16666666666666666 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1 InvestmentFlow_invest(storagenon_convex_electricityBus)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storagenon_convex_0)_:
-0.90000000000000002 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storagenon_convex_1)_:
-0.90000000000000002 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storagenon_convex_2)_:
-0.90000000000000002 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_2)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storagenon_convex_0)_:
+0.10000000000000001 GenericInvestmentStorageBlock_invest(storagenon_convex)
-1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_0)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storagenon_convex_1)_:
+0.10000000000000001 GenericInvestmentStorageBlock_invest(storagenon_convex)
-1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_1)
<= 0

c_u_GenericInvestmentStorageBlock_min_storage_content(storagenon_convex_2)_:
+0.10000000000000001 GenericInvestmentStorageBlock_invest(storagenon_convex)
-1 GenericInvestmentStorageBlock_storage_content(storagenon_convex_2)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storagenon_convex)_:
-1 GenericInvestmentStorageBlock_invest(storagenon_convex)
+1454 GenericInvestmentStorageBlock_invest_status(storagenon_convex)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storagenon_convex)_:
+1 GenericInvestmentStorageBlock_invest(storagenon_convex)
-19 GenericInvestmentStorageBlock_invest_status(storagenon_convex)
>= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storagenon_convex_0) <= +inf
   0 <= flow(electricityBus_storagenon_convex_1) <= +inf
   0 <= flow(electricityBus_storagenon_convex_2) <= +inf
   0 <= flow(storagenon_convex_electricityBus_0) <= +inf
   0 <= flow(storagenon_convex_electricityBus_1) <= +inf
   0 <= flow(storagenon_convex_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_storagenon_convex) <= +inf
   0 <= InvestmentFlow_invest(storagenon_convex_electricityBus) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storagenon_convex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storagenon_convex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storagenon_convex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storagenon_convex) <= 1454
   0 <= GenericInvestmentStorageBlock_init_content(storagenon_convex) <= +inf
   0 <= GenericInvestmentStorageBlock_invest_status(storagenon_convex) <= 1
binary
  GenericInvestmentStorageBlock_invest_status(storagenon_convex)
end
