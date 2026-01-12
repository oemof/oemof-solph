import pandas as pd
import glob
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from entsoe import EntsoePandasClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np

# --- CONFIG ---
API_KEY = '5a9cb209-3b91-443c-8280-749c0fe22f15'
TIMEZONE = 'Europe/Berlin'
GRID_AREA = 'TenneT TSO' 

# PLOT CONFIG
PLOT_START = None  # Optional: '2025-11-01 00:00'  # Optional: None or 'YYYY-MM-DD HH:MM'
PLOT_END   = None  # Optional: '2025-11-03 00:00'  # Optional: None or 'YYYY-MM-DD HH:MM'

print(f"--- START: DATEN-FUSION V37 (Single Column Selection) ---")

script_dir = os.path.dirname(os.path.abspath(__file__))
all_csvs = glob.glob(os.path.join(script_dir, "*.csv"))

if not all_csvs:
    print("❌ Keine CSV-Dateien gefunden!")
    exit()

print(f"📂 {len(all_csvs)} Dateien gefunden.")

dfs_energy = []
dfs_capacity_price = []
dfs_capacity_vol = [] 
dfs_activation_mw = [] 

# --- HAUPTSCHLEIFE ---
for file in all_csvs:
    fname = os.path.basename(file)
    df = None
    
    try:
        # ---------------------------------------------------------
        # FALL 1: PICASSO (Arbeitspreise)
        # ---------------------------------------------------------
        if 'picasso' in fname.lower():
            # Einlesen: Semikolon getrennt, Punkt als Dezimaltrenner (Hybrid)
            df = pd.read_csv(file, sep=';', decimal='.', na_values=['N/A', 'NaN', '-'])
            
            # Zeitspalte finden
            time_col = next((c for c in df.columns if 'ZEIT' in c.upper() or 'ISO' in c.upper()), None)
            
            if time_col:
                # Zeitstempel bereinigen
                df[time_col] = df[time_col].astype(str).str.replace('"', '').str.strip()
                try: df.index = pd.to_datetime(df[time_col], utc=True).dt.tz_convert(TIMEZONE)
                except: df.index = pd.to_datetime(df[time_col]).dt.tz_localize(TIMEZONE, ambiguous='NaT')
                
                # Strategie: Wir nehmen explizit NUR EINE Spalte pro Richtung
                # Priorität: TNG (TenneT) -> 50HZT (50Hertz) -> AMP (Amprion)
                
                # Positiv
                col_pos = None
                for candidate in ['TNG_POS', '50HZT_POS', 'AMP_POS', 'TTG_POS']:
                    found = next((c for c in df.columns if candidate in c.upper()), None)
                    if found:
                        col_pos = found
                        break
                
                # Negativ
                col_neg = None
                for candidate in ['TNG_NEG', '50HZT_NEG', 'AMP_NEG', 'TTG_NEG']:
                    found = next((c for c in df.columns if candidate in c.upper()), None)
                    if found:
                        col_neg = found
                        break
                
                # DataFrame bauen
                sub = pd.DataFrame(index=df.index)
                
                if col_pos:
                    sub['aFRR_Pos_Arbeitspreis'] = pd.to_numeric(df[col_pos], errors='coerce')
                if col_neg:
                    sub['aFRR_Neg_Arbeitspreis'] = pd.to_numeric(df[col_neg], errors='coerce')
                
                if not sub.empty:
                    dfs_energy.append(sub.resample('15min').mean())
                    print(f"   ⚡ {fname}: Arbeitspreise geladen (Quelle: {col_pos}/{col_neg}).")
            continue

        # ---------------------------------------------------------
        # FALL 2: GUI / ENTSO-E (Leistungspreise & Volumen)
        # ---------------------------------------------------------
        elif 'GUI' in fname.upper():
            # Englisch: Komma getrennt, Punkt Dezimal
            df = pd.read_csv(file, sep=',', decimal='.', quotechar='"', na_values=['N/A', 'NaN'])
            
            isp_col = next((c for c in df.columns if 'ISP' in c.upper()), None)
            if isp_col:
                df['temp_time'] = pd.to_datetime(df[isp_col].str.split(' - ').str[0], dayfirst=True, errors='coerce')
                df = df.dropna(subset=['temp_time'])
                df['temp_time'] = df['temp_time'].dt.tz_localize(TIMEZONE, ambiguous='infer')
                df = df.set_index('temp_time')

                col_p = next((c for c in df.columns if 'Price' in c and 'EUR' in c), None)
                col_v = next((c for c in df.columns if 'Volume' in c and 'MW' in c), None)
                col_type = next((c for c in df.columns if 'Reserve Type' in c), None)
                col_dir = next((c for c in df.columns if 'Direction' in c), None)

                df['cat_p'] = None
                df['cat_v'] = None
                
                t_str = df[col_type].astype(str).str.upper()
                d_str = df[col_dir].astype(str).str.upper()

                # FCR
                mask_fcr = t_str.str.contains('FCR')
                df.loc[mask_fcr, 'cat_p'] = 'FCR_Leistungspreis'
                df.loc[mask_fcr, 'cat_v'] = 'FCR_Capacity'

                # aFRR
                mask_afrr = t_str.str.contains('AFRR')
                mask_up = d_str.str.contains('UP')
                mask_down = d_str.str.contains('DOWN')

                df.loc[mask_afrr & mask_up, 'cat_p'] = 'aFRR_Pos_Leistungspreis'
                df.loc[mask_afrr & mask_up, 'cat_v'] = 'aFRR_Pos_Capacity'
                df.loc[mask_afrr & mask_down, 'cat_p'] = 'aFRR_Neg_Leistungspreis'
                df.loc[mask_afrr & mask_down, 'cat_v'] = 'aFRR_Neg_Capacity'

                if col_p:
                    p = df.pivot_table(index=df.index, columns='cat_p', values=col_p, aggfunc='mean')
                    if not p.empty: dfs_capacity_price.append(p.resample('15min').mean())
                
                if col_v:
                    v = df.pivot_table(index=df.index, columns='cat_v', values=col_v, aggfunc='mean')
                    if not v.empty: dfs_capacity_vol.append(v.resample('15min').mean())

                print(f"   🔋 {fname}: Leistung & Volumen geladen.")
            continue

        # ---------------------------------------------------------
        # FALL 3: AKTIVIERUNG (Netztransparenz)
        # ---------------------------------------------------------
        elif 'Aktivierte' in fname:
            # Deutsch: Semikolon getrennt, Komma Dezimal
            df = pd.read_csv(file, sep=';', decimal=',', na_values=['N/A', 'NaN'])
            
            df['ts'] = df['Datum'] + ' ' + df['von']
            df.index = pd.to_datetime(df['ts'], format='%d.%m.%Y %H:%M').dt.tz_localize(TIMEZONE, ambiguous='infer')
            
            c_pos = next((c for c in df.columns if GRID_AREA in c and 'Positiv' in c), None)
            c_neg = next((c for c in df.columns if GRID_AREA in c and 'Negativ' in c), None)
            
            sub = pd.DataFrame(index=df.index)
            if c_pos: sub['aFRR_Activation_Pos_MW'] = pd.to_numeric(df[c_pos], errors='coerce')
            if c_neg: sub['aFRR_Activation_Neg_MW'] = pd.to_numeric(df[c_neg], errors='coerce')
            
            dfs_activation_mw.append(sub.resample('15min').mean())
            print(f"   📈 {fname}: Aktivierung MW geladen.")
            continue

    except Exception as e:
        print(f"   ⚠️ Fehler bei {fname}: {e}")
        continue

