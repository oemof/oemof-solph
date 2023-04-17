\* Source Pyomo model name=CellularModel *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_equate_CellConnector_flows(cc_ec1_ec2_cc_ec2_ec1_0_0)_:
-1 flow(bus_el_2_cc_ec2_ec1_0)
+1 flow(cc_ec1_ec2_bus_el_1_0)
= 0

c_e_equate_CellConnector_flows(cc_ec1_ec2_cc_ec2_ec1_0_1)_:
-1 flow(bus_el_2_cc_ec2_ec1_1)
+1 flow(cc_ec1_ec2_bus_el_1_1)
= 0

c_e_equate_CellConnector_flows(cc_ec1_ec2_cc_ec2_ec1_0_2)_:
-1 flow(bus_el_2_cc_ec2_ec1_2)
+1 flow(cc_ec1_ec2_bus_el_1_2)
= 0

c_e_equate_CellConnector_flows(cc_ec1_ec3_cc_ec3_ec1_0_0)_:
-1 flow(bus_el_3_cc_ec3_ec1_0)
+1 flow(cc_ec1_ec3_bus_el_1_0)
= 0

c_e_equate_CellConnector_flows(cc_ec1_ec3_cc_ec3_ec1_0_1)_:
-1 flow(bus_el_3_cc_ec3_ec1_1)
+1 flow(cc_ec1_ec3_bus_el_1_1)
= 0

c_e_equate_CellConnector_flows(cc_ec1_ec3_cc_ec3_ec1_0_2)_:
-1 flow(bus_el_3_cc_ec3_ec1_2)
+1 flow(cc_ec1_ec3_bus_el_1_2)
= 0

c_e_equate_CellConnector_flows(cc_ec1_es_cc_es_ec1_0_0)_:
-1 flow(bus_el_cc_es_ec1_0)
+1 flow(cc_ec1_es_bus_el_1_0)
= 0

c_e_equate_CellConnector_flows(cc_ec1_es_cc_es_ec1_0_1)_:
-1 flow(bus_el_cc_es_ec1_1)
+1 flow(cc_ec1_es_bus_el_1_1)
= 0

c_e_equate_CellConnector_flows(cc_ec1_es_cc_es_ec1_0_2)_:
-1 flow(bus_el_cc_es_ec1_2)
+1 flow(cc_ec1_es_bus_el_1_2)
= 0

c_e_equate_CellConnector_flows(cc_ec2_ec1_cc_ec1_ec2_0_0)_:
-1 flow(bus_el_1_cc_ec1_ec2_0)
+1 flow(cc_ec2_ec1_bus_el_2_0)
= 0

c_e_equate_CellConnector_flows(cc_ec2_ec1_cc_ec1_ec2_0_1)_:
-1 flow(bus_el_1_cc_ec1_ec2_1)
+1 flow(cc_ec2_ec1_bus_el_2_1)
= 0

c_e_equate_CellConnector_flows(cc_ec2_ec1_cc_ec1_ec2_0_2)_:
-1 flow(bus_el_1_cc_ec1_ec2_2)
+1 flow(cc_ec2_ec1_bus_el_2_2)
= 0

c_e_equate_CellConnector_flows(cc_ec3_ec1_cc_ec1_ec3_0_0)_:
-1 flow(bus_el_1_cc_ec1_ec3_0)
+1 flow(cc_ec3_ec1_bus_el_3_0)
= 0

c_e_equate_CellConnector_flows(cc_ec3_ec1_cc_ec1_ec3_0_1)_:
-1 flow(bus_el_1_cc_ec1_ec3_1)
+1 flow(cc_ec3_ec1_bus_el_3_1)
= 0

c_e_equate_CellConnector_flows(cc_ec3_ec1_cc_ec1_ec3_0_2)_:
-1 flow(bus_el_1_cc_ec1_ec3_2)
+1 flow(cc_ec3_ec1_bus_el_3_2)
= 0

c_e_equate_CellConnector_flows(cc_es_ec1_cc_ec1_es_0_0)_:
-1 flow(bus_el_1_cc_ec1_es_0)
+1 flow(cc_es_ec1_bus_el_0)
= 0

c_e_equate_CellConnector_flows(cc_es_ec1_cc_ec1_es_0_1)_:
-1 flow(bus_el_1_cc_ec1_es_1)
+1 flow(cc_es_ec1_bus_el_1)
= 0

c_e_equate_CellConnector_flows(cc_es_ec1_cc_ec1_es_0_2)_:
-1 flow(bus_el_1_cc_ec1_es_2)
+1 flow(cc_es_ec1_bus_el_2)
= 0

