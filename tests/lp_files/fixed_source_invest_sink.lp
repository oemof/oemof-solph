\* Source Pyomo model name=Model *\

min 
objective:
+500 InvestmentFlow_invest(electricityBus_excess)
+25 flow(electricityBus_excess_0)
+25 flow(electricityBus_excess_1)
+25 flow(electricityBus_excess_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_excess_0)
= -12000000

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_excess_1)
= -16000000

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_excess_2)
= -14000000

c_u_InvestmentFlow_max(electricityBus_excess_0)_:
-0.80000000000000004 InvestmentFlow_invest(electricityBus_excess)
+1 flow(electricityBus_excess_0)
<= 40

c_u_InvestmentFlow_max(electricityBus_excess_1)_:
-0.80000000000000004 InvestmentFlow_invest(electricityBus_excess)
+1 flow(electricityBus_excess_1)
<= 40

c_u_InvestmentFlow_max(electricityBus_excess_2)_:
-0.80000000000000004 InvestmentFlow_invest(electricityBus_excess)
+1 flow(electricityBus_excess_2)
<= 40

c_u_InvestmentFlow_summed_max(electricityBus_excess)_:
-2.2999999999999998 InvestmentFlow_invest(electricityBus_excess)
+1 flow(electricityBus_excess_0)
+1 flow(electricityBus_excess_1)
+1 flow(electricityBus_excess_2)
<= 114.99999999999999

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_excess_0) <= +inf
   0 <= flow(electricityBus_excess_1) <= +inf
   0 <= flow(electricityBus_excess_2) <= +inf
   0 <= InvestmentFlow_invest(electricityBus_excess) <= 1000000
end
