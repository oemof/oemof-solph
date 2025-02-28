import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def hex_from_rgb(rgb):
    """Konvertiert einen RGB-Tupel in einen Hex-String."""
    return "#{:02X}{:02X}{:02X}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


# Dark Mode Palette (Farben in absteigender Wichtigkeit)
dark_palette = {
    "color1": "#1F567D",
    "color2": "#8AA8A1",
    "color3": "#FA8334",
    "color4": "#FF006E",
    "color5": "#FFFD77",
}

# Erzeuge die Light Mode Palette: Die erste Farbe bleibt gleich,
# die weiteren Farben werden um 30 % in Richtung Weiß aufgehellt.
light_palette = {"color1": dark_palette["color1"]}
for key in ["color2", "color3", "color4", "color5"]:
    rgb = mcolors.to_rgb(dark_palette[key])
    new_rgb = [0.7 * c + 0.3 for c in rgb]
    light_palette[key] = hex_from_rgb(new_rgb)


def draw_lin_vs_mixed_int(mode="dark"):
    """
    Erzeugt eine Figur mit zwei Subplots (nebeneinander):
      - Linker Plot: f(x)=2x+1 (linear) – bezeichnet als "linear programming"
      - Rechter Plot: f(x)=2x+1 für x<0 und f(x)=2x+1+5 für x>=0 (mit Sprung) – bezeichnet als "mixed integer"
    Achsenbeschriftungen und Funktionsbeschreibungen werden weggelassen.
    """
    if mode == "dark":
        palette = dark_palette
        bg_color = "#121212"
        text_color = "#FFFFFF"
    else:
        palette = light_palette
        bg_color = "#FFFFFF"
        text_color = "#000000"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(bg_color)

    # Anpassen der Achsen (nur Farben, keine Labels oder Beschriftungen)
    for ax in [ax1, ax2]:
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color(text_color)

    # Linker Plot: einfache lineare Funktion f(x) = 2x + 1
    x = np.linspace(-10, 10, 400)
    y = 2 * x + 1
    ax1.plot(x, y, color=palette["color1"], linewidth=2)
    ax1.set_title("Linear Programming", color=text_color, fontsize=14)
    ax1.set_xticks([])  # Achsenticks entfernen
    ax1.set_yticks([])

    # Rechter Plot: lineare Funktion mit Sprung:
    # f(x)=2x+1 für x < 0 und f(x)=2x+1+5 für x ≥ 0
    x_left = np.linspace(-10, -0.01, 200)
    x_right = np.linspace(0, 10, 200)
    y_left = 2 * x_left + 1
    y_right = 2 * x_right + 1 + 5

    ax2.plot(x_left, y_left, color=palette["color1"], linewidth=2)
    ax2.plot(x_right, y_right, color=palette["color3"], linewidth=2)

    # Markiere den Sprung: Linker Teil endet mit einem offenen Kreis, rechter Teil beginnt mit einem gefüllten Kreis.
    ax2.plot(
        x_left[-1],
        y_left[-1],
        marker="o",
        markersize=8,
        markerfacecolor=bg_color,
        markeredgecolor=palette["color4"],
        markeredgewidth=2,
    )
    ax2.plot(
        x_right[0],
        y_right[0],
        marker="o",
        markersize=8,
        markerfacecolor=palette["color4"],
        markeredgecolor=palette["color4"],
    )

    ax2.set_title("Mixed-Integer Problem", color=text_color, fontsize=14)
    ax2.set_xticks([])
    ax2.set_yticks([])

    plt.tight_layout()
    plt.show()

    if mode == "dark":
        # Beispiel: Speichern der Dark Mode Abbildung unter "plot_dark.png"
        plt.savefig("lin_vs_mixed_int_plot_dark.png")
    if mode == "light":
        # Beispiel: Speichern der Light Mode Abbildung unter "plot_light.png"
        plt.savefig("lin_vs_mixed_int_plot_light.png")


def draw_timeline(mode="dark", savefig_filename=None):
    """
    Erzeugt eine schematische Darstellung eines Multi-Period Optimization-Zeitrahls
    mit Jahreszahlen und speichert diese, falls ein Dateiname übergeben wird.
    """
    if mode == "dark":
        palette = dark_palette
        bg_color = "#121212"
        text_color = "#FFFFFF"
    else:
        palette = light_palette
        bg_color = "#FFFFFF"
        text_color = "#000000"

    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Entferne Achsenrahmen und Ticks
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False, labelleft=False)

    # Definiere den Zeitstrahl: Beispielhaft von 2020 bis 2030
    years = list(range(2020, 2031))

    # Zeichne den horizontalen Strahl
    ax.plot([years[0], years[-1]], [0, 0], color=palette["color1"], linewidth=2)

    # Für jedes Jahr: Marker und Beschriftung
    for i, year in enumerate(years):
        ax.plot(year, 0, marker="o", markersize=8, color=palette["color3"])
        ax.text(
            year, -0.3, str(year), ha="center", va="top", color=text_color, fontsize=10
        )
        ax.text(
            year,
            0.3,
            f"Period {i+1}",
            ha="center",
            va="bottom",
            color=text_color,
            fontsize=10,
        )

    # Titel hinzufügen
    ax.text(
        (years[0] + years[-1]) / 2,
        0.8,
        "Multi-period Optimization",
        ha="center",
        va="bottom",
        color=text_color,
        fontsize=14,
        fontweight="bold",
    )

    ax.set_xlim(years[0] - 1, years[-1] + 1)
    ax.set_ylim(-1, 1)

    plt.tight_layout()

    if mode == "dark":
        # Beispiel: Speichern der Dark Mode Abbildung unter "plot_dark.png"
        plt.savefig("timeline_dark.png")
    if mode == "light":
        # Beispiel: Speichern der Light Mode Abbildung unter "plot_light.png"
        plt.savefig("timeline_light.png")


