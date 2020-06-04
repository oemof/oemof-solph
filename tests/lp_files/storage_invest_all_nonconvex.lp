\* Source Pyomo model name=Model *\

min 
objective:
+20 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
+30 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex)
+10 InvestmentFlow_invest(bus1_storage_all_nonconvex)
+10 InvestmentFlow_invest(storage_all_nonconvex_bus1)
+10 InvestmentFlow_invest_status(bus1_storage_all_nonconvex)
+15 InvestmentFlow_invest_status(storage_all_nonconvex_bus1)

s.t.

c_e_Bus_balance(bus1_0)_:
-1 flow(bus1_storage_all_nonconvex_0)
+1 flow(storage_all_nonconvex_bus1_0)
= 0

c_e_Bus_balance(bus1_1)_:
-1 flow(bus1_storage_all_nonconvex_1)
+1 flow(storage_all_nonconvex_bus1_1)
= 0

c_e_Bus_balance(bus1_2)_:
-1 flow(bus1_storage_all_nonconvex_2)
+1 flow(storage_all_nonconvex_bus1_2)
= 0

c_u_InvestmentFlow_minimum_rule(bus1_storage_all_nonconvex)_:
-1 InvestmentFlow_invest(bus1_storage_all_nonconvex)
+5 InvestmentFlow_invest_status(bus1_storage_all_nonconvex)
<= 0

c_u_InvestmentFlow_minimum_rule(storage_all_nonconvex_bus1)_:
-1 InvestmentFlow_invest(storage_all_nonconvex_bus1)
+8 InvestmentFlow_invest_status(storage_all_nonconvex_bus1)
<= 0

c_u_InvestmentFlow_maximum_rule(bus1_storage_all_nonconvex)_:
+1 InvestmentFlow_invest(bus1_storage_all_nonconvex)
-30 InvestmentFlow_invest_status(bus1_storage_all_nonconvex)
<= 0

c_u_InvestmentFlow_maximum_rule(storage_all_nonconvex_bus1)_:
+1 InvestmentFlow_invest(storage_all_nonconvex_bus1)
-20 InvestmentFlow_invest_status(storage_all_nonconvex_bus1)
<= 0

c_u_InvestmentFlow_max(bus1_storage_all_nonconvex_0)_:
-1 InvestmentFlow_invest(bus1_storage_all_nonconvex)
+1 flow(bus1_storage_all_nonconvex_0)
<= 0

c_u_InvestmentFlow_max(bus1_storage_all_nonconvex_1)_:
-1 InvestmentFlow_invest(bus1_storage_all_nonconvex)
+1 flow(bus1_storage_all_nonconvex_1)
<= 0

c_u_InvestmentFlow_max(bus1_storage_all_nonconvex_2)_:
-1 InvestmentFlow_invest(bus1_storage_all_nonconvex)
+1 flow(bus1_storage_all_nonconvex_2)
<= 0

c_u_InvestmentFlow_max(storage_all_nonconvex_bus1_0)_:
-1 InvestmentFlow_invest(storage_all_nonconvex_bus1)
+1 flow(storage_all_nonconvex_bus1_0)
<= 0

c_u_InvestmentFlow_max(storage_all_nonconvex_bus1_1)_:
-1 InvestmentFlow_invest(storage_all_nonconvex_bus1)
+1 flow(storage_all_nonconvex_bus1_1)
<= 0

c_u_InvestmentFlow_max(storage_all_nonconvex_bus1_2)_:
-1 InvestmentFlow_invest(storage_all_nonconvex_bus1)
+1 flow(storage_all_nonconvex_bus1_2)
<= 0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage_all_nonconvex)_:
+1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
<= 0

c_e_GenericInvestmentStorageBlock_balance_first(storage_all_nonconvex)_:
-1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
-1 flow(bus1_storage_all_nonconvex_0)
+1 flow(storage_all_nonconvex_bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_1)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
-1 flow(bus1_storage_all_nonconvex_1)
+1 flow(storage_all_nonconvex_bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_all_nonconvex_2)_:
-1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
-1 flow(bus1_storage_all_nonconvex_2)
+1 flow(storage_all_nonconvex_bus1_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage_all_nonconvex)_:
-1 GenericInvestmentStorageBlock_init_content(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_all_nonconvex_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
+1 GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2)
<= 0

c_l_GenericInvestmentStorageBlock_limit_max(storage_all_nonconvex)_:
-1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
+100 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex)
>= 0

c_l_GenericInvestmentStorageBlock_limit_min(storage_all_nonconvex)_:
+1 GenericInvestmentStorageBlock_invest(storage_all_nonconvex)
-20 GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex)
>= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus1_storage_all_nonconvex_0) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_1) <= +inf
   0 <= flow(bus1_storage_all_nonconvex_2) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_0) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_1) <= +inf
   0 <= flow(storage_all_nonconvex_bus1_2) <= +inf
   0 <= InvestmentFlow_invest(bus1_storage_all_nonconvex) <= 30
   0 <= InvestmentFlow_invest(storage_all_nonconvex_bus1) <= 20
   0 <= InvestmentFlow_invest_status(bus1_storage_all_nonconvex) <= 1
   0 <= InvestmentFlow_invest_status(storage_all_nonconvex_bus1) <= 1
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_all_nonconvex_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_all_nonconvex) <= 100
   0 <= GenericInvestmentStorageBlock_init_content(storage_all_nonconvex) <= +inf
   0 <= GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex) <= 1
binary
  InvestmentFlow_invest_status(bus1_storage_all_nonconvex)
  InvestmentFlow_invest_status(storage_all_nonconvex_bus1)
  GenericInvestmentStorageBlock_invest_status(storage_all_nonconvex)
end
