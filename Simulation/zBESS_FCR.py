import os
import pandas as pd
import oemof.solph as solph
import matplotlib.pyplot as plt
import numpy as np 
import pyomo.environ as pyo # Wichtig für FCR Ergebnisse
from oemof.network.graph import create_nx_graph
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import networkx as nx

# Import deiner Funktion
from custom_constraints import add_fcr_constraints

# --- 1. DATEN LADEN & BEREINIGEN ---
filename = 'Datamining/market_data.csv' 
try:
    data = pd.read_csv(filename, sep=';', decimal=',')
except FileNotFoundError:
    filename = os.path.join('..', 'market_data.csv') 
    data = pd.read_csv(filename, sep=';', decimal=',')

data['temp_time'] = pd.to_datetime(data['temp_time'])
data.set_index('temp_time', inplace=True)
data.index.freq = '15min'

# Test-Ausschnitt (z.B. 2 Tage)
data_slice = data.head(192*2).copy() #192*15min = 2 Tage #entsprechned anpassen für längere Simulationen

# SICHERHEITS-CHECK: Preise bereinigen
# 1. Spotmarkt
data_slice['Spotmarkt_Preis'] = pd.to_numeric(data_slice['Spotmarkt_Preis'], errors='coerce')
if data_slice['Spotmarkt_Preis'].isnull().any():
    print("WARNUNG: Lücken im Spotpreis gefunden! Werden aufgefüllt.")
    data_slice['Spotmarkt_Preis'] = data_slice['Spotmarkt_Preis'].ffill().fillna(0)

# 2. FCR (Das hat gefehlt!)
data_slice['FCR_Leistungspreis'] = pd.to_numeric(data_slice['FCR_Leistungspreis'], errors='coerce')
if data_slice['FCR_Leistungspreis'].isnull().any():
    print("WARNUNG: Lücken im FCR-Preis gefunden! Werden aufgefüllt.")
    data_slice['FCR_Leistungspreis'] = data_slice['FCR_Leistungspreis'].ffill().fillna(0)

print("Daten geladen und bereinigt.")


# --- 2. ENERGIESYSTEM ---
es = solph.EnergySystem(timeindex=data_slice.index)
b_el = solph.Bus(label="electricity_grid")
es.add(b_el)

spot_price = data_slice['Spotmarkt_Preis']

# Spotmarkt Anbindung
market_source = solph.components.Source(
    label="spot_market_buy",
    outputs={b_el: solph.Flow(variable_costs=spot_price)}
)

market_sink = solph.components.Sink(
    label="spot_market_sell",
    inputs={b_el: solph.Flow(variable_costs=spot_price * -1)} 
)
es.add(market_source, market_sink)

# Parameter für Speicher & FCR definieren
P_MAX = 10          # MW
E_MAX = 20          # MWh
FCR_DURATION = 0.25 # Stunden (15 min)

# Batteriespeicher (Nur EINMAL definieren!)
storage = solph.components.GenericStorage(
    label="battery_storage",
    inputs={b_el: solph.Flow(nominal_value=P_MAX)},
    outputs={b_el: solph.Flow(nominal_value=P_MAX)},
    loss_rate=0.00,
    initial_storage_level=0.5,      
    nominal_capacity=E_MAX,            
    inflow_conversion_factor=0.95,  
    outflow_conversion_factor=0.95
)
es.add(storage)


# --- 3. MODELL ERSTELLEN & CONSTRAINTS ---
print("Erstelle Basis-Modell...")
model = solph.Model(es)

print("Füge FCR-Logik hinzu...")
fcr_price_series = data_slice['FCR_Leistungspreis']

# Constraint Funktion aufrufen
model = add_fcr_constraints(
    model=model,
    storage_component=storage,
    fcr_prices=fcr_price_series,
    p_max=P_MAX,
    e_max=E_MAX,
    fcr_duration=FCR_DURATION
)

# --- 4. SOLVEN ---
print("Löse Optimierungsproblem...")
model.solve(solver='cbc') 


# --- 5. AUSWERTUNG & ERGEBNISSE ---
results = solph.processing.results(model)

# A) Physikalische Daten (Flows & SOC)
price_values = data_slice['Spotmarkt_Preis'].values 
fcr_price_values = data_slice['FCR_Leistungspreis'].values

storage_content = results[(storage, None)]['sequences']['storage_content']
flow_in_values = results[(b_el, storage)]['sequences']['flow'].values[:-1]
flow_out_values = results[(storage, b_el)]['sequences']['flow'].values[:-1]

