\* Source Pyomo model name=unknown *\

min 
objective:
+100 _class__oemof_core_network_entities_components_sources_FixedSource___add_out(wind)
+20000000 ONE_VAR_CONSTANT

s.t.

c_e__class__oemof_core_network_entities_components_sources_FixedSource___invest(wind_0)_:
-50 _class__oemof_core_network_entities_components_sources_FixedSource___add_out(wind)
+1 w(wind_bel_0)
= 50000000

c_e__class__oemof_core_network_entities_components_sources_FixedSource___invest(wind_1)_:
-80 _class__oemof_core_network_entities_components_sources_FixedSource___add_out(wind)
+1 w(wind_bel_1)
= 80000000

c_e__class__oemof_core_network_entities_components_sources_FixedSource___invest(wind_2)_:
-30 _class__oemof_core_network_entities_components_sources_FixedSource___add_out(wind)
+1 w(wind_bel_2)
= 30000000

c_e__class__oemof_core_network_entities_Bus___balance(bel_0)_:
-1 excess_slack(bel_0)
+1 w(wind_bel_0)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bel_1)_:
-1 excess_slack(bel_1)
+1 w(wind_bel_1)
= 0

c_e__class__oemof_core_network_entities_Bus___balance(bel_2)_:
-1 excess_slack(bel_2)
+1 w(wind_bel_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds 
   0 <= w(wind_bel_0) <= +inf
   0 <= w(wind_bel_1) <= +inf
   0 <= w(wind_bel_2) <= +inf
   0 <= excess_slack(bel_0) <= +inf
   0 <= excess_slack(bel_1) <= +inf
   0 <= excess_slack(bel_2) <= +inf
   0 <= _class__oemof_core_network_entities_components_sources_FixedSource___add_out(wind) <= 0
end 
