\* Source Pyomo model name=Model *\

min 
objective:
+100 flow(gas_boiler_0_0)
+100 flow(gas_boiler_0_1)
+100 flow(gas_boiler_0_2)
+200.0 flow(gas_boiler_0_3)
+200.0 flow(gas_boiler_0_4)
+50.0 flow(gas_boiler_0_5)
+50.0 flow(gas_boiler_0_6)
+50.0 flow(gas_boiler_0_7)
+56 flow(heat_storage_0_0)
+56 flow(heat_storage_0_1)
+56 flow(heat_storage_0_2)
+112.0 flow(heat_storage_0_3)
+112.0 flow(heat_storage_0_4)
+28.0 flow(heat_storage_0_5)
+28.0 flow(heat_storage_0_6)
+28.0 flow(heat_storage_0_7)
+24 flow(storage_heat_0_0)
+24 flow(storage_heat_0_1)
+24 flow(storage_heat_0_2)
+48.0 flow(storage_heat_0_3)
+48.0 flow(storage_heat_0_4)
+12.0 flow(storage_heat_0_5)
+12.0 flow(storage_heat_0_6)
+12.0 flow(storage_heat_0_7)

s.t.

c_e_BusBlock_balance(heat_0_0)_:
-1 flow(heat_storage_0_0)
+1 flow(storage_heat_0_0)
+1 flow(boiler_heat_0_0)
= 0

c_e_BusBlock_balance(heat_0_1)_:
-1 flow(heat_storage_0_1)
+1 flow(storage_heat_0_1)
+1 flow(boiler_heat_0_1)
= 0

c_e_BusBlock_balance(heat_0_2)_:
-1 flow(heat_storage_0_2)
+1 flow(storage_heat_0_2)
+1 flow(boiler_heat_0_2)
= 0

c_e_BusBlock_balance(heat_0_3)_:
-1 flow(heat_storage_0_3)
+1 flow(storage_heat_0_3)
+1 flow(boiler_heat_0_3)
= 0

c_e_BusBlock_balance(heat_0_4)_:
-1 flow(heat_storage_0_4)
+1 flow(storage_heat_0_4)
+1 flow(boiler_heat_0_4)
= 0

c_e_BusBlock_balance(heat_0_5)_:
-1 flow(heat_storage_0_5)
+1 flow(storage_heat_0_5)
+1 flow(boiler_heat_0_5)
= 0

c_e_BusBlock_balance(heat_0_6)_:
-1 flow(heat_storage_0_6)
+1 flow(storage_heat_0_6)
+1 flow(boiler_heat_0_6)
= 0

c_e_BusBlock_balance(heat_0_7)_:
-1 flow(heat_storage_0_7)
+1 flow(storage_heat_0_7)
+1 flow(boiler_heat_0_7)
= 0

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_boiler_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_boiler_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_boiler_0_2)
= 0

c_e_BusBlock_balance(gas_0_3)_:
+1 flow(gas_boiler_0_3)
= 0

c_e_BusBlock_balance(gas_0_4)_:
+1 flow(gas_boiler_0_4)
= 0

c_e_BusBlock_balance(gas_0_5)_:
+1 flow(gas_boiler_0_5)
= 0

c_e_BusBlock_balance(gas_0_6)_:
+1 flow(gas_boiler_0_6)
= 0

c_e_BusBlock_balance(gas_0_7)_:
+1 flow(gas_boiler_0_7)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_0)_:
+1 flow(gas_boiler_0_0)
-1 flow(boiler_heat_0_0)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_1)_:
+1 flow(gas_boiler_0_1)
-1 flow(boiler_heat_0_1)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_2)_:
+1 flow(gas_boiler_0_2)
-1 flow(boiler_heat_0_2)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_3)_:
+1 flow(gas_boiler_0_3)
-1 flow(boiler_heat_0_3)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_4)_:
+1 flow(gas_boiler_0_4)
-1 flow(boiler_heat_0_4)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_5)_:
+1 flow(gas_boiler_0_5)
-1 flow(boiler_heat_0_5)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_6)_:
+1 flow(gas_boiler_0_6)
-1 flow(boiler_heat_0_6)
= 0

c_e_ConverterBlock_relation(boiler_gas_heat_0_7)_:
+1 flow(gas_boiler_0_7)
-1 flow(boiler_heat_0_7)
= 0

c_e_GenericStorageBlock_balance(storage_0_0)_:
-1 flow(heat_storage_0_0)
+1 flow(storage_heat_0_0)
+1 GenericStorageBlock_storage_content(storage_1)
= 270.0

