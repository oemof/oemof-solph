\* Source Pyomo model name=OperationalModel *\

min 
objective:
+500 InvestmentFlow_invest(electricityBus_investDemand)

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_investDemand_0)
-1 flow(electricityBus_minDemand_0)
+1 flow(wind_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_investDemand_1)
-1 flow(electricityBus_minDemand_1)
+1 flow(wind_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_investDemand_2)
-1 flow(electricityBus_minDemand_2)
+1 flow(wind_electricityBus_2)
= 0

c_u_InvestmentFlow_max(electricityBus_investDemand_0)_:
-1 InvestmentFlow_invest(electricityBus_investDemand)
+1 flow(electricityBus_investDemand_0)
<= 0

c_u_InvestmentFlow_max(electricityBus_investDemand_1)_:
-1 InvestmentFlow_invest(electricityBus_investDemand)
+1 flow(electricityBus_investDemand_1)
<= 0

c_u_InvestmentFlow_max(electricityBus_investDemand_2)_:
-1 InvestmentFlow_invest(electricityBus_investDemand)
+1 flow(electricityBus_investDemand_2)
<= 0

c_u_InvestmentFlow_min(electricityBus_investDemand_0)_:
+0.83999999999999997 InvestmentFlow_invest(electricityBus_investDemand)
-1 flow(electricityBus_investDemand_0)
<= 0

c_u_InvestmentFlow_min(electricityBus_investDemand_1)_:
+0.93999999999999995 InvestmentFlow_invest(electricityBus_investDemand)
-1 flow(electricityBus_investDemand_1)
<= 0

c_u_InvestmentFlow_min(electricityBus_investDemand_2)_:
+0.58999999999999997 InvestmentFlow_invest(electricityBus_investDemand)
-1 flow(electricityBus_investDemand_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_investDemand_0) <= +inf
   0 <= flow(electricityBus_investDemand_1) <= +inf
   0 <= flow(electricityBus_investDemand_2) <= +inf
   25.199999999999999 <= flow(electricityBus_minDemand_0) <= 30
   28.199999999999999 <= flow(electricityBus_minDemand_1) <= 30
   17.699999999999999 <= flow(electricityBus_minDemand_2) <= 30
   0 <= flow(wind_electricityBus_0) <= 45.899999999999999
   0 <= flow(wind_electricityBus_1) <= 51.299999999999997
   0 <= flow(wind_electricityBus_2) <= 32.939999999999998
   0 <= InvestmentFlow_invest(electricityBus_investDemand) <= +inf
end
