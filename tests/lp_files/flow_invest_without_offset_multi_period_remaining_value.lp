\* Source Pyomo model name=Model *\

min 
objective:
+88.1844182057801 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+58.20563481102971 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_1)
+28.814670698529593 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_2)
+25 flow(electricityBus_sink_nonconvex_invest_0_0)
+25 flow(electricityBus_sink_nonconvex_invest_0_1)
+24.509803921568626 flow(electricityBus_sink_nonconvex_invest_1_2)
+24.509803921568626 flow(electricityBus_sink_nonconvex_invest_1_3)
+24.029219530949632 flow(electricityBus_sink_nonconvex_invest_2_4)
+24.029219530949632 flow(electricityBus_sink_nonconvex_invest_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
= 0

c_u_InvestmentFlowBlock_minimum_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+15 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(electricityBus_sink_nonconvex_invest_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_1)
+15 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(electricityBus_sink_nonconvex_invest_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_2)
+15 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_2)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_sink_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
-172 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_sink_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_1)
-172 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(electricityBus_sink_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_2)
-172 InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_2)
<= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0)
+1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_sink_nonconvex_invest_1)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_1)
-1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
+1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1)
+1 InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricityBus_sink_nonconvex_invest_2)_:
-1 InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_2)
-1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1)
+1 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_2)
+1 InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_sink_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_sink_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricityBus_sink_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_sink_nonconvex_invest_0)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_sink_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricityBus_sink_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_0)
-1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_0)
+1 InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_sink_nonconvex_invest_1)_:
+1 InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_1)
-1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_1)
-1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricityBus_sink_nonconvex_invest_2)_:
+1 InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_2)
-1 InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_2)
-1 InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_2)
= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_0_0)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_0_1)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_1_2)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_1_3)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_2_4)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_2)
<= 0

c_u_InvestmentFlowBlock_max(electricityBus_sink_nonconvex_invest_2_5)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
-0.8 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_2)
<= 0

c_u_InvestmentFlowBlock_full_load_time_max(electricityBus_sink_nonconvex_invest)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
-2.3 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0)
-2.3 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1)
-2.3 InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_2)
<= 0.0

bounds
   0 <= InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_0) <= 172
   0 <= InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_1) <= 172
   0 <= InvestmentFlowBlock_invest(electricityBus_sink_nonconvex_invest_2) <= 172
   0 <= flow(electricityBus_sink_nonconvex_invest_0_0) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_0_1) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_1_2) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_1_3) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_2_4) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_2_5) <= +inf
   0 <= InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0) <= 1
   0 <= InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_1) <= 1
   0 <= InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_2) <= 1
   0 <= InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricityBus_sink_nonconvex_invest_0) <= +inf
binary
  InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_0)
  InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_1)
  InvestmentFlowBlock_invest_status(electricityBus_sink_nonconvex_invest_2)
end
