\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(commodityBus_0_0)_:
+1 flow(commodityBus_variable_chp_gas1_0_0)
+1 flow(commodityBus_variable_chp_gas2_0_0)
= 0

c_e_BusBlock_balance(commodityBus_0_1)_:
+1 flow(commodityBus_variable_chp_gas1_0_1)
+1 flow(commodityBus_variable_chp_gas2_0_1)
= 0

c_e_BusBlock_balance(commodityBus_0_2)_:
+1 flow(commodityBus_variable_chp_gas1_0_2)
+1 flow(commodityBus_variable_chp_gas2_0_2)
= 0

c_e_BusBlock_balance(electricityBus_0_0)_:
+1 flow(variable_chp_gas1_electricityBus_0_0)
+1 flow(variable_chp_gas2_electricityBus_0_0)
= 0

c_e_BusBlock_balance(electricityBus_0_1)_:
+1 flow(variable_chp_gas1_electricityBus_0_1)
+1 flow(variable_chp_gas2_electricityBus_0_1)
= 0

c_e_BusBlock_balance(electricityBus_0_2)_:
+1 flow(variable_chp_gas1_electricityBus_0_2)
+1 flow(variable_chp_gas2_electricityBus_0_2)
= 0

c_e_BusBlock_balance(heatBus_0_0)_:
+1 flow(variable_chp_gas1_heatBus_0_0)
+1 flow(variable_chp_gas2_heatBus_0_0)
= 0

c_e_BusBlock_balance(heatBus_0_1)_:
+1 flow(variable_chp_gas1_heatBus_0_1)
+1 flow(variable_chp_gas2_heatBus_0_1)
= 0

c_e_BusBlock_balance(heatBus_0_2)_:
+1 flow(variable_chp_gas1_heatBus_0_2)
+1 flow(variable_chp_gas2_heatBus_0_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_0_0)_:
+1 flow(commodityBus_variable_chp_gas1_0_0)
-2 flow(variable_chp_gas1_electricityBus_0_0)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_0_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_0_1)_:
+1 flow(commodityBus_variable_chp_gas1_0_1)
-2 flow(variable_chp_gas1_electricityBus_0_1)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_0_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_0_2)_:
+1 flow(commodityBus_variable_chp_gas1_0_2)
-2 flow(variable_chp_gas1_electricityBus_0_2)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_0_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_0_0)_:
+1 flow(commodityBus_variable_chp_gas2_0_0)
-2 flow(variable_chp_gas2_electricityBus_0_0)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_0_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_0_1)_:
+1 flow(commodityBus_variable_chp_gas2_0_1)
-2 flow(variable_chp_gas2_electricityBus_0_1)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_0_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_0_2)_:
+1 flow(commodityBus_variable_chp_gas2_0_2)
-2 flow(variable_chp_gas2_electricityBus_0_2)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_0_2)
= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_0_0)_:
-1 flow(variable_chp_gas1_electricityBus_0_0)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_0_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_0_1)_:
-1 flow(variable_chp_gas1_electricityBus_0_1)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_0_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_0_2)_:
-1 flow(variable_chp_gas1_electricityBus_0_2)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_0_2)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_0_0)_:
-1 flow(variable_chp_gas2_electricityBus_0_0)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_0_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_0_1)_:
-1 flow(variable_chp_gas2_electricityBus_0_1)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_0_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_0_2)_:
-1 flow(variable_chp_gas2_electricityBus_0_2)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_0_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(commodityBus_variable_chp_gas1_0_0) <= 100
   0 <= flow(commodityBus_variable_chp_gas1_0_1) <= 100
   0 <= flow(commodityBus_variable_chp_gas1_0_2) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_0_0) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_0_1) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_0_2) <= 100
   0 <= flow(variable_chp_gas1_electricityBus_0_0) <= +inf
   0 <= flow(variable_chp_gas1_electricityBus_0_1) <= +inf
   0 <= flow(variable_chp_gas1_electricityBus_0_2) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_0_0) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_0_1) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_0_2) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_0_0) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_0_1) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_0_2) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_0_0) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_0_1) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_0_2) <= +inf
end
