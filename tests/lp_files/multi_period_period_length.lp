\* Source Pyomo model name=Model *\

min 
objective:
+61.15671812529034 InvestmentFlowBlock_invest(wind_electricity_0)
+41.15671812529034 InvestmentFlowBlock_invest(wind_electricity_1)
+30.580047805076184 InvestmentFlowBlock_invest(wind_electricity_2)
+25.086290226995217 InvestmentFlowBlock_invest(wind_electricity_3)
+22.72142596292468 InvestmentFlowBlock_invest(wind_electricity_4)
+18.639483159424472 InvestmentFlowBlock_invest(wind_electricity_5)
+13.849410546825318 InvestmentFlowBlock_invest(wind_electricity_6)
+9.320256278457826 InvestmentFlowBlock_invest(wind_electricity_7)
+24.462687250116133 InvestmentFlowBlock_invest(pv_electricity_0)
+16.462687250116133 InvestmentFlowBlock_invest(pv_electricity_1)
+12.232019122030472 InvestmentFlowBlock_invest(pv_electricity_2)
+10.034516090798085 InvestmentFlowBlock_invest(pv_electricity_3)
+9.088570385169872 InvestmentFlowBlock_invest(pv_electricity_4)
+7.455793263769787 InvestmentFlowBlock_invest(pv_electricity_5)
+5.539764218730126 InvestmentFlowBlock_invest(pv_electricity_6)
+3.72810251138313 InvestmentFlowBlock_invest(pv_electricity_7)
+12.231343625058066 InvestmentFlowBlock_invest(storage_electricity_0)
+8.231343625058066 InvestmentFlowBlock_invest(storage_electricity_1)
+6.116009561015236 InvestmentFlowBlock_invest(storage_electricity_2)
+5.017258045399043 InvestmentFlowBlock_invest(storage_electricity_3)
+4.544285192584936 InvestmentFlowBlock_invest(storage_electricity_4)
+3.7278966318848936 InvestmentFlowBlock_invest(storage_electricity_5)
+2.769882109365063 InvestmentFlowBlock_invest(storage_electricity_6)
+1.864051255691565 InvestmentFlowBlock_invest(storage_electricity_7)
+12.231343625058066 InvestmentFlowBlock_invest(electricity_storage_0)
+8.231343625058066 InvestmentFlowBlock_invest(electricity_storage_1)
+6.116009561015236 InvestmentFlowBlock_invest(electricity_storage_2)
+5.017258045399043 InvestmentFlowBlock_invest(electricity_storage_3)
+4.544285192584936 InvestmentFlowBlock_invest(electricity_storage_4)
+3.7278966318848936 InvestmentFlowBlock_invest(electricity_storage_5)
+2.769882109365063 InvestmentFlowBlock_invest(electricity_storage_6)
+1.864051255691565 InvestmentFlowBlock_invest(electricity_storage_7)
+12.231343625058066 GenericInvestmentStorageBlock_invest(storage_0)
+8.231343625058066 GenericInvestmentStorageBlock_invest(storage_1)
+6.116009561015236 GenericInvestmentStorageBlock_invest(storage_2)
+5.017258045399043 GenericInvestmentStorageBlock_invest(storage_3)
+4.544285192584936 GenericInvestmentStorageBlock_invest(storage_4)
+3.7278966318848936 GenericInvestmentStorageBlock_invest(storage_5)
+2.769882109365063 GenericInvestmentStorageBlock_invest(storage_6)
+1.864051255691565 GenericInvestmentStorageBlock_invest(storage_7)

s.t.

c_e_BusBlock_balance(electricity_0_0)_:
+1 flow(pv_electricity_0_0)
+1 flow(storage_electricity_0_0)
+1 flow(wind_electricity_0_0)
-1 flow(electricity_storage_0_0)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_1)_:
+1 flow(pv_electricity_0_1)
+1 flow(storage_electricity_0_1)
+1 flow(wind_electricity_0_1)
-1 flow(electricity_storage_0_1)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_2)_:
+1 flow(pv_electricity_0_2)
+1 flow(storage_electricity_0_2)
+1 flow(wind_electricity_0_2)
-1 flow(electricity_storage_0_2)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_3)_:
+1 flow(pv_electricity_0_3)
+1 flow(storage_electricity_0_3)
+1 flow(wind_electricity_0_3)
-1 flow(electricity_storage_0_3)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_4)_:
+1 flow(pv_electricity_0_4)
+1 flow(storage_electricity_0_4)
+1 flow(wind_electricity_0_4)
-1 flow(electricity_storage_0_4)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_5)_:
+1 flow(pv_electricity_0_5)
+1 flow(storage_electricity_0_5)
+1 flow(wind_electricity_0_5)
-1 flow(electricity_storage_0_5)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_6)_:
+1 flow(pv_electricity_0_6)
+1 flow(storage_electricity_0_6)
+1 flow(wind_electricity_0_6)
-1 flow(electricity_storage_0_6)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_7)_:
+1 flow(pv_electricity_0_7)
+1 flow(storage_electricity_0_7)
+1 flow(wind_electricity_0_7)
-1 flow(electricity_storage_0_7)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_8)_:
+1 flow(pv_electricity_0_8)
+1 flow(storage_electricity_0_8)
+1 flow(wind_electricity_0_8)
-1 flow(electricity_storage_0_8)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_9)_:
+1 flow(pv_electricity_0_9)
+1 flow(storage_electricity_0_9)
+1 flow(wind_electricity_0_9)
-1 flow(electricity_storage_0_9)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_10)_:
+1 flow(pv_electricity_0_10)
+1 flow(storage_electricity_0_10)
+1 flow(wind_electricity_0_10)
-1 flow(electricity_storage_0_10)
= 6.999999999999999

c_e_BusBlock_balance(electricity_0_11)_:
+1 flow(pv_electricity_0_11)
+1 flow(storage_electricity_0_11)
+1 flow(wind_electricity_0_11)
-1 flow(electricity_storage_0_11)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_12)_:
+1 flow(pv_electricity_1_12)
+1 flow(storage_electricity_1_12)
+1 flow(wind_electricity_1_12)
-1 flow(electricity_storage_1_12)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_13)_:
+1 flow(pv_electricity_1_13)
+1 flow(storage_electricity_1_13)
+1 flow(wind_electricity_1_13)
-1 flow(electricity_storage_1_13)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_14)_:
+1 flow(pv_electricity_1_14)
+1 flow(storage_electricity_1_14)
+1 flow(wind_electricity_1_14)
-1 flow(electricity_storage_1_14)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_15)_:
+1 flow(pv_electricity_1_15)
+1 flow(storage_electricity_1_15)
+1 flow(wind_electricity_1_15)
-1 flow(electricity_storage_1_15)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_16)_:
+1 flow(pv_electricity_1_16)
+1 flow(storage_electricity_1_16)
+1 flow(wind_electricity_1_16)
-1 flow(electricity_storage_1_16)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_17)_:
+1 flow(pv_electricity_1_17)
+1 flow(storage_electricity_1_17)
+1 flow(wind_electricity_1_17)
-1 flow(electricity_storage_1_17)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_18)_:
+1 flow(pv_electricity_1_18)
+1 flow(storage_electricity_1_18)
+1 flow(wind_electricity_1_18)
-1 flow(electricity_storage_1_18)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_19)_:
+1 flow(pv_electricity_1_19)
+1 flow(storage_electricity_1_19)
+1 flow(wind_electricity_1_19)
-1 flow(electricity_storage_1_19)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_20)_:
+1 flow(pv_electricity_1_20)
+1 flow(storage_electricity_1_20)
+1 flow(wind_electricity_1_20)
-1 flow(electricity_storage_1_20)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_21)_:
+1 flow(pv_electricity_1_21)
+1 flow(storage_electricity_1_21)
+1 flow(wind_electricity_1_21)
-1 flow(electricity_storage_1_21)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_22)_:
+1 flow(pv_electricity_1_22)
+1 flow(storage_electricity_1_22)
+1 flow(wind_electricity_1_22)
-1 flow(electricity_storage_1_22)
= 6.999999999999999

c_e_BusBlock_balance(electricity_1_23)_:
+1 flow(pv_electricity_1_23)
+1 flow(storage_electricity_1_23)
+1 flow(wind_electricity_1_23)
-1 flow(electricity_storage_1_23)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_24)_:
+1 flow(pv_electricity_2_24)
+1 flow(storage_electricity_2_24)
+1 flow(wind_electricity_2_24)
-1 flow(electricity_storage_2_24)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_25)_:
+1 flow(pv_electricity_2_25)
+1 flow(storage_electricity_2_25)
+1 flow(wind_electricity_2_25)
-1 flow(electricity_storage_2_25)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_26)_:
+1 flow(pv_electricity_2_26)
+1 flow(storage_electricity_2_26)
+1 flow(wind_electricity_2_26)
-1 flow(electricity_storage_2_26)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_27)_:
+1 flow(pv_electricity_2_27)
+1 flow(storage_electricity_2_27)
+1 flow(wind_electricity_2_27)
-1 flow(electricity_storage_2_27)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_28)_:
+1 flow(pv_electricity_2_28)
+1 flow(storage_electricity_2_28)
+1 flow(wind_electricity_2_28)
-1 flow(electricity_storage_2_28)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_29)_:
+1 flow(pv_electricity_2_29)
+1 flow(storage_electricity_2_29)
+1 flow(wind_electricity_2_29)
-1 flow(electricity_storage_2_29)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_30)_:
+1 flow(pv_electricity_2_30)
+1 flow(storage_electricity_2_30)
+1 flow(wind_electricity_2_30)
-1 flow(electricity_storage_2_30)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_31)_:
+1 flow(pv_electricity_2_31)
+1 flow(storage_electricity_2_31)
+1 flow(wind_electricity_2_31)
-1 flow(electricity_storage_2_31)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_32)_:
+1 flow(pv_electricity_2_32)
+1 flow(storage_electricity_2_32)
+1 flow(wind_electricity_2_32)
-1 flow(electricity_storage_2_32)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_33)_:
+1 flow(pv_electricity_2_33)
+1 flow(storage_electricity_2_33)
+1 flow(wind_electricity_2_33)
-1 flow(electricity_storage_2_33)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_34)_:
+1 flow(pv_electricity_2_34)
+1 flow(storage_electricity_2_34)
+1 flow(wind_electricity_2_34)
-1 flow(electricity_storage_2_34)
= 6.999999999999999

c_e_BusBlock_balance(electricity_2_35)_:
+1 flow(pv_electricity_2_35)
+1 flow(storage_electricity_2_35)
+1 flow(wind_electricity_2_35)
-1 flow(electricity_storage_2_35)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_36)_:
+1 flow(pv_electricity_3_36)
+1 flow(storage_electricity_3_36)
+1 flow(wind_electricity_3_36)
-1 flow(electricity_storage_3_36)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_37)_:
+1 flow(pv_electricity_3_37)
+1 flow(storage_electricity_3_37)
+1 flow(wind_electricity_3_37)
-1 flow(electricity_storage_3_37)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_38)_:
+1 flow(pv_electricity_3_38)
+1 flow(storage_electricity_3_38)
+1 flow(wind_electricity_3_38)
-1 flow(electricity_storage_3_38)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_39)_:
+1 flow(pv_electricity_3_39)
+1 flow(storage_electricity_3_39)
+1 flow(wind_electricity_3_39)
-1 flow(electricity_storage_3_39)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_40)_:
+1 flow(pv_electricity_3_40)
+1 flow(storage_electricity_3_40)
+1 flow(wind_electricity_3_40)
-1 flow(electricity_storage_3_40)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_41)_:
+1 flow(pv_electricity_3_41)
+1 flow(storage_electricity_3_41)
+1 flow(wind_electricity_3_41)
-1 flow(electricity_storage_3_41)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_42)_:
+1 flow(pv_electricity_3_42)
+1 flow(storage_electricity_3_42)
+1 flow(wind_electricity_3_42)
-1 flow(electricity_storage_3_42)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_43)_:
+1 flow(pv_electricity_3_43)
+1 flow(storage_electricity_3_43)
+1 flow(wind_electricity_3_43)
-1 flow(electricity_storage_3_43)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_44)_:
+1 flow(pv_electricity_3_44)
+1 flow(storage_electricity_3_44)
+1 flow(wind_electricity_3_44)
-1 flow(electricity_storage_3_44)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_45)_:
+1 flow(pv_electricity_3_45)
+1 flow(storage_electricity_3_45)
+1 flow(wind_electricity_3_45)
-1 flow(electricity_storage_3_45)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_46)_:
+1 flow(pv_electricity_3_46)
+1 flow(storage_electricity_3_46)
+1 flow(wind_electricity_3_46)
-1 flow(electricity_storage_3_46)
= 6.999999999999999

c_e_BusBlock_balance(electricity_3_47)_:
+1 flow(pv_electricity_3_47)
+1 flow(storage_electricity_3_47)
+1 flow(wind_electricity_3_47)
-1 flow(electricity_storage_3_47)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_48)_:
+1 flow(pv_electricity_4_48)
+1 flow(storage_electricity_4_48)
+1 flow(wind_electricity_4_48)
-1 flow(electricity_storage_4_48)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_49)_:
+1 flow(pv_electricity_4_49)
+1 flow(storage_electricity_4_49)
+1 flow(wind_electricity_4_49)
-1 flow(electricity_storage_4_49)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_50)_:
+1 flow(pv_electricity_4_50)
+1 flow(storage_electricity_4_50)
+1 flow(wind_electricity_4_50)
-1 flow(electricity_storage_4_50)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_51)_:
+1 flow(pv_electricity_4_51)
+1 flow(storage_electricity_4_51)
+1 flow(wind_electricity_4_51)
-1 flow(electricity_storage_4_51)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_52)_:
+1 flow(pv_electricity_4_52)
+1 flow(storage_electricity_4_52)
+1 flow(wind_electricity_4_52)
-1 flow(electricity_storage_4_52)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_53)_:
+1 flow(pv_electricity_4_53)
+1 flow(storage_electricity_4_53)
+1 flow(wind_electricity_4_53)
-1 flow(electricity_storage_4_53)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_54)_:
+1 flow(pv_electricity_4_54)
+1 flow(storage_electricity_4_54)
+1 flow(wind_electricity_4_54)
-1 flow(electricity_storage_4_54)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_55)_:
+1 flow(pv_electricity_4_55)
+1 flow(storage_electricity_4_55)
+1 flow(wind_electricity_4_55)
-1 flow(electricity_storage_4_55)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_56)_:
+1 flow(pv_electricity_4_56)
+1 flow(storage_electricity_4_56)
+1 flow(wind_electricity_4_56)
-1 flow(electricity_storage_4_56)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_57)_:
+1 flow(pv_electricity_4_57)
+1 flow(storage_electricity_4_57)
+1 flow(wind_electricity_4_57)
-1 flow(electricity_storage_4_57)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_58)_:
+1 flow(pv_electricity_4_58)
+1 flow(storage_electricity_4_58)
+1 flow(wind_electricity_4_58)
-1 flow(electricity_storage_4_58)
= 6.999999999999999

