\* Source Pyomo model name=Model *\

min 
objective:
+500 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+25 flow(electricityBus_sink_nonconvex_invest_0_0)
+25 flow(electricityBus_sink_nonconvex_invest_0_1)
+25 flow(electricityBus_sink_nonconvex_invest_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_2)
= 0

c_u_InvestmentFlowBlock_minimum_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+15 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_sink_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
-172 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_0_0)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_0_1)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_0_2)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_2)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_full_load_time_max(electricityBus_sink_nonconvex_invest)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
+1 flow(electricityBus_sink_nonconvex_invest_0_2)
-2.3 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0) <= 172
   0 <= flow(electricityBus_sink_nonconvex_invest_0_0) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_0_1) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_0_2) <= +inf
   0 <= InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0) <= 1
   0 <= InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0) <= +inf
binary
  InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
end
