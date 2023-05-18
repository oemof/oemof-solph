\* Source Pyomo model name=CellularModel *\

min 
objective:
+5 flow(source_el_ec_1_2_bus_el_ec_1_2_0)
+5 flow(source_el_ec_1_2_bus_el_ec_1_2_1)
+5 flow(source_el_ec_1_2_bus_el_ec_1_2_2)
+5 flow(source_el_ec_1_bus_el_ec_1_0)
+5 flow(source_el_ec_1_bus_el_ec_1_1)
+5 flow(source_el_ec_1_bus_el_ec_1_2)
+10 flow(source_el_ec_2_1_bus_el_ec_2_1_0)
+10 flow(source_el_ec_2_1_bus_el_ec_2_1_1)
+10 flow(source_el_ec_2_1_bus_el_ec_2_1_2)
+10 flow(source_el_ec_2_2_bus_el_ec_2_2_0)
+10 flow(source_el_ec_2_2_bus_el_ec_2_2_1)
+10 flow(source_el_ec_2_2_bus_el_ec_2_2_2)
+5 flow(source_el_ec_2_bus_el_ec_2_0)
+5 flow(source_el_ec_2_bus_el_ec_2_1)
+5 flow(source_el_ec_2_bus_el_ec_2_2)

s.t.

c_e_BusBlock_balance(bus_el_ec_1_0)_:
-1 flow(bus_el_ec_1_connector_el_ec_1_0)
-1 flow(bus_el_ec_1_connector_el_ec_1_1_0)
-1 flow(bus_el_ec_1_connector_el_ec_1_2_0)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_0)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_0)
+1 flow(connector_el_ec_1_bus_el_ec_1_0)
+1 flow(source_el_ec_1_bus_el_ec_1_0)
= 10

c_e_BusBlock_balance(bus_el_ec_1_1)_:
-1 flow(bus_el_ec_1_connector_el_ec_1_1)
-1 flow(bus_el_ec_1_connector_el_ec_1_1_1)
-1 flow(bus_el_ec_1_connector_el_ec_1_2_1)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_1)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_1)
+1 flow(connector_el_ec_1_bus_el_ec_1_1)
+1 flow(source_el_ec_1_bus_el_ec_1_1)
= 10

c_e_BusBlock_balance(bus_el_ec_1_2)_:
-1 flow(bus_el_ec_1_connector_el_ec_1_1_2)
-1 flow(bus_el_ec_1_connector_el_ec_1_2)
-1 flow(bus_el_ec_1_connector_el_ec_1_2_2)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_2)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_2)
+1 flow(connector_el_ec_1_bus_el_ec_1_2)
+1 flow(source_el_ec_1_bus_el_ec_1_2)
= 10

c_e_BusBlock_balance(bus_el_ec_1_1_0)_:
-1 flow(bus_el_ec_1_1_connector_el_ec_1_1_0)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_1_0)
+1 flow(source_el_ec_1_1_bus_el_ec_1_1_0)
= 10

c_e_BusBlock_balance(bus_el_ec_1_1_1)_:
-1 flow(bus_el_ec_1_1_connector_el_ec_1_1_1)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_1_1)
+1 flow(source_el_ec_1_1_bus_el_ec_1_1_1)
= 10

c_e_BusBlock_balance(bus_el_ec_1_1_2)_:
-1 flow(bus_el_ec_1_1_connector_el_ec_1_1_2)
+1 flow(connector_el_ec_1_1_bus_el_ec_1_1_2)
+1 flow(source_el_ec_1_1_bus_el_ec_1_1_2)
= 10

c_e_BusBlock_balance(bus_el_ec_1_2_0)_:
-1 flow(bus_el_ec_1_2_connector_el_ec_1_2_0)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_2_0)
+1 flow(source_el_ec_1_2_bus_el_ec_1_2_0)
= 10

c_e_BusBlock_balance(bus_el_ec_1_2_1)_:
-1 flow(bus_el_ec_1_2_connector_el_ec_1_2_1)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_2_1)
+1 flow(source_el_ec_1_2_bus_el_ec_1_2_1)
= 10

c_e_BusBlock_balance(bus_el_ec_1_2_2)_:
-1 flow(bus_el_ec_1_2_connector_el_ec_1_2_2)
+1 flow(connector_el_ec_1_2_bus_el_ec_1_2_2)
+1 flow(source_el_ec_1_2_bus_el_ec_1_2_2)
= 10

c_e_BusBlock_balance(bus_el_ec_2_0)_:
-1 flow(bus_el_ec_2_connector_el_ec_2_0)
-1 flow(bus_el_ec_2_connector_el_ec_2_1_0)
-1 flow(bus_el_ec_2_connector_el_ec_2_2_0)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_0)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_0)
+1 flow(connector_el_ec_2_bus_el_ec_2_0)
+1 flow(source_el_ec_2_bus_el_ec_2_0)
= 10

