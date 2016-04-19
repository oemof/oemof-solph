\* Source Pyomo model name=unknown *\

min 
objective: +0.0 ONE_VAR_CONSTANT

s.t.

c_e__class__oemof_core_network_entities_Bus___balance(bel_0)_:
+1 w(bel_bel_excess_0)
= 50000000

c_e__class__oemof_core_network_entities_Bus___balance(bel_1)_:
+1 w(bel_bel_excess_1)
= 80000000

c_e__class__oemof_core_network_entities_Bus___balance(bel_2)_:
+1 w(bel_bel_excess_2)
= 30000000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= w(bel_bel_excess_0) <= +inf
   0 <= w(bel_bel_excess_1) <= +inf
   0 <= w(bel_bel_excess_2) <= +inf
end