# --- 2. MERGE ---
print("2. Führe Daten zusammen...")

def merge_list(lst):
    if not lst: return pd.DataFrame()
    return pd.concat(lst, axis=0).groupby(level=0).mean()

df_final = pd.concat([
    merge_list(dfs_energy),
    merge_list(dfs_capacity_price),
    merge_list(dfs_capacity_vol),
    merge_list(dfs_activation_mw)
], axis=1).groupby(level=0).mean().fillna(0)

# --- 3. QUOTEN & SPOT ---
print("3. Finalisiere Daten...")

for d in ['Pos', 'Neg']:
    mw = f'aFRR_Activation_{d}_MW'
    cap = f'aFRR_{d}_Capacity'
    if mw in df_final and cap in df_final:
        mask = df_final[cap] > 0.1
        df_final[f'aFRR_Activation_{d}'] = 0.0
        df_final.loc[mask, f'aFRR_Activation_{d}'] = (df_final.loc[mask, mw] / df_final.loc[mask, cap]).clip(0, 1)
        print(f"   ✅ Quote {d}: {(df_final[f'aFRR_Activation_{d}'].mean()*100):.2f}%")

try:
    start = df_final.index[0]; end = df_final.index[-1] + pd.Timedelta(minutes=15)
    client = EntsoePandasClient(api_key=API_KEY)
    da = client.query_day_ahead_prices('10Y1001A1001A82H', start=start, end=end)
    da.name = 'Spotmarkt_Preis'
    if da.index.tz is None: da.index = da.index.tz_localize(TIMEZONE)
    else: da.index = da.index.tz_convert(TIMEZONE)
    df_final = df_final.join(da.resample('15min').ffill()).fillna(0)