# B) FCR Ergebnisse auslesen (Spezialfall Pyomo Variable)
# Da FCR eine eigene Variable ist, steht sie nicht im Standard-Result dict
fcr_capacity_values = np.array([pyo.value(model.fcr_capacity[t]) for t in model.TIMESTEPS])

# Längen anpassen (Falls Zeitindex um 1 abweicht)
min_len = min(len(price_values), len(flow_in_values), len(fcr_capacity_values))
price_values = price_values[:min_len]
fcr_price_values = fcr_price_values[:min_len]
flow_in_values = flow_in_values[:min_len]
flow_out_values = flow_out_values[:min_len]
fcr_capacity_values = fcr_capacity_values[:min_len]
plot_index = data_slice.index[:min_len]
storage_content_plot = storage_content.iloc[:min_len]

# C) Wirtschaftlichkeit berechnen
time_factor = 0.25 # 15 min

# Cashflow Spotmarkt
costs_spot = flow_in_values * price_values * time_factor
revenues_spot = flow_out_values * price_values * time_factor

# Cashflow FCR (Leistung * Preis * Zeit)
# Annahme: Preis ist pro MW pro Zeitschritt. Falls pro Stunde -> * 0.25
revenues_fcr = fcr_capacity_values * fcr_price_values * time_factor 

# Gesamtgewinn
profit_per_step = revenues_spot - costs_spot + revenues_fcr
cumulative_profit = np.cumsum(profit_per_step)
total_profit = cumulative_profit[-1]
total_fcr_share = revenues_fcr.sum()

print(f"--- WIRTSCHAFTLICHES ERGEBNIS ---")
print(f"Gesamtgewinn: {total_profit:.2f} EUR")
print(f"Davon aus FCR: {total_fcr_share:.2f} EUR")


# =============================================================================
# 6. VISUALISIERUNG (LEGENDEN FIXED: AUẞERHALB & OBEN)
# =============================================================================
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# Konfiguration
PLOT_OPTIONS = {
    '1_Markt_FCR':      1,
    '2_Markt_SOC':      1,
    '3_Cashflow':       1,
    '4_Systemstruktur': 1,
    '5_SOC_Verlauf':    1,
    '6_Dauerlinie':     1
}

plt.rcParams.update({
    'font.size': 11, 'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'svg.fonttype': 'none', 'axes.grid': True,
    'grid.alpha': 0.6, 'grid.linestyle': ':'
})

def format_date_axis(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=7))

# Helper für externe Legende (Packt sie oben drüber)
def set_legend_outside(ax, lines, labels, ncol=2):
    ax.legend(lines, labels, 
              loc='lower left',              # Ankerpunkt der Legende
              bbox_to_anchor=(0, 1.02, 1, 0.1), # Koordinaten (x, y, breite, höhe) -> 1.02 heißt "knapp über dem Plot"
              mode="expand",                 # Legende auf volle Breite ziehen
              borderaxespad=0,               # Kein Abstand zum Rahmen
              ncol=ncol,                     # Spaltenanzahl (nebeneinander)
              frameon=False)                 # Kein Rahmen um die Legende (sieht moderner aus)

total_throughput = (flow_in_values.sum() + flow_out_values.sum()) * 0.25 
cycles = (total_throughput / 2) / E_MAX

print("\n--- STARTE PLOT-GENERIERUNG (LEGENDEN FIX) ---")

