\* Source Pyomo model name=Model *\

min 
objective:
+0.0 ONE_VAR_CONSTANT

s.t.

c_e_limit_storage_constraint(0)_:
+0.5 GenericStorageBlock_storage_content(storage1_0)
+1.25 GenericStorageBlock_storage_content(storage2_0)
-1 limit_storage(0)
= 0

c_e_limit_storage_constraint(1)_:
+0.5 GenericStorageBlock_storage_content(storage1_1)
+1.25 GenericStorageBlock_storage_content(storage2_1)
-1 limit_storage(1)
= 0

c_e_limit_storage_constraint(2)_:
+0.5 GenericStorageBlock_storage_content(storage1_2)
+1.25 GenericStorageBlock_storage_content(storage2_2)
-1 limit_storage(2)
= 0

c_e_limit_storage_constraint(3)_:
+0.5 GenericStorageBlock_storage_content(storage1_3)
+1.25 GenericStorageBlock_storage_content(storage2_3)
-1 limit_storage(3)
= 0

c_e_limit_storage_constraint(4)_:
+0.5 GenericStorageBlock_storage_content(storage1_4)
+1.25 GenericStorageBlock_storage_content(storage2_4)
-1 limit_storage(4)
= 0

c_e_limit_storage_constraint(5)_:
+0.5 GenericStorageBlock_storage_content(storage1_5)
+1.25 GenericStorageBlock_storage_content(storage2_5)
-1 limit_storage(5)
= 0

c_e_BusBlock_balance(bus_0_0)_:
+1 flow(storage1_bus_0_0)
+1 flow(storage2_bus_0_0)
-1 flow(bus_storage1_0_0)
-1 flow(bus_storage2_0_0)
= 0

c_e_BusBlock_balance(bus_0_1)_:
+1 flow(storage1_bus_0_1)
+1 flow(storage2_bus_0_1)
-1 flow(bus_storage1_0_1)
-1 flow(bus_storage2_0_1)
= 0

c_e_BusBlock_balance(bus_1_2)_:
+1 flow(storage1_bus_1_2)
+1 flow(storage2_bus_1_2)
-1 flow(bus_storage1_1_2)
-1 flow(bus_storage2_1_2)
= 0

c_e_BusBlock_balance(bus_1_3)_:
+1 flow(storage1_bus_1_3)
+1 flow(storage2_bus_1_3)
-1 flow(bus_storage1_1_3)
-1 flow(bus_storage2_1_3)
= 0

c_e_BusBlock_balance(bus_2_4)_:
+1 flow(storage1_bus_2_4)
+1 flow(storage2_bus_2_4)
-1 flow(bus_storage1_2_4)
-1 flow(bus_storage2_2_4)
= 0

c_e_BusBlock_balance(bus_2_5)_:
+1 flow(storage1_bus_2_5)
+1 flow(storage2_bus_2_5)
-1 flow(bus_storage1_2_5)
-1 flow(bus_storage2_2_5)
= 0

c_e_GenericStorageBlock_balance(storage1_0_0)_:
-1 GenericStorageBlock_storage_content(storage1_0)
+1 GenericStorageBlock_storage_content(storage1_1)
+1 flow(storage1_bus_0_0)
-1 flow(bus_storage1_0_0)
= 0

c_e_GenericStorageBlock_balance(storage1_0_1)_:
-1 GenericStorageBlock_storage_content(storage1_1)
+1 GenericStorageBlock_storage_content(storage1_2)
+1 flow(storage1_bus_0_1)
-1 flow(bus_storage1_0_1)
= 0

c_e_GenericStorageBlock_balance(storage1_1_2)_:
-1 GenericStorageBlock_storage_content(storage1_2)
+1 GenericStorageBlock_storage_content(storage1_3)
+1 flow(storage1_bus_1_2)
-1 flow(bus_storage1_1_2)
= 0

c_e_GenericStorageBlock_balance(storage1_1_3)_:
-1 GenericStorageBlock_storage_content(storage1_3)
+1 GenericStorageBlock_storage_content(storage1_4)
+1 flow(storage1_bus_1_3)
-1 flow(bus_storage1_1_3)
= 0

c_e_GenericStorageBlock_balance(storage1_2_4)_:
-1 GenericStorageBlock_storage_content(storage1_4)
+1 GenericStorageBlock_storage_content(storage1_5)
+1 flow(storage1_bus_2_4)
-1 flow(bus_storage1_2_4)
= 0

c_e_GenericStorageBlock_balance(storage1_2_5)_:
-1 GenericStorageBlock_storage_content(storage1_5)
+1 flow(storage1_bus_2_5)
-1 flow(bus_storage1_2_5)
+1 GenericStorageBlock_storage_content(storage1_6)
= 0