except: df_final['Spotmarkt_Preis'] = 0

csv_path = os.path.join(script_dir, 'market_data.csv')
df_final.copy().tz_convert(None).to_csv(csv_path, sep=';', decimal=',')
print(f"💾 Gespeichert: {csv_path}")

# 1. Daten vorbereiten
if PLOT_START: plot_data = df_final.loc[PLOT_START:PLOT_END].copy()
else: plot_data = df_final.copy()
plot_index = plot_data.index

def safe_get(col): 
    return plot_data[col] if col in plot_data else np.zeros(len(plot_index))

# -----------------------------------------------------------------------------
# TEIL A: INTERAKTIVES HTML DASHBOARD
# -----------------------------------------------------------------------------
try:
    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
        subplot_titles=("Arbeitspreise (€/MWh)", "Leistungspreise (€/MW)", "Volumen & Abruf der Regelmärkte (MW)", "Abrufquote der aFRR (Tennet TSO)")
    )
    
    # 1. Arbeitspreise
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('Spotmarkt_Preis'), name='Spotmarkt', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Pos_Arbeitspreis'), name='aFRR Arbeit (+)', line=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Neg_Arbeitspreis'), name='aFRR Arbeit (-)', line=dict(color='red')), row=1, col=1)

    # 2. Leistungspreise
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('FCR_Leistungspreis'), name='FCR Leistung', line=dict(color='orange')), row=2, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Pos_Leistungspreis'), name='aFRR Leistung (+)', line=dict(color='lightgreen')), row=2, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Neg_Leistungspreis'), name='aFRR Leistung (-)', line=dict(color='pink')), row=2, col=1)

    # 3. Volumen (Jetzt alles positiv nach oben!)
    # Vorhaltung
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('FCR_Capacity'), name='FCR Vorhaltung', line=dict(color='orange', dash='dot')), row=3, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Pos_Capacity'), name='aFRR Vorh. (+)', line=dict(color='lightgreen', dash='dot')), row=3, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Neg_Capacity'), name='aFRR Vorh. (-)', line=dict(color='pink', dash='dot')), row=3, col=1)
    # Abruf (Positive Werte)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Activation_Pos_MW'), name='Abruf (+)', fill='tozeroy', line=dict(color='darkgreen')), row=3, col=1)
    # HIER DIE ÄNDERUNG: Kein Minus mehr vor dem Wert!
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Activation_Neg_MW'), name='Abruf (-)', fill='tozeroy', line=dict(color='darkred')), row=3, col=1)
    
    # 4. Quoten (Hier lassen wir Butterfly, das ist übersichtlicher für Verhältnisse)
    fig.add_trace(go.Scatter(x=plot_index, y=safe_get('aFRR_Activation_Pos'), name='Quote (+)', fill='tozeroy', line=dict(color='green')), row=4, col=1)
    fig.add_trace(go.Scatter(x=plot_index, y=-safe_get('aFRR_Activation_Neg'), name='Quote (-)', fill='tozeroy', line=dict(color='red')), row=4, col=1)

    fig.update_layout(height=1400, template='simple_white', title_text="Marktdaten Analyse")
    fig.write_html(os.path.join(script_dir, 'Marktdaten_Interaktiv.html'))
    print("📊 HTML Dashboard gespeichert.")
except Exception as e:
    print(f"Fehler bei HTML: {e}")


# -----------------------------------------------------------------------------
# TEIL B: STATISCHE SVGs
# -----------------------------------------------------------------------------
plt.rcParams.update({'font.size': 11, 'font.family': 'sans-serif', 'svg.fonttype': 'none', 'axes.grid': True, 'grid.alpha': 0.6})

def set_legend_top(ax, lines, labels, ncol=3):
    ax.legend(lines, labels, loc='lower left', bbox_to_anchor=(0, 1.02, 1, 0.1), mode="expand", borderaxespad=0, ncol=ncol, frameon=False)

def format_ax(ax):
    if len(plot_data) < 4*24*4: ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m. %H:%M'))
    else: ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=7))

# 1. ARBEITSPREISE
try:
    f, a = plt.subplots(figsize=(10, 5))
    l1, = a.plot(plot_index, safe_get('Spotmarkt_Preis'), 'b', lw=1.5, label='Spotmarkt')
    l2, = a.plot(plot_index, safe_get('aFRR_Pos_Arbeitspreis'), 'g', alpha=0.8, label='aFRR Arbeit (+)')
    l3, = a.plot(plot_index, safe_get('aFRR_Neg_Arbeitspreis'), 'r', alpha=0.8, label='aFRR Arbeit (-)')
    set_legend_top(a, [l1, l2, l3], ['Spotmarkt', 'aFRR Arbeitspreis (Positiv)', 'aFRR Arbeitspreis (Negativ)'], ncol=3)
    format_ax(a); a.set_ylabel('Preis [€/MWh]'); plt.tight_layout()
    f.savefig(os.path.join(script_dir, 'Datamining_Arbeit.svg'), format='svg')