# -----------------------------------------------------------------------------
# PLOT 1: MARKT & FCR
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['1_Markt_FCR']:
    fig1, ax1 = plt.subplots(figsize=(10, 5)) # Etwas höher für die Legende
    
    ax1.set_ylabel('Spotmarkt Preis [€/MWh]', color='black')
    l1, = ax1.plot(plot_index, price_values, color='tab:red', linewidth=1, label='Spotpreis')
    ax1.tick_params(axis='y', labelcolor='black')
    
    ax1_b = ax1.twinx()
    poly = ax1_b.fill_between(plot_index, 0, fcr_capacity_values, 
                              color='black', alpha=0.3, hatch='///', label='FCR Reservierung')
    ax1_b.set_ylabel('FCR Leistung [MW]', color='darkorange')
    ax1_b.set_ylim(0, P_MAX * 1.25)
    ax1_b.tick_params(axis='y', labelcolor='darkorange')
    
    # Legende oben fixieren
    set_legend_outside(ax1, [l1, poly], ['Spotpreis', 'FCR Reservierung'], ncol=2)
    
    format_date_axis(ax1)
    plt.tight_layout() # Wichtig: Passt den Rand an, damit Legende nicht abgeschnitten wird
    fig1.savefig('Abb_1_Markt_FCR.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_1 fertig.")


# -----------------------------------------------------------------------------
# PLOT 2: MARKT & SOC
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['2_Markt_SOC']:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    ax2.set_ylabel('Spotmarkt Preis [€/MWh]', color='tab:red')
    l1, = ax2.plot(plot_index, price_values, color='tab:red', linestyle='--', linewidth=1, label='Spotpreis')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    ax2_b = ax2.twinx()
    l2, = ax2_b.plot(plot_index, storage_content_plot, color='tab:blue', linewidth=2, label='Speicherstand')
    ax2_b.set_ylabel('Speicherfüllstand [MWh]', color='tab:blue')
    ax2_b.set_ylim(0, E_MAX * 1.05)
    ax2_b.tick_params(axis='y', labelcolor='tab:blue')
    
    set_legend_outside(ax2, [l1, l2], ['Spotpreis (Links)', 'Speicherstand (Rechts)'], ncol=2)
    
    format_date_axis(ax2)
    plt.tight_layout()
    fig2.savefig('Abb_2_Markt_SOC.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_2 fertig.")


# -----------------------------------------------------------------------------
# PLOT 3: CASHFLOW
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['3_Cashflow']:
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    
    ax3.set_ylabel('Kumulierter Erlös [€]', color='black')
    ax3.fill_between(plot_index, cumulative_profit, color='tab:green', alpha=0.3)
    l1, = ax3.plot(plot_index, cumulative_profit, color='darkgreen', linewidth=1.5, label='Kumulierter Cashflow')
    ax3.axhline(0, color='black', linewidth=1)
    
    set_legend_outside(ax3, [l1], ['Kumulierter Cashflow'], ncol=1)

    format_date_axis(ax3)
    plt.tight_layout()
    fig3.savefig('Abb_3_Cashflow.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_3 fertig.")



# -----------------------------------------------------------------------------
# PLOT 4: SYSTEMSTRUKTUR (Oemof Standard + Farben, Robust)
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['4_Systemstruktur']:
    try:
        fig4 = plt.figure(figsize=(8, 5))
        
        # 1. Den Graphen direkt aus dem Energiesystem holen
        graph = create_nx_graph(es)
        
        # 2. Farben basierend auf dem Typ-Namen (String-Check -> Absturzsicher)
        node_colors = []
        for node in graph.nodes():
            type_str = str(type(node))
            
            if 'Bus' in type_str:
                node_colors.append('#ADD8E6')       # Hellblau (Netzknoten)
            elif 'Source' in type_str:
                node_colors.append('#90EE90')       # Hellgrün (Quelle)
            elif 'Sink' in type_str:
                node_colors.append('#F08080')       # Lachsrot (Senke)
            elif 'Storage' in type_str or 'GenericStorage' in type_str:
                node_colors.append('#6495ED')       # Kräftiges Blau (Speicher)
            elif 'Transformer' in type_str or 'Converter' in type_str:
                node_colors.append('#FFFFE0')       # Hellgelb (Wandler)
            else:
                node_colors.append('whitesmoke')    # Fallback Grau
        
        # 3. Layout berechnen
        pos = nx.spring_layout(graph, seed=42, k=0.6)
        
        # 4. Zeichnen
        nx.draw_networkx_nodes(graph, pos, node_size=2200, 
                               node_color=node_colors, 
                               edgecolors='black', linewidths=1.0)
        
        nx.draw_networkx_edges(graph, pos, width=1.5, arrowsize=15, edge_color='black')
        
        # Labels schön formatieren
        labels = {node: str(node).replace('_', '\n') for node in graph.nodes()}
        nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_family='sans-serif')
        
        plt.axis('off')
        plt.tight_layout()
        fig4.savefig('Abb_4_Systemstruktur.svg', format='svg', bbox_inches='tight')
        print("-> [x] Abb_4_Systemstruktur.svg erstellt (Physikalisches Modell).")
        
    except Exception as e:
        print(f"WARNUNG Abb 4: {e}")
else:
    print("-> [ ] Abb_4 übersprungen.")

# -----------------------------------------------------------------------------
# PLOT 5: SOC VERLAUF
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['5_SOC_Verlauf']:
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    
    ax5.set_ylabel('Speicherenergie [MWh]')
    ax5.fill_between(plot_index, storage_content_plot, color='tab:blue', alpha=0.3)
    l1, = ax5.plot(plot_index, storage_content_plot, color='navy', linewidth=1.5, label='SOC')
    ax5.axhline(E_MAX, color='grey', linestyle='--', label='Max. Kapazität')
    
    # Textbox nach unten rechts verschieben (stört dort meist weniger)
    # Oder wir lassen sie oben links, aber kleiner
    text_str = f"Vollzyklen: {cycles:.2f}"
    ax5.text(0.02, 0.92, text_str, transform=ax5.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='lightgrey'))
    
    set_legend_outside(ax5, [l1], ['Speicher Ladezustand (SOC)'], ncol=1)
    
    format_date_axis(ax5)
    plt.tight_layout()
    fig5.savefig('Abb_5_SOC_Verlauf.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_5 fertig.")


# -----------------------------------------------------------------------------
# PLOT 6: DAUERLINIE
# -----------------------------------------------------------------------------
if PLOT_OPTIONS['6_Dauerlinie']:
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    
    soc_sorted = np.sort(storage_content_plot.values)[::-1]
    dur_ax = np.linspace(0, 100, len(soc_sorted))
    
    ax6.set_ylabel('Speicherenergie [MWh]')
    ax6.set_xlabel('Zeitdauer [%]')
    l1, = ax6.plot(dur_ax, soc_sorted, color='navy', linewidth=2, label='Geordnete Dauerlinie')
    ax6.fill_between(dur_ax, soc_sorted, color='navy', alpha=0.1)
    ax6.set_xlim(0, 100)
    
    set_legend_outside(ax6, [l1], ['Jahresdauerlinie SOC'], ncol=1)
    
    plt.tight_layout()
    fig6.savefig('Abb_6_Dauerlinie.svg', format='svg', bbox_inches='tight')
    print("-> [x] Abb_6 fertig.")

print("--- FERTIG ---")

# =============================================================================
# 7. FINAL DASHBOARD: KPIs, VERTEILUNG & ZEITREIHEN (MIT SEKUNDÄRACHSE)
# =============================================================================
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("\n--- ERSTELLE DAS ULTIMATIVE DASHBOARD (DUAL AXIS) ---")

# --- 1. KPI BERECHNUNG ---
specific_revenue = total_profit / P_MAX
total_energy_throughput = (flow_out_values.sum() + flow_in_values.sum()) / 2 * 0.25 
cycles = total_energy_throughput / E_MAX

# --- 2. ZEIT-ANALYSE ---
is_fcr = fcr_capacity_values > 0.01
is_spot = np.abs(flow_out_values - flow_in_values) > 0.01

time_multi_use = (is_fcr & is_spot).sum()
time_only_fcr = (is_fcr & ~is_spot).sum()
time_only_spot = (~is_fcr & is_spot).sum()
time_idle = (~is_fcr & ~is_spot).sum()

labels_pie = ['Multi-Use (Spot + FCR)', 'Nur FCR (Bereitschaft)', 'Nur Spot (Arbitrage)', 'Leerlauf (Idle)']
values_pie = [time_multi_use, time_only_fcr, time_only_spot, time_idle]
colors_pie = ['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'] 

# --- 3. DASHBOARD LAYOUT ---
# Wir aktivieren "secondary_y" für die 2. Reihe (Preise)
fig = make_subplots(
    rows=5, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "domain"}], 
        [{"colspan": 2, "secondary_y": True}, None], # <--- HIER: Sekundärachse aktiviert!
        [{"colspan": 2}, None],                      
        [{"colspan": 2}, None],                      
        [{"colspan": 2}, None]                       
    ],
    row_heights=[0.20, 0.15, 0.30, 0.15, 0.2], 
    shared_xaxes=False, # Manuelles Syncen ist sicherer bei Indikatoren
    vertical_spacing=0.08, # Etwas mehr Platz für die Achsenbeschriftung
    subplot_titles=("Wirtschaftliche KPIs", "Nutzungsverteilung (% der Zeit)", "Marktpreise (Spot vs. FCR)", "Leistungskorridor & Multi-Use", "Speicherfüllstand", "Kumulierter Cashflow")
)