c_e_BusBlock_balance(electricity_4_59)_:
+1 flow(pv_electricity_4_59)
+1 flow(storage_electricity_4_59)
+1 flow(wind_electricity_4_59)
-1 flow(electricity_storage_4_59)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_60)_:
+1 flow(pv_electricity_5_60)
+1 flow(storage_electricity_5_60)
+1 flow(wind_electricity_5_60)
-1 flow(electricity_storage_5_60)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_61)_:
+1 flow(pv_electricity_5_61)
+1 flow(storage_electricity_5_61)
+1 flow(wind_electricity_5_61)
-1 flow(electricity_storage_5_61)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_62)_:
+1 flow(pv_electricity_5_62)
+1 flow(storage_electricity_5_62)
+1 flow(wind_electricity_5_62)
-1 flow(electricity_storage_5_62)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_63)_:
+1 flow(pv_electricity_5_63)
+1 flow(storage_electricity_5_63)
+1 flow(wind_electricity_5_63)
-1 flow(electricity_storage_5_63)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_64)_:
+1 flow(pv_electricity_5_64)
+1 flow(storage_electricity_5_64)
+1 flow(wind_electricity_5_64)
-1 flow(electricity_storage_5_64)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_65)_:
+1 flow(pv_electricity_5_65)
+1 flow(storage_electricity_5_65)
+1 flow(wind_electricity_5_65)
-1 flow(electricity_storage_5_65)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_66)_:
+1 flow(pv_electricity_5_66)
+1 flow(storage_electricity_5_66)
+1 flow(wind_electricity_5_66)
-1 flow(electricity_storage_5_66)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_67)_:
+1 flow(pv_electricity_5_67)
+1 flow(storage_electricity_5_67)
+1 flow(wind_electricity_5_67)
-1 flow(electricity_storage_5_67)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_68)_:
+1 flow(pv_electricity_5_68)
+1 flow(storage_electricity_5_68)
+1 flow(wind_electricity_5_68)
-1 flow(electricity_storage_5_68)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_69)_:
+1 flow(pv_electricity_5_69)
+1 flow(storage_electricity_5_69)
+1 flow(wind_electricity_5_69)
-1 flow(electricity_storage_5_69)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_70)_:
+1 flow(pv_electricity_5_70)
+1 flow(storage_electricity_5_70)
+1 flow(wind_electricity_5_70)
-1 flow(electricity_storage_5_70)
= 6.999999999999999

c_e_BusBlock_balance(electricity_5_71)_:
+1 flow(pv_electricity_5_71)
+1 flow(storage_electricity_5_71)
+1 flow(wind_electricity_5_71)
-1 flow(electricity_storage_5_71)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_72)_:
+1 flow(pv_electricity_6_72)
+1 flow(storage_electricity_6_72)
+1 flow(wind_electricity_6_72)
-1 flow(electricity_storage_6_72)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_73)_:
+1 flow(pv_electricity_6_73)
+1 flow(storage_electricity_6_73)
+1 flow(wind_electricity_6_73)
-1 flow(electricity_storage_6_73)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_74)_:
+1 flow(pv_electricity_6_74)
+1 flow(storage_electricity_6_74)
+1 flow(wind_electricity_6_74)
-1 flow(electricity_storage_6_74)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_75)_:
+1 flow(pv_electricity_6_75)
+1 flow(storage_electricity_6_75)
+1 flow(wind_electricity_6_75)
-1 flow(electricity_storage_6_75)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_76)_:
+1 flow(pv_electricity_6_76)
+1 flow(storage_electricity_6_76)
+1 flow(wind_electricity_6_76)
-1 flow(electricity_storage_6_76)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_77)_:
+1 flow(pv_electricity_6_77)
+1 flow(storage_electricity_6_77)
+1 flow(wind_electricity_6_77)
-1 flow(electricity_storage_6_77)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_78)_:
+1 flow(pv_electricity_6_78)
+1 flow(storage_electricity_6_78)
+1 flow(wind_electricity_6_78)
-1 flow(electricity_storage_6_78)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_79)_:
+1 flow(pv_electricity_6_79)
+1 flow(storage_electricity_6_79)
+1 flow(wind_electricity_6_79)
-1 flow(electricity_storage_6_79)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_80)_:
+1 flow(pv_electricity_6_80)
+1 flow(storage_electricity_6_80)
+1 flow(wind_electricity_6_80)
-1 flow(electricity_storage_6_80)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_81)_:
+1 flow(pv_electricity_6_81)
+1 flow(storage_electricity_6_81)
+1 flow(wind_electricity_6_81)
-1 flow(electricity_storage_6_81)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_82)_:
+1 flow(pv_electricity_6_82)
+1 flow(storage_electricity_6_82)
+1 flow(wind_electricity_6_82)
-1 flow(electricity_storage_6_82)
= 6.999999999999999

c_e_BusBlock_balance(electricity_6_83)_:
+1 flow(pv_electricity_6_83)
+1 flow(storage_electricity_6_83)
+1 flow(wind_electricity_6_83)
-1 flow(electricity_storage_6_83)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_84)_:
+1 flow(pv_electricity_7_84)
+1 flow(storage_electricity_7_84)
+1 flow(wind_electricity_7_84)
-1 flow(electricity_storage_7_84)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_85)_:
+1 flow(pv_electricity_7_85)
+1 flow(storage_electricity_7_85)
+1 flow(wind_electricity_7_85)
-1 flow(electricity_storage_7_85)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_86)_:
+1 flow(pv_electricity_7_86)
+1 flow(storage_electricity_7_86)
+1 flow(wind_electricity_7_86)
-1 flow(electricity_storage_7_86)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_87)_:
+1 flow(pv_electricity_7_87)
+1 flow(storage_electricity_7_87)
+1 flow(wind_electricity_7_87)
-1 flow(electricity_storage_7_87)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_88)_:
+1 flow(pv_electricity_7_88)
+1 flow(storage_electricity_7_88)
+1 flow(wind_electricity_7_88)
-1 flow(electricity_storage_7_88)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_89)_:
+1 flow(pv_electricity_7_89)
+1 flow(storage_electricity_7_89)
+1 flow(wind_electricity_7_89)
-1 flow(electricity_storage_7_89)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_90)_:
+1 flow(pv_electricity_7_90)
+1 flow(storage_electricity_7_90)
+1 flow(wind_electricity_7_90)
-1 flow(electricity_storage_7_90)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_91)_:
+1 flow(pv_electricity_7_91)
+1 flow(storage_electricity_7_91)
+1 flow(wind_electricity_7_91)
-1 flow(electricity_storage_7_91)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_92)_:
+1 flow(pv_electricity_7_92)
+1 flow(storage_electricity_7_92)
+1 flow(wind_electricity_7_92)
-1 flow(electricity_storage_7_92)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_93)_:
+1 flow(pv_electricity_7_93)
+1 flow(storage_electricity_7_93)
+1 flow(wind_electricity_7_93)
-1 flow(electricity_storage_7_93)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_94)_:
+1 flow(pv_electricity_7_94)
+1 flow(storage_electricity_7_94)
+1 flow(wind_electricity_7_94)
-1 flow(electricity_storage_7_94)
= 6.999999999999999

c_e_BusBlock_balance(electricity_7_95)_:
+1 flow(pv_electricity_7_95)
+1 flow(storage_electricity_7_95)
+1 flow(wind_electricity_7_95)
-1 flow(electricity_storage_7_95)
= 6.999999999999999

c_e_InvestmentFlowBlock_total_rule(wind_electricity_0)_:
-1 InvestmentFlowBlock_invest(wind_electricity_0)
+1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_1)_:
-1 InvestmentFlowBlock_invest(wind_electricity_1)
-1 InvestmentFlowBlock_total(wind_electricity_0)
+1 InvestmentFlowBlock_total(wind_electricity_1)
+1 InvestmentFlowBlock_old(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_2)_:
-1 InvestmentFlowBlock_invest(wind_electricity_2)
-1 InvestmentFlowBlock_total(wind_electricity_1)
+1 InvestmentFlowBlock_total(wind_electricity_2)
+1 InvestmentFlowBlock_old(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_3)_:
-1 InvestmentFlowBlock_invest(wind_electricity_3)
-1 InvestmentFlowBlock_total(wind_electricity_2)
+1 InvestmentFlowBlock_total(wind_electricity_3)
+1 InvestmentFlowBlock_old(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_4)_:
-1 InvestmentFlowBlock_invest(wind_electricity_4)
-1 InvestmentFlowBlock_total(wind_electricity_3)
+1 InvestmentFlowBlock_total(wind_electricity_4)
+1 InvestmentFlowBlock_old(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_5)_:
-1 InvestmentFlowBlock_invest(wind_electricity_5)
-1 InvestmentFlowBlock_total(wind_electricity_4)
+1 InvestmentFlowBlock_total(wind_electricity_5)
+1 InvestmentFlowBlock_old(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_6)_:
-1 InvestmentFlowBlock_invest(wind_electricity_6)
-1 InvestmentFlowBlock_total(wind_electricity_5)
+1 InvestmentFlowBlock_total(wind_electricity_6)
+1 InvestmentFlowBlock_old(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_total_rule(wind_electricity_7)_:
-1 InvestmentFlowBlock_invest(wind_electricity_7)
-1 InvestmentFlowBlock_total(wind_electricity_6)
+1 InvestmentFlowBlock_total(wind_electricity_7)
+1 InvestmentFlowBlock_old(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_0)_:
-1 InvestmentFlowBlock_invest(pv_electricity_0)
+1 InvestmentFlowBlock_total(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_1)_:
-1 InvestmentFlowBlock_invest(pv_electricity_1)
-1 InvestmentFlowBlock_total(pv_electricity_0)
+1 InvestmentFlowBlock_total(pv_electricity_1)
+1 InvestmentFlowBlock_old(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_2)_:
-1 InvestmentFlowBlock_invest(pv_electricity_2)
-1 InvestmentFlowBlock_total(pv_electricity_1)
+1 InvestmentFlowBlock_total(pv_electricity_2)
+1 InvestmentFlowBlock_old(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_3)_:
-1 InvestmentFlowBlock_invest(pv_electricity_3)
-1 InvestmentFlowBlock_total(pv_electricity_2)
+1 InvestmentFlowBlock_total(pv_electricity_3)
+1 InvestmentFlowBlock_old(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_4)_:
-1 InvestmentFlowBlock_invest(pv_electricity_4)
-1 InvestmentFlowBlock_total(pv_electricity_3)
+1 InvestmentFlowBlock_total(pv_electricity_4)
+1 InvestmentFlowBlock_old(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_5)_:
-1 InvestmentFlowBlock_invest(pv_electricity_5)
-1 InvestmentFlowBlock_total(pv_electricity_4)
+1 InvestmentFlowBlock_total(pv_electricity_5)
+1 InvestmentFlowBlock_old(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_6)_:
-1 InvestmentFlowBlock_invest(pv_electricity_6)
-1 InvestmentFlowBlock_total(pv_electricity_5)
+1 InvestmentFlowBlock_total(pv_electricity_6)
+1 InvestmentFlowBlock_old(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_total_rule(pv_electricity_7)_:
-1 InvestmentFlowBlock_invest(pv_electricity_7)
-1 InvestmentFlowBlock_total(pv_electricity_6)
+1 InvestmentFlowBlock_total(pv_electricity_7)
+1 InvestmentFlowBlock_old(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_0)_:
-1 InvestmentFlowBlock_invest(storage_electricity_0)
+1 InvestmentFlowBlock_total(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_1)_:
-1 InvestmentFlowBlock_invest(storage_electricity_1)
-1 InvestmentFlowBlock_total(storage_electricity_0)
+1 InvestmentFlowBlock_total(storage_electricity_1)
+1 InvestmentFlowBlock_old(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_2)_:
-1 InvestmentFlowBlock_invest(storage_electricity_2)
-1 InvestmentFlowBlock_total(storage_electricity_1)
+1 InvestmentFlowBlock_total(storage_electricity_2)
+1 InvestmentFlowBlock_old(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_3)_:
-1 InvestmentFlowBlock_invest(storage_electricity_3)
-1 InvestmentFlowBlock_total(storage_electricity_2)
+1 InvestmentFlowBlock_total(storage_electricity_3)
+1 InvestmentFlowBlock_old(storage_electricity_3)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_4)_:
-1 InvestmentFlowBlock_invest(storage_electricity_4)
-1 InvestmentFlowBlock_total(storage_electricity_3)
+1 InvestmentFlowBlock_total(storage_electricity_4)
+1 InvestmentFlowBlock_old(storage_electricity_4)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_5)_:
-1 InvestmentFlowBlock_invest(storage_electricity_5)
-1 InvestmentFlowBlock_total(storage_electricity_4)
+1 InvestmentFlowBlock_total(storage_electricity_5)
+1 InvestmentFlowBlock_old(storage_electricity_5)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_6)_:
-1 InvestmentFlowBlock_invest(storage_electricity_6)
-1 InvestmentFlowBlock_total(storage_electricity_5)
+1 InvestmentFlowBlock_total(storage_electricity_6)
+1 InvestmentFlowBlock_old(storage_electricity_6)
= 0

c_e_InvestmentFlowBlock_total_rule(storage_electricity_7)_:
-1 InvestmentFlowBlock_invest(storage_electricity_7)
-1 InvestmentFlowBlock_total(storage_electricity_6)
+1 InvestmentFlowBlock_total(storage_electricity_7)
+1 InvestmentFlowBlock_old(storage_electricity_7)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_0)_:
-1 InvestmentFlowBlock_invest(electricity_storage_0)
+1 InvestmentFlowBlock_total(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_1)_:
-1 InvestmentFlowBlock_invest(electricity_storage_1)
-1 InvestmentFlowBlock_total(electricity_storage_0)
+1 InvestmentFlowBlock_total(electricity_storage_1)
+1 InvestmentFlowBlock_old(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_2)_:
-1 InvestmentFlowBlock_invest(electricity_storage_2)
-1 InvestmentFlowBlock_total(electricity_storage_1)
+1 InvestmentFlowBlock_total(electricity_storage_2)
+1 InvestmentFlowBlock_old(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_3)_:
-1 InvestmentFlowBlock_invest(electricity_storage_3)
-1 InvestmentFlowBlock_total(electricity_storage_2)
+1 InvestmentFlowBlock_total(electricity_storage_3)
+1 InvestmentFlowBlock_old(electricity_storage_3)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_4)_:
-1 InvestmentFlowBlock_invest(electricity_storage_4)
-1 InvestmentFlowBlock_total(electricity_storage_3)
+1 InvestmentFlowBlock_total(electricity_storage_4)
+1 InvestmentFlowBlock_old(electricity_storage_4)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_5)_:
-1 InvestmentFlowBlock_invest(electricity_storage_5)
-1 InvestmentFlowBlock_total(electricity_storage_4)
+1 InvestmentFlowBlock_total(electricity_storage_5)
+1 InvestmentFlowBlock_old(electricity_storage_5)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_6)_:
-1 InvestmentFlowBlock_invest(electricity_storage_6)
-1 InvestmentFlowBlock_total(electricity_storage_5)
+1 InvestmentFlowBlock_total(electricity_storage_6)
+1 InvestmentFlowBlock_old(electricity_storage_6)
= 0

