\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(bel0_0_0)_:
-1 flow(bel0_link_0_0)
+1 flow(link_bel0_0_0)
= 0

c_e_BusBlock_balance(bel0_0_1)_:
-1 flow(bel0_link_0_1)
+1 flow(link_bel0_0_1)
= 0

c_e_BusBlock_balance(bel0_0_2)_:
-1 flow(bel0_link_0_2)
+1 flow(link_bel0_0_2)
= 0

c_e_BusBlock_balance(bel1_0_0)_:
-1 flow(bel1_link_0_0)
+1 flow(link_bel1_0_0)
= 0

c_e_BusBlock_balance(bel1_0_1)_:
-1 flow(bel1_link_0_1)
+1 flow(link_bel1_0_1)
= 0

c_e_BusBlock_balance(bel1_0_2)_:
-1 flow(bel1_link_0_2)
+1 flow(link_bel1_0_2)
= 0

c_e_LinkBlock_relation(link_bel0_bel1_0_0)_:
-0.80000000000000004 flow(bel0_link_0_0)
+1 flow(link_bel1_0_0)
= 0

c_e_LinkBlock_relation(link_bel0_bel1_0_1)_:
-0.80000000000000004 flow(bel0_link_0_1)
+1 flow(link_bel1_0_1)
= 0

c_e_LinkBlock_relation(link_bel0_bel1_0_2)_:
-0.80000000000000004 flow(bel0_link_0_2)
+1 flow(link_bel1_0_2)
= 0

c_e_LinkBlock_relation(link_bel1_bel0_0_0)_:
-0.90000000000000002 flow(bel1_link_0_0)
+1 flow(link_bel0_0_0)
= 0

c_e_LinkBlock_relation(link_bel1_bel0_0_1)_:
-0.90000000000000002 flow(bel1_link_0_1)
+1 flow(link_bel0_0_1)
= 0

c_e_LinkBlock_relation(link_bel1_bel0_0_2)_:
-0.90000000000000002 flow(bel1_link_0_2)
+1 flow(link_bel0_0_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bel0_link_0_0) <= 4
   0 <= flow(bel0_link_0_1) <= 4
   0 <= flow(bel0_link_0_2) <= 4
   0 <= flow(bel1_link_0_0) <= 2
   0 <= flow(bel1_link_0_1) <= 2
   0 <= flow(bel1_link_0_2) <= 2
   0 <= flow(link_bel0_0_0) <= +inf
   0 <= flow(link_bel0_0_1) <= +inf
   0 <= flow(link_bel0_0_2) <= +inf
   0 <= flow(link_bel1_0_0) <= +inf
   0 <= flow(link_bel1_0_1) <= +inf
   0 <= flow(link_bel1_0_2) <= +inf
end