c_e_BusBlock_balance(bus_el_ec_2_1)_:
-1 flow(bus_el_ec_2_connector_el_ec_2_1)
-1 flow(bus_el_ec_2_connector_el_ec_2_1_1)
-1 flow(bus_el_ec_2_connector_el_ec_2_2_1)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_1)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_1)
+1 flow(connector_el_ec_2_bus_el_ec_2_1)
+1 flow(source_el_ec_2_bus_el_ec_2_1)
= 10

c_e_BusBlock_balance(bus_el_ec_2_2)_:
-1 flow(bus_el_ec_2_connector_el_ec_2_1_2)
-1 flow(bus_el_ec_2_connector_el_ec_2_2)
-1 flow(bus_el_ec_2_connector_el_ec_2_2_2)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_2)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_2)
+1 flow(connector_el_ec_2_bus_el_ec_2_2)
+1 flow(source_el_ec_2_bus_el_ec_2_2)
= 10

c_e_BusBlock_balance(bus_el_ec_2_1_0)_:
-1 flow(bus_el_ec_2_1_connector_el_ec_2_1_0)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_1_0)
+1 flow(source_el_ec_2_1_bus_el_ec_2_1_0)
= 10

c_e_BusBlock_balance(bus_el_ec_2_1_1)_:
-1 flow(bus_el_ec_2_1_connector_el_ec_2_1_1)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_1_1)
+1 flow(source_el_ec_2_1_bus_el_ec_2_1_1)
= 10

c_e_BusBlock_balance(bus_el_ec_2_1_2)_:
-1 flow(bus_el_ec_2_1_connector_el_ec_2_1_2)
+1 flow(connector_el_ec_2_1_bus_el_ec_2_1_2)
+1 flow(source_el_ec_2_1_bus_el_ec_2_1_2)
= 10

c_e_BusBlock_balance(bus_el_ec_2_2_0)_:
-1 flow(bus_el_ec_2_2_connector_el_ec_2_2_0)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_2_0)
+1 flow(source_el_ec_2_2_bus_el_ec_2_2_0)
= 10

c_e_BusBlock_balance(bus_el_ec_2_2_1)_:
-1 flow(bus_el_ec_2_2_connector_el_ec_2_2_1)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_2_1)
+1 flow(source_el_ec_2_2_bus_el_ec_2_2_1)
= 10

c_e_BusBlock_balance(bus_el_ec_2_2_2)_:
-1 flow(bus_el_ec_2_2_connector_el_ec_2_2_2)
+1 flow(connector_el_ec_2_2_bus_el_ec_2_2_2)
+1 flow(source_el_ec_2_2_bus_el_ec_2_2_2)
= 10

c_e_BusBlock_balance(bus_el_es_0)_:
-1 flow(bus_el_es_connector_el_ec_1_0)
-1 flow(bus_el_es_connector_el_ec_2_0)
+1 flow(connector_el_ec_1_bus_el_es_0)
+1 flow(connector_el_ec_2_bus_el_es_0)
= 0

c_e_BusBlock_balance(bus_el_es_1)_:
-1 flow(bus_el_es_connector_el_ec_1_1)
-1 flow(bus_el_es_connector_el_ec_2_1)
+1 flow(connector_el_ec_1_bus_el_es_1)
+1 flow(connector_el_ec_2_bus_el_es_1)
= 0

c_e_BusBlock_balance(bus_el_es_2)_:
-1 flow(bus_el_es_connector_el_ec_1_2)
-1 flow(bus_el_es_connector_el_ec_2_2)
+1 flow(connector_el_ec_1_bus_el_es_2)
+1 flow(connector_el_ec_2_bus_el_es_2)
= 0

c_e_BusBlock_balance(connector_el_ec_1_0)_:
+1 flow(bus_el_ec_1_connector_el_ec_1_0)
+1 flow(bus_el_es_connector_el_ec_1_0)
-1 flow(connector_el_ec_1_bus_el_ec_1_0)
-1 flow(connector_el_ec_1_bus_el_es_0)
= 0

c_e_BusBlock_balance(connector_el_ec_1_1)_:
+1 flow(bus_el_ec_1_connector_el_ec_1_1)
+1 flow(bus_el_es_connector_el_ec_1_1)
-1 flow(connector_el_ec_1_bus_el_ec_1_1)
-1 flow(connector_el_ec_1_bus_el_es_1)
= 0

