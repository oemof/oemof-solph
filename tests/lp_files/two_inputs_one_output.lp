\* Source Pyomo model name=unknown *\

min 
objective: +0.0 ONE_VAR_CONSTANT

s.t.

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___io_relation(postheat_elec_0)_:
+1 w(bus_stor_heat_postheat_elec_0)
+0.94999999999999996 w(bus_test_postheat_elec_0)
-1 w(postheat_elec_bus_distr_heat_0)
= 0

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___io_relation(postheat_elec_1)_:
+1 w(bus_stor_heat_postheat_elec_1)
+0.94999999999999996 w(bus_test_postheat_elec_1)
-1 w(postheat_elec_bus_distr_heat_1)
= 0

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___io_relation(postheat_elec_2)_:
+1 w(bus_stor_heat_postheat_elec_2)
+0.94999999999999996 w(bus_test_postheat_elec_2)
-1 w(postheat_elec_bus_distr_heat_2)
= 0

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___two_inputs_relation(postheat_elec_0)_:
+0.33333333333333331 w(bus_stor_heat_postheat_elec_0)
-0.94999999999999996 w(bus_test_postheat_elec_0)
= 0

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___two_inputs_relation(postheat_elec_1)_:
-0.94999999999999996 w(bus_test_postheat_elec_1)
= 0

c_e__class__oemof_core_network_entities_components_transformers_TwoInputsOneOutput___two_inputs_relation(postheat_elec_2)_:
-0.94999999999999996 w(bus_test_postheat_elec_2)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_distr_heat_0)_:
+1 w(postheat_elec_bus_distr_heat_0)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_distr_heat_1)_:
+1 w(postheat_elec_bus_distr_heat_1)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_distr_heat_2)_:
+1 w(postheat_elec_bus_distr_heat_2)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_stor_heat_0)_:
+1 w(bus_stor_heat_postheat_elec_0)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_stor_heat_1)_:
+1 w(bus_stor_heat_postheat_elec_1)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_stor_heat_2)_:
+1 w(bus_stor_heat_postheat_elec_2)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_test_0)_:
+1 w(bus_test_postheat_elec_0)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_test_1)_:
+1 w(bus_test_postheat_elec_1)
= 0

c_e__class__oemof_core_network_entities_buses_HeatBus___balance(bus_test_2)_:
+1 w(bus_test_postheat_elec_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= w(bus_stor_heat_postheat_elec_0) <= 888
   0 <= w(bus_stor_heat_postheat_elec_1) <= 888
   0 <= w(bus_stor_heat_postheat_elec_2) <= 888
   0 <= w(bus_test_postheat_elec_0) <= 777
   0 <= w(bus_test_postheat_elec_1) <= 777
   0 <= w(bus_test_postheat_elec_2) <= 777
   0 <= w(postheat_elec_bus_distr_heat_0) <= 999993
   0 <= w(postheat_elec_bus_distr_heat_1) <= 999993
   0 <= w(postheat_elec_bus_distr_heat_2) <= 999993
end
