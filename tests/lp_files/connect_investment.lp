\* Source Pyomo model name=Model *\

min 
objective:
+145 GenericInvestmentStorageBlock_invest(storage_constraint)
+500 InvestmentFlow_invest(Bus1_Sink)
+123 InvestmentFlow_invest(Source_Bus1)

s.t.

c_e_equate_InvestmentFlow_invest(Source_Bus1)_InvestmentFlow_invest(Bus1_Sink)_:
-1 InvestmentFlow_invest(Bus1_Sink)
+2 InvestmentFlow_invest(Source_Bus1)
= 0

c_e_equate_InvestmentFlow_invest(Source_Bus1)_GenericInvestmentStorageBlock_invest(storage_constraint)_:
-1 GenericInvestmentStorageBlock_invest(storage_constraint)
+1 InvestmentFlow_invest(Source_Bus1)
= 0

c_e_Bus_balance(Bus1_0)_:
-1 flow(Bus1_Sink_0)
-1 flow(Bus1_storage_constraint_0)
+1 flow(Source_Bus1_0)
+1 flow(storage_constraint_Bus1_0)
= 0

c_e_Bus_balance(Bus1_1)_:
-1 flow(Bus1_Sink_1)
-1 flow(Bus1_storage_constraint_1)
+1 flow(Source_Bus1_1)
+1 flow(storage_constraint_Bus1_1)
= 0

c_e_Bus_balance(Bus1_2)_:
-1 flow(Bus1_Sink_2)
-1 flow(Bus1_storage_constraint_2)
+1 flow(Source_Bus1_2)
+1 flow(storage_constraint_Bus1_2)
= 0

c_u_InvestmentFlow_max(Bus1_Sink_0)_:
-1 InvestmentFlow_invest(Bus1_Sink)
+1 flow(Bus1_Sink_0)
<= 0

c_u_InvestmentFlow_max(Bus1_Sink_1)_:
-1 InvestmentFlow_invest(Bus1_Sink)
+1 flow(Bus1_Sink_1)
<= 0

c_u_InvestmentFlow_max(Bus1_Sink_2)_:
-1 InvestmentFlow_invest(Bus1_Sink)
+1 flow(Bus1_Sink_2)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_constraint_0)_:
-1 InvestmentFlow_invest(Bus1_storage_constraint)
+1 flow(Bus1_storage_constraint_0)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_constraint_1)_:
-1 InvestmentFlow_invest(Bus1_storage_constraint)
+1 flow(Bus1_storage_constraint_1)
<= 0

c_u_InvestmentFlow_max(Bus1_storage_constraint_2)_:
-1 InvestmentFlow_invest(Bus1_storage_constraint)
+1 flow(Bus1_storage_constraint_2)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_0)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_0)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_1)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_1)
<= 0

c_u_InvestmentFlow_max(Source_Bus1_2)_:
-1 InvestmentFlow_invest(Source_Bus1)
+1 flow(Source_Bus1_2)
<= 0

c_u_InvestmentFlow_max(storage_constraint_Bus1_0)_:
-1 InvestmentFlow_invest(storage_constraint_Bus1)
+1 flow(storage_constraint_Bus1_0)
<= 0

c_u_InvestmentFlow_max(storage_constraint_Bus1_1)_:
-1 InvestmentFlow_invest(storage_constraint_Bus1)
+1 flow(storage_constraint_Bus1_1)
<= 0

c_u_InvestmentFlow_max(storage_constraint_Bus1_2)_:
-1 InvestmentFlow_invest(storage_constraint_Bus1)
+1 flow(storage_constraint_Bus1_2)
<= 0

c_e_GenericInvestmentStorageBlock_balance(storage_constraint_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_0)
-1 GenericInvestmentStorageBlock_capacity(storage_constraint_2)
-1 flow(Bus1_storage_constraint_0)
+1 flow(storage_constraint_Bus1_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_constraint_1)_:
-1 GenericInvestmentStorageBlock_capacity(storage_constraint_0)
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_1)
-1 flow(Bus1_storage_constraint_1)
+1 flow(storage_constraint_Bus1_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_constraint_2)_:
-1 GenericInvestmentStorageBlock_capacity(storage_constraint_1)
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_2)
-1 flow(Bus1_storage_constraint_2)
+1 flow(storage_constraint_Bus1_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_constraint)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_constraint)
+1 InvestmentFlow_invest(Bus1_storage_constraint)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_constraint)_:
-0.20000000000000001 GenericInvestmentStorageBlock_invest(storage_constraint)
+1 InvestmentFlow_invest(storage_constraint_Bus1)
= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_constraint_0)_:
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_0)
-1 GenericInvestmentStorageBlock_invest(storage_constraint)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_constraint_1)_:
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_1)
-1 GenericInvestmentStorageBlock_invest(storage_constraint)
<= 0

c_u_GenericInvestmentStorageBlock_max_capacity(storage_constraint_2)_:
+1 GenericInvestmentStorageBlock_capacity(storage_constraint_2)
-1 GenericInvestmentStorageBlock_invest(storage_constraint)
<= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(Bus1_Sink_0) <= +inf
   0 <= flow(Bus1_Sink_1) <= +inf
   0 <= flow(Bus1_Sink_2) <= +inf
   0 <= flow(Bus1_storage_constraint_0) <= +inf
   0 <= flow(Bus1_storage_constraint_1) <= +inf
   0 <= flow(Bus1_storage_constraint_2) <= +inf
   0 <= flow(Source_Bus1_0) <= +inf
   0 <= flow(Source_Bus1_1) <= +inf
   0 <= flow(Source_Bus1_2) <= +inf
   0 <= flow(storage_constraint_Bus1_0) <= +inf
   0 <= flow(storage_constraint_Bus1_1) <= +inf
   0 <= flow(storage_constraint_Bus1_2) <= +inf
   0 <= InvestmentFlow_invest(Bus1_Sink) <= +inf
   0 <= InvestmentFlow_invest(Bus1_storage_constraint) <= +inf
   0 <= InvestmentFlow_invest(Source_Bus1) <= +inf
   0 <= InvestmentFlow_invest(storage_constraint_Bus1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_constraint_0) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_constraint_1) <= +inf
   0 <= GenericInvestmentStorageBlock_capacity(storage_constraint_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_constraint) <= +inf
end
