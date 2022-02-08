\* Source Pyomo model name=Model *\

min 
objective:
+2 flow(Bus1_Sink_0)
+2 flow(Bus1_Sink_1)
+2 flow(Bus1_Sink_2)
+2 flow(Source1_Bus1_0)
+2 flow(Source1_Bus1_1)
+2 flow(Source1_Bus1_2)
+10 flow(Source2_Bus1_0)
+10 flow(Source2_Bus1_1)
+10 flow(Source2_Bus1_2)

s.t.

c_e_equate_flows(0)_:
-1 flow(Bus1_Sink_0)
+2 flow(Source1_Bus1_0)
+2 flow(Source2_Bus1_0)
= 0

c_e_equate_flows(1)_:
-1 flow(Bus1_Sink_1)
+2 flow(Source1_Bus1_1)
+2 flow(Source2_Bus1_1)
= 0

c_e_equate_flows(2)_:
-1 flow(Bus1_Sink_2)
+2 flow(Source1_Bus1_2)
+2 flow(Source2_Bus1_2)
= 0

c_e_BusBlock_balance(Bus1_0)_:
-1 flow(Bus1_Sink_0)
+1 flow(Source1_Bus1_0)
+1 flow(Source2_Bus1_0)
= 0

c_e_BusBlock_balance(Bus1_1)_:
-1 flow(Bus1_Sink_1)
+1 flow(Source1_Bus1_1)
+1 flow(Source2_Bus1_1)
= 0

c_e_BusBlock_balance(Bus1_2)_:
-1 flow(Bus1_Sink_2)
+1 flow(Source1_Bus1_2)
+1 flow(Source2_Bus1_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_Sink_0) <= 300
   0 <= flow(Bus1_Sink_1) <= 300
   0 <= flow(Bus1_Sink_2) <= 300
   0 <= flow(Source1_Bus1_0) <= 400
   0 <= flow(Source1_Bus1_1) <= 400
   0 <= flow(Source1_Bus1_2) <= 400
   0 <= flow(Source2_Bus1_0) <= 200
   0 <= flow(Source2_Bus1_1) <= 200
   0 <= flow(Source2_Bus1_2) <= 200
end
