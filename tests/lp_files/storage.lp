\* Source Pyomo model name=OperationalModel *\

min 
objective:
+56 flow(electricityBus_storage_0)
+56 flow(electricityBus_storage_1)
+56 flow(electricityBus_storage_2)
+24 flow(storage_electricityBus_0)
+24 flow(storage_electricityBus_1)
+24 flow(storage_electricityBus_2)
+3500000 ONE_VAR_CONSTANT

s.t.

c_e_Bus_balance(electricityBus_0)_:
-1 flow(electricityBus_storage_0)
+1 flow(storage_electricityBus_0)
= 0

c_e_Bus_balance(electricityBus_1)_:
-1 flow(electricityBus_storage_1)
+1 flow(storage_electricityBus_1)
= 0

c_e_Bus_balance(electricityBus_2)_:
-1 flow(electricityBus_storage_2)
+1 flow(storage_electricityBus_2)
= 0

c_e_Storage_balance(storage_0)_:
+1 Storage_capacity(storage_0)
-0.87 Storage_capacity(storage_2)
-0.96999999999999997 flow(electricityBus_storage_0)
+1.1627906976744187 flow(storage_electricityBus_0)
= 0

c_e_Storage_balance(storage_1)_:
-0.87 Storage_capacity(storage_0)
+1 Storage_capacity(storage_1)
-0.96999999999999997 flow(electricityBus_storage_1)
+1.1627906976744187 flow(storage_electricityBus_1)
= 0

c_e_Storage_balance(storage_2)_:
-0.87 Storage_capacity(storage_1)
+1 Storage_capacity(storage_2)
-0.96999999999999997 flow(electricityBus_storage_2)
+1.1627906976744187 flow(storage_electricityBus_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(electricityBus_storage_0) <= 16666.666666666664
   0 <= flow(electricityBus_storage_1) <= 16666.666666666664
   0 <= flow(electricityBus_storage_2) <= 16666.666666666664
   0 <= flow(storage_electricityBus_0) <= 16666.666666666664
   0 <= flow(storage_electricityBus_1) <= 16666.666666666664
   0 <= flow(storage_electricityBus_2) <= 16666.666666666664
   0 <= Storage_capacity(storage_0) <= 100000
   0 <= Storage_capacity(storage_1) <= 100000
   0 <= Storage_capacity(storage_2) <= 100000
end
