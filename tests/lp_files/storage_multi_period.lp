\* Source Pyomo model name=Model *\

min 
objective:
+56 flow(electricityBus_storage_no_invest_0)
+56 flow(electricityBus_storage_no_invest_1)
+54.90196078431372 flow(electricityBus_storage_no_invest_2)
+54.90196078431372 flow(electricityBus_storage_no_invest_3)
+53.82545174932718 flow(electricityBus_storage_no_invest_4)
+53.82545174932718 flow(electricityBus_storage_no_invest_5)
+24 flow(storage_no_invest_electricityBus_0)
+24 flow(storage_no_invest_electricityBus_1)
+23.52941176470588 flow(storage_no_invest_electricityBus_2)
+23.52941176470588 flow(storage_no_invest_electricityBus_3)
+23.06805074971165 flow(storage_no_invest_electricityBus_4)
+23.06805074971165 flow(storage_no_invest_electricityBus_5)

s.t.

c_e_BusBlock_balance(electricityBus_0)_:
-1 flow(electricityBus_storage_no_invest_0)
+1 flow(storage_no_invest_electricityBus_0)
= 0

c_e_BusBlock_balance(electricityBus_1)_:
-1 flow(electricityBus_storage_no_invest_1)
+1 flow(storage_no_invest_electricityBus_1)
= 0

c_e_BusBlock_balance(electricityBus_2)_:
-1 flow(electricityBus_storage_no_invest_2)
+1 flow(storage_no_invest_electricityBus_2)
= 0

c_e_BusBlock_balance(electricityBus_3)_:
-1 flow(electricityBus_storage_no_invest_3)
+1 flow(storage_no_invest_electricityBus_3)
= 0

c_e_BusBlock_balance(electricityBus_4)_:
-1 flow(electricityBus_storage_no_invest_4)
+1 flow(storage_no_invest_electricityBus_4)
= 0

c_e_BusBlock_balance(electricityBus_5)_:
-1 flow(electricityBus_storage_no_invest_5)
+1 flow(storage_no_invest_electricityBus_5)
= 0

c_e_GenericStorageBlock_balance(storage_no_invest_0)_:
-0.97 flow(electricityBus_storage_no_invest_0)
+1.1627906976744187 flow(storage_no_invest_electricityBus_0)
+1 GenericStorageBlock_storage_content(storage_no_invest_1)
= 34800.0

c_e_GenericStorageBlock_balance(storage_no_invest_1)_:
-0.97 flow(electricityBus_storage_no_invest_1)
+1.1627906976744187 flow(storage_no_invest_electricityBus_1)
-0.87 GenericStorageBlock_storage_content(storage_no_invest_1)
+1 GenericStorageBlock_storage_content(storage_no_invest_2)
= 0

c_e_GenericStorageBlock_balance(storage_no_invest_2)_:
-0.97 flow(electricityBus_storage_no_invest_2)
+1.1627906976744187 flow(storage_no_invest_electricityBus_2)
-0.87 GenericStorageBlock_storage_content(storage_no_invest_2)
+1 GenericStorageBlock_storage_content(storage_no_invest_3)
= 0

c_e_GenericStorageBlock_balance(storage_no_invest_3)_:
-0.97 flow(electricityBus_storage_no_invest_3)
+1.1627906976744187 flow(storage_no_invest_electricityBus_3)
-0.87 GenericStorageBlock_storage_content(storage_no_invest_3)
+1 GenericStorageBlock_storage_content(storage_no_invest_4)
= 0

c_e_GenericStorageBlock_balance(storage_no_invest_4)_:
-0.97 flow(electricityBus_storage_no_invest_4)
+1.1627906976744187 flow(storage_no_invest_electricityBus_4)
-0.87 GenericStorageBlock_storage_content(storage_no_invest_4)
+1 GenericStorageBlock_storage_content(storage_no_invest_5)
= 0

c_e_GenericStorageBlock_balance(storage_no_invest_5)_:
-0.97 flow(electricityBus_storage_no_invest_5)
+1.1627906976744187 flow(storage_no_invest_electricityBus_5)
-0.87 GenericStorageBlock_storage_content(storage_no_invest_5)
+1 GenericStorageBlock_storage_content(storage_no_invest_6)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage_no_invest)_:
+1 GenericStorageBlock_storage_content(storage_no_invest_6)
= 40000.0

bounds
   0 <= flow(electricityBus_storage_no_invest_0) <= 16667
   0 <= flow(electricityBus_storage_no_invest_1) <= 16667
   0 <= flow(electricityBus_storage_no_invest_2) <= 16667
   0 <= flow(electricityBus_storage_no_invest_3) <= 16667
   0 <= flow(electricityBus_storage_no_invest_4) <= 16667
   0 <= flow(electricityBus_storage_no_invest_5) <= 16667
   0 <= flow(storage_no_invest_electricityBus_0) <= 16667
   0 <= flow(storage_no_invest_electricityBus_1) <= 16667
   0 <= flow(storage_no_invest_electricityBus_2) <= 16667
   0 <= flow(storage_no_invest_electricityBus_3) <= 16667
   0 <= flow(storage_no_invest_electricityBus_4) <= 16667
   0 <= flow(storage_no_invest_electricityBus_5) <= 16667
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_1) <= 100000.0
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_2) <= 100000.0
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_3) <= 100000.0
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_4) <= 100000.0
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_5) <= 100000.0
   0.0 <= GenericStorageBlock_storage_content(storage_no_invest_6) <= 100000.0
end
