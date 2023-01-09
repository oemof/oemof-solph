\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(el1_0)_:
-1 flow(el1_link_0)
+1 flow(link_el1_0)
= 0

c_e_BusBlock_balance(el1_1)_:
-1 flow(el1_link_1)
+1 flow(link_el1_1)
= 0

c_e_BusBlock_balance(el1_2)_:
-1 flow(el1_link_2)
+1 flow(link_el1_2)
= 0

c_e_BusBlock_balance(el2_0)_:
-1 flow(el2_link_0)
+1 flow(link_el2_0)
= 0

c_e_BusBlock_balance(el2_1)_:
-1 flow(el2_link_1)
+1 flow(link_el2_1)
= 0

c_e_BusBlock_balance(el2_2)_:
-1 flow(el2_link_2)
+1 flow(link_el2_2)
= 0

c_e_LinkBlock_relation(link_el1_el2_0)_:
-0.75 flow(el1_link_0)
+1 flow(link_el2_0)
= 0

c_e_LinkBlock_relation(link_el1_el2_1)_:
-0.75 flow(el1_link_1)
+1 flow(link_el2_1)
= 0

c_e_LinkBlock_relation(link_el1_el2_2)_:
-0.75 flow(el1_link_2)
+1 flow(link_el2_2)
= 0

c_e_LinkBlock_relation(link_el2_el1_0)_:
-0.5 flow(el2_link_0)
+1 flow(link_el1_0)
= 0

c_e_LinkBlock_relation(link_el2_el1_1)_:
-0.5 flow(el2_link_1)
+1 flow(link_el1_1)
= 0

c_e_LinkBlock_relation(link_el2_el1_2)_:
-0.5 flow(el2_link_2)
+1 flow(link_el1_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(el1_link_0) <= 4
   0 <= flow(el1_link_1) <= 4
   0 <= flow(el1_link_2) <= 4
   0 <= flow(el2_link_0) <= 2
   0 <= flow(el2_link_1) <= 2
   0 <= flow(el2_link_2) <= 2
   0 <= flow(link_el1_0) <= +inf
   0 <= flow(link_el1_1) <= +inf
   0 <= flow(link_el1_2) <= +inf
   0 <= flow(link_el2_0) <= +inf
   0 <= flow(link_el2_1) <= +inf
   0 <= flow(link_el2_2) <= +inf
end
