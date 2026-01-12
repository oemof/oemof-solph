import os
import pandas as pd
import numpy as np
import oemof.solph as solph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pyomo.environ as pyo
import inspect 
import matplotlib.patches as mpatches   

# Importiere deine Constraints
from custom_constraints import add_transformer_load_constraints, calculate_activation_profile_with_volume

# =============================================================================
# 0. KONFIGURATION (HIER ALLE WERTE EINSTELLEN)
# =============================================================================

# --- Simulation ---
FILENAME = 'market_data.csv'
SIMULATION_DAYS = 4
TIMESTEPS_PER_HOUR = 4
TOTAL_TIMESTEPS = 96 * SIMULATION_DAYS

# --- Technische Daten: Power-to-Heat (Elektroboiler) ---
PTH_P_NOM = 10.0        # [MW] Nennleistung
PTH_EFFICIENCY = 0.99   # [-] Wirkungsgrad (Strom zu Wärme)
PTH_VAR_COST = 0.1      # [€/MWh] Betriebskosten

# --- Technische Daten: Wärmespeicher ---
TES_CAPACITY = 50.0     # [MWh] Kapazität
TES_LOSS_RATE = 0.005   # [1/h] Verlustrate pro Stunde (0.5%)
TES_INITIAL_SOC = 0.5   # [-] Startfüllstand (50%)

# --- Markt-Strategie (aFRR Negativ) ---
# Zu welchem Preis wollen wir Strom kaufen? 
# (Höher = Aggressiver, wir werden öfter abgerufen)
STRATEGY_BID_PRICE_NEG = 50.0  # [€/MWh]

# Spaltennamen in deiner CSV (falls abweichend, hier ändern)
COL_ACTIVATION_NEG_MW = 'aFRR_Activation_Neg_MW' 

# =============================================================================
# HELFER: KLASSEN FINDEN 
# =============================================================================
def get_oemof_class(classname):
    if hasattr(solph.components, classname):
        return getattr(solph.components, classname)
    if hasattr(solph, classname):
        return getattr(solph, classname)
    if classname == 'Transformer' and hasattr(solph.components, 'Converter'):
        print("Info: Nutze 'Converter' statt 'Transformer'")
        return getattr(solph.components, 'Converter')
    raise AttributeError(f"Konnte Klasse '{classname}' in oemof.solph nicht finden!")

Source = get_oemof_class('Source')
Sink = get_oemof_class('Sink')
GenericStorage = get_oemof_class('GenericStorage')
Transformer = get_oemof_class('Transformer') 

