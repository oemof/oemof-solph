import os
import pandas as pd
import numpy as np
import oemof.solph as solph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pyomo.environ as pyo
from oemof.network.graph import create_nx_graph
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import matplotlib.patches as mpatches

from custom_constraints import add_multi_market_constraints, calculate_activation_profile_with_volume

# =============================================================================
# 0. KONFIGURATION
# =============================================================================
FILENAME = 'market_data.csv'
SIMULATION_DAYS = 4 
BESS_P_MAX = 10.0      
BESS_E_MAX = 20.0       
BESS_EFFICIENCY = 0.95 
BESS_INITIAL_SOC = 0.5 

STRATEGY_BID_POS = 50.0 
STRATEGY_BID_NEG = 50.0 

COL_ACT_POS_MW = 'aFRR_Activation_Pos_MW'
COL_ACT_NEG_MW = 'aFRR_Activation_Neg_MW'

FCR_ENABLED = True
AFRR_POS_ENABLED = True
AFRR_NEG_ENABLED = True


# =============================================================================
# MAIN SIMULATION
# =============================================================================
if __name__ == "__main__":
    
    P_MAX = BESS_P_MAX
    E_MAX = BESS_E_MAX
    
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
        data.index.freq = '15min'

        periods = 96 * SIMULATION_DAYS
        data_slice = data.head(periods).copy()
    except Exception as e:
        print(f"FEHLER: {e}")
        exit()

    cols_to_fix = ['Spotmarkt_Preis', 'FCR_Leistungspreis', 
                   'aFRR_Pos_Leistungspreis', 'aFRR_Neg_Leistungspreis',
                   'aFRR_Pos_Arbeitspreis', 'aFRR_Neg_Arbeitspreis',
                   'aFRR_Activation_Pos', 'aFRR_Activation_Neg',
                   COL_ACT_POS_MW, COL_ACT_NEG_MW]
    
    for col in cols_to_fix:
        if col in data_slice.columns:
            data_slice[col] = pd.to_numeric(data_slice[col], errors='coerce').fillna(0)
        else:
            if 'MW' in col: data_slice[col] = np.random.uniform(-50, 50, len(data_slice))
            else: data_slice[col] = 0.0

    # --- 2. STRATEGIE PROFIL ---
    print("Berechne Profile...")
    vol_pos_only = data_slice[COL_ACT_POS_MW].fillna(0).clip(lower=0) 
    profile_pos = calculate_activation_profile_with_volume(
        market_prices=data_slice['aFRR_Pos_Arbeitspreis'], 
        total_activation_mw=vol_pos_only,
        my_bid_price=STRATEGY_BID_POS, my_p_max=P_MAX
    )

    vol_neg_abs = data_slice[COL_ACT_NEG_MW].fillna(0).clip(upper=0).abs()
    profile_neg = calculate_activation_profile_with_volume(
        market_prices=data_slice['aFRR_Neg_Arbeitspreis'], 
        total_activation_mw=vol_neg_abs,
        my_bid_price=STRATEGY_BID_NEG, my_p_max=P_MAX
    )

    # --- 3. ENERGIESYSTEM ---
    es = solph.EnergySystem(timeindex=data_slice.index)
    b_el = solph.Bus(label="electricity_grid")
    es.add(b_el)
    spot_price = data_slice['Spotmarkt_Preis']
    es.add(solph.components.Source(label="spot_market_buy", outputs={b_el: solph.Flow(variable_costs=spot_price)}))
    es.add(solph.components.Sink(label="spot_market_sell", inputs={b_el: solph.Flow(variable_costs=spot_price * -1)}))

    storage = solph.components.GenericStorage(
        label="battery_storage",
        inputs={b_el: solph.Flow(nominal_value=P_MAX)},
        outputs={b_el: solph.Flow(nominal_value=P_MAX)},
        loss_rate=0.00, initial_storage_level=BESS_INITIAL_SOC, nominal_storage_capacity=E_MAX,                        
        inflow_conversion_factor=BESS_EFFICIENCY, outflow_conversion_factor=BESS_EFFICIENCY
    )
    es.add(storage)

    # --- 4. OPTIMIERUNG ---
    print("Optimiere (V4 - Physikalische Kopplung)...")
    model = solph.Model(es)
    model = add_multi_market_constraints(
        model=model, storage_component=storage, market_bus=b_el,
        fcr_prices=data_slice['FCR_Leistungspreis'],
        afrp_pos_cap_prices=data_slice['aFRR_Pos_Leistungspreis'], afrp_neg_cap_prices=data_slice['aFRR_Neg_Leistungspreis'],
        afrp_pos_energy_prices=data_slice['aFRR_Pos_Arbeitspreis'], afrp_neg_energy_prices=data_slice['aFRR_Neg_Arbeitspreis'],
        p_max=P_MAX, e_max=E_MAX, market_block_size=16, 
        activation_factor_pos=profile_pos, activation_factor_neg=profile_neg,
        enable_fcr=FCR_ENABLED, enable_afrr_pos=AFRR_POS_ENABLED, enable_afrr_neg=AFRR_NEG_ENABLED
    )
    model.solve(solver='cbc', solve_kwargs={'tee': True}) 

    # --- 5. ERGEBNISSE ---
    print("Verarbeite Ergebnisse...")
    t_map = model.t_to_block_map
    fcr_vals, afrr_pos_vals, afrr_neg_vals = [], [], []
    for t in model.TIMESTEPS:
        b = t_map[t] if t in t_map else 0
        fcr_vals.append(pyo.value(model.fcr_capacity_block[b]))
        afrr_pos_vals.append(pyo.value(model.afrp_pos_capacity_block[b]))
        afrr_neg_vals.append(pyo.value(model.afrp_neg_capacity_block[b]))

    # Aufräumen (Wichtig!)
    cols_to_del = ['fcr_capacity_block', 'afrp_pos_capacity_block', 'afrp_neg_capacity_block', 
                   'soc_max_reserve', 'soc_min_reserve', 'force_phys_discharge', 'force_phys_charge']
    for attr in cols_to_del:
        if hasattr(model, attr): delattr(model, attr)

    results = solph.processing.results(model)
    soc = results[(storage, None)]['sequences']['storage_content']
    flow_in = results[(b_el, storage)]['sequences']['flow']
    flow_out = results[(storage, b_el)]['sequences']['flow']
    
    L = min(len(data_slice), len(flow_in), len(fcr_vals), len(soc))
    idx = data_slice.index[:L]
    df_res = pd.DataFrame(index=idx)
    
    df_res['Spot_In'] = flow_in.values[:L]; df_res['Spot_Out'] = flow_out.values[:L]; df_res['SOC'] = soc.values[:L] 
    df_res['FCR_Cap'] = np.array(fcr_vals)[:L]; df_res['aFRR_Pos_Cap'] = np.array(afrr_pos_vals)[:L]; df_res['aFRR_Neg_Cap'] = np.array(afrr_neg_vals)[:L]
    
    df_res['Spot_Price'] = data_slice['Spotmarkt_Preis'].values[:L]
    df_res['FCR_Price'] = data_slice['FCR_Leistungspreis'].values[:L]
    df_res['aFRR_Pos_Cap_Price'] = data_slice['aFRR_Pos_Leistungspreis'].values[:L]
    df_res['aFRR_Neg_Cap_Price'] = data_slice['aFRR_Neg_Leistungspreis'].values[:L]
    df_res['aFRR_Pos_En_Price'] = data_slice['aFRR_Pos_Arbeitspreis'].values[:L]
    df_res['aFRR_Neg_En_Price'] = data_slice['aFRR_Neg_Arbeitspreis'].values[:L]
    df_res['act_pos'] = profile_pos[:L]
    df_res['act_neg'] = profile_neg[:L]

    dt = 0.25
    # 1. Berechne die physikalischen Energiemengen für Regelenergie
    # (Diese Mengen fließen physikalisch, gehören aber NICHT dem Spotmarkt)
    energy_afrr_pos = df_res['aFRR_Pos_Cap'] * df_res['act_pos'] # MW * Faktor = MW (Leistung im Zeitfenster)
    energy_afrr_neg = df_res['aFRR_Neg_Cap'] * df_res['act_neg']
    
    # Optional: FCR Arbeit (FCR erbringt auch Arbeit, meist symmetrisch/gering, aber der Ordnung halber)
    # Wir nehmen vereinfacht an: FCR Arbeit ist im Rauschen enthalten oder wird hier vernachlässigt, 
    # da wir keine Frequenzdaten haben. Wenn du es ganz genau willst, müsstest du FCR-Arbeit abziehen.
    # Für jetzt fokusieren wir uns auf den großen Batzen: aFRR.

    # 2. Berechne die WAHREN Spot-Mengen (Netting)
    # Spot Out = Was raus fließt MINUS was für aFRR+ reserviert war
    # .clip(lower=0) verhindert negative Werte durch Rundungsfehler
    df_res['Real_Spot_Out'] = (df_res['Spot_Out'] - energy_afrr_pos).clip(lower=0)
    
    # Spot In = Was rein fließt MINUS was für aFRR- (Laden) reserviert war
    df_res['Real_Spot_In']  = (df_res['Spot_In'] - energy_afrr_neg).clip(lower=0)

    # 3. Cashflow Berechnung (Jetzt mit den bereinigten Real_Spot Werten)
    # 3. GESAMTLEISTUNGSKURVE (Netto-Fluss)
    # Positiv = Laden (Gesamt), Negativ = Entladen (Gesamt)
    # Das ist die Kurve, die du wolltest!
    total_in = df_res['Real_Spot_In'] + energy_afrr_neg
    total_out = df_res['Real_Spot_Out'] + energy_afrr_pos
    df_res['Total_Net_Flow'] = total_in - total_out
    # Leistungserlöse (Bleiben gleich)
    df_res['Rev_FCR_Cap']       = df_res['FCR_Cap'] * df_res['FCR_Price'] * dt
    df_res['Rev_aFRR_Pos_Cap']  = df_res['aFRR_Pos_Cap'] * df_res['aFRR_Pos_Cap_Price'] * dt
    df_res['Rev_aFRR_Neg_Cap']  = df_res['aFRR_Neg_Cap'] * df_res['aFRR_Neg_Cap_Price'] * dt
    
    # Arbeitserlöse (Regelenergie)
    df_res['Rev_aFRR_Pos_En']   = energy_afrr_pos * df_res['aFRR_Pos_En_Price'] * dt
    # Achtung Vorzeichen aFRR Neg: Wir nutzen die Menge energy_afrr_neg (positiv) * Preis
    df_res['Rev_aFRR_Neg_En']   = -1 * (energy_afrr_neg * df_res['aFRR_Neg_En_Price'] * dt)

    # Spotmarkt Erlöse (KORRIGIERT: Nur der Reststrom)
    df_res['Rev_Spot_Sold']     = df_res['Real_Spot_Out'] * df_res['Spot_Price'] * dt
    df_res['Cost_Spot_Bought']  = -1 * (df_res['Real_Spot_In'] * df_res['Spot_Price'] * dt)

    # Summe
    df_res['Total_Profit'] = (df_res['Rev_FCR_Cap'] + df_res['Rev_aFRR_Pos_Cap'] + df_res['Rev_aFRR_Neg_Cap'] +
                              df_res['Rev_aFRR_Pos_En'] + df_res['Rev_aFRR_Neg_En'] +
                              df_res['Rev_Spot_Sold'] + df_res['Cost_Spot_Bought'])
    
    df_res['Cum_Profit'] = df_res['Total_Profit'].cumsum()
    ###################################

    # =========================================================================
    # 5c. EXPORT NACH CSV (NEU)
    # =========================================================================
    print("\n--- EXPORTIERE DATEN ---")
    
    # Dateiname mit Strategie-Parametern, damit man Dateien nicht verwechselt
    csv_filename = f"Ergebnisse_BESS_BidPos{int(STRATEGY_BID_POS)}_BidNeg{int(STRATEGY_BID_NEG)}.csv"
    
    # Exportieren:
    # sep=';' -> Damit Excel Spalten sofort erkennt
    # decimal=',' -> Damit Excel Zahlen als Zahlen erkennt (deutsch)
    # encoding='utf-8-sig' -> Damit Umlaute und €-Zeichen korrekt bleiben
    
    try:
        df_res.to_csv(csv_filename, sep=';', decimal=',', encoding='utf-8-sig')
        print(f"[x] Ergebnisse gespeichert in: {os.path.abspath(csv_filename)}")
    except Exception as e:
        print(f"[!] Fehler beim Speichern der CSV: {e}")

    # =============================================================================
    # 6. SVG PLOTS ... (Hier geht dein Code weiter wie gehabt)
    ########################################################################################################
    ########################################################################################################