# --- REIHE 1: INDICATORS & PIE ---
fig.add_trace(go.Indicator(
    mode="number",
    value=specific_revenue,
    title={"text": "Spezifischer Erlös<br><span style='font-size:0.8em;color:gray'>Extrem wichtig (€/MW)</span>"},
    number={'suffix': " €/MW", 'font': {'size': 40, 'color': "darkblue"}}
), row=1, col=1)

fig.add_trace(go.Pie(
    labels=labels_pie,
    values=values_pie,
    marker=dict(colors=colors_pie),
    hole=0.4,
    textinfo='label+percent',
    hoverinfo='label+value+percent',
    showlegend=False
), row=1, col=2)


# --- REIHE 2: PREISE (MIT SEKUNDÄRACHSE) ---
# Spotpreis (Linke Achse - Standard)
fig.add_trace(go.Scatter(
    x=plot_index, y=price_values, 
    name="Spotpreis (Day-Ahead)", 
    line=dict(color='red', width=1),
    hovertemplate='%{y:.2f} €/MWh'
), row=2, col=1, secondary_y=False)

# FCR Preis (Rechte Achse - Neu!)
fig.add_trace(go.Scatter(
    x=plot_index, y=fcr_price_values, 
    name="FCR Leistungspreis", 
    line=dict(color='orange', dash='dot', width=1.5), 
    hovertemplate='%{y:.2f} €/MW',
    visible=True # Jetzt standardmäßig sichtbar, da eigene Achse
), row=2, col=1, secondary_y=True)

