
# %%[func_lcoh_start]
def LCOH(invest_cost, operation_cost, heat_produced, revenue=0, i=0.05, n=20):
    pvf = ((1 + i)**n - 1)/((1 + i)**n * i)

    return (invest_cost + pvf * (operation_cost - revenue))/(pvf * heat_produced)
# %%[func_lcoh_end]


# %%[func_epc_start]
def epc(capex, lifetime=20, wacc=0.05):
    epc = capex * (wacc * (1 + wacc) ** lifetime) / ((1 + wacc) ** lifetime - 1)
    return epc
# %%[func_epc_end]