except: pass

# 2. LEISTUNGSPREISE
try:
    f, a = plt.subplots(figsize=(10, 5))
    l1, = a.plot(plot_index, safe_get('FCR_Leistungspreis'), 'orange', lw=2, label='FCR')
    l2, = a.plot(plot_index, safe_get('aFRR_Pos_Leistungspreis'), 'lightgreen', label='aFRR (+)')
    l3, = a.plot(plot_index, safe_get('aFRR_Neg_Leistungspreis'), 'salmon', label='aFRR (-)')
    set_legend_top(a, [l1, l2, l3], ['FCR Leistungspreis', 'aFRR Leistungspreis (Positiv)', 'aFRR Leistungspreis (Negativ)'], ncol=3)
    format_ax(a); a.set_ylabel('Preis [€/MW]'); plt.tight_layout()
    f.savefig(os.path.join(script_dir, 'Datamining_Leistung.svg'), format='svg')
except: pass

# 3. VOLUMEN (ALLES NACH OBEN)
try:
    f, a = plt.subplots(figsize=(10, 5))
    # Vorhaltung (Linien)
    l1, = a.plot(plot_index, safe_get('FCR_Capacity'), 'orange', ls='--', label='FCR Vorh.')
    l2, = a.plot(plot_index, safe_get('aFRR_Pos_Capacity'), 'lightgreen', ls='--', label='aFRR+ Vorh.')
    l3, = a.plot(plot_index, safe_get('aFRR_Neg_Capacity'), 'salmon', ls='--', label='aFRR- Vorh.')
    
    # Abruf Positiv (Fläche)
    act_pos = safe_get('aFRR_Activation_Pos_MW')
    a.fill_between(plot_index, 0, act_pos, color='darkgreen', alpha=0.4)
    l4, = a.plot(plot_index, act_pos, 'darkgreen', label='Abruf (+)')
    
    # Abruf Negativ (Fläche auch nach OBEN)
    act_neg = safe_get('aFRR_Activation_Neg_MW') # HIER DIE ÄNDERUNG: Positiver Wert
    a.fill_between(plot_index, 0, act_neg, color='darkred', alpha=0.4)
    l5, = a.plot(plot_index, act_neg, 'darkred', label='Abruf (-)')
    
    # Da sich Flächen überlagern, setzen wir das y-Limit intelligent
    # (Max von Kapazität, damit man die Linien noch sieht)
    max_val = max(safe_get('aFRR_Pos_Capacity').max(), safe_get('aFRR_Neg_Capacity').max(), 10)
    a.set_ylim(0, max_val * 1.2)
    
    set_legend_top(a, [l1, l2, l3, l4, l5], ['FCR Vorhaltung', 'aFRR Vorhaltung (Positiv)', 'aFRR Vorhaltung (Negativ)', 'Abruf Positiv', 'Abruf Negativ'], ncol=3)
    format_ax(a); a.set_ylabel('Leistung [MW]'); plt.tight_layout()
    f.savefig(os.path.join(script_dir, 'Datamining_Volumen_All.svg'), format='svg')
except Exception as e: print(f"Volumen Plot Fehler: {e}")

# 4. QUOTEN (Butterfly bleibt hier sinnvoll zur Unterscheidung)
try:
    f, a = plt.subplots(figsize=(10, 5))
    # Positiv
    q_pos = safe_get('aFRR_Activation_Pos')
    a.fill_between(plot_index, 0, q_pos, color='green', alpha=0.3)
    l1, = a.plot(plot_index, q_pos, 'g', label='Quote (+)')
    
    # Negativ (gespiegelt für Quote)
    q_neg = -safe_get('aFRR_Activation_Neg')
    a.fill_between(plot_index, 0, q_neg, color='red', alpha=0.3)
    l2, = a.plot(plot_index, q_neg, 'r', label='Quote (-)')
    
    a.axhline(0, color='black', lw=0.5)
    a.set_ylim(-1.05, 1.05)
    set_legend_top(a, [l1, l2], ['Abrufquote Einspeisung (+)', 'Abrufquote Ausspeisung (-)'], ncol=2)
    format_ax(a); a.set_ylabel('Abrufquote'); plt.tight_layout()
    f.savefig(os.path.join(script_dir, 'Datamining_Quoten.svg'), format='svg')
except: pass

print("✅ Alle Plots erstellt (Volumen korrigiert).")