c_e_InvestmentFlowBlock_total_rule(electricity_storage_7)_:
-1 InvestmentFlowBlock_invest(electricity_storage_7)
-1 InvestmentFlowBlock_total(electricity_storage_6)
+1 InvestmentFlowBlock_total(electricity_storage_7)
+1 InvestmentFlowBlock_old(electricity_storage_7)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_0)_:
+1 InvestmentFlowBlock_old_end(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_1)_:
-1 InvestmentFlowBlock_invest(wind_electricity_0)
+1 InvestmentFlowBlock_old_end(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_2)_:
+1 InvestmentFlowBlock_old_end(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_3)_:
-1 InvestmentFlowBlock_invest(wind_electricity_1)
+1 InvestmentFlowBlock_old_end(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_4)_:
+1 InvestmentFlowBlock_old_end(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_5)_:
-1 InvestmentFlowBlock_invest(wind_electricity_2)
+1 InvestmentFlowBlock_old_end(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_6)_:
-1 InvestmentFlowBlock_invest(wind_electricity_3)
-1 InvestmentFlowBlock_invest(wind_electricity_4)
+1 InvestmentFlowBlock_old_end(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_end(wind_electricity_7)_:
-1 InvestmentFlowBlock_invest(wind_electricity_5)
-1 InvestmentFlowBlock_invest(wind_electricity_6)
+1 InvestmentFlowBlock_old_end(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_0)_:
+1 InvestmentFlowBlock_old_end(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_1)_:
-1 InvestmentFlowBlock_invest(pv_electricity_0)
+1 InvestmentFlowBlock_old_end(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_2)_:
+1 InvestmentFlowBlock_old_end(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_3)_:
-1 InvestmentFlowBlock_invest(pv_electricity_1)
+1 InvestmentFlowBlock_old_end(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_4)_:
+1 InvestmentFlowBlock_old_end(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_5)_:
-1 InvestmentFlowBlock_invest(pv_electricity_2)
+1 InvestmentFlowBlock_old_end(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_6)_:
-1 InvestmentFlowBlock_invest(pv_electricity_3)
-1 InvestmentFlowBlock_invest(pv_electricity_4)
+1 InvestmentFlowBlock_old_end(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_end(pv_electricity_7)_:
-1 InvestmentFlowBlock_invest(pv_electricity_5)
-1 InvestmentFlowBlock_invest(pv_electricity_6)
+1 InvestmentFlowBlock_old_end(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_0)_:
+1 InvestmentFlowBlock_old_end(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_1)_:
-1 InvestmentFlowBlock_invest(storage_electricity_0)
+1 InvestmentFlowBlock_old_end(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_2)_:
+1 InvestmentFlowBlock_old_end(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_3)_:
-1 InvestmentFlowBlock_invest(storage_electricity_1)
+1 InvestmentFlowBlock_old_end(storage_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_4)_:
+1 InvestmentFlowBlock_old_end(storage_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_5)_:
-1 InvestmentFlowBlock_invest(storage_electricity_2)
+1 InvestmentFlowBlock_old_end(storage_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_6)_:
-1 InvestmentFlowBlock_invest(storage_electricity_3)
-1 InvestmentFlowBlock_invest(storage_electricity_4)
+1 InvestmentFlowBlock_old_end(storage_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_end(storage_electricity_7)_:
-1 InvestmentFlowBlock_invest(storage_electricity_5)
-1 InvestmentFlowBlock_invest(storage_electricity_6)
+1 InvestmentFlowBlock_old_end(storage_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_0)_:
+1 InvestmentFlowBlock_old_end(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_1)_:
-1 InvestmentFlowBlock_invest(electricity_storage_0)
+1 InvestmentFlowBlock_old_end(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_2)_:
+1 InvestmentFlowBlock_old_end(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_3)_:
-1 InvestmentFlowBlock_invest(electricity_storage_1)
+1 InvestmentFlowBlock_old_end(electricity_storage_3)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_4)_:
+1 InvestmentFlowBlock_old_end(electricity_storage_4)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_5)_:
-1 InvestmentFlowBlock_invest(electricity_storage_2)
+1 InvestmentFlowBlock_old_end(electricity_storage_5)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_6)_:
-1 InvestmentFlowBlock_invest(electricity_storage_3)
-1 InvestmentFlowBlock_invest(electricity_storage_4)
+1 InvestmentFlowBlock_old_end(electricity_storage_6)
= 0

c_e_InvestmentFlowBlock_old_rule_end(electricity_storage_7)_:
-1 InvestmentFlowBlock_invest(electricity_storage_5)
-1 InvestmentFlowBlock_invest(electricity_storage_6)
+1 InvestmentFlowBlock_old_end(electricity_storage_7)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_3)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_4)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_5)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_6)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(wind_electricity_7)_:
+1 InvestmentFlowBlock_old_exo(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_3)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_4)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_5)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_6)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(pv_electricity_7)_:
+1 InvestmentFlowBlock_old_exo(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_0)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_1)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_2)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_3)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_4)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_5)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_6)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(storage_electricity_7)_:
+1 InvestmentFlowBlock_old_exo(storage_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_0)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_1)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_2)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_3)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_3)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_4)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_4)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_5)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_5)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_6)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_6)
= 0

c_e_InvestmentFlowBlock_old_rule_exo(electricity_storage_7)_:
+1 InvestmentFlowBlock_old_exo(electricity_storage_7)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_0)_:
-1 InvestmentFlowBlock_old_end(wind_electricity_0)
-1 InvestmentFlowBlock_old_exo(wind_electricity_0)
+1 InvestmentFlowBlock_old(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_1)_:
+1 InvestmentFlowBlock_old(wind_electricity_1)
-1 InvestmentFlowBlock_old_end(wind_electricity_1)
-1 InvestmentFlowBlock_old_exo(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_2)_:
+1 InvestmentFlowBlock_old(wind_electricity_2)
-1 InvestmentFlowBlock_old_end(wind_electricity_2)
-1 InvestmentFlowBlock_old_exo(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_3)_:
+1 InvestmentFlowBlock_old(wind_electricity_3)
-1 InvestmentFlowBlock_old_end(wind_electricity_3)
-1 InvestmentFlowBlock_old_exo(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_4)_:
+1 InvestmentFlowBlock_old(wind_electricity_4)
-1 InvestmentFlowBlock_old_end(wind_electricity_4)
-1 InvestmentFlowBlock_old_exo(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_5)_:
+1 InvestmentFlowBlock_old(wind_electricity_5)
-1 InvestmentFlowBlock_old_end(wind_electricity_5)
-1 InvestmentFlowBlock_old_exo(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_6)_:
+1 InvestmentFlowBlock_old(wind_electricity_6)
-1 InvestmentFlowBlock_old_end(wind_electricity_6)
-1 InvestmentFlowBlock_old_exo(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule(wind_electricity_7)_:
+1 InvestmentFlowBlock_old(wind_electricity_7)
-1 InvestmentFlowBlock_old_end(wind_electricity_7)
-1 InvestmentFlowBlock_old_exo(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_0)_:
-1 InvestmentFlowBlock_old_end(pv_electricity_0)
-1 InvestmentFlowBlock_old_exo(pv_electricity_0)
+1 InvestmentFlowBlock_old(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_1)_:
+1 InvestmentFlowBlock_old(pv_electricity_1)
-1 InvestmentFlowBlock_old_end(pv_electricity_1)
-1 InvestmentFlowBlock_old_exo(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_2)_:
+1 InvestmentFlowBlock_old(pv_electricity_2)
-1 InvestmentFlowBlock_old_end(pv_electricity_2)
-1 InvestmentFlowBlock_old_exo(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_3)_:
+1 InvestmentFlowBlock_old(pv_electricity_3)
-1 InvestmentFlowBlock_old_end(pv_electricity_3)
-1 InvestmentFlowBlock_old_exo(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_4)_:
+1 InvestmentFlowBlock_old(pv_electricity_4)
-1 InvestmentFlowBlock_old_end(pv_electricity_4)
-1 InvestmentFlowBlock_old_exo(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_5)_:
+1 InvestmentFlowBlock_old(pv_electricity_5)
-1 InvestmentFlowBlock_old_end(pv_electricity_5)
-1 InvestmentFlowBlock_old_exo(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_6)_:
+1 InvestmentFlowBlock_old(pv_electricity_6)
-1 InvestmentFlowBlock_old_end(pv_electricity_6)
-1 InvestmentFlowBlock_old_exo(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule(pv_electricity_7)_:
+1 InvestmentFlowBlock_old(pv_electricity_7)
-1 InvestmentFlowBlock_old_end(pv_electricity_7)
-1 InvestmentFlowBlock_old_exo(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_0)_:
-1 InvestmentFlowBlock_old_end(storage_electricity_0)
-1 InvestmentFlowBlock_old_exo(storage_electricity_0)
+1 InvestmentFlowBlock_old(storage_electricity_0)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_1)_:
+1 InvestmentFlowBlock_old(storage_electricity_1)
-1 InvestmentFlowBlock_old_end(storage_electricity_1)
-1 InvestmentFlowBlock_old_exo(storage_electricity_1)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_2)_:
+1 InvestmentFlowBlock_old(storage_electricity_2)
-1 InvestmentFlowBlock_old_end(storage_electricity_2)
-1 InvestmentFlowBlock_old_exo(storage_electricity_2)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_3)_:
+1 InvestmentFlowBlock_old(storage_electricity_3)
-1 InvestmentFlowBlock_old_end(storage_electricity_3)
-1 InvestmentFlowBlock_old_exo(storage_electricity_3)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_4)_:
+1 InvestmentFlowBlock_old(storage_electricity_4)
-1 InvestmentFlowBlock_old_end(storage_electricity_4)
-1 InvestmentFlowBlock_old_exo(storage_electricity_4)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_5)_:
+1 InvestmentFlowBlock_old(storage_electricity_5)
-1 InvestmentFlowBlock_old_end(storage_electricity_5)
-1 InvestmentFlowBlock_old_exo(storage_electricity_5)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_6)_:
+1 InvestmentFlowBlock_old(storage_electricity_6)
-1 InvestmentFlowBlock_old_end(storage_electricity_6)
-1 InvestmentFlowBlock_old_exo(storage_electricity_6)
= 0

c_e_InvestmentFlowBlock_old_rule(storage_electricity_7)_:
+1 InvestmentFlowBlock_old(storage_electricity_7)
-1 InvestmentFlowBlock_old_end(storage_electricity_7)
-1 InvestmentFlowBlock_old_exo(storage_electricity_7)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_0)_:
-1 InvestmentFlowBlock_old_end(electricity_storage_0)
-1 InvestmentFlowBlock_old_exo(electricity_storage_0)
+1 InvestmentFlowBlock_old(electricity_storage_0)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_1)_:
+1 InvestmentFlowBlock_old(electricity_storage_1)
-1 InvestmentFlowBlock_old_end(electricity_storage_1)
-1 InvestmentFlowBlock_old_exo(electricity_storage_1)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_2)_:
+1 InvestmentFlowBlock_old(electricity_storage_2)
-1 InvestmentFlowBlock_old_end(electricity_storage_2)
-1 InvestmentFlowBlock_old_exo(electricity_storage_2)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_3)_:
+1 InvestmentFlowBlock_old(electricity_storage_3)
-1 InvestmentFlowBlock_old_end(electricity_storage_3)
-1 InvestmentFlowBlock_old_exo(electricity_storage_3)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_4)_:
+1 InvestmentFlowBlock_old(electricity_storage_4)
-1 InvestmentFlowBlock_old_end(electricity_storage_4)
-1 InvestmentFlowBlock_old_exo(electricity_storage_4)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_5)_:
+1 InvestmentFlowBlock_old(electricity_storage_5)
-1 InvestmentFlowBlock_old_end(electricity_storage_5)
-1 InvestmentFlowBlock_old_exo(electricity_storage_5)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_6)_:
+1 InvestmentFlowBlock_old(electricity_storage_6)
-1 InvestmentFlowBlock_old_end(electricity_storage_6)
-1 InvestmentFlowBlock_old_exo(electricity_storage_6)
= 0

