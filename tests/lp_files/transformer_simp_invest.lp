\* Source Pyomo model name=unknown *\

min 
objective:
+50 w(pp_gas_bel_0)
+50 w(pp_gas_bel_1)
+50 w(pp_gas_bel_2)

s.t.

c_e__class__oemof_core_network_entities_components_transformers_Simple___io_relation(pp_gas_0)_:
+0.57999999999999996 w(bgas_pp_gas_0)
-1 w(pp_gas_bel_0)
= 0

c_e__class__oemof_core_network_entities_components_transformers_Simple___io_relation(pp_gas_1)_:
+0.57999999999999996 w(bgas_pp_gas_1)
-1 w(pp_gas_bel_1)
= 0

c_e__class__oemof_core_network_entities_components_transformers_Simple___io_relation(pp_gas_2)_:
+0.57999999999999996 w(bgas_pp_gas_2)
-1 w(pp_gas_bel_2)
= 0

c_u__class__oemof_core_network_entities_components_transformers_Simple___output_bound(pp_gas_0)_:
-1 _class__oemof_core_network_entities_components_transformers_Simple___add_out(pp_gas)
+1 w(pp_gas_bel_0)
<= 100000000000

c_u__class__oemof_core_network_entities_components_transformers_Simple___output_bound(pp_gas_1)_:
-1 _class__oemof_core_network_entities_components_transformers_Simple___add_out(pp_gas)
+1 w(pp_gas_bel_1)
<= 100000000000

c_u__class__oemof_core_network_entities_components_transformers_Simple___output_bound(pp_gas_2)_:
-1 _class__oemof_core_network_entities_components_transformers_Simple___add_out(pp_gas)
+1 w(pp_gas_bel_2)
<= 100000000000

c_e__class__oemof_core_network_entities_Bus___balance(bel_0)_:
-1 w(bel_excess_0)
+1 w(pp_gas_bel_0)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bel_1)_:
-1 w(bel_excess_1)
+1 w(pp_gas_bel_1)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bel_2)_:
-1 w(bel_excess_2)
+1 w(pp_gas_bel_2)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bgas_0)_:
+1 w(bgas_pp_gas_0)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bgas_1)_:
+1 w(bgas_pp_gas_1)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bgas_2)_:
+1 w(bgas_pp_gas_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= w(bel_excess_0) <= +inf
   0 <= w(bel_excess_1) <= +inf
   0 <= w(bel_excess_2) <= +inf
   0 <= w(bgas_pp_gas_0) <= +inf
   0 <= w(bgas_pp_gas_1) <= +inf
   0 <= w(bgas_pp_gas_2) <= +inf
   0 <= w(pp_gas_bel_0) <= +inf
   0 <= w(pp_gas_bel_1) <= +inf
   0 <= w(pp_gas_bel_2) <= +inf
   0 <= _class__oemof_core_network_entities_components_transformers_Simple___add_out(pp_gas) <= +inf
end