c_e_BusBlock_balance(connector_el_ec_1_2)_:
+1 flow(bus_el_ec_1_connector_el_ec_1_2)
+1 flow(bus_el_es_connector_el_ec_1_2)
-1 flow(connector_el_ec_1_bus_el_ec_1_2)
-1 flow(connector_el_ec_1_bus_el_es_2)
= 0

c_e_BusBlock_balance(connector_el_ec_1_1_0)_:
+1 flow(bus_el_ec_1_1_connector_el_ec_1_1_0)
+1 flow(bus_el_ec_1_connector_el_ec_1_1_0)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_0)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_1_0)
= 0

c_e_BusBlock_balance(connector_el_ec_1_1_1)_:
+1 flow(bus_el_ec_1_1_connector_el_ec_1_1_1)
+1 flow(bus_el_ec_1_connector_el_ec_1_1_1)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_1)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_1_1)
= 0

c_e_BusBlock_balance(connector_el_ec_1_1_2)_:
+1 flow(bus_el_ec_1_1_connector_el_ec_1_1_2)
+1 flow(bus_el_ec_1_connector_el_ec_1_1_2)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_1_2)
-1 flow(connector_el_ec_1_1_bus_el_ec_1_2)
= 0

c_e_BusBlock_balance(connector_el_ec_1_2_0)_:
+1 flow(bus_el_ec_1_2_connector_el_ec_1_2_0)
+1 flow(bus_el_ec_1_connector_el_ec_1_2_0)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_0)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_2_0)
= 0

c_e_BusBlock_balance(connector_el_ec_1_2_1)_:
+1 flow(bus_el_ec_1_2_connector_el_ec_1_2_1)
+1 flow(bus_el_ec_1_connector_el_ec_1_2_1)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_1)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_2_1)
= 0

c_e_BusBlock_balance(connector_el_ec_1_2_2)_:
+1 flow(bus_el_ec_1_2_connector_el_ec_1_2_2)
+1 flow(bus_el_ec_1_connector_el_ec_1_2_2)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_2)
-1 flow(connector_el_ec_1_2_bus_el_ec_1_2_2)
= 0

c_e_BusBlock_balance(connector_el_ec_2_0)_:
+1 flow(bus_el_ec_2_connector_el_ec_2_0)
+1 flow(bus_el_es_connector_el_ec_2_0)
-1 flow(connector_el_ec_2_bus_el_ec_2_0)
-1 flow(connector_el_ec_2_bus_el_es_0)
= 0

c_e_BusBlock_balance(connector_el_ec_2_1)_:
+1 flow(bus_el_ec_2_connector_el_ec_2_1)
+1 flow(bus_el_es_connector_el_ec_2_1)
-1 flow(connector_el_ec_2_bus_el_ec_2_1)
-1 flow(connector_el_ec_2_bus_el_es_1)
= 0

c_e_BusBlock_balance(connector_el_ec_2_2)_:
+1 flow(bus_el_ec_2_connector_el_ec_2_2)
+1 flow(bus_el_es_connector_el_ec_2_2)
-1 flow(connector_el_ec_2_bus_el_ec_2_2)
-1 flow(connector_el_ec_2_bus_el_es_2)
= 0

c_e_BusBlock_balance(connector_el_ec_2_1_0)_:
+1 flow(bus_el_ec_2_1_connector_el_ec_2_1_0)
+1 flow(bus_el_ec_2_connector_el_ec_2_1_0)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_0)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_1_0)
= 0

c_e_BusBlock_balance(connector_el_ec_2_1_1)_:
+1 flow(bus_el_ec_2_1_connector_el_ec_2_1_1)
+1 flow(bus_el_ec_2_connector_el_ec_2_1_1)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_1)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_1_1)
= 0

c_e_BusBlock_balance(connector_el_ec_2_1_2)_:
+1 flow(bus_el_ec_2_1_connector_el_ec_2_1_2)
+1 flow(bus_el_ec_2_connector_el_ec_2_1_2)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_1_2)
-1 flow(connector_el_ec_2_1_bus_el_ec_2_2)
= 0

c_e_BusBlock_balance(connector_el_ec_2_2_0)_:
+1 flow(bus_el_ec_2_2_connector_el_ec_2_2_0)
+1 flow(bus_el_ec_2_connector_el_ec_2_2_0)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_0)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_2_0)
= 0

c_e_BusBlock_balance(connector_el_ec_2_2_1)_:
+1 flow(bus_el_ec_2_2_connector_el_ec_2_2_1)
+1 flow(bus_el_ec_2_connector_el_ec_2_2_1)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_1)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_2_1)
= 0

