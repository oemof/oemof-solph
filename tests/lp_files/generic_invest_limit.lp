\* Source Pyomo model name=Model *\

min 
objective:
+50 InvestmentFlow_invest(source_0_bus_1)
+100 InvestmentFlow_invest(source_1_bus_1)
+75 InvestmentFlow_invest(source_2_bus_1)

s.t.

c_u_invest_limit_space_constraint_:
+4 InvestmentFlow_invest(source_0_bus_1)
+1 InvestmentFlow_invest(source_1_bus_1)
<= 20

c_e_Bus_balance(bus_1_0)_:
+1 flow(source_0_bus_1_0)
+1 flow(source_1_bus_1_0)
+1 flow(source_2_bus_1_0)
= 0

c_e_Bus_balance(bus_1_1)_:
+1 flow(source_0_bus_1_1)
+1 flow(source_1_bus_1_1)
+1 flow(source_2_bus_1_1)
= 0

c_e_Bus_balance(bus_1_2)_:
+1 flow(source_0_bus_1_2)
+1 flow(source_1_bus_1_2)
+1 flow(source_2_bus_1_2)
= 0

c_u_InvestmentFlow_max(source_0_bus_1_0)_:
-1 InvestmentFlow_invest(source_0_bus_1)
+1 flow(source_0_bus_1_0)
<= 0

c_u_InvestmentFlow_max(source_0_bus_1_1)_:
-1 InvestmentFlow_invest(source_0_bus_1)
+1 flow(source_0_bus_1_1)
<= 0

c_u_InvestmentFlow_max(source_0_bus_1_2)_:
-1 InvestmentFlow_invest(source_0_bus_1)
+1 flow(source_0_bus_1_2)
<= 0

c_u_InvestmentFlow_max(source_1_bus_1_0)_:
-1 InvestmentFlow_invest(source_1_bus_1)
+1 flow(source_1_bus_1_0)
<= 0

c_u_InvestmentFlow_max(source_1_bus_1_1)_:
-1 InvestmentFlow_invest(source_1_bus_1)
+1 flow(source_1_bus_1_1)
<= 0

c_u_InvestmentFlow_max(source_1_bus_1_2)_:
-1 InvestmentFlow_invest(source_1_bus_1)
+1 flow(source_1_bus_1_2)
<= 0

c_u_InvestmentFlow_max(source_2_bus_1_0)_:
-1 InvestmentFlow_invest(source_2_bus_1)
+1 flow(source_2_bus_1_0)
<= 0

c_u_InvestmentFlow_max(source_2_bus_1_1)_:
-1 InvestmentFlow_invest(source_2_bus_1)
+1 flow(source_2_bus_1_1)
<= 0

c_u_InvestmentFlow_max(source_2_bus_1_2)_:
-1 InvestmentFlow_invest(source_2_bus_1)
+1 flow(source_2_bus_1_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source_0_bus_1_0) <= +inf
   0 <= flow(source_0_bus_1_1) <= +inf
   0 <= flow(source_0_bus_1_2) <= +inf
   0 <= flow(source_1_bus_1_0) <= +inf
   0 <= flow(source_1_bus_1_1) <= +inf
   0 <= flow(source_1_bus_1_2) <= +inf
   0 <= flow(source_2_bus_1_0) <= +inf
   0 <= flow(source_2_bus_1_1) <= +inf
   0 <= flow(source_2_bus_1_2) <= +inf
   0 <= InvestmentFlow_invest(source_0_bus_1) <= +inf
   0 <= InvestmentFlow_invest(source_1_bus_1) <= +inf
   0 <= InvestmentFlow_invest(source_2_bus_1) <= +inf
end
