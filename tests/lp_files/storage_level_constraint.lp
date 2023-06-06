\* Source Pyomo model name=Model *\

min 
objective:
-0.125 flow(multiplexer_out_0_0_0)
-0.125 flow(multiplexer_out_0_0_1)
-0.125 flow(multiplexer_out_1_0_0)
-0.125 flow(multiplexer_out_1_0_1)
+0.25 flow(in_0_multiplexer_0_0)
+0.25 flow(in_0_multiplexer_0_1)

s.t.

c_u_multiplexer_output_active_constraint(out_0_0)_:
+0.125 multiplexer_active_output(out_0_0)
-0.25 GenericStorageBlock_storage_content(storage_1)
<= 0

c_u_multiplexer_output_active_constraint(out_0_1)_:
+0.125 multiplexer_active_output(out_0_1)
-0.25 GenericStorageBlock_storage_content(storage_2)
<= 0

c_u_multiplexer_output_active_constraint(out_1_0)_:
-0.25 GenericStorageBlock_storage_content(storage_1)
+0.5 multiplexer_active_output(out_1_0)
<= 0

c_u_multiplexer_output_active_constraint(out_1_1)_:
-0.25 GenericStorageBlock_storage_content(storage_2)
+0.5 multiplexer_active_output(out_1_1)
<= 0

c_u_multiplexer_output_constraint(out_0_0_0)_:
+4.0 flow(multiplexer_out_0_0_0)
-1 multiplexer_active_output(out_0_0)
<= 0

c_u_multiplexer_output_constraint(out_0_0_1)_:
+4.0 flow(multiplexer_out_0_0_1)
-1 multiplexer_active_output(out_0_1)
<= 0

c_u_multiplexer_output_constraint(out_1_0_0)_:
+8.0 flow(multiplexer_out_1_0_0)
-1 multiplexer_active_output(out_1_0)
<= 0

c_u_multiplexer_output_constraint(out_1_0_1)_:
+8.0 flow(multiplexer_out_1_0_1)
-1 multiplexer_active_output(out_1_1)
<= 0

c_u_multiplexer_input_active_constraint(in_1_0)_:
-1 multiplexer_active_input(in_1_0)
<= -0.75

c_u_multiplexer_input_active_constraint(in_1_1)_:
+0.25 GenericStorageBlock_storage_content(storage_1)
-1 multiplexer_active_input(in_1_1)
<= 0.25

c_u_multiplexer_input_constraint(in_1_0_0)_:
+1 multiplexer_active_input(in_1_0)
+8.0 flow(in_1_multiplexer_0_0)
<= 1

c_u_multiplexer_input_constraint(in_1_0_1)_:
+1 multiplexer_active_input(in_1_1)
+8.0 flow(in_1_multiplexer_0_1)
<= 1

c_e_BusBlock_balance(multiplexer_0_0)_:
-1 flow(multiplexer_out_0_0_0)
-1 flow(multiplexer_out_1_0_0)
+1 flow(in_0_multiplexer_0_0)
+1 flow(in_1_multiplexer_0_0)
+1 flow(storage_multiplexer_0_0)
-1 flow(multiplexer_storage_0_0)
= 0

c_e_BusBlock_balance(multiplexer_0_1)_:
-1 flow(multiplexer_out_0_0_1)
-1 flow(multiplexer_out_1_0_1)
+1 flow(in_0_multiplexer_0_1)
+1 flow(in_1_multiplexer_0_1)
+1 flow(storage_multiplexer_0_1)
-1 flow(multiplexer_storage_0_1)
= 0

c_e_GenericStorageBlock_balance(storage_0_0)_:
+1 GenericStorageBlock_storage_content(storage_1)
+1 flow(storage_multiplexer_0_0)
-1 flow(multiplexer_storage_0_0)
= 3.0

c_e_GenericStorageBlock_balance(storage_0_1)_:
-0.75 GenericStorageBlock_storage_content(storage_1)
+1 GenericStorageBlock_storage_content(storage_2)
+1 flow(storage_multiplexer_0_1)
-1 flow(multiplexer_storage_0_1)
= 0

c_e_GenericStorageBlock_balanced_cstr(storage)_:
+1 GenericStorageBlock_storage_content(storage_2)
= 4

bounds
   0.0 <= flow(multiplexer_out_0_0_0) <= 0.25
   0.0 <= flow(multiplexer_out_0_0_1) <= 0.25
   0.0 <= flow(multiplexer_out_1_0_0) <= 0.125
   0.0 <= flow(multiplexer_out_1_0_1) <= 0.125
   0.0 <= flow(in_0_multiplexer_0_0) <= 0.5
   0.0 <= flow(in_0_multiplexer_0_1) <= 0.5
   0 <= multiplexer_active_output(out_0_0) <= 1
   0 <= GenericStorageBlock_storage_content(storage_1) <= 4
   0 <= multiplexer_active_output(out_0_1) <= 1
   0 <= GenericStorageBlock_storage_content(storage_2) <= 4
   0 <= multiplexer_active_output(out_1_0) <= 1
   0 <= multiplexer_active_output(out_1_1) <= 1
   0 <= multiplexer_active_input(in_1_0) <= 1
   0 <= multiplexer_active_input(in_1_1) <= 1
   0.0 <= flow(in_1_multiplexer_0_0) <= 0.125
   0.0 <= flow(in_1_multiplexer_0_1) <= 0.125
   0 <= flow(storage_multiplexer_0_0) <= +inf
   0 <= flow(multiplexer_storage_0_0) <= +inf
   0 <= flow(storage_multiplexer_0_1) <= +inf
   0 <= flow(multiplexer_storage_0_1) <= +inf
binary
  multiplexer_active_output(out_0_0)
  multiplexer_active_output(out_0_1)
  multiplexer_active_output(out_1_0)
  multiplexer_active_output(out_1_1)
  multiplexer_active_input(in_1_0)
  multiplexer_active_input(in_1_1)
end
