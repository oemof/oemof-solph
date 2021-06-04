\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+611.56718125290342 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_0)
+599.57566789500333 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_1)
+587.8192822500032 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_2)
+25 flow(electricityBus_sink_nonconvex_invest_0_0)
+25 flow(electricityBus_sink_nonconvex_invest_0_1)
+24.509803921568626 flow(electricityBus_sink_nonconvex_invest_1_2)
+24.509803921568626 flow(electricityBus_sink_nonconvex_invest_1_3)
+24.029219530949632 flow(electricityBus_sink_nonconvex_invest_2_4)
+24.029219530949632 flow(electricityBus_sink_nonconvex_invest_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_0)
+15 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(electricityBus_sink_nonconvex_invest_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_1)
+15 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_MultiPeriodInvestmentFlow_minimum_rule(electricityBus_sink_nonconvex_invest_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_2)
+15 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_2)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(electricityBus_sink_nonconvex_invest_0)_:
+1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_0)
-172 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_0)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(electricityBus_sink_nonconvex_invest_1)_:
+1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_1)
-172 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_1)
<= 0

c_u_MultiPeriodInvestmentFlow_maximum_rule(electricityBus_sink_nonconvex_invest_2)_:
+1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_2)
-172 MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_2)
<= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_sink_nonconvex_invest_0)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_sink_nonconvex_invest_1)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_1)
+1 MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_1)
-1 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0)
+1 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_MultiPeriodInvestmentFlow_total_rule(electricityBus_sink_nonconvex_invest_2)_:
-1 MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_2)
+1 MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_2)
-1 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1)
+1 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_sink_nonconvex_invest_0)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_sink_nonconvex_invest_1)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_end(electricityBus_sink_nonconvex_invest_2)_:
+1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_sink_nonconvex_invest_0)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_sink_nonconvex_invest_1)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule_exo(electricityBus_sink_nonconvex_invest_2)_:
+1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_2)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_sink_nonconvex_invest_0)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_0)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_0)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_0)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_sink_nonconvex_invest_1)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_1)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_1)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_1)
= 0

c_e_MultiPeriodInvestmentFlow_old_rule(electricityBus_sink_nonconvex_invest_2)_:
+1 MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_2)
-1 MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_2)
-1 MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_2)
= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_0_0)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0)
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_0_1)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0)
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_1_2)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1)
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_1_3)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1)
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_2_4)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_2)
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
<= 0

c_u_MultiPeriodInvestmentFlow_max(electricityBus_sink_nonconvex_invest_2_5)_:
-0.80000000000000004 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_2)
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
<= 0

c_u_MultiPeriodInvestmentFlow_summed_max(electricityBus_sink_nonconvex_invest)_:
-2.2999999999999998 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0)
-2.2999999999999998 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1)
-2.2999999999999998 MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_2)
+1 flow(electricityBus_sink_nonconvex_invest_0_0)
+1 flow(electricityBus_sink_nonconvex_invest_0_1)
+1 flow(electricityBus_sink_nonconvex_invest_1_2)
+1 flow(electricityBus_sink_nonconvex_invest_1_3)
+1 flow(electricityBus_sink_nonconvex_invest_2_4)
+1 flow(electricityBus_sink_nonconvex_invest_2_5)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_sink_nonconvex_invest_0_0) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_0_1) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_1_2) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_1_3) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_2_4) <= +inf
   0 <= flow(electricityBus_sink_nonconvex_invest_2_5) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_0) <= 172
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_1) <= 172
   0 <= MultiPeriodInvestmentFlow_invest(electricityBus_sink_nonconvex_invest_2) <= 172
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_total(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_end(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_0) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_1) <= +inf
   0 <= MultiPeriodInvestmentFlow_old_exo(electricityBus_sink_nonconvex_invest_2) <= +inf
   0 <= MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_0) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_1) <= 1
   0 <= MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_2) <= 1
binary
  MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_0)
  MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_1)
  MultiPeriodInvestmentFlow_invest_status(electricityBus_sink_nonconvex_invest_2)
end
