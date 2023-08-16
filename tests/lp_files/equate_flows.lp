\* Source Pyomo model name=Model *\

min 
objective:
+2 flow(Bus1_Sink_0_0)
+2 flow(Bus1_Sink_0_1)
+2 flow(Bus1_Sink_0_2)
+2 flow(Source1_Bus1_0_0)
+2 flow(Source1_Bus1_0_1)
+2 flow(Source1_Bus1_0_2)
+10 flow(Source2_Bus1_0_0)
+10 flow(Source2_Bus1_0_1)
+10 flow(Source2_Bus1_0_2)

s.t.

c_e_equate_flows(0_0)_:
-1 flow(Bus1_Sink_0_0)
+2 flow(Source1_Bus1_0_0)
+2 flow(Source2_Bus1_0_0)
= 0

c_e_equate_flows(0_1)_:
-1 flow(Bus1_Sink_0_1)
+2 flow(Source1_Bus1_0_1)
+2 flow(Source2_Bus1_0_1)
= 0

c_e_equate_flows(0_2)_:
-1 flow(Bus1_Sink_0_2)
+2 flow(Source1_Bus1_0_2)
+2 flow(Source2_Bus1_0_2)
= 0

c_e_BusBlock_balance(Bus1_0_0)_:
-1 flow(Bus1_Sink_0_0)
+1 flow(Source1_Bus1_0_0)
+1 flow(Source2_Bus1_0_0)
= 0

c_e_BusBlock_balance(Bus1_0_1)_:
-1 flow(Bus1_Sink_0_1)
+1 flow(Source1_Bus1_0_1)
+1 flow(Source2_Bus1_0_1)
= 0

c_e_BusBlock_balance(Bus1_0_2)_:
-1 flow(Bus1_Sink_0_2)
+1 flow(Source1_Bus1_0_2)
+1 flow(Source2_Bus1_0_2)
= 0

bounds
   0 <= flow(Bus1_Sink_0_0) <= 300
   0 <= flow(Bus1_Sink_0_1) <= 300
   0 <= flow(Bus1_Sink_0_2) <= 300
   0 <= flow(Source1_Bus1_0_0) <= 400
   0 <= flow(Source1_Bus1_0_1) <= 400
   0 <= flow(Source1_Bus1_0_2) <= 400
   0 <= flow(Source2_Bus1_0_0) <= 200
   0 <= flow(Source2_Bus1_0_1) <= 200
   0 <= flow(Source2_Bus1_0_2) <= 200
end