c_e_InvestmentFlowBlock_old_rule(electricity_storage_7)_:
+1 InvestmentFlowBlock_old(electricity_storage_7)
-1 InvestmentFlowBlock_old_end(electricity_storage_7)
-1 InvestmentFlowBlock_old_exo(electricity_storage_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_0)_:
+1 flow(wind_electricity_0_0)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_1)_:
+1 flow(wind_electricity_0_1)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_2)_:
+1 flow(wind_electricity_0_2)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_3)_:
+1 flow(wind_electricity_0_3)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_4)_:
+1 flow(wind_electricity_0_4)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_5)_:
+1 flow(wind_electricity_0_5)
-0.2 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_6)_:
+1 flow(wind_electricity_0_6)
-0.2 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_7)_:
+1 flow(wind_electricity_0_7)
-0.2 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_8)_:
+1 flow(wind_electricity_0_8)
-0.2 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_9)_:
+1 flow(wind_electricity_0_9)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_10)_:
+1 flow(wind_electricity_0_10)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_0_11)_:
+1 flow(wind_electricity_0_11)
-0.1 InvestmentFlowBlock_total(wind_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_12)_:
+1 flow(wind_electricity_1_12)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_13)_:
+1 flow(wind_electricity_1_13)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_14)_:
+1 flow(wind_electricity_1_14)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_15)_:
+1 flow(wind_electricity_1_15)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_16)_:
+1 flow(wind_electricity_1_16)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_17)_:
+1 flow(wind_electricity_1_17)
-0.2 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_18)_:
+1 flow(wind_electricity_1_18)
-0.2 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_19)_:
+1 flow(wind_electricity_1_19)
-0.2 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_20)_:
+1 flow(wind_electricity_1_20)
-0.2 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_21)_:
+1 flow(wind_electricity_1_21)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_22)_:
+1 flow(wind_electricity_1_22)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_1_23)_:
+1 flow(wind_electricity_1_23)
-0.1 InvestmentFlowBlock_total(wind_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_24)_:
+1 flow(wind_electricity_2_24)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_25)_:
+1 flow(wind_electricity_2_25)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_26)_:
+1 flow(wind_electricity_2_26)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_27)_:
+1 flow(wind_electricity_2_27)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_28)_:
+1 flow(wind_electricity_2_28)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_29)_:
+1 flow(wind_electricity_2_29)
-0.2 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_30)_:
+1 flow(wind_electricity_2_30)
-0.2 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_31)_:
+1 flow(wind_electricity_2_31)
-0.2 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_32)_:
+1 flow(wind_electricity_2_32)
-0.2 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_33)_:
+1 flow(wind_electricity_2_33)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_34)_:
+1 flow(wind_electricity_2_34)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_2_35)_:
+1 flow(wind_electricity_2_35)
-0.1 InvestmentFlowBlock_total(wind_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_36)_:
+1 flow(wind_electricity_3_36)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_37)_:
+1 flow(wind_electricity_3_37)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_38)_:
+1 flow(wind_electricity_3_38)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_39)_:
+1 flow(wind_electricity_3_39)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_40)_:
+1 flow(wind_electricity_3_40)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_41)_:
+1 flow(wind_electricity_3_41)
-0.2 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_42)_:
+1 flow(wind_electricity_3_42)
-0.2 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_43)_:
+1 flow(wind_electricity_3_43)
-0.2 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_44)_:
+1 flow(wind_electricity_3_44)
-0.2 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_45)_:
+1 flow(wind_electricity_3_45)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_46)_:
+1 flow(wind_electricity_3_46)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_3_47)_:
+1 flow(wind_electricity_3_47)
-0.1 InvestmentFlowBlock_total(wind_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_48)_:
+1 flow(wind_electricity_4_48)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_49)_:
+1 flow(wind_electricity_4_49)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_50)_:
+1 flow(wind_electricity_4_50)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_51)_:
+1 flow(wind_electricity_4_51)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_52)_:
+1 flow(wind_electricity_4_52)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_53)_:
+1 flow(wind_electricity_4_53)
-0.2 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_54)_:
+1 flow(wind_electricity_4_54)
-0.2 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_55)_:
+1 flow(wind_electricity_4_55)
-0.2 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_56)_:
+1 flow(wind_electricity_4_56)
-0.2 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_57)_:
+1 flow(wind_electricity_4_57)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_58)_:
+1 flow(wind_electricity_4_58)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_4_59)_:
+1 flow(wind_electricity_4_59)
-0.1 InvestmentFlowBlock_total(wind_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_60)_:
+1 flow(wind_electricity_5_60)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_61)_:
+1 flow(wind_electricity_5_61)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_62)_:
+1 flow(wind_electricity_5_62)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_63)_:
+1 flow(wind_electricity_5_63)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_64)_:
+1 flow(wind_electricity_5_64)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_65)_:
+1 flow(wind_electricity_5_65)
-0.2 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_66)_:
+1 flow(wind_electricity_5_66)
-0.2 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_67)_:
+1 flow(wind_electricity_5_67)
-0.2 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_68)_:
+1 flow(wind_electricity_5_68)
-0.2 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_69)_:
+1 flow(wind_electricity_5_69)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_70)_:
+1 flow(wind_electricity_5_70)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_5_71)_:
+1 flow(wind_electricity_5_71)
-0.1 InvestmentFlowBlock_total(wind_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_72)_:
+1 flow(wind_electricity_6_72)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_73)_:
+1 flow(wind_electricity_6_73)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_74)_:
+1 flow(wind_electricity_6_74)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_75)_:
+1 flow(wind_electricity_6_75)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_76)_:
+1 flow(wind_electricity_6_76)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_77)_:
+1 flow(wind_electricity_6_77)
-0.2 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_78)_:
+1 flow(wind_electricity_6_78)
-0.2 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_79)_:
+1 flow(wind_electricity_6_79)
-0.2 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_80)_:
+1 flow(wind_electricity_6_80)
-0.2 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_81)_:
+1 flow(wind_electricity_6_81)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_82)_:
+1 flow(wind_electricity_6_82)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_6_83)_:
+1 flow(wind_electricity_6_83)
-0.1 InvestmentFlowBlock_total(wind_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_84)_:
+1 flow(wind_electricity_7_84)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_85)_:
+1 flow(wind_electricity_7_85)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_86)_:
+1 flow(wind_electricity_7_86)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_87)_:
+1 flow(wind_electricity_7_87)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_88)_:
+1 flow(wind_electricity_7_88)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_89)_:
+1 flow(wind_electricity_7_89)
-0.2 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_90)_:
+1 flow(wind_electricity_7_90)
-0.2 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_91)_:
+1 flow(wind_electricity_7_91)
-0.2 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_92)_:
+1 flow(wind_electricity_7_92)
-0.2 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_93)_:
+1 flow(wind_electricity_7_93)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_94)_:
+1 flow(wind_electricity_7_94)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(wind_electricity_7_95)_:
+1 flow(wind_electricity_7_95)
-0.1 InvestmentFlowBlock_total(wind_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_0)_:
+1 flow(pv_electricity_0_0)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_1)_:
+1 flow(pv_electricity_0_1)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_2)_:
+1 flow(pv_electricity_0_2)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_3)_:
+1 flow(pv_electricity_0_3)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_4)_:
+1 flow(pv_electricity_0_4)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_5)_:
+1 flow(pv_electricity_0_5)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_6)_:
+1 flow(pv_electricity_0_6)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_7)_:
+1 flow(pv_electricity_0_7)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_8)_:
+1 flow(pv_electricity_0_8)
-0.1 InvestmentFlowBlock_total(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_9)_:
+1 flow(pv_electricity_0_9)
-0.1 InvestmentFlowBlock_total(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_10)_:
+1 flow(pv_electricity_0_10)
-0.1 InvestmentFlowBlock_total(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_0_11)_:
+1 flow(pv_electricity_0_11)
-0.1 InvestmentFlowBlock_total(pv_electricity_0)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_12)_:
+1 flow(pv_electricity_1_12)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_13)_:
+1 flow(pv_electricity_1_13)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_14)_:
+1 flow(pv_electricity_1_14)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_15)_:
+1 flow(pv_electricity_1_15)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_16)_:
+1 flow(pv_electricity_1_16)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_17)_:
+1 flow(pv_electricity_1_17)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_18)_:
+1 flow(pv_electricity_1_18)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_19)_:
+1 flow(pv_electricity_1_19)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_20)_:
+1 flow(pv_electricity_1_20)
-0.1 InvestmentFlowBlock_total(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_21)_:
+1 flow(pv_electricity_1_21)
-0.1 InvestmentFlowBlock_total(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_22)_:
+1 flow(pv_electricity_1_22)
-0.1 InvestmentFlowBlock_total(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_1_23)_:
+1 flow(pv_electricity_1_23)
-0.1 InvestmentFlowBlock_total(pv_electricity_1)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_24)_:
+1 flow(pv_electricity_2_24)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_25)_:
+1 flow(pv_electricity_2_25)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_26)_:
+1 flow(pv_electricity_2_26)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_27)_:
+1 flow(pv_electricity_2_27)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_28)_:
+1 flow(pv_electricity_2_28)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_29)_:
+1 flow(pv_electricity_2_29)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_30)_:
+1 flow(pv_electricity_2_30)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_31)_:
+1 flow(pv_electricity_2_31)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_32)_:
+1 flow(pv_electricity_2_32)
-0.1 InvestmentFlowBlock_total(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_33)_:
+1 flow(pv_electricity_2_33)
-0.1 InvestmentFlowBlock_total(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_34)_:
+1 flow(pv_electricity_2_34)
-0.1 InvestmentFlowBlock_total(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_2_35)_:
+1 flow(pv_electricity_2_35)
-0.1 InvestmentFlowBlock_total(pv_electricity_2)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_36)_:
+1 flow(pv_electricity_3_36)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_37)_:
+1 flow(pv_electricity_3_37)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_38)_:
+1 flow(pv_electricity_3_38)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_39)_:
+1 flow(pv_electricity_3_39)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_40)_:
+1 flow(pv_electricity_3_40)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_41)_:
+1 flow(pv_electricity_3_41)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_42)_:
+1 flow(pv_electricity_3_42)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_43)_:
+1 flow(pv_electricity_3_43)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_44)_:
+1 flow(pv_electricity_3_44)
-0.1 InvestmentFlowBlock_total(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_45)_:
+1 flow(pv_electricity_3_45)
-0.1 InvestmentFlowBlock_total(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_46)_:
+1 flow(pv_electricity_3_46)
-0.1 InvestmentFlowBlock_total(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_3_47)_:
+1 flow(pv_electricity_3_47)
-0.1 InvestmentFlowBlock_total(pv_electricity_3)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_48)_:
+1 flow(pv_electricity_4_48)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_49)_:
+1 flow(pv_electricity_4_49)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_50)_:
+1 flow(pv_electricity_4_50)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_51)_:
+1 flow(pv_electricity_4_51)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_52)_:
+1 flow(pv_electricity_4_52)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_53)_:
+1 flow(pv_electricity_4_53)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_54)_:
+1 flow(pv_electricity_4_54)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_55)_:
+1 flow(pv_electricity_4_55)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_56)_:
+1 flow(pv_electricity_4_56)
-0.1 InvestmentFlowBlock_total(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_57)_:
+1 flow(pv_electricity_4_57)
-0.1 InvestmentFlowBlock_total(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_58)_:
+1 flow(pv_electricity_4_58)
-0.1 InvestmentFlowBlock_total(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_4_59)_:
+1 flow(pv_electricity_4_59)
-0.1 InvestmentFlowBlock_total(pv_electricity_4)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_60)_:
+1 flow(pv_electricity_5_60)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_61)_:
+1 flow(pv_electricity_5_61)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_62)_:
+1 flow(pv_electricity_5_62)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_63)_:
+1 flow(pv_electricity_5_63)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_64)_:
+1 flow(pv_electricity_5_64)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_65)_:
+1 flow(pv_electricity_5_65)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_66)_:
+1 flow(pv_electricity_5_66)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_67)_:
+1 flow(pv_electricity_5_67)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_68)_:
+1 flow(pv_electricity_5_68)
-0.1 InvestmentFlowBlock_total(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_69)_:
+1 flow(pv_electricity_5_69)
-0.1 InvestmentFlowBlock_total(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_70)_:
+1 flow(pv_electricity_5_70)
-0.1 InvestmentFlowBlock_total(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_5_71)_:
+1 flow(pv_electricity_5_71)
-0.1 InvestmentFlowBlock_total(pv_electricity_5)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_72)_:
+1 flow(pv_electricity_6_72)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_73)_:
+1 flow(pv_electricity_6_73)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_74)_:
+1 flow(pv_electricity_6_74)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_75)_:
+1 flow(pv_electricity_6_75)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_76)_:
+1 flow(pv_electricity_6_76)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_77)_:
+1 flow(pv_electricity_6_77)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_78)_:
+1 flow(pv_electricity_6_78)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_79)_:
+1 flow(pv_electricity_6_79)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_80)_:
+1 flow(pv_electricity_6_80)
-0.1 InvestmentFlowBlock_total(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_81)_:
+1 flow(pv_electricity_6_81)
-0.1 InvestmentFlowBlock_total(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_82)_:
+1 flow(pv_electricity_6_82)
-0.1 InvestmentFlowBlock_total(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_6_83)_:
+1 flow(pv_electricity_6_83)
-0.1 InvestmentFlowBlock_total(pv_electricity_6)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_84)_:
+1 flow(pv_electricity_7_84)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_85)_:
+1 flow(pv_electricity_7_85)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_86)_:
+1 flow(pv_electricity_7_86)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_87)_:
+1 flow(pv_electricity_7_87)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_88)_:
+1 flow(pv_electricity_7_88)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_89)_:
+1 flow(pv_electricity_7_89)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_90)_:
+1 flow(pv_electricity_7_90)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_91)_:
+1 flow(pv_electricity_7_91)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_92)_:
+1 flow(pv_electricity_7_92)
-0.1 InvestmentFlowBlock_total(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_93)_:
+1 flow(pv_electricity_7_93)
-0.1 InvestmentFlowBlock_total(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_94)_:
+1 flow(pv_electricity_7_94)
-0.1 InvestmentFlowBlock_total(pv_electricity_7)
= 0

