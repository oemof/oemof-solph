from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_grouped_bars(
    df1,
    df2=None,
    subtitles=None,
    colors=(
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
        "tab:orange",
        "tab:green",
    ),
    figsize=(10, 4),
    subtitle_fontsize=16,
    tick_fontsize=15,
    legend_fontsize=15,
    avoid_sharey=False,
    ylabels=None,
    add_numbers=None,
):
    """
    df1, df2: DataFrames mit Struktur
        * Index = Gruppen
        * Spalten = Serien (Balken)

    df2 ist optional: Wenn None, wird nur df1 geplottet.
    """

    # Anzahl der Subplots bestimmen
    if df2 is None:
        n_plots = 1
        dataframes = [df1]
    else:
        n_plots = 2
        dataframes = [df1, df2]

    # Untertitel vorbereiten
    if subtitles is None:
        if n_plots == 1:
            subtitles = ("",)
        else:
            subtitles = (
                "Untertitel für Subplot 1",
                "Untertitel für Subplot 2",
            )
    elif isinstance(subtitles, str):
        subtitles = (subtitles,)

    # Figure und Achsen erstellen
    if n_plots > 1 and avoid_sharey is False:
        share_y = True
    else:
        share_y = False
    fig, axes = plt.subplots(1, n_plots, figsize=figsize, sharey=share_y)

    if ylabels is None:
        ylabels = [""] * n_plots
    if add_numbers is None:
        add_numbers = [False] * n_plots

    # Wenn nur ein Plot: axes in Liste verpacken
    if n_plots == 1:
        axes = [axes]

    for ax, df, subtitle, yl, numbers in zip(
        axes, dataframes, subtitles, ylabels, add_numbers
    ):
        x = np.arange(len(df.index))  # Gruppen
        n_series = len(df.columns)
        width = 0.8 / n_series  # dynamische Breite je Balken
        if len(x) < 2:
            f = 1.8
        else:
            f = 1
        for i, (col, color) in enumerate(zip(df.columns, colors)):
            ax.bar(
                x + (f * i - (n_series - 1) / 2) * width,
                df[col],
                width,
                label=col,
                color=color,
            )
        if len(x) < 2:
            ax.tick_params(
                axis="x",  # changes apply to the x-axis
                which="both",  # both major and minor ticks are affected
                bottom=False,  # ticks along the bottom edge are off
                top=False,
            )
        else:
            ax.set_xticks(x)
        ax.set_ylabel(yl, fontsize=subtitle_fontsize)
        ax.set_xticklabels(df.index, fontsize=tick_fontsize)
        ax.tick_params(axis="y", labelsize=tick_fontsize)
        if subtitle:
            ax.set_title(subtitle, fontsize=subtitle_fontsize)

        if numbers is True:
            for p in ax.patches:
                ax.annotate(
                    text=int(np.round(p.get_height())),
                    xy=(p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="center",
                    xytext=(0, 15),
                    textcoords="offset points",
                )
                ax.set_ylim(0, 11000)

    # Gemeinsame Legende
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=min(3, len(labels)),  # max. 3 Spalten
        bbox_to_anchor=(0.5, 1.02),
        fontsize=legend_fontsize,
    )

    fig.tight_layout(rect=(0, 0, 1, 0.9))
    plt.show()


# path = r"C:\Users\ukrien\.oemof\tutorial\time_series"
file = "results_all.csv"

all_results = pd.read_csv(Path(file), index_col=[0], header=[0, 1, 2]).T

renamer = {
    "Gas Boiler": "gas boiler",
    "PV": "pv",
    "Heat pump": "heat pump",
    "Battery": "battery",
    "even": "equidistant",
    "uneven": "non-equidistant",
    "Multi 24/100": "multi 24/100",
}
all_results = all_results.rename(index=renamer, columns=renamer)
all_results = (
    all_results.drop("multi 24/100", level=2).droplevel(1).sort_index()
)

ccols = ["heat pump", "gas boiler", "pv", "battery"]
df_plt1 = all_results.loc["2025"][ccols].T
df_plt2 = all_results.loc["2045"][ccols].T
plot_grouped_bars(
    df_plt1,
    df_plt2,
    subtitles=["year of investment: 2025", "year of investment: 2045"],
    ylabels=["installed capacity", ""],
)

df_plt3 = all_results.loc["2025"][["objective"]].T
df_plt4 = all_results.loc["2025"][["time"]].T
plot_grouped_bars(
    df_plt3,
    df_plt4,
    avoid_sharey=True,
    subtitles=["objective value", "computation time in seconds"],
    ylabels=["value", "seconds"],
)

file = Path("results_even_uneven.csv")
part_results = pd.read_csv(file, index_col=[0], header=[0, 1, 2]).T
renamer = {
    "Gas Boiler": "gas boiler",
    "PV": "pv",
    "Heat pump": "heat pump",
    "Battery": "battery",
    "even": "equidistant",
    "uneven": "non-equidistant",
    "Multi 24/100": "multi 24/100",
}
part_results = part_results.rename(index=renamer, columns=renamer)
part_results = part_results.drop("15", level=1).sort_index()
ccols = ["heat pump", "gas boiler", "pv", "battery"]
df_plt5 = part_results.loc["2025"][ccols].T
df_plt6 = part_results.loc["2045"][ccols].T
df_plt5.columns = ["min ".join(col).strip() for col in df_plt5.columns.values]
df_plt6.columns = ["min ".join(col).strip() for col in df_plt6.columns.values]
plot_grouped_bars(
    df_plt5,
    df_plt6,
    subtitles=["year of investment: 2025", "year of investment: 2045"],
    subtitle_fontsize=18,
    tick_fontsize=17,
    legend_fontsize=17,
)
df_plt7 = part_results.loc["2025"][["objective"]].T
df_plt8 = part_results.loc["2025"][["time"]].T
df_plt7.columns = ["min ".join(col).strip() for col in df_plt7.columns.values]
df_plt8.columns = ["min ".join(col).strip() for col in df_plt8.columns.values]
plot_grouped_bars(
    df_plt7,
    df_plt8,
    avoid_sharey=True,
    subtitles=["objective value", "computation time in seconds"],
    ylabels=["value", "seconds"],
    add_numbers=[False, True],
    subtitle_fontsize=18,
    tick_fontsize=17,
    legend_fontsize=17,
)
