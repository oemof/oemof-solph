\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlow_invest(pv_electricityBus)
+13 flow(pv_electricityBus_0)
+13 flow(pv_electricityBus_1)
+13 flow(pv_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
+1 flow(pv_electricityBus_0)
= 50000

c_e_Bus_balance(electricityBus_1)_:
+1 flow(pv_electricityBus_1)
= 80000

c_e_Bus_balance(electricityBus_2)_:
+1 flow(pv_electricityBus_2)
= 30000

c_u_InvestmentFlow_max(pv_electricityBus_0)_:
-45 InvestmentFlow_invest(pv_electricityBus)
+1 flow(pv_electricityBus_0)
<= 0

c_u_InvestmentFlow_max(pv_electricityBus_1)_:
-83 InvestmentFlow_invest(pv_electricityBus)
+1 flow(pv_electricityBus_1)
<= 0

c_u_InvestmentFlow_max(pv_electricityBus_2)_:
-65 InvestmentFlow_invest(pv_electricityBus)
+1 flow(pv_electricityBus_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(pv_electricityBus_0) <= +inf
   0 <= flow(pv_electricityBus_1) <= +inf
   0 <= flow(pv_electricityBus_2) <= +inf
   0 <= InvestmentFlow_invest(pv_electricityBus) <= +inf
end
