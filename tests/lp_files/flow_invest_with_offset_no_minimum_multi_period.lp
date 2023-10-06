\* Source Pyomo model name=Model *\

min 
objective:
+88.1844182057801 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
+34 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
+58.20563481102971 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_1)
+33.33333333333333 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_1)
+28.814670698529593 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_2)
+32.6797385620915 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_2)
+25 flow(source_nonconvex_invest_electricityBus_0_0)
+25 flow(source_nonconvex_invest_electricityBus_0_1)
+24.509803921568626 flow(source_nonconvex_invest_electricityBus_1_2)
+24.509803921568626 flow(source_nonconvex_invest_electricityBus_1_3)
+24.029219530949632 flow(source_nonconvex_invest_electricityBus_2_4)
+24.029219530949632 flow(source_nonconvex_invest_electricityBus_2_5)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(source_nonconvex_invest_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(source_nonconvex_invest_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_1_2)_:
+1 flow(source_nonconvex_invest_electricityBus_1_2)
= 0

c_e_BusBlock_balance(electricityBus_1_3)_:
+1 flow(source_nonconvex_invest_electricityBus_1_3)
= 0

c_e_BusBlock_balance(electricityBus_2_4)_:
+1 flow(source_nonconvex_invest_electricityBus_2_4)
= 0

c_e_BusBlock_balance(electricityBus_2_5)_:
+1 flow(source_nonconvex_invest_electricityBus_2_5)
= 0

c_u_InvestmentFlowBlock_minimum_rule(source_nonconvex_invest_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(source_nonconvex_invest_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_minimum_rule(source_nonconvex_invest_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(source_nonconvex_invest_electricityBus_0)_:
+1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
-1234 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(source_nonconvex_invest_electricityBus_1)_:
+1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_1)
-1234 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_maximum_rule(source_nonconvex_invest_electricityBus_2)_:
+1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_2)
-1234 InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_2)
<= 0

c_e_InvestmentFlowBlock_total_rule(source_nonconvex_invest_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0)
+1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_total_rule(source_nonconvex_invest_electricityBus_1)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_1)
-1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
+1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1)
+1 InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_total_rule(source_nonconvex_invest_electricityBus_2)_:
-1 InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_2)
-1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1)
+1 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_2)
+1 InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(source_nonconvex_invest_electricityBus_0)_:
+1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(source_nonconvex_invest_electricityBus_1)_:
+1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(source_nonconvex_invest_electricityBus_2)_:
+1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(source_nonconvex_invest_electricityBus_0)_:
+1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(source_nonconvex_invest_electricityBus_1)_:
+1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(source_nonconvex_invest_electricityBus_2)_:
+1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_2)
= 0

c_e_InvestmentFlowBlock_old_rule(source_nonconvex_invest_electricityBus_0)_:
-1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_0)
-1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_0)
+1 InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_0)
= 0

c_e_InvestmentFlowBlock_old_rule(source_nonconvex_invest_electricityBus_1)_:
+1 InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_1)
-1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_1)
-1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_1)
= 0

c_e_InvestmentFlowBlock_old_rule(source_nonconvex_invest_electricityBus_2)_:
+1 InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_2)
-1 InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_2)
-1 InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_2)
= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_0_0)_:
+1 flow(source_nonconvex_invest_electricityBus_0_0)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_0_1)_:
+1 flow(source_nonconvex_invest_electricityBus_0_1)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_1_2)_:
+1 flow(source_nonconvex_invest_electricityBus_1_2)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_1_3)_:
+1 flow(source_nonconvex_invest_electricityBus_1_3)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_2_4)_:
+1 flow(source_nonconvex_invest_electricityBus_2_4)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_max(source_nonconvex_invest_electricityBus_2_5)_:
+1 flow(source_nonconvex_invest_electricityBus_2_5)
-0.8 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_2)
<= 0

c_u_InvestmentFlowBlock_full_load_time_max(source_nonconvex_invest_electricityBus)_:
+1 flow(source_nonconvex_invest_electricityBus_0_0)
+1 flow(source_nonconvex_invest_electricityBus_0_1)
+1 flow(source_nonconvex_invest_electricityBus_1_2)
+1 flow(source_nonconvex_invest_electricityBus_1_3)
+1 flow(source_nonconvex_invest_electricityBus_2_4)
+1 flow(source_nonconvex_invest_electricityBus_2_5)
-2.3 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0)
-2.3 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1)
-2.3 InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_2)
<= 0.0

bounds
   0 <= InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_0) <= 1234
   0 <= InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0) <= 1
   0 <= InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_1) <= 1234
   0 <= InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_1) <= 1
   0 <= InvestmentFlowBlock_invest(source_nonconvex_invest_electricityBus_2) <= 1234
   0 <= InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_2) <= 1
   0 <= flow(source_nonconvex_invest_electricityBus_0_0) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_0_1) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_1_2) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_1_3) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_2_4) <= +inf
   0 <= flow(source_nonconvex_invest_electricityBus_2_5) <= +inf
   0 <= InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_total(source_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(source_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(source_nonconvex_invest_electricityBus_2) <= +inf
   0 <= InvestmentFlowBlock_old(source_nonconvex_invest_electricityBus_0) <= +inf
binary
  InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_0)
  InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_1)
  InvestmentFlowBlock_invest_status(source_nonconvex_invest_electricityBus_2)
end
