\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(gasBus_0_0)_:
+1 flow(gasBus_gasboiler_0_0)
= 0

c_e_BusBlock_balance(gasBus_0_1)_:
+1 flow(gasBus_gasboiler_0_1)
= 0

c_e_BusBlock_balance(gasBus_1_2)_:
+1 flow(gasBus_gasboiler_1_2)
= 0

c_e_BusBlock_balance(gasBus_1_3)_:
+1 flow(gasBus_gasboiler_1_3)
= 0

c_e_BusBlock_balance(gasBus_2_4)_:
+1 flow(gasBus_gasboiler_2_4)
= 0

c_e_BusBlock_balance(gasBus_2_5)_:
+1 flow(gasBus_gasboiler_2_5)
= 0

c_e_BusBlock_balance(thermalBus_0_0)_:
+1 flow(gasboiler_thermalBus_0_0)
= 0

c_e_BusBlock_balance(thermalBus_0_1)_:
+1 flow(gasboiler_thermalBus_0_1)
= 0

c_e_BusBlock_balance(thermalBus_1_2)_:
+1 flow(gasboiler_thermalBus_1_2)
= 0

c_e_BusBlock_balance(thermalBus_1_3)_:
+1 flow(gasboiler_thermalBus_1_3)
= 0

c_e_BusBlock_balance(thermalBus_2_4)_:
+1 flow(gasboiler_thermalBus_2_4)
= 0

c_e_BusBlock_balance(thermalBus_2_5)_:
+1 flow(gasboiler_thermalBus_2_5)
= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_0_0)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_0)
-1 flow(gasBus_gasboiler_0_0)
<= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_0_1)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_1)
-1 flow(gasBus_gasboiler_0_1)
<= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_1_2)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_2)
-1 flow(gasBus_gasboiler_1_2)
<= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_1_3)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_3)
-1 flow(gasBus_gasboiler_1_3)
<= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_2_4)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_4)
-1 flow(gasBus_gasboiler_2_4)
<= 0

c_u_NonConvexFlowBlock_min(gasBus_gasboiler_2_5)_:
+32 NonConvexFlowBlock_status(gasBus_gasboiler_5)
-1 flow(gasBus_gasboiler_2_5)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_0_0)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_0)
+1 flow(gasBus_gasboiler_0_0)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_0_1)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_1)
+1 flow(gasBus_gasboiler_0_1)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_1_2)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_2)
+1 flow(gasBus_gasboiler_1_2)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_1_3)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_3)
+1 flow(gasBus_gasboiler_1_3)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_2_4)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_4)
+1 flow(gasBus_gasboiler_2_4)
<= 0

c_u_NonConvexFlowBlock_max(gasBus_gasboiler_2_5)_:
-100 NonConvexFlowBlock_status(gasBus_gasboiler_5)
+1 flow(gasBus_gasboiler_2_5)
<= 0

c_e_OffsetTransformerBlock_relation(gasboiler_0_0)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_0)
+0.90000000000000002 flow(gasBus_gasboiler_0_0)
-1 flow(gasboiler_thermalBus_0_0)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_0_1)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_1)
+0.90000000000000002 flow(gasBus_gasboiler_0_1)
-1 flow(gasboiler_thermalBus_0_1)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_1_2)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_2)
+0.90000000000000002 flow(gasBus_gasboiler_1_2)
-1 flow(gasboiler_thermalBus_1_2)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_1_3)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_3)
+0.90000000000000002 flow(gasBus_gasboiler_1_3)
-1 flow(gasboiler_thermalBus_1_3)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_2_4)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_4)
+0.90000000000000002 flow(gasBus_gasboiler_2_4)
-1 flow(gasboiler_thermalBus_2_4)
= 0

c_e_OffsetTransformerBlock_relation(gasboiler_2_5)_:
-17 NonConvexFlowBlock_status(gasBus_gasboiler_5)
+0.90000000000000002 flow(gasBus_gasboiler_2_5)
-1 flow(gasboiler_thermalBus_2_5)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(gasBus_gasboiler_0_0) <= 100
   0 <= flow(gasBus_gasboiler_0_1) <= 100
   0 <= flow(gasBus_gasboiler_1_2) <= 100
   0 <= flow(gasBus_gasboiler_1_3) <= 100
   0 <= flow(gasBus_gasboiler_2_4) <= 100
   0 <= flow(gasBus_gasboiler_2_5) <= 100
   0 <= flow(gasboiler_thermalBus_0_0) <= +inf
   0 <= flow(gasboiler_thermalBus_0_1) <= +inf
   0 <= flow(gasboiler_thermalBus_1_2) <= +inf
   0 <= flow(gasboiler_thermalBus_1_3) <= +inf
   0 <= flow(gasboiler_thermalBus_2_4) <= +inf
   0 <= flow(gasboiler_thermalBus_2_5) <= +inf
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_0) <= 1
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_1) <= 1
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_2) <= 1
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_3) <= 1
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_4) <= 1
   0 <= NonConvexFlowBlock_status(gasBus_gasboiler_5) <= 1
binary
  NonConvexFlowBlock_status(gasBus_gasboiler_0)
  NonConvexFlowBlock_status(gasBus_gasboiler_1)
  NonConvexFlowBlock_status(gasBus_gasboiler_2)
  NonConvexFlowBlock_status(gasBus_gasboiler_3)
  NonConvexFlowBlock_status(gasBus_gasboiler_4)
  NonConvexFlowBlock_status(gasBus_gasboiler_5)
end