# =============================================================================
# MAIN SIMULATION
# =============================================================================
if __name__ == "__main__":
    
    # --- 1. DATEN LADEN ---
    filename = FILENAME
    if not os.path.exists(filename): filename = os.path.join('Datamining', FILENAME)
    
    print(f"Versuche Daten zu laden von: {filename}")
    
    try:
        data = pd.read_csv(filename, sep=';', decimal=',')
        if 'Unnamed: 0' in data.columns:
            data.rename(columns={'Unnamed: 0': 'timestamp'}, inplace=True)
            data.set_index('timestamp', inplace=True)
        data.index = pd.to_datetime(data.index)
        data_slice = data.head(TOTAL_TIMESTEPS).copy()
        print("-> Marktdaten erfolgreich geladen.")
    except Exception as e:
        print(f"-> WARNUNG: CSV Fehler ({e}). Nutze Zufallsdaten.")
        idx = pd.date_range(start="2025-01-01 00:00", periods=TOTAL_TIMESTEPS, freq="15min")
        data_slice = pd.DataFrame(index=idx)
        data_slice['Spotmarkt_Preis'] = np.random.uniform(10, 150, TOTAL_TIMESTEPS)
        for c in ['FCR_Leistungspreis', 'aFRR_Pos_Leistungspreis', 'aFRR_Neg_Leistungspreis']:
            data_slice[c] = 5.0
        for c in ['aFRR_Pos_Arbeitspreis', 'aFRR_Neg_Arbeitspreis']:
            data_slice[c] = 50.0
        data_slice['aFRR_Activation_Pos'] = 0.05
        data_slice['aFRR_Activation_Neg'] = 0.05

    data_slice = data_slice.fillna(0)

    # --- 2. VORBEREITUNG (Profile & Strategie) ---
    
    # A) Wärmebedarf (Dummy Profil)
    hour = data_slice.index.hour
    profile = 2 + 4 * np.sin((hour - 6) * np.pi / 12)**2 
    noise = np.random.normal(0, 0.5, len(data_slice))
    # Wir begrenzen den Bedarf auf die Leistung des Boilers (damit es lösbar bleibt)
    data_slice['Heat_Demand'] = np.clip(profile + noise, 0, PTH_P_NOM)

    # B) Strategie-Profil berechnen (WICHTIG!)
    # Fallback für Volumen-Spalte
    if COL_ACTIVATION_NEG_MW not in data_slice.columns:
        print(f"Warnung: Spalte '{COL_ACTIVATION_NEG_MW}' fehlt. Generiere Zufallsdaten.")
        data_slice[COL_ACTIVATION_NEG_MW] = np.random.uniform(-500, 0, len(data_slice))

    # Berechnung des Binären Abrufs (Preis & Volumen Logik)
    vol_neg_abs = data_slice[COL_ACTIVATION_NEG_MW].abs()
    
    my_neg_profile = calculate_activation_profile_with_volume(
        market_prices=data_slice['aFRR_Neg_Arbeitspreis'],
        total_activation_mw=vol_neg_abs,
        my_bid_price=STRATEGY_BID_PRICE_NEG, # <--- Nutzt Config-Wert
        my_p_max=PTH_P_NOM                   # <--- Nutzt Config-Wert
    )

    # --- 3. ENERGIESYSTEM BAUEN ---
    es = solph.EnergySystem(timeindex=data_slice.index)
    
    b_el = solph.Bus(label="electricity_grid")
    b_th = solph.Bus(label="thermal_grid")
    es.add(b_el, b_th)

    es.add(Source(
        label="spot_buy",
        outputs={b_el: solph.Flow(variable_costs=data_slice['Spotmarkt_Preis'])}
    ))

    # Versions-Check für Parameter-Namen
    flow_sig = inspect.signature(solph.Flow)
    store_sig = inspect.signature(GenericStorage)
    cap_key = 'nominal_capacity' if 'nominal_capacity' in flow_sig.parameters else 'nominal_value'
    store_key = 'nominal_storage_capacity' if 'nominal_storage_capacity' in store_sig.parameters else 'nominal_capacity'

    # --- PtH Anlage ---
    pth_out_args = {'variable_costs': PTH_VAR_COST}
    pth_out_args[cap_key] = PTH_P_NOM # <--- Nutzt Config-Wert

    pth = Transformer(
        label="electric_boiler",
        inputs={b_el: solph.Flow()},
        outputs={b_th: solph.Flow(**pth_out_args)}, 
        conversion_factors={b_th: PTH_EFFICIENCY} # <--- Nutzt Config-Wert
    )
    es.add(pth)

    # --- Wärmespeicher ---
    store_args = {
        'label': "thermal_storage",
        'inputs': {b_th: solph.Flow()},
        'outputs': {b_th: solph.Flow()},
        'loss_rate': TES_LOSS_RATE,         # <--- Nutzt Config-Wert
        'initial_storage_level': TES_INITIAL_SOC, # <--- Nutzt Config-Wert
        'balanced': False
    }
    store_args[store_key] = TES_CAPACITY    # <--- Nutzt Config-Wert

    storage_th = GenericStorage(**store_args)
    es.add(storage_th)

    # --- Wärmesenke ---
    sink_flow_args = {'fix': data_slice['Heat_Demand']}
    sink_flow_args[cap_key] = 1 # Skalierung ist 1, da Profil absolut
    
    es.add(Sink(
        label="heat_demand",
        inputs={b_th: solph.Flow(**sink_flow_args)}
    ))

    # --- 4. MODELL & CONSTRAINTS ---
    print("Erstelle Modell...")
    model = solph.Model(es)

    print(f"Füge PtH-Regelmarkt Constraints hinzu (Strategie-Preis: {STRATEGY_BID_PRICE_NEG} €)...")
    add_transformer_load_constraints(
        model=model,
        transformer_component=pth,
        input_bus=b_el,
        afrp_pos_cap_prices=data_slice['aFRR_Pos_Leistungspreis'],
        afrp_neg_cap_prices=data_slice['aFRR_Neg_Leistungspreis'],
        afrp_pos_energy_prices=data_slice['aFRR_Pos_Arbeitspreis'],
        afrp_neg_energy_prices=data_slice['aFRR_Neg_Arbeitspreis'],
        p_max=PTH_P_NOM,          # <--- Nutzt Config-Wert
        market_block_size=16,
        activation_factor_pos=0.0, 
        activation_factor_neg=my_neg_profile, # <--- Hier das oben berechnete Profil
        enable_afrr_neg=True,
        enable_afrr_pos=True
    )

    # --- 5. LÖSEN ---
    print("Starte Solver (CBC)...")
    model.solve(solver='cbc', solve_kwargs={'tee': True})

    # --- 6. ERGEBNISSE VERARBEITEN ---
    print("Verarbeite Ergebnisse...")

    # A) Block-Variablen sichern
    t_map = model.trans_map[pth]
    res_neg_vals = []
    res_pos_vals = []
    for t in model.TIMESTEPS:
        b_idx = t_map[t]
        res_neg_vals.append(pyo.value(model.trans_afrr_neg_block[b_idx]))
        res_pos_vals.append(pyo.value(model.trans_afrr_pos_block[b_idx]))

    # B) Clean-up (Constraint-Objekte entfernen für sauberen Export)
    if hasattr(model, 'trans_afrr_pos_block'): del model.trans_afrr_pos_block
    if hasattr(model, 'trans_afrr_neg_block'): del model.trans_afrr_neg_block
    if hasattr(model, 'trans_headroom'): del model.trans_headroom
    if hasattr(model, 'trans_footroom'): del model.trans_footroom

    # C) Results abrufen
    results = solph.processing.results(model)

    # D) Daten extrahieren & Angleichen
    try:
        flow_pth = results[(pth, b_th)]['sequences']['flow']
    except KeyError:
        for key in results.keys():
            if key[0] == pth and key[1] == b_th:
                flow_pth = results[key]['sequences']['flow']
                break
                
    soc = results[(storage_th, None)]['sequences']['storage_content']

    # Konvertieren in Arrays für sicheren Längencheck
    arr_flow = np.array(flow_pth)
    arr_soc = np.array(soc)
    arr_neg = np.array(res_neg_vals)
    arr_pos = np.array(res_pos_vals)
    
    L = min(len(data_slice), len(arr_flow), len(arr_soc), len(arr_neg))
    print(f"Angleichen auf L={L}")

    df = pd.DataFrame(index=data_slice.index[:L])
    df['PtH_Real'] = arr_flow[:L]
    df['Heat_Demand'] = data_slice['Heat_Demand'].values[:L]
    df['SOC'] = arr_soc[:L]
    df['aFRR_Neg'] = arr_neg[:L]
    df['aFRR_Pos'] = arr_pos[:L]
    
    # E) Fahrplan zurückrechnen (Schedule)
    # Hier nutzen wir für die Visualisierung das berechnete Strategie-Profil
    # Damit der Plot zeigt, wann der Abruf tatsächlich "gegriffen" hat.
    # Achtung: Längen anpassen!
    profile_neg_cut = my_neg_profile[:L]
    
    # Schedule = Real - (Reserve * Aktivierungsfaktor)
    # Wir nehmen an pos_activiation ist 0 (wie oben konfiguriert)
    df['PtH_Schedule'] = df['PtH_Real'] - (df['aFRR_Neg'] * profile_neg_cut)

    # =============================================================================
    # 6. DATEN-AUFBEREITUNG & KPI (Für Plots)
    # =============================================================================
    print("\n--- BEREITE DATEN AUF ---")
    
    # 1. Physikalische Flüsse berechnen
    # aFRR Negativ = Zusätzlicher Stromverbrauch (Lasterhöhung)
    # aFRR Positiv = Weniger Stromverbrauch (Lastabwurf)
    
    # Profil zurechtschneiden
    prof_neg_cut = my_neg_profile[:L]
    
    # WICHTIG: aFRR Negativ bedeutet bei Verbrauchern: Mehr Konsum. 
    # Wir definieren flow_afrr_neg als POSITIVEN Wert (MW), der zusätzlich verheizt wird.
    flow_afrr_neg = df['aFRR_Neg'] * prof_neg_cut
    
    # Der "Fahrplan" (Schedule) ist das, was ohne Regelenergie geplant war.
    # Real = Schedule + aFRR_Neg_Flow
    df['PtH_Schedule'] = df['PtH_Real'] - flow_afrr_neg
    
    # 2. Cashflow Berechnung
    dt = 0.25
    
    # Kosten für Spotmarkt-Strom (Realverbrauch - aFRR Anteil, falls wir das trennen wollen)
    # Vereinfachung: Wir zahlen Spotpreis für den Fahrplan.
    # Für aFRR Negativ (Zusatzverbrauch) zahlen wir meist weniger oder kriegen Geld (Arbeitspreis).
    
    # A) Kosten für Fahrplan-Strom (Spot)
    df['Cost_Spot'] = -1 * df['PtH_Schedule'] * data_slice['Spotmarkt_Preis'].values[:L] * dt
    
    # B) Erlöse aus Regelenergie (Leistungspreis)
    df['Rev_aFRR_Neg_Cap'] = df['aFRR_Neg'] * data_slice['aFRR_Neg_Leistungspreis'].values[:L] * dt
    df['Rev_aFRR_Pos_Cap'] = df['aFRR_Pos'] * data_slice['aFRR_Pos_Leistungspreis'].values[:L] * dt
    
    # C) Erlöse/Kosten aus Regelarbeits
    # aFRR Neg Arbeit (Wir verbrauchen mehr -> Zahlen meistens, aber weniger als Spot)
    # Achtung Vorzeichen: Wenn Arbeitspreis positiv ist, zahlen wir.
    # Wir modellieren es als "Revenue" (negativ = Kosten).
    # Menge ist flow_afrr_neg (positiv).
    df['Rev_aFRR_Neg_En'] = -1 * flow_afrr_neg * data_slice['aFRR_Neg_Arbeitspreis'].values[:L] * dt
    
    # D) Variable Kosten (Verschleiß Boiler)
    df['Cost_Var'] = -1 * df['PtH_Real'] * PTH_VAR_COST * dt
    
    # Summe
    df['Total_Profit'] = df['Cost_Spot'] + df['Rev_aFRR_Neg_Cap'] + df['Rev_aFRR_Pos_Cap'] + df['Rev_aFRR_Neg_En'] + df['Cost_Var']
    df['Cum_Profit'] = df['Total_Profit'].cumsum()

    # =============================================================================
    # 7. SVG PLOTS (WISSENSCHAFTLICH)
    # =============================================================================
    print("\n--- ERSTELLE SVG PLOTS ---")
    
    plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif', 'svg.fonttype': 'none', 'axes.grid': True, 'grid.alpha': 0.5})
    
    def format_date_axis(ax):
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    
    def set_legend_top(ax, lines, labels, ncol=3):
        ax.legend(lines, labels, loc='lower left', bbox_to_anchor=(0, 1.02, 1, 0.1), mode="expand", borderaxespad=0, ncol=ncol, frameon=False)

    x = df.index
    w = 0.008

    # --- PLOT 1: WÄRMEVERSORGUNG & MARKT (Stacked) ---
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    
    # Hintergrund: Wärmebedarf (Linie)
    l1, = ax1.plot(x, df['Heat_Demand'], color='black', linestyle='--', linewidth=1.5, label='Wärmebedarf')
    ax1.set_ylabel('Thermische Leistung [MW]')
    
    # Gestapelte Balken: Woher kommt die Wärme?
    # Basis: Fahrplan
    b_base = ax1.bar(x, df['PtH_Schedule'], w, color='skyblue', label='PtH Fahrplan', alpha=0.7)
    # Oben drauf: aFRR Negativ (Zusatzheizung)
    b_afrr = ax1.bar(x, flow_afrr_neg, w, bottom=df['PtH_Schedule'], color='darkred', label='aFRR- (Zusatz)', alpha=0.7)
    
    # Zweitachse: Spotpreis
    ax1_b = ax1.twinx()
    l_price, = ax1_b.plot(x, data_slice['Spotmarkt_Preis'].values[:L], color='blue', linewidth=1, alpha=0.3, label='Spotpreis')
    ax1_b.set_ylabel('Spot [€/MWh]')
    
    # Legende
    handles = [l1, b_base, b_afrr, l_price]
    labels = ['Wärmebedarf', 'PtH Fahrplan', 'aFRR- (Zusatz)', 'Spotpreis']
    set_legend_top(ax1, handles, labels, ncol=4)
    
    format_date_axis(ax1)
    fig1.savefig('PtH_Abb_1_Waermeversorgung.svg', format='svg', bbox_inches='tight')
    print("[x] PtH Abb 1 (Wärme) gespeichert.")

    # --- PLOT 2: KAPAZITÄTS-RESERVIERUNG ---
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # Preise
    l_p_pos, = ax2.plot(x, data_slice['aFRR_Pos_Leistungspreis'].values[:L], color='green', linestyle='--', label='Preis aFRR+')
    l_p_neg, = ax2.plot(x, data_slice['aFRR_Neg_Leistungspreis'].values[:L], color='red', linestyle='--', label='Preis aFRR-')
    ax2.set_ylabel('Leistungspreis [€/MW]')
    
    # Reservierte Mengen (Fläche)
    ax2_b = ax2.twinx()
    
    # Wir plotten aFRR- nach oben (positive Reserve) und aFRR+ auch nach oben (gestapelt oder transparent)
    # Besser: Stackplot
    ax2_b.stackplot(x, df['aFRR_Neg'], df['aFRR_Pos'], labels=['Res. aFRR-', 'Res. aFRR+'], colors=['lightcoral', 'lightgreen'], alpha=0.5)
    ax2_b.set_ylabel('Reservierte Leistung [MW]')
    ax2_b.set_ylim(0, PTH_P_NOM * 1.1)
    
    # Proxy Artists für Legende
    p_neg = mpatches.Patch(color='lightcoral', alpha=0.5)
    p_pos = mpatches.Patch(color='lightgreen', alpha=0.5)
    
    set_legend_top(ax2, [l_p_neg, l_p_pos, p_neg, p_pos], ['Preis aFRR-', 'Preis aFRR+', 'Res. aFRR-', 'Res. aFRR+'], ncol=4)
    format_date_axis(ax2)
    fig2.savefig('PtH_Abb_2_Reserve.svg', format='svg', bbox_inches='tight')
    print("[x] PtH Abb 2 (Reserve) gespeichert.")

    # --- PLOT 3: SPEICHERFÜLLSTAND ---
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    
    l_soc, = ax3.plot(x, df['SOC'], color='purple', linewidth=2, label='Wärmespeicher')
    ax3.fill_between(x, df['SOC'], color='purple', alpha=0.1)
    ax3.axhline(TES_CAPACITY, color='gray', linestyle=':', label='Max Kapazität')
    
    ax3.set_ylabel('Energie [MWh]')
    ax3.set_ylim(0, TES_CAPACITY * 1.1)
    
    set_legend_top(ax3, [l_soc], ['Wärmespeicher SOC'], ncol=1)
    format_date_axis(ax3)
    fig3.savefig('PtH_Abb_3_SOC.svg', format='svg', bbox_inches='tight')
    print("[x] PtH Abb 3 (SOC) gespeichert.")
    
    # --- PLOT 4: CASHFLOW ---
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    # Einnahmen
    b1 = ax4.bar(x, df['Rev_aFRR_Neg_Cap'], w, color='lightcoral', label='aFRR- Leist.')
    b2 = ax4.bar(x, df['Rev_aFRR_Pos_Cap'], w, bottom=df['Rev_aFRR_Neg_Cap'], color='lightgreen', label='aFRR+ Leist.')
    
    # Kosten (Negativ)
    n1 = df['Cost_Spot']
    n2 = df['Rev_aFRR_Neg_En'] # Ist negativ (Kosten)
    n3 = df['Cost_Var']
    
    bn1 = ax4.bar(x, n1, w, color='darkblue', label='Stromkosten (Fahrplan)')
    bn2 = ax4.bar(x, n2, w, bottom=n1, color='darkred', label='aFRR- Arbeit (Kosten)')
    
    # Summe
    ax4_b = ax4.twinx()
    l_sum, = ax4_b.plot(x, df['Cum_Profit'], 'k', lw=2, label='∑ Kosten/Gewinn')
    
    ax4.set_ylabel('Cashflow [€]')
    ax4_b.set_ylabel('Kumuliert [€]')
    
    set_legend_top(ax4, [b1, b2, bn1, bn2, l_sum], ['aFRR- Leist.', 'aFRR+ Leist.', 'Strom (Fahrplan)', 'aFRR- Arbeit', '∑ Total'], ncol=5)
    format_date_axis(ax4)
    fig4.savefig('PtH_Abb_4_Cashflow.svg', format='svg', bbox_inches='tight')
    print("[x] PtH Abb 4 (Cashflow) gespeichert.")


    # =============================================================================
    # 8. DASHBOARD (HTML) - IDENTISCHER STIL WIE BESS
    # =============================================================================
    print("\n--- ERSTELLE DASHBOARD ---")
    
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import webbrowser
    
    # KPIs
    kpi_spot_cost = df['Cost_Spot'].sum()
    kpi_afrr_rev = (df['Rev_aFRR_Neg_Cap'] + df['Rev_aFRR_Pos_Cap']).sum()
    kpi_total = df['Total_Profit'].sum()
    
    # Pie Chart (Aufteilung Strombezug)
    # Wie viel ist Fahrplan, wie viel ist aFRR?
    sum_schedule = df['PtH_Schedule'].sum()
    sum_afrr_neg = flow_afrr_neg.sum()
    
    fig = make_subplots(
        rows=5, cols=4, shared_xaxes=True,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "domain"}],
            [{"colspan": 4, "secondary_y": True}, None, None, None],
            [{"colspan": 4}, None, None, None],
            [{"colspan": 4}, None, None, None],
            [{"colspan": 4, "secondary_y": True}, None, None, None]
        ],
        row_heights=[0.14, 0.20, 0.20, 0.18, 0.28], 
        vertical_spacing=0.08,
        subplot_titles=(None, None, None, "Strom-Mix", "Wärmeversorgung & Spotpreis", "Leistungs-Allokation (Reserve)", "Wärmespeicher (SOC)", "Cashflow Analyse")
    )
    
    # ROW 1: KPIs
    fig.add_trace(go.Indicator(
        mode="number", value=PTH_P_NOM, 
        title={"text": "Nennleistung [MW]", 'font': {'size': 20}},
        number={'font': {'color': "#444", 'size': 40}}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number", value=kpi_total, 
        title={"text": "Gesamtergebnis [€]", 'font': {'size': 20}},
        number={'valueformat': ",.0f", 'font': {'color': "red" if kpi_total < 0 else "green", 'size': 40}}
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="number", value=kpi_afrr_rev, 
        title={"text": "Erlös aFRR [€]", 'font': {'size': 20}},
        number={'valueformat': ",.0f", 'font': {'color': "green", 'size': 40}}
    ), row=1, col=3)

    fig.add_trace(go.Pie(
        labels=['Fahrplan Strom', 'aFRR- Zusatzstrom'], 
        values=[sum_schedule, sum_afrr_neg], 
        marker=dict(colors=['skyblue', 'darkred']), 
        hole=0.4, textinfo='percent', showlegend=False
    ), row=1, col=4)

    # ROW 2: WÄRMEVERSORGUNG (Stacked Bar + Line)
    # Ähnlich wie BESS Leistungsbilanz, aber nur positiv (Verbrauch)
    fig.add_trace(go.Bar(x=df.index, y=df['PtH_Schedule'], name='PtH Fahrplan', marker_color='skyblue', opacity=0.7), row=2, col=1)
    fig.add_trace(go.Bar(x=df.index, y=flow_afrr_neg, name='aFRR- Zusatz', marker_color='darkred', opacity=0.7), row=2, col=1)
    
    # Wärmebedarf als Linie
    fig.add_trace(go.Scatter(x=df.index, y=df['Heat_Demand'], name='Wärmebedarf', line=dict(color='black', dash='dot', width=2)), row=2, col=1)
    
    # Spotpreis (Sekundär)
    fig.add_trace(go.Scatter(x=df.index, y=data_slice['Spotmarkt_Preis'].values[:L], name='Spotpreis', line=dict(color='blue', width=1)), row=2, col=1, secondary_y=True)

    # ROW 3: RESERVE (Stacked Area)
    fig.add_trace(go.Scatter(x=df.index, y=df['aFRR_Neg'], name='Reserve aFRR-', stackgroup='one', fillcolor='lightcoral', line=dict(width=0)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['aFRR_Pos'], name='Reserve aFRR+', stackgroup='one', fillcolor='lightgreen', line=dict(width=0)), row=3, col=1)

    # ROW 4: SOC
    fig.add_trace(go.Scatter(x=df.index, y=df['SOC'], name='Speicherstand', fill='tozeroy', line=dict(color='purple')), row=4, col=1)
    
    # ROW 5: CASHFLOW
    fig.add_trace(go.Bar(x=df.index, y=df['Rev_aFRR_Neg_Cap'], name='Erlös aFRR- Leist.', marker_color='lightcoral'), row=5, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['Rev_aFRR_Pos_Cap'], name='Erlös aFRR+ Leist.', marker_color='lightgreen'), row=5, col=1)
    
    fig.add_trace(go.Bar(x=df.index, y=df['Cost_Spot'], name='Kosten Spot', marker_color='darkblue'), row=5, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['Rev_aFRR_Neg_En'], name='Kosten aFRR- Arbeit', marker_color='darkred'), row=5, col=1)
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Cum_Profit'], name='Summe', line=dict(color='black', width=3)), row=5, col=1, secondary_y=True)

    # LAYOUT
    for r in [2,3,4,5]: fig.update_xaxes(matches='x2', row=r, col=1)

    fig.update_yaxes(title_text="Thermische Leistung [MW]", row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Spotpreis [€/MWh]", row=2, col=1, secondary_y=True)
    fig.update_yaxes(title_text="Reserve [MW]", row=3, col=1)
    fig.update_yaxes(title_text="Energie [MWh]", row=4, col=1)
    fig.update_yaxes(title_text="Cashflow [€]", row=5, col=1)

    info_bar_html = f"""
    <div style="width: 95%; margin: 0 auto; background-color: #f8f9fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 10px; font-family: Arial; font-size: 13px; color: #333; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <table style="width: 100%;">
            <tr>
                <td style="width:33%;text-align:center;border-right:1px solid #ddd;"><b>ANLAGE</b><br>PtH {PTH_P_NOM} MW (Eta {PTH_EFFICIENCY})<br>Speicher: {TES_CAPACITY} MWh</td>
                <td style="width:33%;text-align:center;border-right:1px solid #ddd;"><b>STRATEGIE</b><br>Bid aFRR-: {STRATEGY_BID_PRICE_NEG:.0f} €/MWh</td>
                <td style="width:33%;text-align:center;"><b>ERGEBNIS</b><br>Regelenergie-Erlös: {kpi_afrr_rev:,.0f} €</td>
            </tr>
        </table>
    </div>
    """
    
    fig.add_annotation(text=info_bar_html, xref="paper", yref="paper", x=0.5, y=1.22, xanchor="center", yanchor="top", showarrow=False)

    fig.update_layout(
        height=1600, 
        template="plotly_white", 
        title_text="<b>Power-to-Heat & aFRR Analyse</b>", 
        hovermode="x unified", 
        barmode='relative', 
        margin=dict(t=240, b=50, l=50, r=50)
    )
    
    filename_html = "PtH_Dashboard.html"
    fig.write_html(filename_html)
    print(f"Dashboard gespeichert: {os.path.abspath(filename_html)}")
    print("Fertig.")