\* Source Pyomo model name=Model *\

min 
objective:
+200.0 ONE_VAR_CONSTANT
+50 flow(powerplant_gas_electricity_0_0)
+50 flow(powerplant_gas_electricity_0_1)
+50 flow(powerplant_gas_electricity_0_2)

s.t.

c_e_BusBlock_balance(gas_0_0)_:
+1 flow(gas_source_gas_0_0)
-1 flow(gas_powerplant_gas_0_0)
= 0

c_e_BusBlock_balance(gas_0_1)_:
+1 flow(gas_source_gas_0_1)
-1 flow(gas_powerplant_gas_0_1)
= 0

c_e_BusBlock_balance(gas_0_2)_:
+1 flow(gas_source_gas_0_2)
-1 flow(gas_powerplant_gas_0_2)
= 0

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(powerplant_gas_electricity_0_0)
+1 flow(storage_electricity_0_0)
-1 flow(electricity_storage_0_0)
= 80.0

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(powerplant_gas_electricity_0_1)
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
= 90.0

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(powerplant_gas_electricity_0_2)
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
= 100.0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_0)_:
-1 flow(powerplant_gas_electricity_0_0)
+0.58 flow(gas_powerplant_gas_0_0)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_1)_:
-1 flow(powerplant_gas_electricity_0_1)
+0.58 flow(gas_powerplant_gas_0_1)
= 0

c_e_ConverterBlock_relation(powerplant_gas_gas_electricity_0_2)_:
-1 flow(powerplant_gas_electricity_0_2)
+0.58 flow(gas_powerplant_gas_0_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_u_InvestmentFlowBlock_max(storage_electricity_0_0)_:
+1 flow(storage_electricity_0_0)
<= 10.0

c_u_InvestmentFlowBlock_max(storage_electricity_0_1)_:
+1 flow(storage_electricity_0_1)
<= 10.0

c_u_InvestmentFlowBlock_max(storage_electricity_0_2)_:
+1 flow(storage_electricity_0_2)
<= 10.0

c_u_InvestmentFlowBlock_max(electricity_storage_0_0)_:
+1 flow(electricity_storage_0_0)
<= 10.0

c_u_InvestmentFlowBlock_max(electricity_storage_0_1)_:
+1 flow(electricity_storage_0_1)
<= 10.0

c_u_InvestmentFlowBlock_max(electricity_storage_0_2)_:
+1 flow(electricity_storage_0_2)
<= 10.0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_u_GenericInvestmentStorageBlock_init_content_limit(storage)_:
+1 GenericInvestmentStorageBlock_init_content(storage)
<= 10.0

c_e_GenericInvestmentStorageBlock_balance_first(storage)_:
+1 flow(storage_electricity_0_0)
-1 flow(electricity_storage_0_0)
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balanced_cstr(storage)_:
-1 GenericInvestmentStorageBlock_init_content(storage)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_e_GenericInvestmentStorageBlock_storage_capacity_inflow(storage_0)_:
+0 ONE_VAR_CONSTANT
= 0.0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 10.0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 10.0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 10.0

bounds
   1 <= ONE_VAR_CONSTANT <= 1
   0 <= flow(powerplant_gas_electricity_0_0) <= 90
   0 <= flow(powerplant_gas_electricity_0_1) <= 90
   0 <= flow(powerplant_gas_electricity_0_2) <= 90
   0 <= flow(gas_source_gas_0_0) <= +inf
   0 <= flow(gas_powerplant_gas_0_0) <= +inf
   0 <= flow(gas_source_gas_0_1) <= +inf
   0 <= flow(gas_powerplant_gas_0_1) <= +inf
   0 <= flow(gas_source_gas_0_2) <= +inf
   0 <= flow(gas_powerplant_gas_0_2) <= +inf
   0 <= flow(storage_electricity_0_0) <= +inf
   0 <= flow(electricity_storage_0_0) <= +inf
   0 <= flow(storage_electricity_0_1) <= +inf
   0 <= flow(electricity_storage_0_1) <= +inf
   0 <= flow(storage_electricity_0_2) <= +inf
   0 <= flow(electricity_storage_0_2) <= +inf
   0 <= GenericInvestmentStorageBlock_init_content(storage) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
end