c_e_BusBlock_balance(bus_el_0)_:
-1 flow(bus_el_cc_es_ec1_0)
+1 flow(cc_es_ec1_bus_el_0)
= 0

c_e_BusBlock_balance(bus_el_1)_:
-1 flow(bus_el_cc_es_ec1_1)
+1 flow(cc_es_ec1_bus_el_1)
= 0

c_e_BusBlock_balance(bus_el_2)_:
-1 flow(bus_el_cc_es_ec1_2)
+1 flow(cc_es_ec1_bus_el_2)
= 0

c_e_BusBlock_balance(bus_el_1_0)_:
-1 flow(bus_el_1_cc_ec1_ec2_0)
-1 flow(bus_el_1_cc_ec1_ec3_0)
-1 flow(bus_el_1_cc_ec1_es_0)
+1 flow(cc_ec1_ec2_bus_el_1_0)
+1 flow(cc_ec1_ec3_bus_el_1_0)
+1 flow(cc_ec1_es_bus_el_1_0)
+1 flow(pv_source_1_bus_el_1_0)
= 10

c_e_BusBlock_balance(bus_el_1_1)_:
-1 flow(bus_el_1_cc_ec1_ec2_1)
-1 flow(bus_el_1_cc_ec1_ec3_1)
-1 flow(bus_el_1_cc_ec1_es_1)
+1 flow(cc_ec1_ec2_bus_el_1_1)
+1 flow(cc_ec1_ec3_bus_el_1_1)
+1 flow(cc_ec1_es_bus_el_1_1)
+1 flow(pv_source_1_bus_el_1_1)
= 10

c_e_BusBlock_balance(bus_el_1_2)_:
-1 flow(bus_el_1_cc_ec1_ec2_2)
-1 flow(bus_el_1_cc_ec1_ec3_2)
-1 flow(bus_el_1_cc_ec1_es_2)
+1 flow(cc_ec1_ec2_bus_el_1_2)
+1 flow(cc_ec1_ec3_bus_el_1_2)
+1 flow(cc_ec1_es_bus_el_1_2)
+1 flow(pv_source_1_bus_el_1_2)
= 10

c_e_BusBlock_balance(bus_el_2_0)_:
-1 flow(bus_el_2_cc_ec2_ec1_0)
+1 flow(cc_ec2_ec1_bus_el_2_0)
+1 flow(pv_source_2_bus_el_2_0)
= 10

c_e_BusBlock_balance(bus_el_2_1)_:
-1 flow(bus_el_2_cc_ec2_ec1_1)
+1 flow(cc_ec2_ec1_bus_el_2_1)
+1 flow(pv_source_2_bus_el_2_1)
= 10

c_e_BusBlock_balance(bus_el_2_2)_:
-1 flow(bus_el_2_cc_ec2_ec1_2)
+1 flow(cc_ec2_ec1_bus_el_2_2)
+1 flow(pv_source_2_bus_el_2_2)
= 10

c_e_BusBlock_balance(bus_el_3_0)_:
-1 flow(bus_el_3_cc_ec3_ec1_0)
+1 flow(cc_ec3_ec1_bus_el_3_0)
+1 flow(pv_source_3_bus_el_3_0)
= 80

c_e_BusBlock_balance(bus_el_3_1)_:
-1 flow(bus_el_3_cc_ec3_ec1_1)
+1 flow(cc_ec3_ec1_bus_el_3_1)
+1 flow(pv_source_3_bus_el_3_1)
= 80

