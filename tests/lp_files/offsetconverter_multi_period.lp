\* Source Pyomo model name=Model *\

min 
objective:
+0 ONE_VAR_CONSTANT

s.t.

c_e_BusBlock_balance(gasBus_0)_:
+1 flow(gasBus_gasboiler_0)
= 0

c_e_BusBlock_balance(gasBus_1)_:
+1 flow(gasBus_gasboiler_1)
= 0

c_e_BusBlock_balance(gasBus_2)_:
+1 flow(gasBus_gasboiler_2)
= 0

c_e_BusBlock_balance(gasBus_3)_:
+1 flow(gasBus_gasboiler_3)
= 0

c_e_BusBlock_balance(gasBus_4)_:
+1 flow(gasBus_gasboiler_4)
= 0

c_e_BusBlock_balance(gasBus_5)_:
+1 flow(gasBus_gasboiler_5)
= 0

c_e_BusBlock_balance(thermalBus_0)_:
+1 flow(gasboiler_thermalBus_0)
= 0

c_e_BusBlock_balance(thermalBus_1)_:
+1 flow(gasboiler_thermalBus_1)
= 0

c_e_BusBlock_balance(thermalBus_2)_:
+1 flow(gasboiler_thermalBus_2)
= 0

c_e_BusBlock_balance(thermalBus_3)_:
+1 flow(gasboiler_thermalBus_3)
= 0

c_e_BusBlock_balance(thermalBus_4)_:
+1 flow(gasboiler_thermalBus_4)
= 0

c_e_BusBlock_balance(thermalBus_5)_:
+1 flow(gasboiler_thermalBus_5)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_0)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_0)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_0)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_1)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_1)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_1)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_2)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_2)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_2)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_3)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_3)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_3)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_4)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_4)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_4)
= 0

c_e_NonConvexFlowBlock_status_nominal_constraint(gasboiler_thermalBus_5)_:
+1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_5)
-100 NonConvexFlowBlock_status(gasboiler_thermalBus_5)
= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_0)_:
-1 flow(gasboiler_thermalBus_0)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_0)
<= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_1)_:
-1 flow(gasboiler_thermalBus_1)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_1)
<= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_2)_:
-1 flow(gasboiler_thermalBus_2)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_2)
<= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_3)_:
-1 flow(gasboiler_thermalBus_3)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_3)
<= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_4)_:
-1 flow(gasboiler_thermalBus_4)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_4)
<= 0

c_u_NonConvexFlowBlock_min(gasboiler_thermalBus_5)_:
-1 flow(gasboiler_thermalBus_5)
+0.32 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_5)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_0)_:
+1 flow(gasboiler_thermalBus_0)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_0)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_1)_:
+1 flow(gasboiler_thermalBus_1)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_1)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_2)_:
+1 flow(gasboiler_thermalBus_2)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_2)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_3)_:
+1 flow(gasboiler_thermalBus_3)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_3)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_4)_:
+1 flow(gasboiler_thermalBus_4)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_4)
<= 0

c_u_NonConvexFlowBlock_max(gasboiler_thermalBus_5)_:
+1 flow(gasboiler_thermalBus_5)
-1 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_5)
<= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_0)_:
-1 flow(gasBus_gasboiler_0)
+0.9617180205415501 flow(gasboiler_thermalBus_0)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_0)
= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_1)_:
-1 flow(gasBus_gasboiler_1)
+0.9617180205415501 flow(gasboiler_thermalBus_1)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_1)
= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_2)_:
-1 flow(gasBus_gasboiler_2)
+0.9617180205415501 flow(gasboiler_thermalBus_2)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_2)
= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_3)_:
-1 flow(gasBus_gasboiler_3)
+0.9617180205415501 flow(gasboiler_thermalBus_3)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_3)
= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_4)_:
-1 flow(gasBus_gasboiler_4)
+0.9617180205415501 flow(gasboiler_thermalBus_4)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_4)
= 0

c_e_OffsetConverterBlock_relation(gasboiler_thermalBus_gasBus_5)_:
-1 flow(gasBus_gasboiler_5)
+0.9617180205415501 flow(gasboiler_thermalBus_5)
+0.14939309056956107 NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_5)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(gasBus_gasboiler_0) <= +inf
   0 <= flow(gasBus_gasboiler_1) <= +inf
   0 <= flow(gasBus_gasboiler_2) <= +inf
   0 <= flow(gasBus_gasboiler_3) <= +inf
   0 <= flow(gasBus_gasboiler_4) <= +inf
   0 <= flow(gasBus_gasboiler_5) <= +inf
   0 <= flow(gasboiler_thermalBus_0) <= 100
   0 <= flow(gasboiler_thermalBus_1) <= 100
   0 <= flow(gasboiler_thermalBus_2) <= 100
   0 <= flow(gasboiler_thermalBus_3) <= 100
   0 <= flow(gasboiler_thermalBus_4) <= 100
   0 <= flow(gasboiler_thermalBus_5) <= 100
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_0) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_0) <= 1
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_1) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_1) <= 1
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_2) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_2) <= 1
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_3) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_3) <= 1
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_4) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_4) <= 1
   0 <= NonConvexFlowBlock_status_nominal(gasboiler_thermalBus_5) <= +inf
   0 <= NonConvexFlowBlock_status(gasboiler_thermalBus_5) <= 1
binary
  NonConvexFlowBlock_status(gasboiler_thermalBus_0)
  NonConvexFlowBlock_status(gasboiler_thermalBus_1)
  NonConvexFlowBlock_status(gasboiler_thermalBus_2)
  NonConvexFlowBlock_status(gasboiler_thermalBus_3)
  NonConvexFlowBlock_status(gasboiler_thermalBus_4)
  NonConvexFlowBlock_status(gasboiler_thermalBus_5)
end
