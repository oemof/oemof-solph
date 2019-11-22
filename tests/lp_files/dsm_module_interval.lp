\* Source Pyomo model name=Model *\

min 
objective:
+1 flow(bus_elec_demand_dsm_0)
+1 flow(bus_elec_demand_dsm_1)
+1 flow(bus_elec_demand_dsm_2)

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
-1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_0)
+1 flow(bus_elec_demand_dsm_0)
= 1

c_e_SinkDSMIntervalBlock_input_output_relation(demand_dsm_1)_:
-1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_1)
+1 flow(bus_elec_demand_dsm_1)
= 1

c_e_SinkDSMIntervalBlock_input_output_relation(demand_dsm_2)_:
-1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_2)
+1 flow(bus_elec_demand_dsm_2)
= 1

c_e_SinkDSMIntervalBlock_dsm_sum_constraint(demand_dsm_0)_:
+1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_0)
+1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_1)
= 0

c_e_SinkDSMIntervalBlock_dsm_sum_constraint(demand_dsm_1)_:
+1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_0)
+1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_1)
= 0

c_e_SinkDSMIntervalBlock_dsm_sum_constraint(demand_dsm_2)_:
+1 SinkDSMIntervalBlock_dsm_up_down(demand_dsm_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_elec_demand_dsm_0) <= +inf
   0 <= flow(bus_elec_demand_dsm_1) <= +inf
   0 <= flow(bus_elec_demand_dsm_2) <= +inf
   -0.5 <= SinkDSMIntervalBlock_dsm_up_down(demand_dsm_0) <= 0.5
   -0.4 <= SinkDSMIntervalBlock_dsm_up_down(demand_dsm_1) <= 0.4
   -0.5 <= SinkDSMIntervalBlock_dsm_up_down(demand_dsm_2) <= 0.5
end
