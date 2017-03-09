\* Source Pyomo model name=OperationalModel *\

min 
objective:
+50 flow(powerplantGasCoal_electricityBus_0)
+50 flow(powerplantGasCoal_electricityBus_1)
+50 flow(powerplantGasCoal_electricityBus_2)

s.t.

c_e_Bus_balance(biomassBus_0)_:
+1 flow(biomassBus_powerplantGasCoal_0)
= 0

c_e_Bus_balance(biomassBus_1)_:
+1 flow(biomassBus_powerplantGasCoal_1)
= 0

c_e_Bus_balance(biomassBus_2)_:
+1 flow(biomassBus_powerplantGasCoal_2)
= 0

c_e_Bus_balance(electricityBus_0)_:
+1 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
+1 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
+1 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_Bus_balance(gasBus_0)_:
+1 flow(gasBus_powerplantGasCoal_0)
= 0

c_e_Bus_balance(gasBus_1)_:
+1 flow(gasBus_powerplantGasCoal_1)
= 0

c_e_Bus_balance(gasBus_2)_:
+1 flow(gasBus_powerplantGasCoal_2)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_biomassBus_0)_:
-0.10000000000000001 flow(biomassBus_powerplantGasCoal_0)
+1 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_biomassBus_1)_:
-0.10000000000000001 flow(biomassBus_powerplantGasCoal_1)
+1 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_biomassBus_2)_:
-0.10000000000000001 flow(biomassBus_powerplantGasCoal_2)
+1 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_gasBus_0)_:
-0.40000000000000002 flow(gasBus_powerplantGasCoal_0)
+1 flow(powerplantGasCoal_electricityBus_0)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_gasBus_1)_:
-0.40000000000000002 flow(gasBus_powerplantGasCoal_1)
+1 flow(powerplantGasCoal_electricityBus_1)
= 0

c_e_LinearN1Transformer_relation(powerplantGasCoal_gasBus_2)_:
-0.40000000000000002 flow(gasBus_powerplantGasCoal_2)
+1 flow(powerplantGasCoal_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(biomassBus_powerplantGasCoal_0) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_1) <= +inf
   0 <= flow(biomassBus_powerplantGasCoal_2) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_0) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_1) <= +inf
   0 <= flow(gasBus_powerplantGasCoal_2) <= +inf
   0 <= flow(powerplantGasCoal_electricityBus_0) <= 100000000000
   0 <= flow(powerplantGasCoal_electricityBus_1) <= 100000000000
   0 <= flow(powerplantGasCoal_electricityBus_2) <= 100000000000
end
