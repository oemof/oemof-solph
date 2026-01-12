import pandas as pd
import requests
import xml.etree.ElementTree as ET
from entsoe import EntsoePandasClient

# --- KONFIGURATION ---
API_KEY = '5a9cb209-3b91-443c-8280-749c0fe22f15'
START_DATE = '2025-01-01'
END_DATE = '2025-06-01'
AREA_CODE = '10Y1001A1001A83F' # DE Control Area (Einheitlicher Markt)

print("--- START: LÖSUNG ÜBER 'PROCURED CAPACITY' (A81) ---")

# 1. Day Ahead (Funktioniert stabil über Library)
# ----------------------------------------------------
try:
    print("1. Lade Day-Ahead...")
    client = EntsoePandasClient(api_key=API_KEY)
    start_ts = pd.Timestamp(START_DATE, tz='Europe/Berlin')
    end_ts = pd.Timestamp(END_DATE, tz='Europe/Berlin')
    
    da = client.query_day_ahead_prices('10Y1001A1001A82H', start=start_ts, end=end_ts)
    da.name = 'day_ahead_price'
    print(f"   ✅ Day-Ahead: {len(da)} Werte.")
except Exception as e:
    print(f"   ❌ Day-Ahead Fehler: {e}")
    da = pd.Series(dtype=float)

# 2. Regelleistung (Direkt als 'Procured Capacity' A81)
# ----------------------------------------------------
def get_capacity_price(business_type, direction=None):
    url = "https://web-api.tp.entsoe.eu/api"
    
    # WICHTIGE ÄNDERUNG: Wir nutzen A81 statt A89!
    # A81 = Procured balancing capacity (Enthält Volumen UND Preis)
    params = {
        'securityToken': API_KEY,
        'documentType': 'A81',          # <--- HIER IST DER FIX
        'controlArea_Domain': AREA_CODE,
        'periodStart': start_ts.strftime('%Y%m%d%H%M'),
        'periodEnd': end_ts.strftime('%Y%m%d%H%M'),
        'processType': 'A51',           # Allocation
        'businessType': business_type,  # A95=FCR, A96=aFRR
        'type_MarketAgreement.Type': 'A01' # Daily (Tägliche Auktion)
    }
    
    # Bei A81 heißt der Richtungsparameter oft anders oder ist implizit, 
    # aber wir versuchen es standardkonform:
    if direction:
        params['flowDirection.Direction'] = direction

    name = f"{business_type} {direction if direction else ''}"
    print(f"   -> Sende Anfrage (A81) für {name}...")
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"      ❌ API Fehler {response.status_code}: {response.text[:150]}...")
        return pd.Series(dtype=float)

    # XML Parsen
    try:
        root = ET.fromstring(response.content)
        data_points = {}
        
        # Namespace ignorieren mit {*}-Syntax
        for timeseries in root.findall('.//{*}TimeSeries'):
            period = timeseries.find('.//{*}Period')
            if period is None: continue
            
            start_str = period.find('.//{*}timeInterval/{*}start').text
            start_dt = pd.to_datetime(start_str).tz_convert('Europe/Berlin')
            
            # Auflösung prüfen
            res_node = period.find('.//{*}resolution')
            res_txt = res_node.text if res_node is not None else "PT60M"
            res_minutes = 15 if res_txt == 'PT15M' else 60
            if res_txt == 'PT4H': res_minutes = 240
            
            for point in period.findall('.//{*}Point'):
                pos = int(point.find('.//{*}position').text)
                
                # HIER IST DER UNTERSCHIED: A81 hat 'price.amount' für den Preis
                # Manche A81 Files haben nur Volumen. Wir suchen den Preis.
                price_node = point.find('.//{*}price.amount')
                
                if price_node is not None:
                    price = float(price_node.text)
                    current_time = start_dt + pd.Timedelta(minutes=(pos-1)*res_minutes)
                    # Wir überschreiben evtl. Duplikate, nehmen den letzten Wert
                    data_points[current_time] = price
        
        if not data_points:
            print("      ⚠️ XML geladen, aber keine 'price.amount' Tags gefunden.")
            return pd.Series(dtype=float)

        s = pd.Series(data_points)
        s = s.sort_index()
        s = s.resample('h').ffill() # Auf Stunden ziehen
        
        print(f"      ✅ {len(s)} Preise geladen.")
        return s
        
    except Exception as e:
        print(f"      ❌ Parsing Fehler: {e}")
        return pd.Series(dtype=float)

# ABFRAGEN
# A95 = FCR
prl = get_capacity_price(business_type='A95') 

# A96 = aFRR
srl_pos = get_capacity_price(business_type='A96', direction='A01') # Up
srl_neg = get_capacity_price(business_type='A96', direction='A02') # Down

# 3. CSV Speichern
# ----------------------------------------------------
print("3. CSV schreiben...")
df = pd.DataFrame(index=pd.date_range(start_ts, end_ts, freq='h', inclusive='left'))
df = df.join(da)

# Robustes Einfügen
if not prl.empty: df['prl'] = prl.reindex(df.index, method='ffill')
else: df['prl'] = 0

if not srl_pos.empty: df['srl_pos'] = srl_pos.reindex(df.index, method='ffill')
else: df['srl_pos'] = 0

if not srl_neg.empty: df['srl_neg'] = srl_neg.reindex(df.index, method='ffill')
else: df['srl_neg'] = 0

df = df.fillna(0)
filename = 'market_data_2025_A81.csv'
df.to_csv(filename, sep=';', decimal=',')

print("-" * 30)
print(f"FERTIG! Datei: {filename}")
print(df.head())