c_e_BusBlock_balance(bus_el_3_2)_:
-1 flow(bus_el_3_cc_ec3_ec1_2)
+1 flow(cc_ec3_ec1_bus_el_3_2)
+1 flow(pv_source_3_bus_el_3_2)
= 80

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec2_0)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_0)
-1 flow(cc_ec1_ec2_bus_el_1_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec2_1)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_1)
-1 flow(cc_ec1_ec2_bus_el_1_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec2_2)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_2)
-1 flow(cc_ec1_ec2_bus_el_1_2)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec3_0)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_0)
-1 flow(cc_ec1_ec3_bus_el_1_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec3_1)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_1)
-1 flow(cc_ec1_ec3_bus_el_1_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_ec3_2)_:
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_2)
-1 flow(cc_ec1_ec3_bus_el_1_2)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_es_0)_:
+1 CellConnectorBlock_input_flow(cc_ec1_es_0)
-1 flow(cc_ec1_es_bus_el_1_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_es_1)_:
+1 CellConnectorBlock_input_flow(cc_ec1_es_1)
-1 flow(cc_ec1_es_bus_el_1_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec1_es_2)_:
+1 CellConnectorBlock_input_flow(cc_ec1_es_2)
-1 flow(cc_ec1_es_bus_el_1_2)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec2_ec1_0)_:
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_0)
-1 flow(cc_ec2_ec1_bus_el_2_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec2_ec1_1)_:
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_1)
-1 flow(cc_ec2_ec1_bus_el_2_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec2_ec1_2)_:
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_2)
-1 flow(cc_ec2_ec1_bus_el_2_2)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec3_ec1_0)_:
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_0)
-1 flow(cc_ec3_ec1_bus_el_3_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec3_ec1_1)_:
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_1)
-1 flow(cc_ec3_ec1_bus_el_3_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_ec3_ec1_2)_:
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_2)
-1 flow(cc_ec3_ec1_bus_el_3_2)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_es_ec1_0)_:
+1 CellConnectorBlock_input_flow(cc_es_ec1_0)
-1 flow(cc_es_ec1_bus_el_0)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_es_ec1_1)_:
+1 CellConnectorBlock_input_flow(cc_es_ec1_1)
-1 flow(cc_es_ec1_bus_el_1)
= 0

c_e_CellConnectorBlock_input_flow_rule(cc_es_ec1_2)_:
+1 CellConnectorBlock_input_flow(cc_es_ec1_2)
-1 flow(cc_es_ec1_bus_el_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec2_0)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_0)
-1 flow(bus_el_1_cc_ec1_ec2_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec2_1)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_1)
-1 flow(bus_el_1_cc_ec1_ec2_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec2_2)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_2)
-1 flow(bus_el_1_cc_ec1_ec2_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec3_0)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_0)
-1 flow(bus_el_1_cc_ec1_ec3_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec3_1)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_1)
-1 flow(bus_el_1_cc_ec1_ec3_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_ec3_2)_:
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_2)
-1 flow(bus_el_1_cc_ec1_ec3_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_es_0)_:
+1 CellConnectorBlock_output_flow(cc_ec1_es_0)
-1 flow(bus_el_1_cc_ec1_es_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_es_1)_:
+1 CellConnectorBlock_output_flow(cc_ec1_es_1)
-1 flow(bus_el_1_cc_ec1_es_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec1_es_2)_:
+1 CellConnectorBlock_output_flow(cc_ec1_es_2)
-1 flow(bus_el_1_cc_ec1_es_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec2_ec1_0)_:
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_0)
-1 flow(bus_el_2_cc_ec2_ec1_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec2_ec1_1)_:
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_1)
-1 flow(bus_el_2_cc_ec2_ec1_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec2_ec1_2)_:
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_2)
-1 flow(bus_el_2_cc_ec2_ec1_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec3_ec1_0)_:
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_0)
-1 flow(bus_el_3_cc_ec3_ec1_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec3_ec1_1)_:
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_1)
-1 flow(bus_el_3_cc_ec3_ec1_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_ec3_ec1_2)_:
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_2)
-1 flow(bus_el_3_cc_ec3_ec1_2)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_es_ec1_0)_:
+1 CellConnectorBlock_output_flow(cc_es_ec1_0)
-1 flow(bus_el_cc_es_ec1_0)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_es_ec1_1)_:
+1 CellConnectorBlock_output_flow(cc_es_ec1_1)
-1 flow(bus_el_cc_es_ec1_1)
= 0

c_e_CellConnectorBlock_output_flow_rule(cc_es_ec1_2)_:
+1 CellConnectorBlock_output_flow(cc_es_ec1_2)
-1 flow(bus_el_cc_es_ec1_2)
= 0

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec2_0)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_0)
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec2_1)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_1)
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec2_2)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_2)
+1 CellConnectorBlock_input_flow(cc_ec1_ec2_2)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec3_0)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_0)
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec3_1)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_1)
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_ec3_2)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_2)
+1 CellConnectorBlock_input_flow(cc_ec1_ec3_2)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_es_0)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_es_0)
+1 CellConnectorBlock_input_flow(cc_ec1_es_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_es_1)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_es_1)
+1 CellConnectorBlock_input_flow(cc_ec1_es_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec1_es_2)_:
+10000 CellConnectorBlock_Y_exp(cc_ec1_es_2)
+1 CellConnectorBlock_input_flow(cc_ec1_es_2)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec2_ec1_0)_:
+10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_0)
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec2_ec1_1)_:
+10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_1)
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec2_ec1_2)_:
+10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_2)
+1 CellConnectorBlock_input_flow(cc_ec2_ec1_2)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec3_ec1_0)_:
+10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_0)
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec3_ec1_1)_:
+10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_1)
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_ec3_ec1_2)_:
+10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_2)
+1 CellConnectorBlock_input_flow(cc_ec3_ec1_2)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_es_ec1_0)_:
+10000 CellConnectorBlock_Y_exp(cc_es_ec1_0)
+1 CellConnectorBlock_input_flow(cc_es_ec1_0)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_es_ec1_1)_:
+10000 CellConnectorBlock_Y_exp(cc_es_ec1_1)
+1 CellConnectorBlock_input_flow(cc_es_ec1_1)
<= 10000

