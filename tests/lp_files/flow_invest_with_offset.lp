\* Source Pyomo model name=Model *\

min 
objective:
+500 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
+34 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
+25 flow(source_nonconvex_invest_electricityBus_0_0)
+25 flow(source_nonconvex_invest_electricityBus_0_1)
+25 flow(source_nonconvex_invest_electricityBus_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(source_nonconvex_invest_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(source_nonconvex_invest_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(source_nonconvex_invest_electricityBus_0_2)
= 0

c_u_InvestmentFlowBlock_minimum_rule(source_nonconvex_invest_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
+15 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(source_nonconvex_invest_electricityBus_0)_:
+1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
-20 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
<= 0

c_e_InvestmentFlowBlock_total_rule(source_nonconvex_invest_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
+1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_0_0)_:
-0.80000000000000004 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
+1 flow(source_nonconvex_invest_electricityBus_0_0)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_0_1)_:
-0.80000000000000004 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
+1 flow(source_nonconvex_invest_electricityBus_0_1)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_0_2)_:
-0.80000000000000004 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
+1 flow(source_nonconvex_invest_electricityBus_0_2)
<= 0

c_u_InvestmentFlowBlock_full_load_time_max(source_nonconvex_invest_electricityBus)_:
-2.2999999999999998 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
+1 flow(source_nonconvex_invest_electricityBus_0_0)
+1 flow(source_nonconvex_invest_electricityBus_0_1)
+1 flow(source_nonconvex_invest_electricityBus_0_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(source_nonconvex_invest_electricityBus_0_0) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_0_1) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_0_2) <= +inf
   0 <= InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0) <= 20
   0 <= InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0) <= 1
binary
  InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
end