c_e_InvestmentFlowBlock_fixed(pv_electricity_7_95)_:
+1 flow(pv_electricity_7_95)
-0.1 InvestmentFlowBlock_total(pv_electricity_7)
= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_0)_:
+1 flow(storage_electricity_0_0)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_1)_:
+1 flow(storage_electricity_0_1)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_2)_:
+1 flow(storage_electricity_0_2)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_3)_:
+1 flow(storage_electricity_0_3)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_4)_:
+1 flow(storage_electricity_0_4)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_5)_:
+1 flow(storage_electricity_0_5)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_6)_:
+1 flow(storage_electricity_0_6)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_7)_:
+1 flow(storage_electricity_0_7)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_8)_:
+1 flow(storage_electricity_0_8)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_9)_:
+1 flow(storage_electricity_0_9)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_10)_:
+1 flow(storage_electricity_0_10)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_0_11)_:
+1 flow(storage_electricity_0_11)
-1 InvestmentFlowBlock_total(storage_electricity_0)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_12)_:
+1 flow(storage_electricity_1_12)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_13)_:
+1 flow(storage_electricity_1_13)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_14)_:
+1 flow(storage_electricity_1_14)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_15)_:
+1 flow(storage_electricity_1_15)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_16)_:
+1 flow(storage_electricity_1_16)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_17)_:
+1 flow(storage_electricity_1_17)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_18)_:
+1 flow(storage_electricity_1_18)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_19)_:
+1 flow(storage_electricity_1_19)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_20)_:
+1 flow(storage_electricity_1_20)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_21)_:
+1 flow(storage_electricity_1_21)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_22)_:
+1 flow(storage_electricity_1_22)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_1_23)_:
+1 flow(storage_electricity_1_23)
-1 InvestmentFlowBlock_total(storage_electricity_1)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_24)_:
+1 flow(storage_electricity_2_24)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_25)_:
+1 flow(storage_electricity_2_25)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_26)_:
+1 flow(storage_electricity_2_26)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_27)_:
+1 flow(storage_electricity_2_27)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_28)_:
+1 flow(storage_electricity_2_28)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_29)_:
+1 flow(storage_electricity_2_29)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_30)_:
+1 flow(storage_electricity_2_30)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_31)_:
+1 flow(storage_electricity_2_31)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_32)_:
+1 flow(storage_electricity_2_32)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_33)_:
+1 flow(storage_electricity_2_33)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_34)_:
+1 flow(storage_electricity_2_34)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_2_35)_:
+1 flow(storage_electricity_2_35)
-1 InvestmentFlowBlock_total(storage_electricity_2)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_36)_:
+1 flow(storage_electricity_3_36)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_37)_:
+1 flow(storage_electricity_3_37)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_38)_:
+1 flow(storage_electricity_3_38)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_39)_:
+1 flow(storage_electricity_3_39)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_40)_:
+1 flow(storage_electricity_3_40)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_41)_:
+1 flow(storage_electricity_3_41)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_42)_:
+1 flow(storage_electricity_3_42)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_43)_:
+1 flow(storage_electricity_3_43)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_44)_:
+1 flow(storage_electricity_3_44)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_45)_:
+1 flow(storage_electricity_3_45)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_46)_:
+1 flow(storage_electricity_3_46)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_3_47)_:
+1 flow(storage_electricity_3_47)
-1 InvestmentFlowBlock_total(storage_electricity_3)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_48)_:
+1 flow(storage_electricity_4_48)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_49)_:
+1 flow(storage_electricity_4_49)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_50)_:
+1 flow(storage_electricity_4_50)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_51)_:
+1 flow(storage_electricity_4_51)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_52)_:
+1 flow(storage_electricity_4_52)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_53)_:
+1 flow(storage_electricity_4_53)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_54)_:
+1 flow(storage_electricity_4_54)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_55)_:
+1 flow(storage_electricity_4_55)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_56)_:
+1 flow(storage_electricity_4_56)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_57)_:
+1 flow(storage_electricity_4_57)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_58)_:
+1 flow(storage_electricity_4_58)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_4_59)_:
+1 flow(storage_electricity_4_59)
-1 InvestmentFlowBlock_total(storage_electricity_4)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_60)_:
+1 flow(storage_electricity_5_60)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_61)_:
+1 flow(storage_electricity_5_61)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_62)_:
+1 flow(storage_electricity_5_62)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_63)_:
+1 flow(storage_electricity_5_63)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_64)_:
+1 flow(storage_electricity_5_64)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_65)_:
+1 flow(storage_electricity_5_65)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_66)_:
+1 flow(storage_electricity_5_66)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_67)_:
+1 flow(storage_electricity_5_67)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_68)_:
+1 flow(storage_electricity_5_68)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_69)_:
+1 flow(storage_electricity_5_69)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_70)_:
+1 flow(storage_electricity_5_70)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_5_71)_:
+1 flow(storage_electricity_5_71)
-1 InvestmentFlowBlock_total(storage_electricity_5)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_72)_:
+1 flow(storage_electricity_6_72)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_73)_:
+1 flow(storage_electricity_6_73)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_74)_:
+1 flow(storage_electricity_6_74)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_75)_:
+1 flow(storage_electricity_6_75)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_76)_:
+1 flow(storage_electricity_6_76)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_77)_:
+1 flow(storage_electricity_6_77)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_78)_:
+1 flow(storage_electricity_6_78)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_79)_:
+1 flow(storage_electricity_6_79)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_80)_:
+1 flow(storage_electricity_6_80)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_81)_:
+1 flow(storage_electricity_6_81)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_82)_:
+1 flow(storage_electricity_6_82)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_6_83)_:
+1 flow(storage_electricity_6_83)
-1 InvestmentFlowBlock_total(storage_electricity_6)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_84)_:
+1 flow(storage_electricity_7_84)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_85)_:
+1 flow(storage_electricity_7_85)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_86)_:
+1 flow(storage_electricity_7_86)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_87)_:
+1 flow(storage_electricity_7_87)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_88)_:
+1 flow(storage_electricity_7_88)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_89)_:
+1 flow(storage_electricity_7_89)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_90)_:
+1 flow(storage_electricity_7_90)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_91)_:
+1 flow(storage_electricity_7_91)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_92)_:
+1 flow(storage_electricity_7_92)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_93)_:
+1 flow(storage_electricity_7_93)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_94)_:
+1 flow(storage_electricity_7_94)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(storage_electricity_7_95)_:
+1 flow(storage_electricity_7_95)
-1 InvestmentFlowBlock_total(storage_electricity_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_0)_:
+1 flow(electricity_storage_0_0)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_1)_:
+1 flow(electricity_storage_0_1)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_2)_:
+1 flow(electricity_storage_0_2)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_3)_:
+1 flow(electricity_storage_0_3)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_4)_:
+1 flow(electricity_storage_0_4)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_5)_:
+1 flow(electricity_storage_0_5)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_6)_:
+1 flow(electricity_storage_0_6)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_7)_:
+1 flow(electricity_storage_0_7)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_8)_:
+1 flow(electricity_storage_0_8)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_9)_:
+1 flow(electricity_storage_0_9)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_10)_:
+1 flow(electricity_storage_0_10)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_0_11)_:
+1 flow(electricity_storage_0_11)
-1 InvestmentFlowBlock_total(electricity_storage_0)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_12)_:
+1 flow(electricity_storage_1_12)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_13)_:
+1 flow(electricity_storage_1_13)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_14)_:
+1 flow(electricity_storage_1_14)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_15)_:
+1 flow(electricity_storage_1_15)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_16)_:
+1 flow(electricity_storage_1_16)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_17)_:
+1 flow(electricity_storage_1_17)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_18)_:
+1 flow(electricity_storage_1_18)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_19)_:
+1 flow(electricity_storage_1_19)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_20)_:
+1 flow(electricity_storage_1_20)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_21)_:
+1 flow(electricity_storage_1_21)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_22)_:
+1 flow(electricity_storage_1_22)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_1_23)_:
+1 flow(electricity_storage_1_23)
-1 InvestmentFlowBlock_total(electricity_storage_1)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_24)_:
+1 flow(electricity_storage_2_24)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_25)_:
+1 flow(electricity_storage_2_25)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_26)_:
+1 flow(electricity_storage_2_26)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_27)_:
+1 flow(electricity_storage_2_27)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_28)_:
+1 flow(electricity_storage_2_28)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_29)_:
+1 flow(electricity_storage_2_29)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_30)_:
+1 flow(electricity_storage_2_30)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_31)_:
+1 flow(electricity_storage_2_31)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_32)_:
+1 flow(electricity_storage_2_32)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_33)_:
+1 flow(electricity_storage_2_33)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_34)_:
+1 flow(electricity_storage_2_34)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_2_35)_:
+1 flow(electricity_storage_2_35)
-1 InvestmentFlowBlock_total(electricity_storage_2)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_36)_:
+1 flow(electricity_storage_3_36)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_37)_:
+1 flow(electricity_storage_3_37)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_38)_:
+1 flow(electricity_storage_3_38)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_39)_:
+1 flow(electricity_storage_3_39)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_40)_:
+1 flow(electricity_storage_3_40)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_41)_:
+1 flow(electricity_storage_3_41)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_42)_:
+1 flow(electricity_storage_3_42)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_43)_:
+1 flow(electricity_storage_3_43)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_44)_:
+1 flow(electricity_storage_3_44)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_45)_:
+1 flow(electricity_storage_3_45)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_46)_:
+1 flow(electricity_storage_3_46)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_3_47)_:
+1 flow(electricity_storage_3_47)
-1 InvestmentFlowBlock_total(electricity_storage_3)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_48)_:
+1 flow(electricity_storage_4_48)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_49)_:
+1 flow(electricity_storage_4_49)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_50)_:
+1 flow(electricity_storage_4_50)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_51)_:
+1 flow(electricity_storage_4_51)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_52)_:
+1 flow(electricity_storage_4_52)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_53)_:
+1 flow(electricity_storage_4_53)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_54)_:
+1 flow(electricity_storage_4_54)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_55)_:
+1 flow(electricity_storage_4_55)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_56)_:
+1 flow(electricity_storage_4_56)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_57)_:
+1 flow(electricity_storage_4_57)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_58)_:
+1 flow(electricity_storage_4_58)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_4_59)_:
+1 flow(electricity_storage_4_59)
-1 InvestmentFlowBlock_total(electricity_storage_4)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_60)_:
+1 flow(electricity_storage_5_60)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_61)_:
+1 flow(electricity_storage_5_61)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_62)_:
+1 flow(electricity_storage_5_62)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_63)_:
+1 flow(electricity_storage_5_63)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_64)_:
+1 flow(electricity_storage_5_64)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_65)_:
+1 flow(electricity_storage_5_65)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_66)_:
+1 flow(electricity_storage_5_66)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_67)_:
+1 flow(electricity_storage_5_67)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_68)_:
+1 flow(electricity_storage_5_68)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_69)_:
+1 flow(electricity_storage_5_69)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_70)_:
+1 flow(electricity_storage_5_70)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_5_71)_:
+1 flow(electricity_storage_5_71)
-1 InvestmentFlowBlock_total(electricity_storage_5)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_72)_:
+1 flow(electricity_storage_6_72)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_73)_:
+1 flow(electricity_storage_6_73)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_74)_:
+1 flow(electricity_storage_6_74)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_75)_:
+1 flow(electricity_storage_6_75)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_76)_:
+1 flow(electricity_storage_6_76)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_77)_:
+1 flow(electricity_storage_6_77)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_78)_:
+1 flow(electricity_storage_6_78)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_79)_:
+1 flow(electricity_storage_6_79)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_80)_:
+1 flow(electricity_storage_6_80)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_81)_:
+1 flow(electricity_storage_6_81)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_82)_:
+1 flow(electricity_storage_6_82)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_6_83)_:
+1 flow(electricity_storage_6_83)
-1 InvestmentFlowBlock_total(electricity_storage_6)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_84)_:
+1 flow(electricity_storage_7_84)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_85)_:
+1 flow(electricity_storage_7_85)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_86)_:
+1 flow(electricity_storage_7_86)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_87)_:
+1 flow(electricity_storage_7_87)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_88)_:
+1 flow(electricity_storage_7_88)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_89)_:
+1 flow(electricity_storage_7_89)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_90)_:
+1 flow(electricity_storage_7_90)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_91)_:
+1 flow(electricity_storage_7_91)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_92)_:
+1 flow(electricity_storage_7_92)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_93)_:
+1 flow(electricity_storage_7_93)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_94)_:
+1 flow(electricity_storage_7_94)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_u_InvestmentFlowBlock_max(electricity_storage_7_95)_:
+1 flow(electricity_storage_7_95)
-1 InvestmentFlowBlock_total(electricity_storage_7)
<= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_1)
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_old(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_2)_:
-1 GenericInvestmentStorageBlock_invest(storage_2)
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_old(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_3)_:
-1 GenericInvestmentStorageBlock_invest(storage_3)
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_old(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_4)_:
-1 GenericInvestmentStorageBlock_invest(storage_4)
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_old(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_5)_:
-1 GenericInvestmentStorageBlock_invest(storage_5)
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_old(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_6)_:
-1 GenericInvestmentStorageBlock_invest(storage_6)
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_old(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_total_storage_rule(storage_7)_:
-1 GenericInvestmentStorageBlock_invest(storage_7)
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_old(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_0)_:
+1 GenericInvestmentStorageBlock_old_end(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_1)_:
-1 GenericInvestmentStorageBlock_invest(storage_0)
+1 GenericInvestmentStorageBlock_old_end(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_2)_:
+1 GenericInvestmentStorageBlock_old_end(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_3)_:
-1 GenericInvestmentStorageBlock_invest(storage_1)
+1 GenericInvestmentStorageBlock_old_end(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_4)_:
+1 GenericInvestmentStorageBlock_old_end(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_5)_:
-1 GenericInvestmentStorageBlock_invest(storage_2)
+1 GenericInvestmentStorageBlock_old_end(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_6)_:
-1 GenericInvestmentStorageBlock_invest(storage_3)
-1 GenericInvestmentStorageBlock_invest(storage_4)
+1 GenericInvestmentStorageBlock_old_end(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_end(storage_7)_:
-1 GenericInvestmentStorageBlock_invest(storage_5)
-1 GenericInvestmentStorageBlock_invest(storage_6)
+1 GenericInvestmentStorageBlock_old_end(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_0)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_1)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_2)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_3)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_4)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_5)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_6)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_old_rule_exo(storage_7)_:
+1 GenericInvestmentStorageBlock_old_exo(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_0)_:
-1 GenericInvestmentStorageBlock_old_end(storage_0)
-1 GenericInvestmentStorageBlock_old_exo(storage_0)
+1 GenericInvestmentStorageBlock_old(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_1)_:
+1 GenericInvestmentStorageBlock_old(storage_1)
-1 GenericInvestmentStorageBlock_old_end(storage_1)
-1 GenericInvestmentStorageBlock_old_exo(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_2)_:
+1 GenericInvestmentStorageBlock_old(storage_2)
-1 GenericInvestmentStorageBlock_old_end(storage_2)
-1 GenericInvestmentStorageBlock_old_exo(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_3)_:
+1 GenericInvestmentStorageBlock_old(storage_3)
-1 GenericInvestmentStorageBlock_old_end(storage_3)
-1 GenericInvestmentStorageBlock_old_exo(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_4)_:
+1 GenericInvestmentStorageBlock_old(storage_4)
-1 GenericInvestmentStorageBlock_old_end(storage_4)
-1 GenericInvestmentStorageBlock_old_exo(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_5)_:
+1 GenericInvestmentStorageBlock_old(storage_5)
-1 GenericInvestmentStorageBlock_old_end(storage_5)
-1 GenericInvestmentStorageBlock_old_exo(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_6)_:
+1 GenericInvestmentStorageBlock_old(storage_6)
-1 GenericInvestmentStorageBlock_old_end(storage_6)
-1 GenericInvestmentStorageBlock_old_exo(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_old_rule(storage_7)_:
+1 GenericInvestmentStorageBlock_old(storage_7)
-1 GenericInvestmentStorageBlock_old_end(storage_7)
-1 GenericInvestmentStorageBlock_old_exo(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_1)_:
+1 flow(storage_electricity_0_1)
-1 flow(electricity_storage_0_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
-1 GenericInvestmentStorageBlock_storage_content(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_2)_:
+1 flow(storage_electricity_0_2)
-1 flow(electricity_storage_0_2)
-1 GenericInvestmentStorageBlock_storage_content(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_3)_:
+1 flow(storage_electricity_0_3)
-1 flow(electricity_storage_0_3)
-1 GenericInvestmentStorageBlock_storage_content(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_4)_:
+1 flow(storage_electricity_0_4)
-1 flow(electricity_storage_0_4)
-1 GenericInvestmentStorageBlock_storage_content(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_5)_:
+1 flow(storage_electricity_0_5)
-1 flow(electricity_storage_0_5)
-1 GenericInvestmentStorageBlock_storage_content(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_6)_:
+1 flow(storage_electricity_0_6)
-1 flow(electricity_storage_0_6)
-1 GenericInvestmentStorageBlock_storage_content(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_7)_:
+1 flow(storage_electricity_0_7)
-1 flow(electricity_storage_0_7)
-1 GenericInvestmentStorageBlock_storage_content(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_8)_:
+1 flow(storage_electricity_0_8)
-1 flow(electricity_storage_0_8)
-1 GenericInvestmentStorageBlock_storage_content(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_9)_:
+1 flow(storage_electricity_0_9)
-1 flow(electricity_storage_0_9)
-1 GenericInvestmentStorageBlock_storage_content(storage_8)
+1 GenericInvestmentStorageBlock_storage_content(storage_9)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_10)_:
+1 flow(storage_electricity_0_10)
-1 flow(electricity_storage_0_10)
-1 GenericInvestmentStorageBlock_storage_content(storage_9)
+1 GenericInvestmentStorageBlock_storage_content(storage_10)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_0_11)_:
+1 flow(storage_electricity_0_11)
-1 flow(electricity_storage_0_11)
-1 GenericInvestmentStorageBlock_storage_content(storage_10)
+1 GenericInvestmentStorageBlock_storage_content(storage_11)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_12)_:
+1 flow(storage_electricity_1_12)
-1 flow(electricity_storage_1_12)
-1 GenericInvestmentStorageBlock_storage_content(storage_11)
+1 GenericInvestmentStorageBlock_storage_content(storage_12)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_13)_:
+1 flow(storage_electricity_1_13)
-1 flow(electricity_storage_1_13)
-1 GenericInvestmentStorageBlock_storage_content(storage_12)
+1 GenericInvestmentStorageBlock_storage_content(storage_13)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_14)_:
+1 flow(storage_electricity_1_14)
-1 flow(electricity_storage_1_14)
-1 GenericInvestmentStorageBlock_storage_content(storage_13)
+1 GenericInvestmentStorageBlock_storage_content(storage_14)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_15)_:
+1 flow(storage_electricity_1_15)
-1 flow(electricity_storage_1_15)
-1 GenericInvestmentStorageBlock_storage_content(storage_14)
+1 GenericInvestmentStorageBlock_storage_content(storage_15)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_16)_:
+1 flow(storage_electricity_1_16)
-1 flow(electricity_storage_1_16)
-1 GenericInvestmentStorageBlock_storage_content(storage_15)
+1 GenericInvestmentStorageBlock_storage_content(storage_16)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_17)_:
+1 flow(storage_electricity_1_17)
-1 flow(electricity_storage_1_17)
-1 GenericInvestmentStorageBlock_storage_content(storage_16)
+1 GenericInvestmentStorageBlock_storage_content(storage_17)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_18)_:
+1 flow(storage_electricity_1_18)
-1 flow(electricity_storage_1_18)
-1 GenericInvestmentStorageBlock_storage_content(storage_17)
+1 GenericInvestmentStorageBlock_storage_content(storage_18)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_19)_:
+1 flow(storage_electricity_1_19)
-1 flow(electricity_storage_1_19)
-1 GenericInvestmentStorageBlock_storage_content(storage_18)
+1 GenericInvestmentStorageBlock_storage_content(storage_19)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_20)_:
+1 flow(storage_electricity_1_20)
-1 flow(electricity_storage_1_20)
-1 GenericInvestmentStorageBlock_storage_content(storage_19)
+1 GenericInvestmentStorageBlock_storage_content(storage_20)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_21)_:
+1 flow(storage_electricity_1_21)
-1 flow(electricity_storage_1_21)
-1 GenericInvestmentStorageBlock_storage_content(storage_20)
+1 GenericInvestmentStorageBlock_storage_content(storage_21)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_22)_:
+1 flow(storage_electricity_1_22)
-1 flow(electricity_storage_1_22)
-1 GenericInvestmentStorageBlock_storage_content(storage_21)
+1 GenericInvestmentStorageBlock_storage_content(storage_22)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_1_23)_:
+1 flow(storage_electricity_1_23)
-1 flow(electricity_storage_1_23)
-1 GenericInvestmentStorageBlock_storage_content(storage_22)
+1 GenericInvestmentStorageBlock_storage_content(storage_23)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_24)_:
+1 flow(storage_electricity_2_24)
-1 flow(electricity_storage_2_24)
-1 GenericInvestmentStorageBlock_storage_content(storage_23)
+1 GenericInvestmentStorageBlock_storage_content(storage_24)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_25)_:
+1 flow(storage_electricity_2_25)
-1 flow(electricity_storage_2_25)
-1 GenericInvestmentStorageBlock_storage_content(storage_24)
+1 GenericInvestmentStorageBlock_storage_content(storage_25)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_26)_:
+1 flow(storage_electricity_2_26)
-1 flow(electricity_storage_2_26)
-1 GenericInvestmentStorageBlock_storage_content(storage_25)
+1 GenericInvestmentStorageBlock_storage_content(storage_26)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_27)_:
+1 flow(storage_electricity_2_27)
-1 flow(electricity_storage_2_27)
-1 GenericInvestmentStorageBlock_storage_content(storage_26)
+1 GenericInvestmentStorageBlock_storage_content(storage_27)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_28)_:
+1 flow(storage_electricity_2_28)
-1 flow(electricity_storage_2_28)
-1 GenericInvestmentStorageBlock_storage_content(storage_27)
+1 GenericInvestmentStorageBlock_storage_content(storage_28)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_29)_:
+1 flow(storage_electricity_2_29)
-1 flow(electricity_storage_2_29)
-1 GenericInvestmentStorageBlock_storage_content(storage_28)
+1 GenericInvestmentStorageBlock_storage_content(storage_29)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_30)_:
+1 flow(storage_electricity_2_30)
-1 flow(electricity_storage_2_30)
-1 GenericInvestmentStorageBlock_storage_content(storage_29)
+1 GenericInvestmentStorageBlock_storage_content(storage_30)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_31)_:
+1 flow(storage_electricity_2_31)
-1 flow(electricity_storage_2_31)
-1 GenericInvestmentStorageBlock_storage_content(storage_30)
+1 GenericInvestmentStorageBlock_storage_content(storage_31)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_32)_:
+1 flow(storage_electricity_2_32)
-1 flow(electricity_storage_2_32)
-1 GenericInvestmentStorageBlock_storage_content(storage_31)
+1 GenericInvestmentStorageBlock_storage_content(storage_32)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_33)_:
+1 flow(storage_electricity_2_33)
-1 flow(electricity_storage_2_33)
-1 GenericInvestmentStorageBlock_storage_content(storage_32)
+1 GenericInvestmentStorageBlock_storage_content(storage_33)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_34)_:
+1 flow(storage_electricity_2_34)
-1 flow(electricity_storage_2_34)
-1 GenericInvestmentStorageBlock_storage_content(storage_33)
+1 GenericInvestmentStorageBlock_storage_content(storage_34)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_2_35)_:
+1 flow(storage_electricity_2_35)
-1 flow(electricity_storage_2_35)
-1 GenericInvestmentStorageBlock_storage_content(storage_34)
+1 GenericInvestmentStorageBlock_storage_content(storage_35)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_36)_:
+1 flow(storage_electricity_3_36)
-1 flow(electricity_storage_3_36)
-1 GenericInvestmentStorageBlock_storage_content(storage_35)
+1 GenericInvestmentStorageBlock_storage_content(storage_36)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_37)_:
+1 flow(storage_electricity_3_37)
-1 flow(electricity_storage_3_37)
-1 GenericInvestmentStorageBlock_storage_content(storage_36)
+1 GenericInvestmentStorageBlock_storage_content(storage_37)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_38)_:
+1 flow(storage_electricity_3_38)
-1 flow(electricity_storage_3_38)
-1 GenericInvestmentStorageBlock_storage_content(storage_37)
+1 GenericInvestmentStorageBlock_storage_content(storage_38)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_39)_:
+1 flow(storage_electricity_3_39)
-1 flow(electricity_storage_3_39)
-1 GenericInvestmentStorageBlock_storage_content(storage_38)
+1 GenericInvestmentStorageBlock_storage_content(storage_39)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_40)_:
+1 flow(storage_electricity_3_40)
-1 flow(electricity_storage_3_40)
-1 GenericInvestmentStorageBlock_storage_content(storage_39)
+1 GenericInvestmentStorageBlock_storage_content(storage_40)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_41)_:
+1 flow(storage_electricity_3_41)
-1 flow(electricity_storage_3_41)
-1 GenericInvestmentStorageBlock_storage_content(storage_40)
+1 GenericInvestmentStorageBlock_storage_content(storage_41)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_42)_:
+1 flow(storage_electricity_3_42)
-1 flow(electricity_storage_3_42)
-1 GenericInvestmentStorageBlock_storage_content(storage_41)
+1 GenericInvestmentStorageBlock_storage_content(storage_42)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_43)_:
+1 flow(storage_electricity_3_43)
-1 flow(electricity_storage_3_43)
-1 GenericInvestmentStorageBlock_storage_content(storage_42)
+1 GenericInvestmentStorageBlock_storage_content(storage_43)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_44)_:
+1 flow(storage_electricity_3_44)
-1 flow(electricity_storage_3_44)
-1 GenericInvestmentStorageBlock_storage_content(storage_43)
+1 GenericInvestmentStorageBlock_storage_content(storage_44)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_45)_:
+1 flow(storage_electricity_3_45)
-1 flow(electricity_storage_3_45)
-1 GenericInvestmentStorageBlock_storage_content(storage_44)
+1 GenericInvestmentStorageBlock_storage_content(storage_45)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_46)_:
+1 flow(storage_electricity_3_46)
-1 flow(electricity_storage_3_46)
-1 GenericInvestmentStorageBlock_storage_content(storage_45)
+1 GenericInvestmentStorageBlock_storage_content(storage_46)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_3_47)_:
+1 flow(storage_electricity_3_47)
-1 flow(electricity_storage_3_47)
-1 GenericInvestmentStorageBlock_storage_content(storage_46)
+1 GenericInvestmentStorageBlock_storage_content(storage_47)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_48)_:
+1 flow(storage_electricity_4_48)
-1 flow(electricity_storage_4_48)
-1 GenericInvestmentStorageBlock_storage_content(storage_47)
+1 GenericInvestmentStorageBlock_storage_content(storage_48)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_49)_:
+1 flow(storage_electricity_4_49)
-1 flow(electricity_storage_4_49)
-1 GenericInvestmentStorageBlock_storage_content(storage_48)
+1 GenericInvestmentStorageBlock_storage_content(storage_49)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_50)_:
+1 flow(storage_electricity_4_50)
-1 flow(electricity_storage_4_50)
-1 GenericInvestmentStorageBlock_storage_content(storage_49)
+1 GenericInvestmentStorageBlock_storage_content(storage_50)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_51)_:
+1 flow(storage_electricity_4_51)
-1 flow(electricity_storage_4_51)
-1 GenericInvestmentStorageBlock_storage_content(storage_50)
+1 GenericInvestmentStorageBlock_storage_content(storage_51)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_52)_:
+1 flow(storage_electricity_4_52)
-1 flow(electricity_storage_4_52)
-1 GenericInvestmentStorageBlock_storage_content(storage_51)
+1 GenericInvestmentStorageBlock_storage_content(storage_52)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_53)_:
+1 flow(storage_electricity_4_53)
-1 flow(electricity_storage_4_53)
-1 GenericInvestmentStorageBlock_storage_content(storage_52)
+1 GenericInvestmentStorageBlock_storage_content(storage_53)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_54)_:
+1 flow(storage_electricity_4_54)
-1 flow(electricity_storage_4_54)
-1 GenericInvestmentStorageBlock_storage_content(storage_53)
+1 GenericInvestmentStorageBlock_storage_content(storage_54)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_55)_:
+1 flow(storage_electricity_4_55)
-1 flow(electricity_storage_4_55)
-1 GenericInvestmentStorageBlock_storage_content(storage_54)
+1 GenericInvestmentStorageBlock_storage_content(storage_55)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_56)_:
+1 flow(storage_electricity_4_56)
-1 flow(electricity_storage_4_56)
-1 GenericInvestmentStorageBlock_storage_content(storage_55)
+1 GenericInvestmentStorageBlock_storage_content(storage_56)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_57)_:
+1 flow(storage_electricity_4_57)
-1 flow(electricity_storage_4_57)
-1 GenericInvestmentStorageBlock_storage_content(storage_56)
+1 GenericInvestmentStorageBlock_storage_content(storage_57)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_58)_:
+1 flow(storage_electricity_4_58)
-1 flow(electricity_storage_4_58)
-1 GenericInvestmentStorageBlock_storage_content(storage_57)
+1 GenericInvestmentStorageBlock_storage_content(storage_58)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_4_59)_:
+1 flow(storage_electricity_4_59)
-1 flow(electricity_storage_4_59)
-1 GenericInvestmentStorageBlock_storage_content(storage_58)
+1 GenericInvestmentStorageBlock_storage_content(storage_59)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_60)_:
+1 flow(storage_electricity_5_60)
-1 flow(electricity_storage_5_60)
-1 GenericInvestmentStorageBlock_storage_content(storage_59)
+1 GenericInvestmentStorageBlock_storage_content(storage_60)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_61)_:
+1 flow(storage_electricity_5_61)
-1 flow(electricity_storage_5_61)
-1 GenericInvestmentStorageBlock_storage_content(storage_60)
+1 GenericInvestmentStorageBlock_storage_content(storage_61)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_62)_:
+1 flow(storage_electricity_5_62)
-1 flow(electricity_storage_5_62)
-1 GenericInvestmentStorageBlock_storage_content(storage_61)
+1 GenericInvestmentStorageBlock_storage_content(storage_62)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_63)_:
+1 flow(storage_electricity_5_63)
-1 flow(electricity_storage_5_63)
-1 GenericInvestmentStorageBlock_storage_content(storage_62)
+1 GenericInvestmentStorageBlock_storage_content(storage_63)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_64)_:
+1 flow(storage_electricity_5_64)
-1 flow(electricity_storage_5_64)
-1 GenericInvestmentStorageBlock_storage_content(storage_63)
+1 GenericInvestmentStorageBlock_storage_content(storage_64)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_65)_:
+1 flow(storage_electricity_5_65)
-1 flow(electricity_storage_5_65)
-1 GenericInvestmentStorageBlock_storage_content(storage_64)
+1 GenericInvestmentStorageBlock_storage_content(storage_65)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_66)_:
+1 flow(storage_electricity_5_66)
-1 flow(electricity_storage_5_66)
-1 GenericInvestmentStorageBlock_storage_content(storage_65)
+1 GenericInvestmentStorageBlock_storage_content(storage_66)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_67)_:
+1 flow(storage_electricity_5_67)
-1 flow(electricity_storage_5_67)
-1 GenericInvestmentStorageBlock_storage_content(storage_66)
+1 GenericInvestmentStorageBlock_storage_content(storage_67)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_68)_:
+1 flow(storage_electricity_5_68)
-1 flow(electricity_storage_5_68)
-1 GenericInvestmentStorageBlock_storage_content(storage_67)
+1 GenericInvestmentStorageBlock_storage_content(storage_68)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_69)_:
+1 flow(storage_electricity_5_69)
-1 flow(electricity_storage_5_69)
-1 GenericInvestmentStorageBlock_storage_content(storage_68)
+1 GenericInvestmentStorageBlock_storage_content(storage_69)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_70)_:
+1 flow(storage_electricity_5_70)
-1 flow(electricity_storage_5_70)
-1 GenericInvestmentStorageBlock_storage_content(storage_69)
+1 GenericInvestmentStorageBlock_storage_content(storage_70)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_5_71)_:
+1 flow(storage_electricity_5_71)
-1 flow(electricity_storage_5_71)
-1 GenericInvestmentStorageBlock_storage_content(storage_70)
+1 GenericInvestmentStorageBlock_storage_content(storage_71)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_72)_:
+1 flow(storage_electricity_6_72)
-1 flow(electricity_storage_6_72)
-1 GenericInvestmentStorageBlock_storage_content(storage_71)
+1 GenericInvestmentStorageBlock_storage_content(storage_72)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_73)_:
+1 flow(storage_electricity_6_73)
-1 flow(electricity_storage_6_73)
-1 GenericInvestmentStorageBlock_storage_content(storage_72)
+1 GenericInvestmentStorageBlock_storage_content(storage_73)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_74)_:
+1 flow(storage_electricity_6_74)
-1 flow(electricity_storage_6_74)
-1 GenericInvestmentStorageBlock_storage_content(storage_73)
+1 GenericInvestmentStorageBlock_storage_content(storage_74)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_75)_:
+1 flow(storage_electricity_6_75)
-1 flow(electricity_storage_6_75)
-1 GenericInvestmentStorageBlock_storage_content(storage_74)
+1 GenericInvestmentStorageBlock_storage_content(storage_75)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_76)_:
+1 flow(storage_electricity_6_76)
-1 flow(electricity_storage_6_76)
-1 GenericInvestmentStorageBlock_storage_content(storage_75)
+1 GenericInvestmentStorageBlock_storage_content(storage_76)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_77)_:
+1 flow(storage_electricity_6_77)
-1 flow(electricity_storage_6_77)
-1 GenericInvestmentStorageBlock_storage_content(storage_76)
+1 GenericInvestmentStorageBlock_storage_content(storage_77)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_78)_:
+1 flow(storage_electricity_6_78)
-1 flow(electricity_storage_6_78)
-1 GenericInvestmentStorageBlock_storage_content(storage_77)
+1 GenericInvestmentStorageBlock_storage_content(storage_78)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_79)_:
+1 flow(storage_electricity_6_79)
-1 flow(electricity_storage_6_79)
-1 GenericInvestmentStorageBlock_storage_content(storage_78)
+1 GenericInvestmentStorageBlock_storage_content(storage_79)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_80)_:
+1 flow(storage_electricity_6_80)
-1 flow(electricity_storage_6_80)
-1 GenericInvestmentStorageBlock_storage_content(storage_79)
+1 GenericInvestmentStorageBlock_storage_content(storage_80)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_81)_:
+1 flow(storage_electricity_6_81)
-1 flow(electricity_storage_6_81)
-1 GenericInvestmentStorageBlock_storage_content(storage_80)
+1 GenericInvestmentStorageBlock_storage_content(storage_81)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_82)_:
+1 flow(storage_electricity_6_82)
-1 flow(electricity_storage_6_82)
-1 GenericInvestmentStorageBlock_storage_content(storage_81)
+1 GenericInvestmentStorageBlock_storage_content(storage_82)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_6_83)_:
+1 flow(storage_electricity_6_83)
-1 flow(electricity_storage_6_83)
-1 GenericInvestmentStorageBlock_storage_content(storage_82)
+1 GenericInvestmentStorageBlock_storage_content(storage_83)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_84)_:
+1 flow(storage_electricity_7_84)
-1 flow(electricity_storage_7_84)
-1 GenericInvestmentStorageBlock_storage_content(storage_83)
+1 GenericInvestmentStorageBlock_storage_content(storage_84)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_85)_:
+1 flow(storage_electricity_7_85)
-1 flow(electricity_storage_7_85)
-1 GenericInvestmentStorageBlock_storage_content(storage_84)
+1 GenericInvestmentStorageBlock_storage_content(storage_85)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_86)_:
+1 flow(storage_electricity_7_86)
-1 flow(electricity_storage_7_86)
-1 GenericInvestmentStorageBlock_storage_content(storage_85)
+1 GenericInvestmentStorageBlock_storage_content(storage_86)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_87)_:
+1 flow(storage_electricity_7_87)
-1 flow(electricity_storage_7_87)
-1 GenericInvestmentStorageBlock_storage_content(storage_86)
+1 GenericInvestmentStorageBlock_storage_content(storage_87)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_88)_:
+1 flow(storage_electricity_7_88)
-1 flow(electricity_storage_7_88)
-1 GenericInvestmentStorageBlock_storage_content(storage_87)
+1 GenericInvestmentStorageBlock_storage_content(storage_88)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_89)_:
+1 flow(storage_electricity_7_89)
-1 flow(electricity_storage_7_89)
-1 GenericInvestmentStorageBlock_storage_content(storage_88)
+1 GenericInvestmentStorageBlock_storage_content(storage_89)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_90)_:
+1 flow(storage_electricity_7_90)
-1 flow(electricity_storage_7_90)
-1 GenericInvestmentStorageBlock_storage_content(storage_89)
+1 GenericInvestmentStorageBlock_storage_content(storage_90)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_91)_:
+1 flow(storage_electricity_7_91)
-1 flow(electricity_storage_7_91)
-1 GenericInvestmentStorageBlock_storage_content(storage_90)
+1 GenericInvestmentStorageBlock_storage_content(storage_91)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_92)_:
+1 flow(storage_electricity_7_92)
-1 flow(electricity_storage_7_92)
-1 GenericInvestmentStorageBlock_storage_content(storage_91)
+1 GenericInvestmentStorageBlock_storage_content(storage_92)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_93)_:
+1 flow(storage_electricity_7_93)
-1 flow(electricity_storage_7_93)
-1 GenericInvestmentStorageBlock_storage_content(storage_92)
+1 GenericInvestmentStorageBlock_storage_content(storage_93)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_94)_:
+1 flow(storage_electricity_7_94)
-1 flow(electricity_storage_7_94)
-1 GenericInvestmentStorageBlock_storage_content(storage_93)
+1 GenericInvestmentStorageBlock_storage_content(storage_94)
= 0

