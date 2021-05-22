\* Source Pyomo model name=Model *\

min 
objective:
+23 flow(powerplant_electricityBus_0)
+23 flow(powerplant_electricityBus_1)
+23 flow(powerplant_electricityBus_2)

s.t.

c_e_Bus_balance(electricityBus_0)_:
+1 flow(powerplant_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(powerplant_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(powerplant_electricityBus_2)
= 0

c_e_Flow_integer_flow_constr(powerplant_electricityBus_0)_:
+1 Flow_integer_flow(powerplant_electricityBus_0)
-1 flow(powerplant_electricityBus_0)
= 0

c_e_Flow_integer_flow_constr(powerplant_electricityBus_1)_:
+1 Flow_integer_flow(powerplant_electricityBus_1)
-1 flow(powerplant_electricityBus_1)
= 0

c_e_Flow_integer_flow_constr(powerplant_electricityBus_2)_:
+1 Flow_integer_flow(powerplant_electricityBus_2)
-1 flow(powerplant_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(powerplant_electricityBus_0) <= 999
   0 <= flow(powerplant_electricityBus_1) <= 999
   0 <= flow(powerplant_electricityBus_2) <= 999
   0 <= Flow_integer_flow(powerplant_electricityBus_0) <= +inf
   0 <= Flow_integer_flow(powerplant_electricityBus_1) <= +inf
   0 <= Flow_integer_flow(powerplant_electricityBus_2) <= +inf
general
  Flow_integer_flow(powerplant_electricityBus_0)
  Flow_integer_flow(powerplant_electricityBus_1)
  Flow_integer_flow(powerplant_electricityBus_2)
end