# =============================================================================
    # 6. VISUALISIERUNG (WISSENSCHAFTLICHE PLOTS FÜR WORD)
    # =============================================================================
    print("\n--- ERSTELLE WISSENSCHAFTLICHE PLOTS (SVG) ---")
    
    # 1. Globales Styling für Paper/Thesis
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], # Serifenlose Schrift für Plots
        'svg.fonttype': 'none',   # Text als Text speichern (nicht als Pfade), wichtig für Nachbearbeitung
        'axes.grid': True,
        'grid.alpha': 0.5,
        'grid.linestyle': ':',
        'axes.axisbelow': True,   # Gitter hinter den Balken
        'lines.linewidth': 1.5
    })

    # Helfer-Funktionen für konsistentes Design
    def format_date_axis(ax):
        """Formatiert X-Achse auf Tag.Monat."""
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    
    def set_legend_top(ax, lines, labels, ncol=3):
        """Platziert Legende sauber ÜBER dem Plot (wie in Screenshots)."""
        ax.legend(lines, labels, 
                  loc='lower left', 
                  bbox_to_anchor=(0, 1.02, 1, 0.1), # Beginnt exakt über dem Plot
                  mode="expand",                    # Zieht Legende über volle Breite
                  borderaxespad=0, 
                  ncol=ncol, 
                  frameon=False)                    # Kein Rahmen um Legende
    


    # --- PLOT 1: LEISTUNGSBILANZ MIT PREIS & GESAMTKURVE ---
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    x = df_res.index
    w = 0.008 
    
    # A) Zweitachse zuerst erstellen (Hintergrund: Balken)
    ax1_b = ax1.twinx()
    transparency = 0.2
    # Balken (Transparent: alpha=0.6)
    p_spot = df_res['Real_Spot_In']
    p_afrr = energy_afrr_neg
    b_in_spot = ax1_b.bar(x, p_spot, w, color='darkblue', alpha=transparency, label='Spot Ladung', zorder=1)
    b_in_afrr = ax1_b.bar(x, p_afrr, w, bottom=p_spot, color='darkred', alpha=transparency, label='aFRR- Ladung', zorder=1)

    n_spot = -1 * df_res['Real_Spot_Out']
    n_afrr = -1 * energy_afrr_pos
    b_out_spot = ax1_b.bar(x, n_spot, w, color='skyblue', alpha=transparency, label='Spot Entladung', zorder=1)
    b_out_afrr = ax1_b.bar(x, n_afrr, w, bottom=n_spot, color='darkgreen', alpha=transparency, label='aFRR+ Entladung', zorder=1)
    
    # B) Die NEUE Gesamtleistungskurve (Vordergrund auf Zweitachse)
    l_net, = ax1_b.plot(x, df_res['Total_Net_Flow'], color='black', linewidth=1.2, label='∑ Netto-Leistung', zorder=5)

    # Achsen-Setup Rechts
    ax1_b.set_ylabel('Leistung [MW]')
    ax1_b.set_ylim(-P_MAX*1.1, P_MAX*1.1)
    ax1_b.axhline(0, color='black', linewidth=0.8, zorder=2)

    # C) Spotpreis (Linke Achse) - Trick für Vordergrund
    # Wir setzen ax1 (Links) NACH OBEN (zorder) und machen den Hintergrund transparent
    ax1.set_zorder(ax1_b.get_zorder() + 1) 
    ax1.patch.set_visible(False) # Hintergrund unsichtbar machen damit man Balken sieht
    
    l1, = ax1.plot(x, df_res['Spot_Price'], color='red', linewidth=1.2, label='Spotpreis', zorder=10)
    ax1.set_ylabel('Spotpreis [€/MWh]')
    
    # Legende
    handles = [l1, l_net, b_in_spot, b_in_afrr, b_out_spot, b_out_afrr]
    labels = ['Spotpreis', '∑ Netto-Leistung', 'Spot Ladung', 'aFRR(neg) Ladung', 'Spot Entladung', 'aFRR(pos) Entladung']
    set_legend_top(ax1, handles, labels, ncol=3)
    
    format_date_axis(ax1)
    fig1.savefig('Abb_1_Leistungsbilanz.svg', format='svg', bbox_inches='tight')
    print("[x] Abb 1 (Leistungsbilanz & Netto-Kurve) gespeichert.")

    # -------------------------------------------------------------------------
    # PLOT 2: PREISE (Linien)
    # -------------------------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    l1, = ax2.plot(df_res.index, df_res['FCR_Price'], color='#ff7f0e', ls='-', label='FCR')
    l2, = ax2.plot(df_res.index, df_res['aFRR_Pos_Cap_Price'], color='#2ca02c', ls='--', label='aFRR+ Leist.')
    l3, = ax2.plot(df_res.index, df_res['aFRR_Neg_Cap_Price'], color='#d62728', ls=':', label='aFRR- Leist.')
    
    ax2.set_ylabel('Leistungspreis [€/MW]')
    
    set_legend_top(ax2, [l1, l2, l3], ['FCR', 'aFRR(pos) Kapazitätspreis', 'aFRR(neg) Kapazitätspreis'], ncol=3)
    format_date_axis(ax2)
    
    plt.tight_layout()
    fig2.savefig('Abb_2_Markt_Preise.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_2 (Preise) gespeichert.")

    # -------------------------------------------------------------------------
    # PLOT 3: SOC & SPOT (Wie Screenshot 2)
    # -------------------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    
    # Linke Achse: Spot (Rot gestrichelt)
    l1, = ax3.plot(df_res.index, df_res['Spot_Price'], color='#d62728', ls='--', linewidth=1, label='Spotpreis')
    ax3.set_ylabel('Spotmarkt Preis [€/MWh]')
    
    # Rechte Achse: SOC (Dunkelblau fett)
    ax3_b = ax3.twinx()
    l2, = ax3_b.plot(df_res.index, df_res['SOC'], color='navy', linewidth=2, label='Speicherstand')
    ax3_b.set_ylabel('Speicherfüllstand [MWh]')
    ax3_b.set_ylim(0, E_MAX * 1.05)
    
    set_legend_top(ax3, [l1, l2], ['Spotpreis', 'Speicherstand'], ncol=2)
    format_date_axis(ax3)
    
    plt.tight_layout()
    fig3.savefig('Abb_3_Markt_SOC.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_3 (SOC) gespeichert.")

   # --- PLOT 4 (Cashflow - auch mit Transparenz) ---
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    # Handles für Legende
    p1 = df_res['Rev_FCR_Cap']; p2 = df_res['Rev_aFRR_Pos_Cap']; p3 = df_res['Rev_aFRR_Neg_Cap']; p4 = df_res['Rev_aFRR_Pos_En']; p5 = df_res['Rev_Spot_Sold']
    # Transparenz (alpha=0.7)
    b1 = ax4.bar(x, p1, w, color='orange', alpha=0.7, label='FCR Cap')
    b2 = ax4.bar(x, p2, w, bottom=p1, color='#32CD32', alpha=0.7, label='aFRR+ Cap')
    b3 = ax4.bar(x, p3, w, bottom=p1+p2, color='lightcoral', alpha=0.7, label='aFRR- Cap')
    b4 = ax4.bar(x, p4, w, bottom=p1+p2+p3, color='darkgreen', alpha=0.7, label='aFRR+ Work')
    b5 = ax4.bar(x, p5, w, bottom=p1+p2+p3+p4, color='skyblue', alpha=0.7, label='Spot Sold')
    
    n1 = df_res['Cost_Spot_Bought']; n2 = df_res['Rev_aFRR_Neg_En']
    bn1 = ax4.bar(x, n1, w, color='darkblue', alpha=0.7, label='Spot Buy')
    bn2 = ax4.bar(x, n2, w, bottom=n1, color='darkred', alpha=0.7, label='aFRR- Work')
    
    # Summenlinie (Vordergrund)
    ax4_b = ax4.twinx()
    l_sum, = ax4_b.plot(x, df_res['Cum_Profit'], 'black', lw=2, label='Total')
    
    # Achsen-Setup
    ax4.set_zorder(ax4_b.get_zorder()+1); ax4.patch.set_visible(False) # Linke Achse nach vorne
    ax4.set_ylabel('Cashflow seperiert [€]'); ax4_b.set_ylabel('Cashflow Gesamt [€]')
    
    set_legend_top(ax4, [b1,b2,b3,b4,b5,bn1,bn2,l_sum], ['FCR','aFRR(pos) Leistungsmarkte','aFRR(neg) Leistungsmarkt','aFRR(pos) Arbeitsmarkt','aFRR(neg) Arbeitsmarkt',' Spotmarkt Verkauf','Spotmarkt Kauf','aFRR(neg) Arbeitsmarkt','Total'], ncol=4)
    format_date_axis(ax4); fig4.savefig('Abb_4_Cashflow_Detail.svg', format='svg', bbox_inches='tight')
    # -------------------------------------------------------------------------
    # PLOT 5: SYSTEMSTRUKTUR (Netzwerk)
    # -------------------------------------------------------------------------
    # Wird oft als PNG besser, SVG geht aber auch. Hier vereinfacht.
    try:
        fig5 = plt.figure(figsize=(8, 5))
        graph = create_nx_graph(es)
        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, node_color='lightgray', edge_color='black')
        plt.tight_layout()
        plt.savefig('Abb_5_Systemstruktur.svg', format='svg')
        print("-> [x] Abb_5 (System) gespeichert.")
    except:
        pass

    # -------------------------------------------------------------------------
    # PLOT 6: DAUERLINIE (SOC)
    # -------------------------------------------------------------------------
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    
    # Sortieren für Dauerlinie
    soc_sorted = np.sort(df_res['SOC'].values)[::-1] # Absteigend
    duration_axis = np.linspace(0, 100, len(soc_sorted))
    
    l1, = ax6.plot(duration_axis, soc_sorted, color='navy', linewidth=2, label='SOC Dauerlinie')
    ax6.fill_between(duration_axis, soc_sorted, color='navy', alpha=0.1)
    
    ax6.set_ylabel('Speicherenergie [MWh]')
    ax6.set_xlabel('Zeitdauer [%]')
    ax6.set_xlim(0, 100)
    ax6.set_ylim(0, E_MAX * 1.05)
    
    set_legend_top(ax6, [l1], ['SOC Jahresdauerlinie'], ncol=1)
    
    plt.tight_layout()
    fig6.savefig('Abb_6_Dauerlinie.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_6 (Dauerlinie) gespeichert.")

 # -------------------------------------------------------------------------
    # PLOT 7: NUTZUNGSVERTEILUNG (KORRIGIERT & SYNCHRON MIT DASHBOARD)
    # -------------------------------------------------------------------------
    fig7, ax7 = plt.subplots(figsize=(8, 5))
    
    # 1. Logik exakt wie im Dashboard definieren
    thr = 0.01
    
    # WICHTIG: Wir nutzen die bereinigten Real_Spot Werte (Netto-Fluss)
    is_spot = (df_res['Real_Spot_In'] > thr) | (df_res['Real_Spot_Out'] > thr)
    
    # Reserven prüfen
    has_fcr = df_res['FCR_Cap'] > thr
    has_afrr_pos = df_res['aFRR_Pos_Cap'] > thr
    has_afrr_neg = df_res['aFRR_Neg_Cap'] > thr
    is_res_any = has_fcr | has_afrr_pos | has_afrr_neg
    
    # 2. Kategorien bilden (Exklusiv)
    # A. Multi-Use: Spot + Reserve
    c_multi = (is_spot & is_res_any).sum()
    
    # B. Spot Only: Spot + KEINE Reserve
    c_spot = (is_spot & (~is_res_any)).sum()
    
    # C. Idle: Nichts
    c_idle = ((~is_spot) & (~is_res_any)).sum()
    
    # D. Reserve Only: Keine Spot-Aktivität, aber Reserve
    # (Hier fassen wir alle Reserve-Typen zusammen für den einfachen Plot)
    c_res_only = ((~is_spot) & is_res_any).sum()
    
    # 3. Plotten
    categories = ['Multi-Use', 'Nur Reserve', 'Nur Spot', 'Leerlauf']
    values = [c_multi, c_res_only, c_spot, c_idle]
    colors = ['purple', 'orange', 'blue', 'gray']
    
    # Bar Chart mit Beschriftung
    bars = ax7.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
    
    # Text-Label über den Balken
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax7.text(bar.get_x() + bar.get_width()/2., height + (max(values)*0.01),
                     f'{int(height)}\n({height/len(df_res)*100:.1f}%)',
                     ha='center', va='bottom', fontsize=10)
            
    ax7.set_ylabel('Anzahl Zeitschritte (15 min)')
    ax7.set_ylim(0, max(values)*1.15) # Platz für Labels oben lassen
    ax7.set_title('Betriebszustände (Basierend auf Netto-Flüssen)')
    
    fig7.savefig('Abb_7_Nutzungsverteilung.svg', format='svg', bbox_inches='tight')
    print("[x] Abb 7 (Nutzungsverteilung) korrigiert gespeichert.")

# =============================================================================
    # 7. DASHBOARD (PRO UPDATE)
    # =============================================================================
    print("\n--- ERSTELLE DASHBOARD ---")
    sum_profit = df_res['Total_Profit'].sum()
    sum_fcr = df_res['Rev_FCR_Cap'].sum()
    sum_afrr = (df_res['Rev_aFRR_Pos_Cap'] + df_res['Rev_aFRR_Neg_Cap'] + df_res['Rev_aFRR_Pos_En'] + df_res['Rev_aFRR_Neg_En']).sum()
    sum_spot = (df_res['Rev_Spot_Sold'] + df_res['Cost_Spot_Bought']).sum()
    cycles = ((df_res['Spot_Out'].sum() + df_res['Spot_In'].sum()) * 0.25 / 2) / E_MAX


    # 2. Pie Chart Daten (KORRIGIERT: Exklusive Kategorien)
    thr = 0.01
    has_spot = (df_res['Real_Spot_In'] > thr) | (df_res['Real_Spot_Out'] > thr)
    has_fcr = df_res['FCR_Cap'] > thr
    has_afrr_pos = df_res['aFRR_Pos_Cap'] > thr
    has_afrr_neg = df_res['aFRR_Neg_Cap'] > thr
    
    # Hilfsvariable: Ist IRGENDEINE Reserve aktiv?
    is_res_any = has_fcr | has_afrr_pos | has_afrr_neg

    # 1. Multi-Use: Spot + Irgendeine Reserve
    c_multi = (has_spot & is_res_any).sum()

    # 2. Spot Only: Spot + KEINE Reserve
    c_spot = (has_spot & (~is_res_any)).sum()

    # 3. Idle: Weder Spot noch Reserve
    c_idle = ((~has_spot) & (~is_res_any)).sum()

    # JETZT KOMMT DER FIX FÜR DIE RESERVEN (Nur wenn KEIN Spot da ist):
    # Wir müssen symmetrische Angebote (Pos & Neg) abfangen.
    
    # Res Mix: Mehr als eine Reserve-Art gleichzeitig (z.B. FCR+aFRR oder aFRR+ & aFRR-)
    # Wir zählen, wie viele Reserve-Flags True sind (als int addieren)
    res_count = has_fcr.astype(int) + has_afrr_pos.astype(int) + has_afrr_neg.astype(int)
    c_res_mix = ((~has_spot) & (res_count > 1)).sum()

    # Single Types (Nur genau EINE Art aktiv)
    c_fcr_only = ((~has_spot) & has_fcr & (res_count == 1)).sum()
    c_afrr_pos_only = ((~has_spot) & has_afrr_pos & (res_count == 1)).sum()
    c_afrr_neg_only = ((~has_spot) & has_afrr_neg & (res_count == 1)).sum()

    vals_pie = [c_multi, c_res_mix, c_fcr_only, c_afrr_pos_only, c_afrr_neg_only, c_spot, c_idle]
    # Labels müssen dazu passen:
    labels_pie = ['Multi', 'Res Mix', 'FCR Only', 'aFRR+ Only', 'aFRR- Only', 'Spot Only', 'Idle']
    labels_pie = ['Multi', 'Res Mix', 'FCR', 'aFRR+', 'aFRR-', 'Spot', 'Idle']
    colors_pie = ['#800080', '#FFA500', '#FFD700', '#32CD32', '#CD5C5C', '#1f77b4', '#D3D3D3']

    fig = make_subplots(
        rows=5, cols=4, shared_xaxes=True,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "domain"}], [{"colspan": 4, "secondary_y": True}, None, None, None], [{"colspan": 4}, None, None, None], [{"colspan": 4}, None, None, None], [{"colspan": 4, "secondary_y": True}, None, None, None]],
        row_heights=[0.14, 0.20, 0.20, 0.18, 0.28], vertical_spacing=0.08,
        subplot_titles=(None, None, None, "Zeit-Nutzung", "Marktpreise", "Leistungsbilanz", "SOC", "Cashflow")
    )

    fig.add_trace(go.Indicator(mode="number", value=P_MAX, title={"text": f"Elektrische Leistung [MW]", 'font':{'size': 20}}, number={'font': {'color': "#444", 'size': 40}}), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number", value=sum_profit, title={"text": "Gewinn [€]", 'font':{'size': 20}}, number={'valueformat': ",.0f", 'font': {'color': "green", 'size': 40}}), row=1, col=2)
    fig.add_trace(go.Indicator(mode="number", value=cycles, title={"text": "Gesamtzyklen", 'font':{'size': 20}}, number={'valueformat': ".1f", 'font': {'color': "#1f77b4", 'size': 40}}), row=1, col=3)
    fig.add_trace(go.Pie(labels=labels_pie, values=vals_pie, marker=dict(colors=colors_pie), hole=0.4, textinfo='percent', showlegend=False), row=1, col=4)

    # --- ROW 2: ALLE PREISE (NEU) ---
    
    # 1. Energie-Preise (Links / Primär / Durchgezogen)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Spot_Price'], name='Spot [En]', line=dict(color='blue', width=1.5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['aFRR_Pos_En_Price'], name='aFRR+ Arbeit', line=dict(color='green', width=1)), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['aFRR_Neg_En_Price'], name='aFRR- Arbeit', line=dict(color='red', width=1)), row=2, col=1)

    # 2. Leistungs-Preise (Rechts / Sekundär / Gestrichelt)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['FCR_Price'], name='FCR Leist.', line=dict(color='#FFD700', dash='dot')), row=2, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['aFRR_Pos_Cap_Price'], name='aFRR+ Leist.', line=dict(color='#32CD32', dash='dot')), row=2, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['aFRR_Neg_Cap_Price'], name='aFRR- Leist.', line=dict(color='lightcoral', dash='dot')), row=2, col=1, secondary_y=True)
    
    # ROW 3: LEISTUNGSBILANZ (UPDATE: Transparenz & Netto-Kurve)
    # Balken (opacity=0.6)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Real_Spot_In'], name='Spot Ladung', marker_color='darkblue', opacity=0.6), row=3, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=energy_afrr_neg, name='aFRR- Ladung', marker_color='darkred', opacity=0.6), row=3, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=-1*df_res['Real_Spot_Out'], name='Spot Entladung', marker_color='skyblue', opacity=0.6), row=3, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=-1*energy_afrr_pos, name='aFRR+ Entladung', marker_color='darkgreen', opacity=0.6), row=3, col=1)

    # NEU: Gesamtleistungskurve (Schwarz, Fett, Vordergrund)
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Total_Net_Flow'], name='∑ Netto-Leistung', line=dict(color='black', width=2)), row=3, col=1)

    # Row 4: SOC
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['SOC'], name='SOC', fill='tozeroy', line=dict(color='purple')), row=4, col=1)

    # Row 5: Cashflow
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_FCR_Cap'], name='FCR Cap', marker_color='orange', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_aFRR_Pos_Cap'], name='aFRR+ Cap', marker_color='#32CD32', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_aFRR_Neg_Cap'], name='aFRR- Cap', marker_color='lightcoral', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_aFRR_Pos_En'], name='aFRR+ Work', marker_color='darkgreen', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_Spot_Sold'], name='Spot Sold', marker_color='skyblue', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Cost_Spot_Bought'], name='Spot Buy', marker_color='darkblue', opacity=0.7), row=5, col=1)
    fig.add_trace(go.Bar(x=df_res.index, y=df_res['Rev_aFRR_Neg_En'], name='aFRR- Work', marker_color='darkred', opacity=0.7), row=5, col=1)
    
    fig.add_trace(go.Scatter(x=df_res.index, y=df_res['Cum_Profit'], name='Summe', line=dict(color='black', width=3)), row=5, col=1, secondary_y=True)

    for r in [2,3,4,5]: fig.update_xaxes(matches='x2', row=r, col=1)
    
    fig.update_yaxes(title_text="€ / MWh", row=2, col=1)
    fig.update_yaxes(title_text="Leistung [MW]", row=3, col=1)
    fig.update_yaxes(title_text="Energie [MWh]", row=4, col=1)
    fig.update_yaxes(title_text="Cashflow [€]", row=5, col=1)


    fig.update_layout(height=1600, template="plotly_white", title_text="<b>Batteriespeicher Multi-Market Analyse</b>", hovermode="x unified", barmode='relative', margin=dict(t=240, b=50, l=50, r=50))
    
    filename_html = "Dashboard_Final.html"
    fig.write_html(filename_html)
    print(f"Dashboard gespeichert: {os.path.abspath(filename_html)}")
    print("Fertig.")