c_e_GenericInvestmentStorageBlock_balance(storage_7_95)_:
+1 flow(storage_electricity_7_95)
-1 flow(electricity_storage_7_95)
-1 GenericInvestmentStorageBlock_storage_content(storage_94)
+1 GenericInvestmentStorageBlock_storage_content(storage_95)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_0)_:
+1 InvestmentFlowBlock_total(storage_electricity_0)
-1 InvestmentFlowBlock_total(electricity_storage_0)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_1)_:
+1 InvestmentFlowBlock_total(storage_electricity_1)
-1 InvestmentFlowBlock_total(electricity_storage_1)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_2)_:
+1 InvestmentFlowBlock_total(storage_electricity_2)
-1 InvestmentFlowBlock_total(electricity_storage_2)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_3)_:
+1 InvestmentFlowBlock_total(storage_electricity_3)
-1 InvestmentFlowBlock_total(electricity_storage_3)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_4)_:
+1 InvestmentFlowBlock_total(storage_electricity_4)
-1 InvestmentFlowBlock_total(electricity_storage_4)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_5)_:
+1 InvestmentFlowBlock_total(storage_electricity_5)
-1 InvestmentFlowBlock_total(electricity_storage_5)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_6)_:
+1 InvestmentFlowBlock_total(storage_electricity_6)
-1 InvestmentFlowBlock_total(electricity_storage_6)
= 0