c_e_GenericStorageBlock_balance(storage2_0_0)_:
-1 GenericStorageBlock_storage_content(storage2_0)
+1 GenericStorageBlock_storage_content(storage2_1)
+1 flow(storage2_bus_0_0)
-1 flow(bus_storage2_0_0)
= 0

c_e_GenericStorageBlock_balance(storage2_0_1)_:
-1 GenericStorageBlock_storage_content(storage2_1)
+1 GenericStorageBlock_storage_content(storage2_2)
+1 flow(storage2_bus_0_1)
-1 flow(bus_storage2_0_1)
= 0

c_e_GenericStorageBlock_balance(storage2_1_2)_:
-1 GenericStorageBlock_storage_content(storage2_2)
+1 GenericStorageBlock_storage_content(storage2_3)
+1 flow(storage2_bus_1_2)
-1 flow(bus_storage2_1_2)
= 0

c_e_GenericStorageBlock_balance(storage2_1_3)_:
-1 GenericStorageBlock_storage_content(storage2_3)
+1 GenericStorageBlock_storage_content(storage2_4)
+1 flow(storage2_bus_1_3)
-1 flow(bus_storage2_1_3)
= 0

c_e_GenericStorageBlock_balance(storage2_2_4)_:
-1 GenericStorageBlock_storage_content(storage2_4)
+1 GenericStorageBlock_storage_content(storage2_5)
+1 flow(storage2_bus_2_4)
-1 flow(bus_storage2_2_4)
= 0

c_e_GenericStorageBlock_balance(storage2_2_5)_:
-1 GenericStorageBlock_storage_content(storage2_5)
+1 flow(storage2_bus_2_5)
-1 flow(bus_storage2_2_5)
+1 GenericStorageBlock_storage_content(storage2_6)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage1)_:
-1 GenericStorageBlock_storage_content(storage1_0)
+1 GenericStorageBlock_storage_content(storage1_6)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage2)_:
-1 GenericStorageBlock_storage_content(storage2_0)
+1 GenericStorageBlock_storage_content(storage2_6)
= 0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= GenericStorageBlock_storage_content(storage1_0) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_0) <= 5
   0 <= limit_storage(0) <= 7
   0 <= GenericStorageBlock_storage_content(storage1_1) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_1) <= 5
   0 <= limit_storage(1) <= 7
   0 <= GenericStorageBlock_storage_content(storage1_2) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_2) <= 5
   0 <= limit_storage(2) <= 7
   0 <= GenericStorageBlock_storage_content(storage1_3) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_3) <= 5
   0 <= limit_storage(3) <= 7
   0 <= GenericStorageBlock_storage_content(storage1_4) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_4) <= 5
   0 <= limit_storage(4) <= 7
   0 <= GenericStorageBlock_storage_content(storage1_5) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_5) <= 5
   0 <= limit_storage(5) <= 7
   0 <= flow(storage1_bus_0_0) <= +inf
   0 <= flow(storage2_bus_0_0) <= +inf
   0 <= flow(bus_storage1_0_0) <= +inf
   0 <= flow(bus_storage2_0_0) <= +inf
   0 <= flow(storage1_bus_0_1) <= +inf
   0 <= flow(storage2_bus_0_1) <= +inf
   0 <= flow(bus_storage1_0_1) <= +inf
   0 <= flow(bus_storage2_0_1) <= +inf
   0 <= flow(storage1_bus_1_2) <= +inf
   0 <= flow(storage2_bus_1_2) <= +inf
   0 <= flow(bus_storage1_1_2) <= +inf
   0 <= flow(bus_storage2_1_2) <= +inf
   0 <= flow(storage1_bus_1_3) <= +inf
   0 <= flow(storage2_bus_1_3) <= +inf
   0 <= flow(bus_storage1_1_3) <= +inf
   0 <= flow(bus_storage2_1_3) <= +inf
   0 <= flow(storage1_bus_2_4) <= +inf
   0 <= flow(storage2_bus_2_4) <= +inf
   0 <= flow(bus_storage1_2_4) <= +inf
   0 <= flow(bus_storage2_2_4) <= +inf
   0 <= flow(storage1_bus_2_5) <= +inf
   0 <= flow(storage2_bus_2_5) <= +inf
   0 <= flow(bus_storage1_2_5) <= +inf
   0 <= flow(bus_storage2_2_5) <= +inf
   0 <= GenericStorageBlock_storage_content(storage1_6) <= 5
   0 <= GenericStorageBlock_storage_content(storage2_6) <= 5
end
