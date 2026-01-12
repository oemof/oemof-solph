import os
import pandas as pd
import numpy as np
import oemof.solph as solph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pyomo.environ as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import matplotlib.patches as mpatches

# Import der Baukasten-Funktionen
# (Stelle sicher, dass deine custom_constraints.py aktuell ist!)
from custom_constraints import (
    add_multi_market_constraints, 
    add_transformer_load_constraints, 
    calculate_activation_profile_with_volume
)

# =============================================================================
# 0. KONFIGURATION
# =============================================================================
FILENAME = 'market_data.csv'
SIMULATION_DAYS = 4 

# --- A) Batteriespeicher (BESS) ---
BESS_P_MAX = 5.0        # [MW] Leistung
BESS_E_MAX = 10.0       # [MWh] Kapazität
BESS_EFFICIENCY = 0.95 
BESS_INITIAL_SOC = 0.5 

# --- B) Power-to-Heat (PtH / E-Boiler) ---
PTH_P_MAX = 5.0         # [MW] Thermische Leistung
PTH_EFFICIENCY = 0.99   # Strom zu Wärme
PTH_VAR_COST = 0.5      # [€/MWh] Verschleißkosten

# --- C) Wärmespeicher (TES) ---
TES_CAPACITY = 15.0     # [MWh]
TES_LOSS = 0.005        # 0.5% Verlust pro Stunde

# --- Strategien ---
BID_BESS_POS = 100.0    # BESS will teuer verkaufen
BID_BESS_NEG = 10.0     # BESS will billig kaufen

BID_PTH_NEG = 50.0      # PtH zahlt bis zu 50€ fürs Heizen (oder kriegt Geld)
BID_PTH_POS = 150.0     # PtH will 150€ fürs Abschalten

# CSV Spalten
COL_ACT_POS_MW = 'aFRR_Activation_Pos_MW'
COL_ACT_NEG_MW = 'aFRR_Activation_Neg_MW'