c_u_CellConnectorBlock_max_input_rule(cc_es_ec1_2)_:
+10000 CellConnectorBlock_Y_exp(cc_es_ec1_2)
+1 CellConnectorBlock_input_flow(cc_es_ec1_2)
<= 10000

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec2_0)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_0)
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec2_1)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_1)
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec2_2)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec2_2)
+1 CellConnectorBlock_output_flow(cc_ec1_ec2_2)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec3_0)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_0)
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec3_1)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_1)
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_ec3_2)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_ec3_2)
+1 CellConnectorBlock_output_flow(cc_ec1_ec3_2)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_es_0)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_es_0)
+1 CellConnectorBlock_output_flow(cc_ec1_es_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_es_1)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_es_1)
+1 CellConnectorBlock_output_flow(cc_ec1_es_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec1_es_2)_:
-10000 CellConnectorBlock_Y_exp(cc_ec1_es_2)
+1 CellConnectorBlock_output_flow(cc_ec1_es_2)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec2_ec1_0)_:
-10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_0)
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec2_ec1_1)_:
-10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_1)
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec2_ec1_2)_:
-10000 CellConnectorBlock_Y_exp(cc_ec2_ec1_2)
+1 CellConnectorBlock_output_flow(cc_ec2_ec1_2)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec3_ec1_0)_:
-10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_0)
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec3_ec1_1)_:
-10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_1)
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_ec3_ec1_2)_:
-10000 CellConnectorBlock_Y_exp(cc_ec3_ec1_2)
+1 CellConnectorBlock_output_flow(cc_ec3_ec1_2)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_es_ec1_0)_:
-10000 CellConnectorBlock_Y_exp(cc_es_ec1_0)
+1 CellConnectorBlock_output_flow(cc_es_ec1_0)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_es_ec1_1)_:
-10000 CellConnectorBlock_Y_exp(cc_es_ec1_1)
+1 CellConnectorBlock_output_flow(cc_es_ec1_1)
<= 0