c_e_GenericInvestmentStorageBlock_power_coupled(storage_7)_:
+1 InvestmentFlowBlock_total(storage_electricity_7)
-1 InvestmentFlowBlock_total(electricity_storage_7)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_0)_:
+1 InvestmentFlowBlock_total(storage_electricity_0)
-0.2 GenericInvestmentStorageBlock_total(storage_0)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_1)_:
+1 InvestmentFlowBlock_total(storage_electricity_1)
-0.2 GenericInvestmentStorageBlock_total(storage_1)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_2)_:
+1 InvestmentFlowBlock_total(storage_electricity_2)
-0.2 GenericInvestmentStorageBlock_total(storage_2)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_3)_:
+1 InvestmentFlowBlock_total(storage_electricity_3)
-0.2 GenericInvestmentStorageBlock_total(storage_3)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_4)_:
+1 InvestmentFlowBlock_total(storage_electricity_4)
-0.2 GenericInvestmentStorageBlock_total(storage_4)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_5)_:
+1 InvestmentFlowBlock_total(storage_electricity_5)
-0.2 GenericInvestmentStorageBlock_total(storage_5)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_6)_:
+1 InvestmentFlowBlock_total(storage_electricity_6)
-0.2 GenericInvestmentStorageBlock_total(storage_6)
= 0

c_e_GenericInvestmentStorageBlock_storage_capacity_outflow(storage_7)_:
+1 InvestmentFlowBlock_total(storage_electricity_7)
-0.2 GenericInvestmentStorageBlock_total(storage_7)
= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_0)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_0)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_1)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_1)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_2)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_2)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_3)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_3)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_4)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_4)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_5)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_5)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_6)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_6)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_7)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_7)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_8)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_8)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_9)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_9)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_10)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_10)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_0_11)_:
-1 GenericInvestmentStorageBlock_total(storage_0)
+1 GenericInvestmentStorageBlock_storage_content(storage_11)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_12)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_12)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_13)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_13)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_14)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_14)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_15)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_15)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_16)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_16)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_17)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_17)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_18)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_18)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_19)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_19)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_20)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_20)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_21)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_21)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_22)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_22)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_1_23)_:
-1 GenericInvestmentStorageBlock_total(storage_1)
+1 GenericInvestmentStorageBlock_storage_content(storage_23)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_24)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_24)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_25)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_25)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_26)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_26)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_27)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_27)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_28)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_28)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_29)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_29)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_30)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_30)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_31)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_31)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_32)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_32)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_33)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_33)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_34)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_34)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_2_35)_:
-1 GenericInvestmentStorageBlock_total(storage_2)
+1 GenericInvestmentStorageBlock_storage_content(storage_35)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_36)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_36)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_37)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_37)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_38)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_38)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_39)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_39)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_40)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_40)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_41)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_41)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_42)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_42)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_43)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_43)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_44)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_44)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_45)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_45)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_46)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_46)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_3_47)_:
-1 GenericInvestmentStorageBlock_total(storage_3)
+1 GenericInvestmentStorageBlock_storage_content(storage_47)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_48)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_48)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_49)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_49)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_50)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_50)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_51)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_51)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_52)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_52)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_53)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_53)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_54)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_54)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_55)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_55)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_56)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_56)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_57)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_57)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_58)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_58)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_4_59)_:
-1 GenericInvestmentStorageBlock_total(storage_4)
+1 GenericInvestmentStorageBlock_storage_content(storage_59)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_60)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_60)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_61)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_61)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_62)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_62)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_63)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_63)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_64)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_64)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_65)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_65)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_66)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_66)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_67)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_67)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_68)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_68)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_69)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_69)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_70)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_70)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_5_71)_:
-1 GenericInvestmentStorageBlock_total(storage_5)
+1 GenericInvestmentStorageBlock_storage_content(storage_71)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_72)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_72)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_73)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_73)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_74)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_74)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_75)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_75)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_76)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_76)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_77)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_77)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_78)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_78)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_79)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_79)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_80)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_80)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_81)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_81)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_82)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_82)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_6_83)_:
-1 GenericInvestmentStorageBlock_total(storage_6)
+1 GenericInvestmentStorageBlock_storage_content(storage_83)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_84)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_84)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_85)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_85)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_86)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_86)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_87)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_87)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_88)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_88)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_89)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_89)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_90)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_90)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_91)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_91)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_92)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_92)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_93)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_93)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_94)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_94)
<= 0

c_u_GenericInvestmentStorageBlock_max_storage_content(storage_7_95)_:
-1 GenericInvestmentStorageBlock_total(storage_7)
+1 GenericInvestmentStorageBlock_storage_content(storage_95)
<= 0