c_e_BusBlock_balance(connector_el_ec_2_2_2)_:
+1 flow(bus_el_ec_2_2_connector_el_ec_2_2_2)
+1 flow(bus_el_ec_2_connector_el_ec_2_2_2)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_2)
-1 flow(connector_el_ec_2_2_bus_el_ec_2_2_2)
= 0

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= flow(bus_el_ec_1_connector_el_ec_1_0) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_1) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_2) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_1_0) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_1_1) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_1_2) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_2_0) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_2_1) <= +inf
   0 <= flow(bus_el_ec_1_connector_el_ec_1_2_2) <= +inf
   0 <= flow(bus_el_ec_1_1_connector_el_ec_1_1_0) <= +inf
   0 <= flow(bus_el_ec_1_1_connector_el_ec_1_1_1) <= +inf
   0 <= flow(bus_el_ec_1_1_connector_el_ec_1_1_2) <= +inf
   0 <= flow(bus_el_ec_1_2_connector_el_ec_1_2_0) <= +inf
   0 <= flow(bus_el_ec_1_2_connector_el_ec_1_2_1) <= +inf
   0 <= flow(bus_el_ec_1_2_connector_el_ec_1_2_2) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_0) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_1) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_2) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_1_0) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_1_1) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_1_2) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_2_0) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_2_1) <= +inf
   0 <= flow(bus_el_ec_2_connector_el_ec_2_2_2) <= +inf
   0 <= flow(bus_el_ec_2_1_connector_el_ec_2_1_0) <= +inf
   0 <= flow(bus_el_ec_2_1_connector_el_ec_2_1_1) <= +inf
   0 <= flow(bus_el_ec_2_1_connector_el_ec_2_1_2) <= +inf
   0 <= flow(bus_el_ec_2_2_connector_el_ec_2_2_0) <= +inf
   0 <= flow(bus_el_ec_2_2_connector_el_ec_2_2_1) <= +inf
   0 <= flow(bus_el_ec_2_2_connector_el_ec_2_2_2) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_1_0) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_1_1) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_1_2) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_2_0) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_2_1) <= +inf
   0 <= flow(bus_el_es_connector_el_ec_2_2) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_ec_1_0) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_ec_1_1) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_ec_1_2) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_es_0) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_es_1) <= +inf
   0 <= flow(connector_el_ec_1_bus_el_es_2) <= +inf
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_0) <= 30
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_1) <= 30
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_2) <= 30
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_1_0) <= +inf
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_1_1) <= +inf
   0 <= flow(connector_el_ec_1_1_bus_el_ec_1_1_2) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_0) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_1) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_2) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_2_0) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_2_1) <= +inf
   0 <= flow(connector_el_ec_1_2_bus_el_ec_1_2_2) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_ec_2_0) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_ec_2_1) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_ec_2_2) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_es_0) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_es_1) <= +inf
   0 <= flow(connector_el_ec_2_bus_el_es_2) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_0) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_1) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_2) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_1_0) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_1_1) <= +inf
   0 <= flow(connector_el_ec_2_1_bus_el_ec_2_1_2) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_0) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_1) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_2) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_2_0) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_2_1) <= +inf
   0 <= flow(connector_el_ec_2_2_bus_el_ec_2_2_2) <= +inf
   0 <= flow(source_el_ec_1_bus_el_ec_1_0) <= 100
   0 <= flow(source_el_ec_1_bus_el_ec_1_1) <= 100
   0 <= flow(source_el_ec_1_bus_el_ec_1_2) <= 100
   0 <= flow(source_el_ec_1_1_bus_el_ec_1_1_0) <= 100
   0 <= flow(source_el_ec_1_1_bus_el_ec_1_1_1) <= 100
   0 <= flow(source_el_ec_1_1_bus_el_ec_1_1_2) <= 100
   0 <= flow(source_el_ec_1_2_bus_el_ec_1_2_0) <= 100
   0 <= flow(source_el_ec_1_2_bus_el_ec_1_2_1) <= 100
   0 <= flow(source_el_ec_1_2_bus_el_ec_1_2_2) <= 100
   0 <= flow(source_el_ec_2_bus_el_ec_2_0) <= 100
   0 <= flow(source_el_ec_2_bus_el_ec_2_1) <= 100
   0 <= flow(source_el_ec_2_bus_el_ec_2_2) <= 100
   0 <= flow(source_el_ec_2_1_bus_el_ec_2_1_0) <= 100
   0 <= flow(source_el_ec_2_1_bus_el_ec_2_1_1) <= 100
   0 <= flow(source_el_ec_2_1_bus_el_ec_2_1_2) <= 100
   0 <= flow(source_el_ec_2_2_bus_el_ec_2_2_0) <= 100
   0 <= flow(source_el_ec_2_2_bus_el_ec_2_2_1) <= 100
   0 <= flow(source_el_ec_2_2_bus_el_ec_2_2_2) <= 100
end