c_u_CellConnectorBlock_max_output_rule(cc_es_ec1_2)_:
-10000 CellConnectorBlock_Y_exp(cc_es_ec1_2)
+1 CellConnectorBlock_output_flow(cc_es_ec1_2)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_el_cc_es_ec1_0) <= +inf
   0 <= flow(bus_el_cc_es_ec1_1) <= +inf
   0 <= flow(bus_el_cc_es_ec1_2) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec2_0) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec2_1) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec2_2) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec3_0) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec3_1) <= +inf
   0 <= flow(bus_el_1_cc_ec1_ec3_2) <= +inf
   0 <= flow(bus_el_1_cc_ec1_es_0) <= +inf
   0 <= flow(bus_el_1_cc_ec1_es_1) <= +inf
   0 <= flow(bus_el_1_cc_ec1_es_2) <= +inf
   0 <= flow(bus_el_2_cc_ec2_ec1_0) <= +inf
   0 <= flow(bus_el_2_cc_ec2_ec1_1) <= +inf
   0 <= flow(bus_el_2_cc_ec2_ec1_2) <= +inf
   0 <= flow(bus_el_3_cc_ec3_ec1_0) <= +inf
   0 <= flow(bus_el_3_cc_ec3_ec1_1) <= +inf
   0 <= flow(bus_el_3_cc_ec3_ec1_2) <= +inf
   0 <= flow(cc_ec1_ec2_bus_el_1_0) <= +inf
   0 <= flow(cc_ec1_ec2_bus_el_1_1) <= +inf
   0 <= flow(cc_ec1_ec2_bus_el_1_2) <= +inf
   0 <= flow(cc_ec1_ec3_bus_el_1_0) <= +inf
   0 <= flow(cc_ec1_ec3_bus_el_1_1) <= +inf
   0 <= flow(cc_ec1_ec3_bus_el_1_2) <= +inf
   0 <= flow(cc_ec1_es_bus_el_1_0) <= +inf
   0 <= flow(cc_ec1_es_bus_el_1_1) <= +inf
   0 <= flow(cc_ec1_es_bus_el_1_2) <= +inf
   0 <= flow(cc_ec2_ec1_bus_el_2_0) <= +inf
   0 <= flow(cc_ec2_ec1_bus_el_2_1) <= +inf
   0 <= flow(cc_ec2_ec1_bus_el_2_2) <= +inf
   0 <= flow(cc_ec3_ec1_bus_el_3_0) <= +inf
   0 <= flow(cc_ec3_ec1_bus_el_3_1) <= +inf
   0 <= flow(cc_ec3_ec1_bus_el_3_2) <= +inf
   0 <= flow(cc_es_ec1_bus_el_0) <= +inf
   0 <= flow(cc_es_ec1_bus_el_1) <= +inf
   0 <= flow(cc_es_ec1_bus_el_2) <= +inf
   0 <= flow(pv_source_1_bus_el_1_0) <= 100
   0 <= flow(pv_source_1_bus_el_1_1) <= 100
   0 <= flow(pv_source_1_bus_el_1_2) <= 100
   0 <= flow(pv_source_2_bus_el_2_0) <= 10
   0 <= flow(pv_source_2_bus_el_2_1) <= 10
   0 <= flow(pv_source_2_bus_el_2_2) <= 10
   0 <= flow(pv_source_3_bus_el_3_0) <= 10
   0 <= flow(pv_source_3_bus_el_3_1) <= 10
   0 <= flow(pv_source_3_bus_el_3_2) <= 10
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec2_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec2_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec2_2) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec3_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec3_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_ec3_2) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_es_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_es_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec1_es_2) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec2_ec1_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec2_ec1_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec2_ec1_2) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec3_ec1_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec3_ec1_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_ec3_ec1_2) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_es_ec1_0) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_es_ec1_1) <= +inf
   0 <= CellConnectorBlock_input_flow(cc_es_ec1_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec2_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec2_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec2_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec3_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec3_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_ec3_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_es_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_es_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec1_es_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec2_ec1_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec2_ec1_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec2_ec1_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec3_ec1_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec3_ec1_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_ec3_ec1_2) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_es_ec1_0) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_es_ec1_1) <= +inf
   0 <= CellConnectorBlock_output_flow(cc_es_ec1_2) <= +inf
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec2_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec2_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec2_2) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec3_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec3_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_ec3_2) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_es_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_es_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec1_es_2) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec2_ec1_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec2_ec1_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec2_ec1_2) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec3_ec1_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec3_ec1_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_ec3_ec1_2) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_es_ec1_0) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_es_ec1_1) <= 1
   0 <= CellConnectorBlock_Y_exp(cc_es_ec1_2) <= 1
binary
  CellConnectorBlock_Y_exp(cc_ec1_ec2_0)
  CellConnectorBlock_Y_exp(cc_ec1_ec2_1)
  CellConnectorBlock_Y_exp(cc_ec1_ec2_2)
  CellConnectorBlock_Y_exp(cc_ec1_ec3_0)
  CellConnectorBlock_Y_exp(cc_ec1_ec3_1)
  CellConnectorBlock_Y_exp(cc_ec1_ec3_2)
  CellConnectorBlock_Y_exp(cc_ec1_es_0)
  CellConnectorBlock_Y_exp(cc_ec1_es_1)
  CellConnectorBlock_Y_exp(cc_ec1_es_2)
  CellConnectorBlock_Y_exp(cc_ec2_ec1_0)
  CellConnectorBlock_Y_exp(cc_ec2_ec1_1)
  CellConnectorBlock_Y_exp(cc_ec2_ec1_2)
  CellConnectorBlock_Y_exp(cc_ec3_ec1_0)
  CellConnectorBlock_Y_exp(cc_ec3_ec1_1)
  CellConnectorBlock_Y_exp(cc_ec3_ec1_2)
  CellConnectorBlock_Y_exp(cc_es_ec1_0)
  CellConnectorBlock_Y_exp(cc_es_ec1_1)
  CellConnectorBlock_Y_exp(cc_es_ec1_2)
end
