\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(gasBus_0)_:
+1 flow(gasBus_gasboiler_0)
= 0

c_e_Bus_balance(gasBus_1)_:
+1 flow(gasBus_gasboiler_1)
= 0

c_e_Bus_balance(gasBus_2)_:
+1 flow(gasBus_gasboiler_2)
= 0

c_e_Bus_balance(thermalBus_0)_:
+1 flow(gasboiler_thermalBus_0)
= 0

c_e_Bus_balance(thermalBus_1)_:
+1 flow(gasboiler_thermalBus_1)
= 0

c_e_Bus_balance(thermalBus_2)_:
+1 flow(gasboiler_thermalBus_2)
= 0

c_u_NonConvexFlow_min(gasBus_gasboiler_0)_:
+32 NonConvexFlow_status(gasBus_gasboiler_0)
-1 flow(gasBus_gasboiler_0)
<= 0

c_u_NonConvexFlow_min(gasBus_gasboiler_1)_:
+32 NonConvexFlow_status(gasBus_gasboiler_1)
-1 flow(gasBus_gasboiler_1)
<= 0

c_u_NonConvexFlow_min(gasBus_gasboiler_2)_:
+32 NonConvexFlow_status(gasBus_gasboiler_2)
-1 flow(gasBus_gasboiler_2)
<= 0

c_u_NonConvexFlow_max(gasBus_gasboiler_0)_:
-100 NonConvexFlow_status(gasBus_gasboiler_0)
+1 flow(gasBus_gasboiler_0)
<= 0

c_u_NonConvexFlow_max(gasBus_gasboiler_1)_:
-100 NonConvexFlow_status(gasBus_gasboiler_1)
+1 flow(gasBus_gasboiler_1)
<= 0

c_u_NonConvexFlow_max(gasBus_gasboiler_2)_:
-100 NonConvexFlow_status(gasBus_gasboiler_2)
+1 flow(gasBus_gasboiler_2)
<= 0

c_e_OffsetTransformerBlock_relation(gasboiler_0)_:
-17 NonConvexFlow_status(gasBus_gasboiler_0)
+0.90000000000000002 flow(gasBus_gasboiler_0)
-1 flow(gasboiler_thermalBus_0)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_1)_:
-17 NonConvexFlow_status(gasBus_gasboiler_1)
+0.90000000000000002 flow(gasBus_gasboiler_1)
-1 flow(gasboiler_thermalBus_1)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_2)_:
-17 NonConvexFlow_status(gasBus_gasboiler_2)
+0.90000000000000002 flow(gasBus_gasboiler_2)
-1 flow(gasboiler_thermalBus_2)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gasBus_gasboiler_0) <= 100
   0 <= flow(gasBus_gasboiler_1) <= 100
   0 <= flow(gasBus_gasboiler_2) <= 100
   0 <= flow(gasboiler_thermalBus_0) <= +inf
   0 <= flow(gasboiler_thermalBus_1) <= +inf
   0 <= flow(gasboiler_thermalBus_2) <= +inf
   0 <= NonConvexFlow_status(gasBus_gasboiler_0) <= 1
   0 <= NonConvexFlow_status(gasBus_gasboiler_1) <= 1
   0 <= NonConvexFlow_status(gasBus_gasboiler_2) <= 1
binary
  NonConvexFlow_status(gasBus_gasboiler_0)
  NonConvexFlow_status(gasBus_gasboiler_1)
  NonConvexFlow_status(gasBus_gasboiler_2)
end
