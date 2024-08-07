\* Source Pyomo model name=Model *\

min 
objective:
+20 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0)
+50 flow(powerplant_gas_coal_electricityBus_0)
+50 flow(powerplant_gas_coal_electricityBus_1)
+50 flow(powerplant_gas_coal_electricityBus_2)
+20 flow(powerplant_gas_coal_thermalBus_0)
+20 flow(powerplant_gas_coal_thermalBus_1)
+20 flow(powerplant_gas_coal_thermalBus_2)

s.t.

c_e_BusBlock_balance(coalBus_0)_:
+1 flow(coalBus_powerplant_gas_coal_0)
= 0

c_e_BusBlock_balance(coalBus_1)_:
+1 flow(coalBus_powerplant_gas_coal_1)
= 0

c_e_BusBlock_balance(coalBus_2)_:
+1 flow(coalBus_powerplant_gas_coal_2)
= 0

c_e_BusBlock_balance(electricityBus_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
+1 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
+1 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_powerplant_gas_coal_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_powerplant_gas_coal_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_powerplant_gas_coal_2)
= 0

c_e_BusBlock_balance(thermalBus_0)_:
+1 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_BusBlock_balance(thermalBus_1)_:
+1 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_BusBlock_balance(thermalBus_2)_:
+1 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_0)_:
+0.3 flow(coalBus_powerplant_gas_coal_0)
-0.2 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_0)_:
+0.3 flow(gasBus_powerplant_gas_coal_0)
-0.58 flow(powerplant_gas_coal_electricityBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_0)_:
+0.5 flow(coalBus_powerplant_gas_coal_0)
-0.2 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_0)_:
+0.5 flow(gasBus_powerplant_gas_coal_0)
-0.58 flow(powerplant_gas_coal_thermalBus_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_1)_:
+0.3 flow(coalBus_powerplant_gas_coal_1)
-0.2 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_1)_:
+0.3 flow(gasBus_powerplant_gas_coal_1)
-0.58 flow(powerplant_gas_coal_electricityBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_1)_:
+0.5 flow(coalBus_powerplant_gas_coal_1)
-0.2 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_1)_:
+0.5 flow(gasBus_powerplant_gas_coal_1)
-0.58 flow(powerplant_gas_coal_thermalBus_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_electricityBus_2)_:
+0.3 flow(coalBus_powerplant_gas_coal_2)
-0.2 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_electricityBus_2)_:
+0.3 flow(gasBus_powerplant_gas_coal_2)
-0.58 flow(powerplant_gas_coal_electricityBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_coalBus_thermalBus_2)_:
+0.5 flow(coalBus_powerplant_gas_coal_2)
-0.2 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_ConverterBlock_relation(powerplant_gas_coal_gasBus_thermalBus_2)_:
+0.5 flow(gasBus_powerplant_gas_coal_2)
-0.58 flow(powerplant_gas_coal_thermalBus_2)
= 0

c_e_InvestmentFlowBlock_total_rule(powerplant_gas_coal_electricityBus_0)_:
-1 InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0)
+1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
= 200

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_0_0)_:
+1 flow(powerplant_gas_coal_electricityBus_0)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_0_1)_:
+1 flow(powerplant_gas_coal_electricityBus_1)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
<= 0

c_u_InvestmentFlowBlock_max(powerplant_gas_coal_electricityBus_0_2)_:
+1 flow(powerplant_gas_coal_electricityBus_2)
-1 InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(powerplant_gas_coal_electricityBus_0) <= 1000
   0 <= flow(gasBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(gasBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_0) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_1) <= +inf
   0 <= flow(coalBus_powerplant_gas_coal_2) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_0) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_1) <= +inf
   0 <= flow(powerplant_gas_coal_electricityBus_2) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_0) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_1) <= +inf
   0 <= flow(powerplant_gas_coal_thermalBus_2) <= +inf
   0 <= InvestmentFlowBlock_total(powerplant_gas_coal_electricityBus_0) <= +inf
end
