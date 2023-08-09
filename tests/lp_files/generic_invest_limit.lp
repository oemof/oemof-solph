\* Source Pyomo model name=Model *\

min 
objective:
+100 InvestmentFlowBlock_invest(source_1_bus_1_0)
+75 InvestmentFlowBlock_invest(source_2_bus_1_0)
+50 InvestmentFlowBlock_invest(source_0_bus_1_0)

s.t.

c_u_invest_limit_space_constraint_:
+1 InvestmentFlowBlock_invest(source_1_bus_1_0)
+4 InvestmentFlowBlock_invest(source_0_bus_1_0)
<= 20

c_e_BusBlock_balance(bus_1_0_0)_:
+1 flow(source_0_bus_1_0_0)
+1 flow(source_2_bus_1_0_0)
+1 flow(source_1_bus_1_0_0)
= 0

c_e_BusBlock_balance(bus_1_0_1)_:
+1 flow(source_0_bus_1_0_1)
+1 flow(source_2_bus_1_0_1)
+1 flow(source_1_bus_1_0_1)
= 0

c_e_BusBlock_balance(bus_1_0_2)_:
+1 flow(source_0_bus_1_0_2)
+1 flow(source_2_bus_1_0_2)
+1 flow(source_1_bus_1_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(source_1_bus_1_0)_:
-1 InvestmentFlowBlock_invest(source_1_bus_1_0)
+1 InvestmentFlowBlock_total(source_1_bus_1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(source_2_bus_1_0)_:
-1 InvestmentFlowBlock_invest(source_2_bus_1_0)
+1 InvestmentFlowBlock_total(source_2_bus_1_0)
= 0

c_e_InvestmentFlowBlock_total_rule(source_0_bus_1_0)_:
-1 InvestmentFlowBlock_invest(source_0_bus_1_0)
+1 InvestmentFlowBlock_total(source_0_bus_1_0)
= 0

c_u_InvestmentFlowBlock_max(source_1_bus_1_0_0)_:
+1 flow(source_1_bus_1_0_0)
-1 InvestmentFlowBlock_total(source_1_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_1_bus_1_0_1)_:
+1 flow(source_1_bus_1_0_1)
-1 InvestmentFlowBlock_total(source_1_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_1_bus_1_0_2)_:
+1 flow(source_1_bus_1_0_2)
-1 InvestmentFlowBlock_total(source_1_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_2_bus_1_0_0)_:
+1 flow(source_2_bus_1_0_0)
-1 InvestmentFlowBlock_total(source_2_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_2_bus_1_0_1)_:
+1 flow(source_2_bus_1_0_1)
-1 InvestmentFlowBlock_total(source_2_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_2_bus_1_0_2)_:
+1 flow(source_2_bus_1_0_2)
-1 InvestmentFlowBlock_total(source_2_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_0_bus_1_0_0)_:
+1 flow(source_0_bus_1_0_0)
-1 InvestmentFlowBlock_total(source_0_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_0_bus_1_0_1)_:
+1 flow(source_0_bus_1_0_1)
-1 InvestmentFlowBlock_total(source_0_bus_1_0)
<= 0

c_u_InvestmentFlowBlock_max(source_0_bus_1_0_2)_:
+1 flow(source_0_bus_1_0_2)
-1 InvestmentFlowBlock_total(source_0_bus_1_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(source_1_bus_1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(source_2_bus_1_0) <= +inf
   0 <= InvestmentFlowBlock_invest(source_0_bus_1_0) <= +inf
   0 <= flow(source_0_bus_1_0_0) <= +inf
   0 <= flow(source_2_bus_1_0_0) <= +inf
   0 <= flow(source_1_bus_1_0_0) <= +inf
   0 <= flow(source_0_bus_1_0_1) <= +inf
   0 <= flow(source_2_bus_1_0_1) <= +inf
   0 <= flow(source_1_bus_1_0_1) <= +inf
   0 <= flow(source_0_bus_1_0_2) <= +inf
   0 <= flow(source_2_bus_1_0_2) <= +inf
   0 <= flow(source_1_bus_1_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(source_1_bus_1_0) <= +inf
   0 <= InvestmentFlowBlock_total(source_2_bus_1_0) <= +inf
   0 <= InvestmentFlowBlock_total(source_0_bus_1_0) <= +inf
end