# Achsen beschriften
fig.update_yaxes(title_text="Spotpreis [€/MWh]", title_font=dict(color="red"), tickfont=dict(color="red"), row=2, col=1, secondary_y=False)
fig.update_yaxes(title_text="FCR Preis [€/MW]", title_font=dict(color="orange"), tickfont=dict(color="orange"), row=2, col=1, secondary_y=True)


# --- REIHE 3: KORRIDOR ---
spot_net_flow = flow_out_values - flow_in_values
upper_band = spot_net_flow + fcr_capacity_values
lower_band = spot_net_flow - fcr_capacity_values

fig.add_trace(go.Scatter(x=plot_index, y=upper_band, showlegend=False, line=dict(width=0), hoverinfo='skip'), row=3, col=1)
fig.add_trace(go.Scatter(x=plot_index, y=lower_band, name="FCR Band", fill='tonexty', fillcolor='rgba(255, 165, 0, 0.3)', line=dict(width=0), hoverinfo='skip'), row=3, col=1)
fig.add_trace(go.Scatter(x=plot_index, y=spot_net_flow, name="Spot Fahrplan", line=dict(color='black', width=2, shape='hv')), row=3, col=1)

# LIMITS (Workaround mit Scatter-Linien)
line_limit_style = dict(color="grey", dash="dash", width=1)
fig.add_trace(go.Scatter(x=[plot_index[0], plot_index[-1]], y=[P_MAX, P_MAX], mode="lines", line=line_limit_style, name="Limit +10", showlegend=False, hoverinfo="skip"), row=3, col=1)
fig.add_trace(go.Scatter(x=[plot_index[0], plot_index[-1]], y=[-P_MAX, -P_MAX], mode="lines", line=line_limit_style, name="Limit -10", showlegend=False, hoverinfo="skip"), row=3, col=1)


# --- REIHE 4: SOC ---
fig.add_trace(go.Scatter(x=plot_index, y=storage_content_plot, name="SOC", fill='tozeroy', line=dict(color='#1f77b4')), row=4, col=1)
fig.add_trace(go.Scatter(x=[plot_index[0], plot_index[-1]], y=[E_MAX, E_MAX], mode="lines", line=dict(color="grey", dash="dot", width=1), name="Kapazität", showlegend=False, hoverinfo="skip"), row=4, col=1)


# --- REIHE 5: CASHFLOW ---
fig.add_trace(go.Scatter(x=plot_index, y=cumulative_profit, name="Gewinn", line=dict(color='green', width=2), fill='tozeroy'), row=5, col=1)


# --- FINISHING TOUCHES ---
# Manuelles Synchronisieren der X-Achsen
fig.update_xaxes(matches='x', row=2, col=1)
fig.update_xaxes(matches='x', row=3, col=1)
fig.update_xaxes(matches='x', row=4, col=1)
fig.update_xaxes(matches='x', row=5, col=1)

fig.update_layout(
    title_text=f"<b>Analyse Dashboard: Batteriespeicher (10MW/20MWh)</b><br>Gesamtgewinn: {total_profit:,.2f} € | Zyklen: {cycles:.1f}",
    height=1400,
    template="plotly_white",
    hovermode="x unified"
)

# Y-Achsen Labels für den Rest
fig.update_yaxes(title_text="Leistung [MW]", row=3, col=1)
fig.update_yaxes(title_text="Energie [MWh]", row=4, col=1)
fig.update_yaxes(title_text="Euro [€]", row=5, col=1)

filename_html = "Dashboard_Complete_DualAxis.html"
fig.write_html(filename_html)
print(f"-> Dashboard gespeichert: {os.path.abspath(filename_html)}")

import webbrowser
try:
    webbrowser.open(filename_html)
except:
    pass