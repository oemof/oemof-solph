\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(commodityBus_0)_:
+1 flow(commodityBus_variable_chp_gas1_0)
+1 flow(commodityBus_variable_chp_gas2_0)
= 0

c_e_Bus_balance(commodityBus_1)_:
+1 flow(commodityBus_variable_chp_gas1_1)
+1 flow(commodityBus_variable_chp_gas2_1)
= 0

c_e_Bus_balance(commodityBus_2)_:
+1 flow(commodityBus_variable_chp_gas1_2)
+1 flow(commodityBus_variable_chp_gas2_2)
= 0

c_e_Bus_balance(electricityBus_0)_:
+1 flow(variable_chp_gas1_electricityBus_0)
+1 flow(variable_chp_gas2_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(variable_chp_gas1_electricityBus_1)
+1 flow(variable_chp_gas2_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(variable_chp_gas1_electricityBus_2)
+1 flow(variable_chp_gas2_electricityBus_2)
= 0

c_e_Bus_balance(heatBus_0)_:
+1 flow(variable_chp_gas1_heatBus_0)
+1 flow(variable_chp_gas2_heatBus_0)
= 0

c_e_Bus_balance(heatBus_1)_:
+1 flow(variable_chp_gas1_heatBus_1)
+1 flow(variable_chp_gas2_heatBus_1)
= 0

c_e_Bus_balance(heatBus_2)_:
+1 flow(variable_chp_gas1_heatBus_2)
+1 flow(variable_chp_gas2_heatBus_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_0)_:
+1 flow(commodityBus_variable_chp_gas1_0)
-2 flow(variable_chp_gas1_electricityBus_0)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_1)_:
+1 flow(commodityBus_variable_chp_gas1_1)
-2 flow(variable_chp_gas1_electricityBus_1)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas1_2)_:
+1 flow(commodityBus_variable_chp_gas1_2)
-2 flow(variable_chp_gas1_electricityBus_2)
-0.80000000000000004 flow(variable_chp_gas1_heatBus_2)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_0)_:
+1 flow(commodityBus_variable_chp_gas2_0)
-2 flow(variable_chp_gas2_electricityBus_0)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_0)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_1)_:
+1 flow(commodityBus_variable_chp_gas2_1)
-2 flow(variable_chp_gas2_electricityBus_1)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_1)
= 0

c_e_ExtractionTurbineCHPBlock_input_output_relation(variable_chp_gas2_2)_:
+1 flow(commodityBus_variable_chp_gas2_2)
-2 flow(variable_chp_gas2_electricityBus_2)
-0.80000000000000004 flow(variable_chp_gas2_heatBus_2)
= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_0)_:
-1 flow(variable_chp_gas1_electricityBus_0)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_1)_:
-1 flow(variable_chp_gas1_electricityBus_1)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas1_2)_:
-1 flow(variable_chp_gas1_electricityBus_2)
+0.59999999999999998 flow(variable_chp_gas1_heatBus_2)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_0)_:
-1 flow(variable_chp_gas2_electricityBus_0)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_0)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_1)_:
-1 flow(variable_chp_gas2_electricityBus_1)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_1)
<= 0

c_u_ExtractionTurbineCHPBlock_out_flow_relation(variable_chp_gas2_2)_:
-1 flow(variable_chp_gas2_electricityBus_2)
+0.59999999999999998 flow(variable_chp_gas2_heatBus_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(commodityBus_variable_chp_gas1_0) <= 100
   0 <= flow(commodityBus_variable_chp_gas1_1) <= 100
   0 <= flow(commodityBus_variable_chp_gas1_2) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_0) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_1) <= 100
   0 <= flow(commodityBus_variable_chp_gas2_2) <= 100
   0 <= flow(variable_chp_gas1_electricityBus_0) <= +inf
   0 <= flow(variable_chp_gas1_electricityBus_1) <= +inf
   0 <= flow(variable_chp_gas1_electricityBus_2) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_0) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_1) <= +inf
   0 <= flow(variable_chp_gas1_heatBus_2) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_0) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_1) <= +inf
   0 <= flow(variable_chp_gas2_electricityBus_2) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_0) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_1) <= +inf
   0 <= flow(variable_chp_gas2_heatBus_2) <= +inf
end