def plot_dispatch_invest(csv_path, mode="dark"):
    """
    Liest eine CSV-Datei ein, generiert (falls nicht vorhanden) einen stündlichen Zeitindex ab dem 1.1.2020,
    und zeichnet in einer Figur zwei Subplots:
      - Links: Dispatch-Zeitreihe (Spalte 'demand_th')
      - Rechts: Ein Blockdiagramm, das den Ablauf der Investment Optimization symbolisiert
        (Input Data -> Investment Optimization Model -> Investment Decision)
    Das Diagramm wird im gewünschten Farbschema (dark/light) dargestellt.
    """
    # CSV-Daten einlesen
    df = pd.read_csv(csv_path)

    # Falls keine 'Time'-Spalte vorhanden ist, generiere einen stündlichen Zeitindex
    if "Time" not in df.columns:
        df["Time"] = pd.date_range(start="2020-01-01", periods=len(df), freq="H")

    # Wähle Farbschema basierend auf dem Modus
    if mode.lower() == "dark":
        palette = dark_palette
        bg_color = "#121212"
        text_color = "#FFFFFF"
    else:
        palette = light_palette
        bg_color = "#FFFFFF"
        text_color = "#000000"

    # Erzeuge Figur mit 2 Subplots (nebeneinander)
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor(bg_color)

    # --- Linker Subplot: Dispatch-Zeitreihe in kW ---
    ax1 = axs[0]
    ax1.set_facecolor(bg_color)
    for spine in ax1.spines.values():
        spine.set_color(text_color)
    ax1.tick_params(colors=text_color, labelleft=False)  # Y-Achse: keine Zahlen

    # Plotten der Dispatch-Zeitreihe – hier wird die Spalte 'demand_th' (in kW) genutzt
    ax1.plot(
        df["Time"],
        df["demand_th"],
        marker="o",
        linestyle="-",
        color=palette["color1"],
        linewidth=2,
    )
    ax1.set_title("Dispatch Time Series (kW)", color=text_color, fontsize=14)
    ax1.set_xlabel("Time", color=text_color)
    ax1.set_ylabel("kW", color=text_color)

    # --- Rechter Subplot: Balkendiagramm für Technologiegrößen ---
    # Berechne die Durchschnittswerte der Technologien.
    # Hier werden nur die Spalten 'pv', 'wind', 'heatpump' und 'solarthermie' verwendet.
    avg_pv = df["pv"].mean() if "pv" in df.columns else 0
    avg_wind = df["wind"].mean() if "wind" in df.columns else 0
    avg_heatpump = 0.3
    avg_solarthermie = 0.09

    labels = ["PV", "Wind", "Heat Pump", "Solarthermie"]
    values = [avg_pv, avg_wind, avg_heatpump, avg_solarthermie]
    # Weisen den Balken Farben zu: PV (color3), Wind (color4), Heat Pump (color2), Solarthermie (color5)
    bar_colors = [
        palette["color3"],
        palette["color4"],
        palette["color2"],
        palette["color5"],
    ]

    ax2 = axs[1]
    ax2.set_facecolor(bg_color)
    for spine in ax2.spines.values():
        spine.set_color(text_color)
    ax2.tick_params(colors=text_color, labelleft=False)  # Y-Achse ohne Zahlen

    bars = ax2.bar(
        labels, values, color=bar_colors, edgecolor=text_color, linewidth=1.5
    )

    ax2.set_title("Investment Technology Sizes", color=text_color, fontsize=14)
    ax2.set_ylabel("Average Value", color=text_color, fontsize=14)

    # Gesamttitel der Figur
    fig.suptitle("Dispatch vs. Invest-Optimization", color=text_color, fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    if mode == "dark":
        # Beispiel: Speichern der Dark Mode Abbildung unter "plot_dark.png"
        plt.savefig("plot_dispatch_invest_dark.png")
    if mode == "light":
        # Beispiel: Speichern der Light Mode Abbildung unter "plot_light.png"
        plt.savefig("plot_dispatch_invest_light.png")


# draw_lin_vs_mixed_int('light')
# draw_lin_vs_mixed_int('dark')

# draw_timeline("dark")  # Speichert als "timeline_dark.png"
# draw_timeline("light")  # Speichert als "timeline_light.png"

plot_dispatch_invest(
    r"D:\oemof-solph_fork\tests\test_outputlib\input_data.csv", mode="light"
)
plot_dispatch_invest(
    r"D:\oemof-solph_fork\tests\test_outputlib\input_data.csv", mode="dark"
)