bounds
   0 <= InvestmentFlowBlock_invest(wind_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_invest(wind_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_invest(pv_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_invest(storage_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_3) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_4) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_5) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_6) <= +inf
   0 <= InvestmentFlowBlock_invest(electricity_storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_invest(storage_7) <= +inf
   0 <= flow(pv_electricity_0_0) <= +inf
   0 <= flow(storage_electricity_0_0) <= +inf
   0 <= flow(wind_electricity_0_0) <= +inf
   0 <= flow(electricity_storage_0_0) <= +inf
   0 <= flow(pv_electricity_0_1) <= +inf
   0 <= flow(storage_electricity_0_1) <= +inf
   0 <= flow(wind_electricity_0_1) <= +inf
   0 <= flow(electricity_storage_0_1) <= +inf
   0 <= flow(pv_electricity_0_2) <= +inf
   0 <= flow(storage_electricity_0_2) <= +inf
   0 <= flow(wind_electricity_0_2) <= +inf
   0 <= flow(electricity_storage_0_2) <= +inf
   0 <= flow(pv_electricity_0_3) <= +inf
   0 <= flow(storage_electricity_0_3) <= +inf
   0 <= flow(wind_electricity_0_3) <= +inf
   0 <= flow(electricity_storage_0_3) <= +inf
   0 <= flow(pv_electricity_0_4) <= +inf
   0 <= flow(storage_electricity_0_4) <= +inf
   0 <= flow(wind_electricity_0_4) <= +inf
   0 <= flow(electricity_storage_0_4) <= +inf
   0 <= flow(pv_electricity_0_5) <= +inf
   0 <= flow(storage_electricity_0_5) <= +inf
   0 <= flow(wind_electricity_0_5) <= +inf
   0 <= flow(electricity_storage_0_5) <= +inf
   0 <= flow(pv_electricity_0_6) <= +inf
   0 <= flow(storage_electricity_0_6) <= +inf
   0 <= flow(wind_electricity_0_6) <= +inf
   0 <= flow(electricity_storage_0_6) <= +inf
   0 <= flow(pv_electricity_0_7) <= +inf
   0 <= flow(storage_electricity_0_7) <= +inf
   0 <= flow(wind_electricity_0_7) <= +inf
   0 <= flow(electricity_storage_0_7) <= +inf
   0 <= flow(pv_electricity_0_8) <= +inf
   0 <= flow(storage_electricity_0_8) <= +inf
   0 <= flow(wind_electricity_0_8) <= +inf
   0 <= flow(electricity_storage_0_8) <= +inf
   0 <= flow(pv_electricity_0_9) <= +inf
   0 <= flow(storage_electricity_0_9) <= +inf
   0 <= flow(wind_electricity_0_9) <= +inf
   0 <= flow(electricity_storage_0_9) <= +inf
   0 <= flow(pv_electricity_0_10) <= +inf
   0 <= flow(storage_electricity_0_10) <= +inf
   0 <= flow(wind_electricity_0_10) <= +inf
   0 <= flow(electricity_storage_0_10) <= +inf
   0 <= flow(pv_electricity_0_11) <= +inf
   0 <= flow(storage_electricity_0_11) <= +inf
   0 <= flow(wind_electricity_0_11) <= +inf
   0 <= flow(electricity_storage_0_11) <= +inf
   0 <= flow(pv_electricity_1_12) <= +inf
   0 <= flow(storage_electricity_1_12) <= +inf
   0 <= flow(wind_electricity_1_12) <= +inf
   0 <= flow(electricity_storage_1_12) <= +inf
   0 <= flow(pv_electricity_1_13) <= +inf
   0 <= flow(storage_electricity_1_13) <= +inf
   0 <= flow(wind_electricity_1_13) <= +inf
   0 <= flow(electricity_storage_1_13) <= +inf
   0 <= flow(pv_electricity_1_14) <= +inf
   0 <= flow(storage_electricity_1_14) <= +inf
   0 <= flow(wind_electricity_1_14) <= +inf
   0 <= flow(electricity_storage_1_14) <= +inf
   0 <= flow(pv_electricity_1_15) <= +inf
   0 <= flow(storage_electricity_1_15) <= +inf
   0 <= flow(wind_electricity_1_15) <= +inf
   0 <= flow(electricity_storage_1_15) <= +inf
   0 <= flow(pv_electricity_1_16) <= +inf
   0 <= flow(storage_electricity_1_16) <= +inf
   0 <= flow(wind_electricity_1_16) <= +inf
   0 <= flow(electricity_storage_1_16) <= +inf
   0 <= flow(pv_electricity_1_17) <= +inf
   0 <= flow(storage_electricity_1_17) <= +inf
   0 <= flow(wind_electricity_1_17) <= +inf
   0 <= flow(electricity_storage_1_17) <= +inf
   0 <= flow(pv_electricity_1_18) <= +inf
   0 <= flow(storage_electricity_1_18) <= +inf
   0 <= flow(wind_electricity_1_18) <= +inf
   0 <= flow(electricity_storage_1_18) <= +inf
   0 <= flow(pv_electricity_1_19) <= +inf
   0 <= flow(storage_electricity_1_19) <= +inf
   0 <= flow(wind_electricity_1_19) <= +inf
   0 <= flow(electricity_storage_1_19) <= +inf
   0 <= flow(pv_electricity_1_20) <= +inf
   0 <= flow(storage_electricity_1_20) <= +inf
   0 <= flow(wind_electricity_1_20) <= +inf
   0 <= flow(electricity_storage_1_20) <= +inf
   0 <= flow(pv_electricity_1_21) <= +inf
   0 <= flow(storage_electricity_1_21) <= +inf
   0 <= flow(wind_electricity_1_21) <= +inf
   0 <= flow(electricity_storage_1_21) <= +inf
   0 <= flow(pv_electricity_1_22) <= +inf
   0 <= flow(storage_electricity_1_22) <= +inf
   0 <= flow(wind_electricity_1_22) <= +inf
   0 <= flow(electricity_storage_1_22) <= +inf
   0 <= flow(pv_electricity_1_23) <= +inf
   0 <= flow(storage_electricity_1_23) <= +inf
   0 <= flow(wind_electricity_1_23) <= +inf
   0 <= flow(electricity_storage_1_23) <= +inf
   0 <= flow(pv_electricity_2_24) <= +inf
   0 <= flow(storage_electricity_2_24) <= +inf
   0 <= flow(wind_electricity_2_24) <= +inf
   0 <= flow(electricity_storage_2_24) <= +inf
   0 <= flow(pv_electricity_2_25) <= +inf
   0 <= flow(storage_electricity_2_25) <= +inf
   0 <= flow(wind_electricity_2_25) <= +inf
   0 <= flow(electricity_storage_2_25) <= +inf
   0 <= flow(pv_electricity_2_26) <= +inf
   0 <= flow(storage_electricity_2_26) <= +inf
   0 <= flow(wind_electricity_2_26) <= +inf
   0 <= flow(electricity_storage_2_26) <= +inf
   0 <= flow(pv_electricity_2_27) <= +inf
   0 <= flow(storage_electricity_2_27) <= +inf
   0 <= flow(wind_electricity_2_27) <= +inf
   0 <= flow(electricity_storage_2_27) <= +inf
   0 <= flow(pv_electricity_2_28) <= +inf
   0 <= flow(storage_electricity_2_28) <= +inf
   0 <= flow(wind_electricity_2_28) <= +inf
   0 <= flow(electricity_storage_2_28) <= +inf
   0 <= flow(pv_electricity_2_29) <= +inf
   0 <= flow(storage_electricity_2_29) <= +inf
   0 <= flow(wind_electricity_2_29) <= +inf
   0 <= flow(electricity_storage_2_29) <= +inf
   0 <= flow(pv_electricity_2_30) <= +inf
   0 <= flow(storage_electricity_2_30) <= +inf
   0 <= flow(wind_electricity_2_30) <= +inf
   0 <= flow(electricity_storage_2_30) <= +inf
   0 <= flow(pv_electricity_2_31) <= +inf
   0 <= flow(storage_electricity_2_31) <= +inf
   0 <= flow(wind_electricity_2_31) <= +inf
   0 <= flow(electricity_storage_2_31) <= +inf
   0 <= flow(pv_electricity_2_32) <= +inf
   0 <= flow(storage_electricity_2_32) <= +inf
   0 <= flow(wind_electricity_2_32) <= +inf
   0 <= flow(electricity_storage_2_32) <= +inf
   0 <= flow(pv_electricity_2_33) <= +inf
   0 <= flow(storage_electricity_2_33) <= +inf
   0 <= flow(wind_electricity_2_33) <= +inf
   0 <= flow(electricity_storage_2_33) <= +inf
   0 <= flow(pv_electricity_2_34) <= +inf
   0 <= flow(storage_electricity_2_34) <= +inf
   0 <= flow(wind_electricity_2_34) <= +inf
   0 <= flow(electricity_storage_2_34) <= +inf
   0 <= flow(pv_electricity_2_35) <= +inf
   0 <= flow(storage_electricity_2_35) <= +inf
   0 <= flow(wind_electricity_2_35) <= +inf
   0 <= flow(electricity_storage_2_35) <= +inf
   0 <= flow(pv_electricity_3_36) <= +inf
   0 <= flow(storage_electricity_3_36) <= +inf
   0 <= flow(wind_electricity_3_36) <= +inf
   0 <= flow(electricity_storage_3_36) <= +inf
   0 <= flow(pv_electricity_3_37) <= +inf
   0 <= flow(storage_electricity_3_37) <= +inf
   0 <= flow(wind_electricity_3_37) <= +inf
   0 <= flow(electricity_storage_3_37) <= +inf
   0 <= flow(pv_electricity_3_38) <= +inf
   0 <= flow(storage_electricity_3_38) <= +inf
   0 <= flow(wind_electricity_3_38) <= +inf
   0 <= flow(electricity_storage_3_38) <= +inf
   0 <= flow(pv_electricity_3_39) <= +inf
   0 <= flow(storage_electricity_3_39) <= +inf
   0 <= flow(wind_electricity_3_39) <= +inf
   0 <= flow(electricity_storage_3_39) <= +inf
   0 <= flow(pv_electricity_3_40) <= +inf
   0 <= flow(storage_electricity_3_40) <= +inf
   0 <= flow(wind_electricity_3_40) <= +inf
   0 <= flow(electricity_storage_3_40) <= +inf
   0 <= flow(pv_electricity_3_41) <= +inf
   0 <= flow(storage_electricity_3_41) <= +inf
   0 <= flow(wind_electricity_3_41) <= +inf
   0 <= flow(electricity_storage_3_41) <= +inf
   0 <= flow(pv_electricity_3_42) <= +inf
   0 <= flow(storage_electricity_3_42) <= +inf
   0 <= flow(wind_electricity_3_42) <= +inf
   0 <= flow(electricity_storage_3_42) <= +inf
   0 <= flow(pv_electricity_3_43) <= +inf
   0 <= flow(storage_electricity_3_43) <= +inf
   0 <= flow(wind_electricity_3_43) <= +inf
   0 <= flow(electricity_storage_3_43) <= +inf
   0 <= flow(pv_electricity_3_44) <= +inf
   0 <= flow(storage_electricity_3_44) <= +inf
   0 <= flow(wind_electricity_3_44) <= +inf
   0 <= flow(electricity_storage_3_44) <= +inf
   0 <= flow(pv_electricity_3_45) <= +inf
   0 <= flow(storage_electricity_3_45) <= +inf
   0 <= flow(wind_electricity_3_45) <= +inf
   0 <= flow(electricity_storage_3_45) <= +inf
   0 <= flow(pv_electricity_3_46) <= +inf
   0 <= flow(storage_electricity_3_46) <= +inf
   0 <= flow(wind_electricity_3_46) <= +inf
   0 <= flow(electricity_storage_3_46) <= +inf
   0 <= flow(pv_electricity_3_47) <= +inf
   0 <= flow(storage_electricity_3_47) <= +inf
   0 <= flow(wind_electricity_3_47) <= +inf
   0 <= flow(electricity_storage_3_47) <= +inf
   0 <= flow(pv_electricity_4_48) <= +inf
   0 <= flow(storage_electricity_4_48) <= +inf
   0 <= flow(wind_electricity_4_48) <= +inf
   0 <= flow(electricity_storage_4_48) <= +inf
   0 <= flow(pv_electricity_4_49) <= +inf
   0 <= flow(storage_electricity_4_49) <= +inf
   0 <= flow(wind_electricity_4_49) <= +inf
   0 <= flow(electricity_storage_4_49) <= +inf
   0 <= flow(pv_electricity_4_50) <= +inf
   0 <= flow(storage_electricity_4_50) <= +inf
   0 <= flow(wind_electricity_4_50) <= +inf
   0 <= flow(electricity_storage_4_50) <= +inf
   0 <= flow(pv_electricity_4_51) <= +inf
   0 <= flow(storage_electricity_4_51) <= +inf
   0 <= flow(wind_electricity_4_51) <= +inf
   0 <= flow(electricity_storage_4_51) <= +inf
   0 <= flow(pv_electricity_4_52) <= +inf
   0 <= flow(storage_electricity_4_52) <= +inf
   0 <= flow(wind_electricity_4_52) <= +inf
   0 <= flow(electricity_storage_4_52) <= +inf
   0 <= flow(pv_electricity_4_53) <= +inf
   0 <= flow(storage_electricity_4_53) <= +inf
   0 <= flow(wind_electricity_4_53) <= +inf
   0 <= flow(electricity_storage_4_53) <= +inf
   0 <= flow(pv_electricity_4_54) <= +inf
   0 <= flow(storage_electricity_4_54) <= +inf
   0 <= flow(wind_electricity_4_54) <= +inf
   0 <= flow(electricity_storage_4_54) <= +inf
   0 <= flow(pv_electricity_4_55) <= +inf
   0 <= flow(storage_electricity_4_55) <= +inf
   0 <= flow(wind_electricity_4_55) <= +inf
   0 <= flow(electricity_storage_4_55) <= +inf
   0 <= flow(pv_electricity_4_56) <= +inf
   0 <= flow(storage_electricity_4_56) <= +inf
   0 <= flow(wind_electricity_4_56) <= +inf
   0 <= flow(electricity_storage_4_56) <= +inf
   0 <= flow(pv_electricity_4_57) <= +inf
   0 <= flow(storage_electricity_4_57) <= +inf
   0 <= flow(wind_electricity_4_57) <= +inf
   0 <= flow(electricity_storage_4_57) <= +inf
   0 <= flow(pv_electricity_4_58) <= +inf
   0 <= flow(storage_electricity_4_58) <= +inf
   0 <= flow(wind_electricity_4_58) <= +inf
   0 <= flow(electricity_storage_4_58) <= +inf
   0 <= flow(pv_electricity_4_59) <= +inf
   0 <= flow(storage_electricity_4_59) <= +inf
   0 <= flow(wind_electricity_4_59) <= +inf
   0 <= flow(electricity_storage_4_59) <= +inf
   0 <= flow(pv_electricity_5_60) <= +inf
   0 <= flow(storage_electricity_5_60) <= +inf
   0 <= flow(wind_electricity_5_60) <= +inf
   0 <= flow(electricity_storage_5_60) <= +inf
   0 <= flow(pv_electricity_5_61) <= +inf
   0 <= flow(storage_electricity_5_61) <= +inf
   0 <= flow(wind_electricity_5_61) <= +inf
   0 <= flow(electricity_storage_5_61) <= +inf
   0 <= flow(pv_electricity_5_62) <= +inf
   0 <= flow(storage_electricity_5_62) <= +inf
   0 <= flow(wind_electricity_5_62) <= +inf
   0 <= flow(electricity_storage_5_62) <= +inf
   0 <= flow(pv_electricity_5_63) <= +inf
   0 <= flow(storage_electricity_5_63) <= +inf
   0 <= flow(wind_electricity_5_63) <= +inf
   0 <= flow(electricity_storage_5_63) <= +inf
   0 <= flow(pv_electricity_5_64) <= +inf
   0 <= flow(storage_electricity_5_64) <= +inf
   0 <= flow(wind_electricity_5_64) <= +inf
   0 <= flow(electricity_storage_5_64) <= +inf
   0 <= flow(pv_electricity_5_65) <= +inf
   0 <= flow(storage_electricity_5_65) <= +inf
   0 <= flow(wind_electricity_5_65) <= +inf
   0 <= flow(electricity_storage_5_65) <= +inf
   0 <= flow(pv_electricity_5_66) <= +inf
   0 <= flow(storage_electricity_5_66) <= +inf
   0 <= flow(wind_electricity_5_66) <= +inf
   0 <= flow(electricity_storage_5_66) <= +inf
   0 <= flow(pv_electricity_5_67) <= +inf
   0 <= flow(storage_electricity_5_67) <= +inf
   0 <= flow(wind_electricity_5_67) <= +inf
   0 <= flow(electricity_storage_5_67) <= +inf
   0 <= flow(pv_electricity_5_68) <= +inf
   0 <= flow(storage_electricity_5_68) <= +inf
   0 <= flow(wind_electricity_5_68) <= +inf
   0 <= flow(electricity_storage_5_68) <= +inf
   0 <= flow(pv_electricity_5_69) <= +inf
   0 <= flow(storage_electricity_5_69) <= +inf
   0 <= flow(wind_electricity_5_69) <= +inf
   0 <= flow(electricity_storage_5_69) <= +inf
   0 <= flow(pv_electricity_5_70) <= +inf
   0 <= flow(storage_electricity_5_70) <= +inf
   0 <= flow(wind_electricity_5_70) <= +inf
   0 <= flow(electricity_storage_5_70) <= +inf
   0 <= flow(pv_electricity_5_71) <= +inf
   0 <= flow(storage_electricity_5_71) <= +inf
   0 <= flow(wind_electricity_5_71) <= +inf
   0 <= flow(electricity_storage_5_71) <= +inf
   0 <= flow(pv_electricity_6_72) <= +inf
   0 <= flow(storage_electricity_6_72) <= +inf
   0 <= flow(wind_electricity_6_72) <= +inf
   0 <= flow(electricity_storage_6_72) <= +inf
   0 <= flow(pv_electricity_6_73) <= +inf
   0 <= flow(storage_electricity_6_73) <= +inf
   0 <= flow(wind_electricity_6_73) <= +inf
   0 <= flow(electricity_storage_6_73) <= +inf
   0 <= flow(pv_electricity_6_74) <= +inf
   0 <= flow(storage_electricity_6_74) <= +inf
   0 <= flow(wind_electricity_6_74) <= +inf
   0 <= flow(electricity_storage_6_74) <= +inf
   0 <= flow(pv_electricity_6_75) <= +inf
   0 <= flow(storage_electricity_6_75) <= +inf
   0 <= flow(wind_electricity_6_75) <= +inf
   0 <= flow(electricity_storage_6_75) <= +inf
   0 <= flow(pv_electricity_6_76) <= +inf
   0 <= flow(storage_electricity_6_76) <= +inf
   0 <= flow(wind_electricity_6_76) <= +inf
   0 <= flow(electricity_storage_6_76) <= +inf
   0 <= flow(pv_electricity_6_77) <= +inf
   0 <= flow(storage_electricity_6_77) <= +inf
   0 <= flow(wind_electricity_6_77) <= +inf
   0 <= flow(electricity_storage_6_77) <= +inf
   0 <= flow(pv_electricity_6_78) <= +inf
   0 <= flow(storage_electricity_6_78) <= +inf
   0 <= flow(wind_electricity_6_78) <= +inf
   0 <= flow(electricity_storage_6_78) <= +inf
   0 <= flow(pv_electricity_6_79) <= +inf
   0 <= flow(storage_electricity_6_79) <= +inf
   0 <= flow(wind_electricity_6_79) <= +inf
   0 <= flow(electricity_storage_6_79) <= +inf
   0 <= flow(pv_electricity_6_80) <= +inf
   0 <= flow(storage_electricity_6_80) <= +inf
   0 <= flow(wind_electricity_6_80) <= +inf
   0 <= flow(electricity_storage_6_80) <= +inf
   0 <= flow(pv_electricity_6_81) <= +inf
   0 <= flow(storage_electricity_6_81) <= +inf
   0 <= flow(wind_electricity_6_81) <= +inf
   0 <= flow(electricity_storage_6_81) <= +inf
   0 <= flow(pv_electricity_6_82) <= +inf
   0 <= flow(storage_electricity_6_82) <= +inf
   0 <= flow(wind_electricity_6_82) <= +inf
   0 <= flow(electricity_storage_6_82) <= +inf
   0 <= flow(pv_electricity_6_83) <= +inf
   0 <= flow(storage_electricity_6_83) <= +inf
   0 <= flow(wind_electricity_6_83) <= +inf
   0 <= flow(electricity_storage_6_83) <= +inf
   0 <= flow(pv_electricity_7_84) <= +inf
   0 <= flow(storage_electricity_7_84) <= +inf
   0 <= flow(wind_electricity_7_84) <= +inf
   0 <= flow(electricity_storage_7_84) <= +inf
   0 <= flow(pv_electricity_7_85) <= +inf
   0 <= flow(storage_electricity_7_85) <= +inf
   0 <= flow(wind_electricity_7_85) <= +inf
   0 <= flow(electricity_storage_7_85) <= +inf
   0 <= flow(pv_electricity_7_86) <= +inf
   0 <= flow(storage_electricity_7_86) <= +inf
   0 <= flow(wind_electricity_7_86) <= +inf
   0 <= flow(electricity_storage_7_86) <= +inf
   0 <= flow(pv_electricity_7_87) <= +inf
   0 <= flow(storage_electricity_7_87) <= +inf
   0 <= flow(wind_electricity_7_87) <= +inf
   0 <= flow(electricity_storage_7_87) <= +inf
   0 <= flow(pv_electricity_7_88) <= +inf
   0 <= flow(storage_electricity_7_88) <= +inf
   0 <= flow(wind_electricity_7_88) <= +inf
   0 <= flow(electricity_storage_7_88) <= +inf
   0 <= flow(pv_electricity_7_89) <= +inf
   0 <= flow(storage_electricity_7_89) <= +inf
   0 <= flow(wind_electricity_7_89) <= +inf
   0 <= flow(electricity_storage_7_89) <= +inf
   0 <= flow(pv_electricity_7_90) <= +inf
   0 <= flow(storage_electricity_7_90) <= +inf
   0 <= flow(wind_electricity_7_90) <= +inf
   0 <= flow(electricity_storage_7_90) <= +inf
   0 <= flow(pv_electricity_7_91) <= +inf
   0 <= flow(storage_electricity_7_91) <= +inf
   0 <= flow(wind_electricity_7_91) <= +inf
   0 <= flow(electricity_storage_7_91) <= +inf
   0 <= flow(pv_electricity_7_92) <= +inf
   0 <= flow(storage_electricity_7_92) <= +inf
   0 <= flow(wind_electricity_7_92) <= +inf
   0 <= flow(electricity_storage_7_92) <= +inf
   0 <= flow(pv_electricity_7_93) <= +inf
   0 <= flow(storage_electricity_7_93) <= +inf
   0 <= flow(wind_electricity_7_93) <= +inf
   0 <= flow(electricity_storage_7_93) <= +inf
   0 <= flow(pv_electricity_7_94) <= +inf
   0 <= flow(storage_electricity_7_94) <= +inf
   0 <= flow(wind_electricity_7_94) <= +inf
   0 <= flow(electricity_storage_7_94) <= +inf
   0 <= flow(pv_electricity_7_95) <= +inf
   0 <= flow(storage_electricity_7_95) <= +inf
   0 <= flow(wind_electricity_7_95) <= +inf
   0 <= flow(electricity_storage_7_95) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_total(wind_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_total(pv_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_total(storage_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_3) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_3) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_4) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_4) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_5) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_5) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_6) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_6) <= +inf
   0 <= InvestmentFlowBlock_total(electricity_storage_7) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_7) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_end(wind_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_end(pv_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_end(storage_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_3) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_4) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_5) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_6) <= +inf
   0 <= InvestmentFlowBlock_old_end(electricity_storage_7) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_exo(wind_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_exo(pv_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_3) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_4) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_5) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_6) <= +inf
   0 <= InvestmentFlowBlock_old_exo(storage_electricity_7) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_0) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_1) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_2) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_3) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_4) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_5) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_6) <= +inf
   0 <= InvestmentFlowBlock_old_exo(electricity_storage_7) <= +inf
   0 <= InvestmentFlowBlock_old(wind_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old(pv_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old(storage_electricity_0) <= +inf
   0 <= InvestmentFlowBlock_old(electricity_storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_total(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_old_end(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_old_exo(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_old(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_1) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_0) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_2) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_3) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_4) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_5) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_6) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_7) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_8) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_9) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_10) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_11) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_12) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_13) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_14) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_15) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_16) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_17) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_18) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_19) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_20) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_21) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_22) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_23) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_24) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_25) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_26) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_27) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_28) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_29) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_30) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_31) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_32) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_33) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_34) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_35) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_36) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_37) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_38) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_39) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_40) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_41) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_42) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_43) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_44) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_45) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_46) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_47) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_48) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_49) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_50) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_51) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_52) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_53) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_54) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_55) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_56) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_57) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_58) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_59) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_60) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_61) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_62) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_63) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_64) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_65) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_66) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_67) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_68) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_69) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_70) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_71) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_72) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_73) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_74) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_75) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_76) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_77) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_78) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_79) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_80) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_81) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_82) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_83) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_84) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_85) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_86) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_87) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_88) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_89) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_90) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_91) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_92) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_93) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_94) <= +inf
   0 <= GenericInvestmentStorageBlock_storage_content(storage_95) <= +inf
end