c_e_GenericStorageBlock_balance(storage_0_1)_:
-1 flow(heat_storage_0_1)
+1 flow(storage_heat_0_1)
-0.9 GenericStorageBlock_storage_content(storage_1)
+1 GenericStorageBlock_storage_content(storage_2)
= 0

c_e_GenericStorageBlock_balance(storage_0_2)_:
-1 flow(heat_storage_0_2)
+1 flow(storage_heat_0_2)
-0.9 GenericStorageBlock_storage_content(storage_2)
+1 GenericStorageBlock_storage_content(storage_3)
= 0

c_e_GenericStorageBlock_balance(storage_0_3)_:
-2.0 flow(heat_storage_0_3)
+2.0 flow(storage_heat_0_3)
-0.81 GenericStorageBlock_storage_content(storage_3)
+1 GenericStorageBlock_storage_content(storage_4)
= 0

c_e_GenericStorageBlock_balance(storage_0_4)_:
-2.0 flow(heat_storage_0_4)
+2.0 flow(storage_heat_0_4)
-0.81 GenericStorageBlock_storage_content(storage_4)
+1 GenericStorageBlock_storage_content(storage_5)
= 0

c_e_GenericStorageBlock_balance(storage_0_5)_:
-0.5 flow(heat_storage_0_5)
+0.5 flow(storage_heat_0_5)
-0.9486832980505138 GenericStorageBlock_storage_content(storage_5)
+1 GenericStorageBlock_storage_content(storage_6)
= 0

c_e_GenericStorageBlock_balance(storage_0_6)_:
-0.5 flow(heat_storage_0_6)
+0.5 flow(storage_heat_0_6)
-0.9486832980505138 GenericStorageBlock_storage_content(storage_6)
+1 GenericStorageBlock_storage_content(storage_7)
= 0

c_e_GenericStorageBlock_balance(storage_0_7)_:
-0.5 flow(heat_storage_0_7)
+0.5 flow(storage_heat_0_7)
-0.9486832980505138 GenericStorageBlock_storage_content(storage_7)
+1 GenericStorageBlock_storage_content(storage_8)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage)_:
+1 GenericStorageBlock_storage_content(storage_8)
= 300

bounds
   0 <= flow(gas_boiler_0_0) <= +inf
   0 <= flow(gas_boiler_0_1) <= +inf
   0 <= flow(gas_boiler_0_2) <= +inf
   0 <= flow(gas_boiler_0_3) <= +inf
   0 <= flow(gas_boiler_0_4) <= +inf
   0 <= flow(gas_boiler_0_5) <= +inf
   0 <= flow(gas_boiler_0_6) <= +inf
   0 <= flow(gas_boiler_0_7) <= +inf
   0 <= flow(heat_storage_0_0) <= 100
   0 <= flow(heat_storage_0_1) <= 100
   0 <= flow(heat_storage_0_2) <= 100
   0 <= flow(heat_storage_0_3) <= 100
   0 <= flow(heat_storage_0_4) <= 100
   0 <= flow(heat_storage_0_5) <= 100
   0 <= flow(heat_storage_0_6) <= 100
   0 <= flow(heat_storage_0_7) <= 100
   0 <= flow(storage_heat_0_0) <= 100
   0 <= flow(storage_heat_0_1) <= 100
   0 <= flow(storage_heat_0_2) <= 100
   0 <= flow(storage_heat_0_3) <= 100
   0 <= flow(storage_heat_0_4) <= 100
   0 <= flow(storage_heat_0_5) <= 100
   0 <= flow(storage_heat_0_6) <= 100
   0 <= flow(storage_heat_0_7) <= 100
   0 <= flow(boiler_heat_0_0) <= 200
   0 <= flow(boiler_heat_0_1) <= 200
   0 <= flow(boiler_heat_0_2) <= 200
   0 <= flow(boiler_heat_0_3) <= 200
   0 <= flow(boiler_heat_0_4) <= 200
   0 <= flow(boiler_heat_0_5) <= 200
   0 <= flow(boiler_heat_0_6) <= 200
   0 <= flow(boiler_heat_0_7) <= 200
   0 <= GenericStorageBlock_storage_content(storage_1) <= 300
   0 <= GenericStorageBlock_storage_content(storage_2) <= 300
   0 <= GenericStorageBlock_storage_content(storage_3) <= 300
   0 <= GenericStorageBlock_storage_content(storage_4) <= 300
   0 <= GenericStorageBlock_storage_content(storage_5) <= 300
   0 <= GenericStorageBlock_storage_content(storage_6) <= 300
   0 <= GenericStorageBlock_storage_content(storage_7) <= 300
   0 <= GenericStorageBlock_storage_content(storage_8) <= 300
end
