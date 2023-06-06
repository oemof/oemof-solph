\* Source Pyomo model name=Model *\

min 
objective:
+123 InvestmentFlowBlock_invest(pv_electricityBus_0)
+13 flow(pv_electricityBus_0_0)
+13 flow(pv_electricityBus_0_1)
+13 flow(pv_electricityBus_0_2)

s.t.

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
= 50000.0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
= 80000.0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(pv_electricityBus_0_2)
= 30000.0

c_e_InvestmentFlowBlock_total_rule(pv_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(pv_electricityBus_0)
+1 InvestmentFlowBlock_total(pv_electricityBus_0)
= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_0)_:
+1 flow(pv_electricityBus_0_0)
-45 InvestmentFlowBlock_total(pv_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_1)_:
+1 flow(pv_electricityBus_0_1)
-83 InvestmentFlowBlock_total(pv_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(pv_electricityBus_0_2)_:
+1 flow(pv_electricityBus_0_2)
-65 InvestmentFlowBlock_total(pv_electricityBus_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(pv_electricityBus_0) <= +inf
   0 <= flow(pv_electricityBus_0_0) <= +inf
   0 <= flow(pv_electricityBus_0_1) <= +inf
   0 <= flow(pv_electricityBus_0_2) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricityBus_0) <= +inf
end
