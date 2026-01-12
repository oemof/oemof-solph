import pandas as pd
import glob
import os

# --- CONFIG ---
script_dir = os.path.dirname(os.path.abspath(__file__))
search_pattern = os.path.join(script_dir, "GUI_BALANCING_*.csv")
csv_files = glob.glob(search_pattern)
csv_files.sort() # Sortieren für bessere Übersicht

print(f"--- ANALYSE DER CSV-ABDECKUNG ({len(csv_files)} Dateien) ---")

all_starts = []
all_ends = []

for file in csv_files:
    try:
        # Nur die ersten und letzten Zeilen lesen (schneller)
        df = pd.read_csv(file, sep=None, engine='python')
        
        # Spalte finden
        cols = df.columns
        isp_col = next((c for c in cols if 'ISP' in c), None)
        
        if isp_col:
            # Erster und letzter Eintrag
            start_raw = str(df[isp_col].iloc[0]).split(' - ')[0]
            end_raw = str(df[isp_col].iloc[-1]).split(' - ')[0]
            
            print(f"📄 {os.path.basename(file)}")
            print(f"   Start: {start_raw}  ->  Ende: {end_raw}")
            print(f"   Zeilen: {len(df)}")
            print("-" * 20)
        else:
            print(f"⚠️ {os.path.basename(file)}: Keine Zeitspalte gefunden!")

    except Exception as e:
        print(f"❌ Fehler bei {os.path.basename(file)}: {e}")

print("\n--- FAZIT ---")
print("Wenn sich die Zeiträume nicht nahtlos berühren (z.B. Ende Datei 1 ist nicht Start Datei 2),")
print("dann hast du dort die Nullen im Graphen.")