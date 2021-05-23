\* Source Pyomo model name=MultiPeriodModel *\

min 
objective:
+56 flow(electricityBus_storage_no_invest_0_0)
+56 flow(electricityBus_storage_no_invest_0_1)
+54.901960784313722 flow(electricityBus_storage_no_invest_1_2)
+54.901960784313722 flow(electricityBus_storage_no_invest_1_3)
+53.825451749327179 flow(electricityBus_storage_no_invest_2_4)
+53.825451749327179 flow(electricityBus_storage_no_invest_2_5)
+24 flow(storage_no_invest_electricityBus_0_0)
+24 flow(storage_no_invest_electricityBus_0_1)
+23.52941176470588 flow(storage_no_invest_electricityBus_1_2)
+23.52941176470588 flow(storage_no_invest_electricityBus_1_3)
+23.068050749711649 flow(storage_no_invest_electricityBus_2_4)
+23.068050749711649 flow(storage_no_invest_electricityBus_2_5)

s.t.

c_e_MultiPeriodBus_balance(electricityBus_0_0)_:
-1 flow(electricityBus_storage_no_invest_0_0)
+1 flow(storage_no_invest_electricityBus_0_0)
= 0

c_e_MultiPeriodBus_balance(electricityBus_0_1)_:
-1 flow(electricityBus_storage_no_invest_0_1)
+1 flow(storage_no_invest_electricityBus_0_1)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_2)_:
-1 flow(electricityBus_storage_no_invest_1_2)
+1 flow(storage_no_invest_electricityBus_1_2)
= 0

c_e_MultiPeriodBus_balance(electricityBus_1_3)_:
-1 flow(electricityBus_storage_no_invest_1_3)
+1 flow(storage_no_invest_electricityBus_1_3)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_4)_:
-1 flow(electricityBus_storage_no_invest_2_4)
+1 flow(storage_no_invest_electricityBus_2_4)
= 0

c_e_MultiPeriodBus_balance(electricityBus_2_5)_:
-1 flow(electricityBus_storage_no_invest_2_5)
+1 flow(storage_no_invest_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodStorageBlock_balance_first(storage_no_invest)_:
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_0)
-0.96999999999999997 flow(electricityBus_storage_no_invest_0_0)
+1.1627906976744187 flow(storage_no_invest_electricityBus_0_0)
= 34800

c_e_GenericMultiPeriodStorageBlock_balance(storage_no_invest_0_1)_:
-0.87 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_0)
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_1)
-0.96999999999999997 flow(electricityBus_storage_no_invest_0_1)
+1.1627906976744187 flow(storage_no_invest_electricityBus_0_1)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage_no_invest_1_2)_:
-0.87 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_1)
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_2)
-0.96999999999999997 flow(electricityBus_storage_no_invest_1_2)
+1.1627906976744187 flow(storage_no_invest_electricityBus_1_2)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage_no_invest_1_3)_:
-0.87 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_2)
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_3)
-0.96999999999999997 flow(electricityBus_storage_no_invest_1_3)
+1.1627906976744187 flow(storage_no_invest_electricityBus_1_3)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage_no_invest_2_4)_:
-0.87 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_3)
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_4)
-0.96999999999999997 flow(electricityBus_storage_no_invest_2_4)
+1.1627906976744187 flow(storage_no_invest_electricityBus_2_4)
= 0

c_e_GenericMultiPeriodStorageBlock_balance(storage_no_invest_2_5)_:
-0.87 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_4)
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_5)
-0.96999999999999997 flow(electricityBus_storage_no_invest_2_5)
+1.1627906976744187 flow(storage_no_invest_electricityBus_2_5)
= 0

c_e_GenericMultiPeriodStorageBlock_balanced_cstr(storage_no_invest)_:
+1 GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_5)
= 40000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage_no_invest_0_0) <= 16667
   0 <= flow(electricityBus_storage_no_invest_0_1) <= 16667
   0 <= flow(electricityBus_storage_no_invest_1_2) <= 16667
   0 <= flow(electricityBus_storage_no_invest_1_3) <= 16667
   0 <= flow(electricityBus_storage_no_invest_2_4) <= 16667
   0 <= flow(electricityBus_storage_no_invest_2_5) <= 16667
   0 <= flow(storage_no_invest_electricityBus_0_0) <= 16667
   0 <= flow(storage_no_invest_electricityBus_0_1) <= 16667
   0 <= flow(storage_no_invest_electricityBus_1_2) <= 16667
   0 <= flow(storage_no_invest_electricityBus_1_3) <= 16667
   0 <= flow(storage_no_invest_electricityBus_2_4) <= 16667
   0 <= flow(storage_no_invest_electricityBus_2_5) <= 16667
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_0) <= 100000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_1) <= 100000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_2) <= 100000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_3) <= 100000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_4) <= 100000
   0 <= GenericMultiPeriodStorageBlock_storage_content(storage_no_invest_5) <= 100000
end
