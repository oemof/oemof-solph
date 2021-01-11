\* Source Pyomo model name=Model *\

min 
objective:
+2 SinkDSMIntervalBlock_dsm_do(demand_dsm_0)
+2 SinkDSMIntervalBlock_dsm_do(demand_dsm_1)
+2 SinkDSMIntervalBlock_dsm_do(demand_dsm_2)

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

c_e_SinkDSMIntervalBlock_input_output_relation(demand_dsm_0)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_0)
-1 SinkDSMIntervalBlock_dsm_up(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0)
= 1

c_e_SinkDSMIntervalBlock_input_output_relation(demand_dsm_1)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_1)
-1 SinkDSMIntervalBlock_dsm_up(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_1)
= 1

c_e_SinkDSMIntervalBlock_input_output_relation(demand_dsm_2)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_2)
-1 SinkDSMIntervalBlock_dsm_up(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_2)
= 1

c_u_SinkDSMIntervalBlock_dsm_up_constraint(demand_dsm_0)_:
+1 SinkDSMIntervalBlock_dsm_up(demand_dsm_0)
<= 0.5

c_u_SinkDSMIntervalBlock_dsm_up_constraint(demand_dsm_1)_:
+1 SinkDSMIntervalBlock_dsm_up(demand_dsm_1)
<= 0.40000000000000002

c_u_SinkDSMIntervalBlock_dsm_up_constraint(demand_dsm_2)_:
+1 SinkDSMIntervalBlock_dsm_up(demand_dsm_2)
<= 0.5

c_u_SinkDSMIntervalBlock_dsm_down_constraint(demand_dsm_0)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_0)
<= 0.5

c_u_SinkDSMIntervalBlock_dsm_down_constraint(demand_dsm_1)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_1)
<= 0.40000000000000002

c_u_SinkDSMIntervalBlock_dsm_down_constraint(demand_dsm_2)_:
+1 SinkDSMIntervalBlock_dsm_do(demand_dsm_2)
<= 0.5

c_e_SinkDSMIntervalBlock_dsm_sum_constraint(demand_dsm_0)_:
-1 SinkDSMIntervalBlock_dsm_do(demand_dsm_0)
-1 SinkDSMIntervalBlock_dsm_do(demand_dsm_1)
+1 SinkDSMIntervalBlock_dsm_up(demand_dsm_0)
+1 SinkDSMIntervalBlock_dsm_up(demand_dsm_1)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_do(demand_dsm_0) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_do(demand_dsm_1) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_do(demand_dsm_2) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_up(demand_dsm_0) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_up(demand_dsm_1) <= +inf
   0 <= SinkDSMIntervalBlock_dsm_up(demand_dsm_2) <= +inf
end
