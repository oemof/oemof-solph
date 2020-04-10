\* Source Pyomo model name=Model *\

min
objective:
+100 flow(gas_boiler_0)
+100 flow(gas_boiler_1)
+100 flow(gas_boiler_2)
+200 flow(gas_boiler_3)
+200 flow(gas_boiler_4)
+50 flow(gas_boiler_5)
+50 flow(gas_boiler_6)
+50 flow(gas_boiler_7)

s.t.

c_e_Bus_balance(gas_0)_:
+1 flow(gas_boiler_0)
= 0

c_e_Bus_balance(gas_1)_:
+1 flow(gas_boiler_1)
= 0

c_e_Bus_balance(gas_2)_:
+1 flow(gas_boiler_2)
= 0

c_e_Bus_balance(gas_3)_:
+1 flow(gas_boiler_3)
= 0

c_e_Bus_balance(gas_4)_:
+1 flow(gas_boiler_4)
= 0

c_e_Bus_balance(gas_5)_:
+1 flow(gas_boiler_5)
= 0

c_e_Bus_balance(gas_6)_:
+1 flow(gas_boiler_6)
= 0

c_e_Bus_balance(gas_7)_:
+1 flow(gas_boiler_7)
= 0

c_e_Bus_balance(heat_0)_:
+1 flow(boiler_heat_0)
= 0

c_e_Bus_balance(heat_1)_:
+1 flow(boiler_heat_1)
= 0

c_e_Bus_balance(heat_2)_:
+1 flow(boiler_heat_2)
= 0

c_e_Bus_balance(heat_3)_:
+1 flow(boiler_heat_3)
= 0

c_e_Bus_balance(heat_4)_:
+1 flow(boiler_heat_4)
= 0

c_e_Bus_balance(heat_5)_:
+1 flow(boiler_heat_5)
= 0

c_e_Bus_balance(heat_6)_:
+1 flow(boiler_heat_6)
= 0

c_e_Bus_balance(heat_7)_:
+1 flow(boiler_heat_7)
= 0

c_e_Transformer_relation(boiler_gas_heat_0)_:
-1 flow(boiler_heat_0)
+1 flow(gas_boiler_0)
= 0

c_e_Transformer_relation(boiler_gas_heat_1)_:
-1 flow(boiler_heat_1)
+1 flow(gas_boiler_1)
= 0

c_e_Transformer_relation(boiler_gas_heat_2)_:
-1 flow(boiler_heat_2)
+1 flow(gas_boiler_2)
= 0

c_e_Transformer_relation(boiler_gas_heat_3)_:
-1 flow(boiler_heat_3)
+1 flow(gas_boiler_3)
= 0

c_e_Transformer_relation(boiler_gas_heat_4)_:
-1 flow(boiler_heat_4)
+1 flow(gas_boiler_4)
= 0

c_e_Transformer_relation(boiler_gas_heat_5)_:
-1 flow(boiler_heat_5)
+1 flow(gas_boiler_5)
= 0

c_e_Transformer_relation(boiler_gas_heat_6)_:
-1 flow(boiler_heat_6)
+1 flow(gas_boiler_6)
= 0

c_e_Transformer_relation(boiler_gas_heat_7)_:
-1 flow(boiler_heat_7)
+1 flow(gas_boiler_7)
= 0

c_e_ONE_VAR_CONSTANT:
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(boiler_heat_0) <= 200
   0 <= flow(boiler_heat_1) <= 200
   0 <= flow(boiler_heat_2) <= 200
   0 <= flow(boiler_heat_3) <= 200
   0 <= flow(boiler_heat_4) <= 200
   0 <= flow(boiler_heat_5) <= 200
   0 <= flow(boiler_heat_6) <= 200
   0 <= flow(boiler_heat_7) <= 200
   0 <= flow(gas_boiler_0) <= +inf
   0 <= flow(gas_boiler_1) <= +inf
   0 <= flow(gas_boiler_2) <= +inf
   0 <= flow(gas_boiler_3) <= +inf
   0 <= flow(gas_boiler_4) <= +inf
   0 <= flow(gas_boiler_5) <= +inf
   0 <= flow(gas_boiler_6) <= +inf
   0 <= flow(gas_boiler_7) <= +inf
end
