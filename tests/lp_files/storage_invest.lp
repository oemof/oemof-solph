\* Source Pyomo model name=OperationalModel *\

min 
objective:
+180 InvestmentStorage_invest(storage)
+56 flow(electricityBus_storage_0)
+56 flow(electricityBus_storage_1)
+56 flow(electricityBus_storage_2)
+24 flow(storage_electricityBus_0)
+24 flow(storage_electricityBus_1)
+24 flow(storage_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storage_0)
+1 flow(storage_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storage_1)
+1 flow(storage_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storage_2)
+1 flow(storage_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_storage_0)_:
-1 InvestmentFlow_invest(electricityBus_storage)
+1 flow(electricityBus_storage_0)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage_1)_:
-1 InvestmentFlow_invest(electricityBus_storage)
+1 flow(electricityBus_storage_1)
<= 0

c_u_InvestmentFlow_max(electricityBus_storage_2)_:
-1 InvestmentFlow_invest(electricityBus_storage)
+1 flow(electricityBus_storage_2)
<= 0

c_u_InvestmentFlow_max(storage_electricityBus_0)_:
-1 InvestmentFlow_invest(storage_electricityBus)
+1 flow(storage_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(storage_electricityBus_1)_:
-1 InvestmentFlow_invest(storage_electricityBus)
+1 flow(storage_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(storage_electricityBus_2)_:
-1 InvestmentFlow_invest(storage_electricityBus)
+1 flow(storage_electricityBus_2)
<= 0

c_e_InvestmentStorage_balance(storage_0)_:
+1 InvestmentStorage_capacity(storage_0)
-0.87 InvestmentStorage_capacity(storage_2)
-0.96999999999999997 flow(electricityBus_storage_0)
+1.1627906976744187 flow(storage_electricityBus_0)
= 0

c_e_InvestmentStorage_balance(storage_1)_:
-0.87 InvestmentStorage_capacity(storage_0)
+1 InvestmentStorage_capacity(storage_1)
-0.96999999999999997 flow(electricityBus_storage_1)
+1.1627906976744187 flow(storage_electricityBus_1)
= 0

c_e_InvestmentStorage_balance(storage_2)_:
-0.87 InvestmentStorage_capacity(storage_1)
+1 InvestmentStorage_capacity(storage_2)
-0.96999999999999997 flow(electricityBus_storage_2)
+1.1627906976744187 flow(storage_electricityBus_2)
= 0

c_e_InvestmentStorage_storage_capacity_inflow(storage)_:
+1 InvestmentFlow_invest(electricityBus_storage)
-0.16666666666666666 InvestmentStorage_invest(storage)
= 0

c_e_InvestmentStorage_storage_capacity_outflow(storage)_:
+1 InvestmentFlow_invest(storage_electricityBus)
-0.16666666666666666 InvestmentStorage_invest(storage)
= 0

c_u_InvestmentStorage_max_capacity(storage_0)_:
+1 InvestmentStorage_capacity(storage_0)
-0.90000000000000002 InvestmentStorage_invest(storage)
<= 0

c_u_InvestmentStorage_max_capacity(storage_1)_:
+1 InvestmentStorage_capacity(storage_1)
-0.90000000000000002 InvestmentStorage_invest(storage)
<= 0

c_u_InvestmentStorage_max_capacity(storage_2)_:
+1 InvestmentStorage_capacity(storage_2)
-0.90000000000000002 InvestmentStorage_invest(storage)
<= 0

c_u_InvestmentStorage_min_capacity(storage_0)_:
-1 InvestmentStorage_capacity(storage_0)
+0.10000000000000001 InvestmentStorage_invest(storage)
<= 0

c_u_InvestmentStorage_min_capacity(storage_1)_:
-1 InvestmentStorage_capacity(storage_1)
+0.10000000000000001 InvestmentStorage_invest(storage)
<= 0

c_u_InvestmentStorage_min_capacity(storage_2)_:
-1 InvestmentStorage_capacity(storage_2)
+0.10000000000000001 InvestmentStorage_invest(storage)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage_0) <= +inf
   0 <= flow(electricityBus_storage_1) <= +inf
   0 <= flow(electricityBus_storage_2) <= +inf
   0 <= flow(storage_electricityBus_0) <= +inf
   0 <= flow(storage_electricityBus_1) <= +inf
   0 <= flow(storage_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_storage) <= +inf
   0 <= InvestmentFlow_invest(storage_electricityBus) <= +inf
   0 <= InvestmentStorage_capacity(storage_0) <= +inf
   0 <= InvestmentStorage_capacity(storage_1) <= +inf
   0 <= InvestmentStorage_capacity(storage_2) <= +inf
   0 <= InvestmentStorage_invest(storage) <= 234
end
