\* Source Pyomo model name=Model *\

min 
objective:
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_0_0)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_0_1)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_0_2)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_1_0)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_1_1)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_1_2)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_2_0)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_2_1)
+2 SinkDSMDelayBlock_dsm_do(demand_dsm_2_2)

s.t.

c_e_Bus_balance(bus_elec_0)_:
+1 flow(bus_elec_demand_dsm_0)
= 0

c_e_Bus_balance(bus_elec_1)_:
+1 flow(bus_elec_demand_dsm_1)
= 0

c_e_Bus_balance(bus_elec_2)_:
+1 flow(bus_elec_demand_dsm_2)
= 0

c_e_SinkDSMDelayBlock_input_output_relation(demand_dsm_0)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_0)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_0)
-1 SinkDSMDelayBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0)
= 1

c_e_SinkDSMDelayBlock_input_output_relation(demand_dsm_1)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_1)
-1 SinkDSMDelayBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_1)
= 1

c_e_SinkDSMDelayBlock_input_output_relation(demand_dsm_2)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_2)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_2)
-1 SinkDSMDelayBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_2)
= 1

c_e_SinkDSMDelayBlock_dsm_updo_constraint(demand_dsm_0)_:
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_0)
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_1)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_0)
= 0

c_e_SinkDSMDelayBlock_dsm_updo_constraint(demand_dsm_1)_:
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_0)
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_1)
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_2)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_1)
= 0

c_e_SinkDSMDelayBlock_dsm_updo_constraint(demand_dsm_2)_:
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_1)
-1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_2)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_2)
= 0

c_u_SinkDSMDelayBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDelayBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_1)
<= 0.5

c_u_SinkDSMDelayBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMDelayBlock_dsm_do_constraint(demand_dsm_0)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_0)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_0)
<= 0.5

c_u_SinkDSMDelayBlock_dsm_do_constraint(demand_dsm_1)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_1)
<= 0.5

c_u_SinkDSMDelayBlock_dsm_do_constraint(demand_dsm_2)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_2)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_2)
<= 0.5

c_u_SinkDSMDelayBlock_C2_constraint(demand_dsm_0)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_0)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_0)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMDelayBlock_C2_constraint(demand_dsm_1)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_0_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_1)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_1)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_1)
<= 0.5

c_u_SinkDSMDelayBlock_C2_constraint(demand_dsm_2)_:
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_1_2)
+1 SinkDSMDelayBlock_dsm_do(demand_dsm_2_2)
+1 SinkDSMDelayBlock_dsm_up(demand_dsm_2)
<= 0.5

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_0_0) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_0_1) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_0_2) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_1_0) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_1_1) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_1_2) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_2_0) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_2_1) <= +inf
   0 <= SinkDSMDelayBlock_dsm_do(demand_dsm_2_2) <= +inf
   0 <= SinkDSMDelayBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMDelayBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMDelayBlock_dsm_up(demand_dsm_2) <= +inf
end
