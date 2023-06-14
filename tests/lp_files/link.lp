\* Source Pyomo model name=Model *\

min
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(el1_0_0)_:
-1 flow(el1_link_0_0)
+1 flow(link_el1_0_0)
= 0

c_e_BusBlock_balance(el1_0_1)_:
-1 flow(el1_link_0_1)
+1 flow(link_el1_0_1)
= 0

c_e_BusBlock_balance(el1_0_2)_:
-1 flow(el1_link_0_2)
+1 flow(link_el1_0_2)
= 0

c_e_BusBlock_balance(el2_0_0)_:
-1 flow(el2_link_0_0)
+1 flow(link_el2_0_0)
= 0

c_e_BusBlock_balance(el2_0_1)_:
-1 flow(el2_link_0_1)
+1 flow(link_el2_0_1)
= 0

c_e_BusBlock_balance(el2_0_2)_:
-1 flow(el2_link_0_2)
+1 flow(link_el2_0_2)
= 0

c_e_LinkBlock_relation(link_el1_el2_0_0)_:
-0.75 flow(el1_link_0_0)
+1 flow(link_el2_0_0)
= 0

c_e_LinkBlock_relation(link_el1_el2_0_1)_:
-0.75 flow(el1_link_0_1)
+1 flow(link_el2_0_1)
= 0

c_e_LinkBlock_relation(link_el1_el2_0_2)_:
-0.75 flow(el1_link_0_2)
+1 flow(link_el2_0_2)
= 0

c_e_LinkBlock_relation(link_el2_el1_0_0)_:
-0.5 flow(el2_link_0_0)
+1 flow(link_el1_0_0)
= 0

c_e_LinkBlock_relation(link_el2_el1_0_1)_:
-0.5 flow(el2_link_0_1)
+1 flow(link_el1_0_1)
= 0

c_e_LinkBlock_relation(link_el2_el1_0_2)_:
-0.5 flow(el2_link_0_2)
+1 flow(link_el1_0_2)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(el1_link_0_0) <= 4
   0 <= flow(el1_link_0_1) <= 4
   0 <= flow(el1_link_0_2) <= 4
   0 <= flow(el2_link_0_0) <= 2
   0 <= flow(el2_link_0_1) <= 2
   0 <= flow(el2_link_0_2) <= 2
   0 <= flow(link_el1_0_0) <= +inf
   0 <= flow(link_el1_0_1) <= +inf
   0 <= flow(link_el1_0_2) <= +inf
   0 <= flow(link_el2_0_0) <= +inf
   0 <= flow(link_el2_0_1) <= +inf
   0 <= flow(link_el2_0_2) <= +inf
end