# =============================================================================
# MAIN SIMULATION
# =============================================================================
if __name__ == "__main__":
    
    # --- 1. DATEN LADEN ---
    filename = FILENAME
    if not os.path.exists(filename): filename = os.path.join('Datamining', FILENAME)
    
    print(f"Lade Daten von: {filename}")
    try:
        data = pd.read_csv(filename, sep=';', decimal=',')
        if 'Unnamed: 0' in data.columns:
            data.rename(columns={'Unnamed: 0': 'timestamp'}, inplace=True)
            data.set_index('timestamp', inplace=True)
        data.index = pd.to_datetime(data.index)
        
        periods = 96 * SIMULATION_DAYS
        data_slice = data.head(periods).copy()
    except Exception as e:
        print(f"FEHLER: {e}. Bitte CSV prüfen.")
        exit()

    # Spalten bereinigen
    cols_to_fix = ['Spotmarkt_Preis', 'FCR_Leistungspreis', 
                   'aFRR_Pos_Leistungspreis', 'aFRR_Neg_Leistungspreis',
                   'aFRR_Pos_Arbeitspreis', 'aFRR_Neg_Arbeitspreis',
                   COL_ACT_POS_MW, COL_ACT_NEG_MW]
    
    for col in cols_to_fix:
        if col in data_slice.columns:
            data_slice[col] = pd.to_numeric(data_slice[col], errors='coerce').fillna(0)

    # --- 1b. WÄRMEBEDARF (Profil generieren) ---
    hour = data_slice.index.hour
    heat_profile_base = 1.0 + 1.5 * np.sin((hour - 6) * np.pi / 12)**2 
    heat_demand = heat_profile_base * 1.5 + np.random.normal(0, 0.2, len(data_slice))
    data_slice['Heat_Demand'] = np.clip(heat_demand, 0, PTH_P_MAX * 0.9)

    # --- 2. PROFILE BERECHNEN ---
    print("Berechne Aktivierungsprofile...")
    
    # BESS Profile
    prof_bess_pos = calculate_activation_profile_with_volume(
        data_slice['aFRR_Pos_Arbeitspreis'], data_slice[COL_ACT_POS_MW], BID_BESS_POS, BESS_P_MAX)
    prof_bess_neg = calculate_activation_profile_with_volume(
        data_slice['aFRR_Neg_Arbeitspreis'], data_slice[COL_ACT_NEG_MW].abs(), BID_BESS_NEG, BESS_P_MAX)

    # PtH Profile
    prof_pth_pos = calculate_activation_profile_with_volume(
        data_slice['aFRR_Pos_Arbeitspreis'], data_slice[COL_ACT_POS_MW], BID_PTH_POS, PTH_P_MAX)
    prof_pth_neg = calculate_activation_profile_with_volume(
        data_slice['aFRR_Neg_Arbeitspreis'], data_slice[COL_ACT_NEG_MW].abs(), BID_PTH_NEG, PTH_P_MAX)

    # --- 3. ENERGIESYSTEM ---
    print("Baue Oemof-Modell...")
    es = solph.EnergySystem(timeindex=data_slice.index)

    # Busse
    b_el = solph.Bus(label="electricity_grid")
    b_th = solph.Bus(label="thermal_grid")
    es.add(b_el, b_th)

    # Strommarkt (Quelle/Senke)
    spot_price = data_slice['Spotmarkt_Preis']
    es.add(solph.components.Source(label="spot_buy", outputs={b_el: solph.Flow(variable_costs=spot_price)}))
    es.add(solph.components.Sink(label="spot_sell", inputs={b_el: solph.Flow(variable_costs=spot_price * -1)}))

    # Wärmebedarf
    es.add(solph.components.Sink(
        label="heat_demand_sink", 
        inputs={b_th: solph.Flow(nominal_value=1, fix=data_slice['Heat_Demand'])}
    ))

    # Komponenten
    # 1. BESS
    bess = solph.components.GenericStorage(
        label="battery",
        inputs={b_el: solph.Flow(nominal_value=BESS_P_MAX)},
        outputs={b_el: solph.Flow(nominal_value=BESS_P_MAX)},
        nominal_storage_capacity=BESS_E_MAX,
        initial_storage_level=BESS_INITIAL_SOC,
        inflow_conversion_factor=BESS_EFFICIENCY,
        outflow_conversion_factor=BESS_EFFICIENCY
    )
    es.add(bess)

    # 2. PtH (Converter)
    pth = solph.components.Converter(
        label="pth_boiler",
        inputs={b_el: solph.Flow()},
        outputs={b_th: solph.Flow(nominal_value=PTH_P_MAX, variable_costs=PTH_VAR_COST)},
        conversion_factors={b_th: PTH_EFFICIENCY}
    )
    es.add(pth)

    # 3. Wärmespeicher
    tes = solph.components.GenericStorage(
        label="thermal_storage",
        inputs={b_th: solph.Flow()},
        outputs={b_th: solph.Flow()},
        nominal_storage_capacity=TES_CAPACITY,
        initial_storage_level=0.2, 
        loss_rate=TES_LOSS
    )
    es.add(tes)

    # --- 4. OPTIMIERUNG & CONSTRAINTS ---
    print("Füge Constraints hinzu...")
    model = solph.Model(es)

    # A) BESS Constraints
    model = add_multi_market_constraints(
        model=model, storage_component=bess, market_bus=b_el,
        fcr_prices=data_slice['FCR_Leistungspreis'],
        afrp_pos_cap_prices=data_slice['aFRR_Pos_Leistungspreis'], afrp_neg_cap_prices=data_slice['aFRR_Neg_Leistungspreis'],
        afrp_pos_energy_prices=data_slice['aFRR_Pos_Arbeitspreis'], afrp_neg_energy_prices=data_slice['aFRR_Neg_Arbeitspreis'],
        p_max=BESS_P_MAX, e_max=BESS_E_MAX, 
        activation_factor_pos=prof_bess_pos, activation_factor_neg=prof_bess_neg,
        enable_fcr=True, enable_afrr_pos=True, enable_afrr_neg=True
    )

    # B) PtH Constraints
    model = add_transformer_load_constraints(
        model=model, transformer_component=pth, input_bus=b_el,
        afrp_pos_cap_prices=data_slice['aFRR_Pos_Leistungspreis'], afrp_neg_cap_prices=data_slice['aFRR_Neg_Leistungspreis'],
        afrp_pos_energy_prices=data_slice['aFRR_Pos_Arbeitspreis'], afrp_neg_energy_prices=data_slice['aFRR_Neg_Arbeitspreis'],
        p_max=PTH_P_MAX,
        activation_factor_pos=prof_pth_pos, activation_factor_neg=prof_pth_neg,
        enable_afrr_pos=True, enable_afrr_neg=True
    )

    print("Starte Solver (CBC)...")
    model.solve(solver='cbc', solve_kwargs={'tee': True})

   # =============================================================================
    # 6. ERGEBNISSE & CLEANUP
    # =============================================================================
    print("Extrahiere Ergebnisse...")
    
    # 1. Block-Variablen sichern
    t_map = model.t_to_block_map
    res_bess_fcr, res_bess_pos, res_bess_neg = [], [], []
    res_pth_pos, res_pth_neg = [], []

    for t in model.TIMESTEPS:
        b = t_map[t]
        res_bess_fcr.append(pyo.value(model.fcr_capacity_block[b]))
        res_bess_pos.append(pyo.value(model.afrp_pos_capacity_block[b]))
        res_bess_neg.append(pyo.value(model.afrp_neg_capacity_block[b]))
        res_pth_pos.append(pyo.value(model.trans_afrr_pos_block[b]))
        res_pth_neg.append(pyo.value(model.trans_afrr_neg_block[b]))

    # --- FIX: Listen auf korrekte Länge bringen (Padding) ---
    # Wir füllen fehlende Werte am Ende einfach mit 0 auf.
    target_len = len(data_slice.index)

    def pad_list(lst, length):
        diff = length - len(lst)
        if diff > 0:
            return lst + [0.0] * diff
        return lst

    res_bess_fcr = pad_list(res_bess_fcr, target_len)
    res_bess_pos = pad_list(res_bess_pos, target_len)
    res_bess_neg = pad_list(res_bess_neg, target_len)
    res_pth_pos  = pad_list(res_pth_pos, target_len)
    res_pth_neg  = pad_list(res_pth_neg, target_len)
    # -------------------------------------------------------

    # 2. Cleanup (Variablen löschen VOR solph.processing)
    vars_to_del = [
        'fcr_capacity_block', 'afrp_pos_capacity_block', 'afrp_neg_capacity_block',
        'trans_afrr_pos_block', 'trans_afrr_neg_block',
        'soc_max_reserve', 'soc_min_reserve', 'force_phys_discharge', 'force_phys_charge',
        'trans_headroom', 'trans_footroom', 'trans_force_cons', 'trans_force_red',
        'charge_power_limit', 'discharge_power_limit'
    ]
    for attr in vars_to_del:
        if hasattr(model, attr): delattr(model, attr)

    results = solph.processing.results(model)

    # =============================================================================
    # 7. DATAFRAME BAUEN
    # =============================================================================
    
    # Robuste Flow-Funktion
    def get_flow_robust(src, dst):
        try:
            val = results[(src, dst)]['sequences']['flow']
            return val.reindex(data_slice.index, fill_value=0)
        except KeyError:
            return pd.Series(0.0, index=data_slice.index)
    
    def get_soc_robust(node):
        try:
            val = results[(node, None)]['sequences']['storage_content']
            return val.reindex(data_slice.index, fill_value=0)
        except KeyError:
            return pd.Series(0.0, index=data_slice.index)

    df_res = pd.DataFrame(index=data_slice.index)
    
    # Objekte holen
    src_buy = es.groups['spot_buy']
    snk_sell = es.groups['spot_sell']

    # Physikalische Daten
    df_res['Grid_Import'] = get_flow_robust(src_buy, b_el)
    df_res['Grid_Export'] = get_flow_robust(b_el, snk_sell)
    df_res['BESS_Charge'] = get_flow_robust(b_el, bess)
    df_res['BESS_Discharge'] = get_flow_robust(bess, b_el)
    df_res['PtH_Power_El'] = get_flow_robust(b_el, pth)
    df_res['PtH_Heat'] = get_flow_robust(pth, b_th)
    df_res['SOC_BESS'] = get_soc_robust(bess)
    df_res['SOC_TES'] = get_soc_robust(tes)
    
    # Input & Preise
    df_res['Heat_Load'] = data_slice['Heat_Demand']
    df_res['Spot_Price'] = data_slice['Spotmarkt_Preis']
    
    # Preise für Plots
    df_res['FCR_Price'] = data_slice['FCR_Leistungspreis']
    df_res['aFRR_Pos_Cap_Price'] = data_slice['aFRR_Pos_Leistungspreis']
    df_res['aFRR_Neg_Cap_Price'] = data_slice['aFRR_Neg_Leistungspreis']
    df_res['aFRR_Pos_En_Price'] = data_slice['aFRR_Pos_Arbeitspreis']
    df_res['aFRR_Neg_En_Price'] = data_slice['aFRR_Neg_Arbeitspreis']
    
    # Reserve Daten (Jetzt sicher dank Padding)
    df_res['Res_BESS_FCR'] = pd.Series(res_bess_fcr, index=data_slice.index)
    df_res['Res_BESS_aFRR+'] = pd.Series(res_bess_pos, index=data_slice.index)
    df_res['Res_BESS_aFRR-'] = pd.Series(res_bess_neg, index=data_slice.index)
    df_res['Res_PtH_aFRR+'] = pd.Series(res_pth_pos, index=data_slice.index)
    df_res['Res_PtH_aFRR-'] = pd.Series(res_pth_neg, index=data_slice.index)

    # --- 7. VISUALISIERUNG (KOMBINIERT) ---
    print("Erstelle Plots...")
    plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': 0.5})

    def format_ax(ax):
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %Hh'))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))

    # PLOT 1: Strom-Mix
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_res.index, df_res['BESS_Charge'], label='BESS Laden', color='blue')
    ax1.plot(df_res.index, df_res['PtH_Power_El'], label='PtH Verbrauch', color='red', alpha=0.7)
    ax1.plot(df_res.index, -df_res['BESS_Discharge'], label='BESS Entladen', color='green')
    ax1.plot(df_res.index, df_res['Grid_Import'] - df_res['Grid_Export'], label='Netz Saldo', color='black', ls='--')
    
    ax1.set_ylabel('Leistung [MW]')
    ax1.legend(loc='upper left', ncol=2)
    ax1.set_title('Strombilanz (BESS & PtH)')
    format_ax(ax1)
    
    # Zweitachse SOC
    ax1b = ax1.twinx()
    ax1b.plot(df_res.index, df_res['SOC_BESS'], color='navy', ls=':', label='BESS SOC')
    ax1b.set_ylabel('BESS [MWh]')
    ax1b.legend(loc='upper right')
    
    plt.tight_layout()
    fig1.savefig('Kombi_Abb_1_Strom.svg')

    # PLOT 2: Wärme & Speicher
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(df_res.index, df_res['Heat_Load'], label='Wärmebedarf', color='black', ls='--')
    ax2.plot(df_res.index, df_res['PtH_Heat'], label='PtH Erzeugung', color='red')
    ax2.set_ylabel('Thermische Leistung [MW]')
    ax2.legend(loc='upper left')
    ax2.set_title('Wärmeversorgung & Pufferung')
    format_ax(ax2)

    ax2b = ax2.twinx()
    ax2b.plot(df_res.index, df_res['SOC_TES'], color='purple', ls=':', label='TES SOC')
    ax2b.set_ylabel('Wärmespeicher [MWh]')
    ax2b.legend(loc='upper right')
    
    plt.tight_layout()
    fig2.savefig('Kombi_Abb_2_Waerme.svg')

    # PLOT 3: Regelenergie
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(df_res.index, df_res['Res_BESS_FCR'], label='BESS FCR', color='orange')
    ax3.plot(df_res.index, df_res['Res_BESS_aFRR+'], label='BESS aFRR+', color='green', ls='--')
    ax3.plot(df_res.index, df_res['Res_BESS_aFRR-'], label='BESS aFRR-', color='blue', ls='--')
    
    ax3.fill_between(df_res.index, df_res['Res_PtH_aFRR+'], alpha=0.3, color='darkred', label='PtH aFRR+')
    ax3.fill_between(df_res.index, df_res['Res_PtH_aFRR-'], alpha=0.3, color='pink', label='PtH aFRR-')
    
    ax3.set_ylabel('Reserve [MW]')
    ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    ax3.set_title('Regelenergie Allokation')
    format_ax(ax3)
    
    plt.tight_layout()
    fig3.savefig('Kombi_Abb_3_Regelenergie.svg')

    # DASHBOARD
    print("Erstelle Dashboard...")
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=("Strombilanz", "Wärme", "BESS Reserve", "PtH Reserve"))
    
    # 1. Strom
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Grid_Import']-df_res['Grid_Export'], name='Netz Saldo'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['PtH_Power_El'], name='PtH Last'), row=1, col=1)
    
    # 2. Wärme
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Heat_Load'], name='Wärmebedarf', line=dict(dash='dash')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['SOC_TES'], name='TES SOC', yaxis='y2'), row=2, col=1)
    
    # 3. BESS Reserve
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Res_BESS_FCR'], name='FCR'), row=3, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Res_BESS_aFRR+'], name='BESS aFRR+'), row=3, col=1)
    
    # 4. PtH Reserve
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Res_PtH_aFRR+'], name='PtH aFRR+', fill='tozeroy'), row=4, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Res_PtH_aFRR-'], name='PtH aFRR-', fill='tozeroy'), row=4, col=1)
    
    fig.update_layout(height=1000, title_text="Kombi-System Analyse")
    fig.write_html("Dashboard_Kombi_Final.html")
    
    print("Fertig.")