import os
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# creates the icons in the grid view of the documentation


def hex_from_rgb(rgb):
    """makes rgb to hex"""
    return "#{:02X}{:02X}{:02X}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


# colors of the color palette
dark_palette = {
    "color1": "#1F567D",
    "color2": "#8AA8A1",
    "color3": "#FA8334",
    "color4": "#FF006E",
    "color5": "#FFFD77",
}

# crates light mode color palet
light_palette = {"color1": dark_palette["color1"]}
for key in ["color2", "color3", "color4", "color5"]:
    rgb = mcolors.to_rgb(dark_palette[key])
    new_rgb = [0.7 * c + 0.3 for c in rgb]
    light_palette[key] = hex_from_rgb(new_rgb)


def draw_lin_vs_mixed_int(mode="dark"):
    """
    draws plot for the linear optimization vs. Mix Integer section
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

    for ax in [ax1, ax2]:
        ax.set_facecolor(bg_color)
        ax.tick_params(colors=text_color)
        for spine in ax.spines.values():
            spine.set_color(text_color)

    # linear function
    x = np.linspace(-10, 10, 400)
    y = 2 * x + 1
    ax1.plot(x, y, color=palette["color1"], linewidth=2)
    ax1.set_title("Linear Programming", color=text_color, fontsize=14)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # function including a jump
    x_left = np.linspace(-10, -0.01, 200)
    x_right = np.linspace(0, 10, 200)
    y_left = 2 * x_left + 1
    y_right = 2 * x_right + 1 + 5

    ax2.plot(x_left, y_left, color=palette["color1"], linewidth=2)
    ax2.plot(x_right, y_right, color=palette["color3"], linewidth=2)

    # setting maker for the jump
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

    # save the plot
    if mode == "dark":

        plt.savefig("lin_vs_mixed_int_plot_dark.png")
    if mode == "light":

        plt.savefig("lin_vs_mixed_int_plot_light.png")


def draw_timeline(mode="dark", savefig_filename=None):
    """
    draws timeline for the multiperiod icon
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

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(
        left=False, bottom=False, labelbottom=False, labelleft=False
    )

    years = list(range(2020, 2031))

    # draw line
    ax.plot(
        [years[0], years[-1]], [0, 0], color=palette["color1"], linewidth=2
    )

    # set markings for every year
    for i, year in enumerate(years):
        ax.plot(year, 0, marker="o", markersize=8, color=palette["color3"])
        ax.text(
            year,
            -0.3,
            str(year),
            ha="center",
            va="top",
            color=text_color,
            fontsize=10,
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

    # Set title
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

    # save png
    if mode == "dark":

        plt.savefig("timeline_dark.png")
    if mode == "light":

        plt.savefig("timeline_light.png")


def plot_dispatch_invest(csv_path, mode="dark"):
    """
    draws a demand timeseries next to an bar plot symbolizing the investment decisions
    """

    df = pd.read_csv(csv_path)

    if "Time" not in df.columns:
        df["Time"] = pd.date_range(
            start="2020-01-01", periods=len(df), freq="H"
        )

    if mode.lower() == "dark":
        palette = dark_palette
        bg_color = "#121212"
        text_color = "#FFFFFF"
    else:
        palette = light_palette
        bg_color = "#FFFFFF"
        text_color = "#000000"

    # create two subplots
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor(bg_color)

    ax1 = axs[0]
    ax1.set_facecolor(bg_color)
    for spine in ax1.spines.values():
        spine.set_color(text_color)
    ax1.tick_params(colors=text_color, labelleft=False)

    # draw dispatch timeseries
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

    avg_pv = df["pv"].mean() if "pv" in df.columns else 0
    avg_wind = df["wind"].mean() if "wind" in df.columns else 0
    avg_heatpump = 0.3
    avg_solarthermie = 0.09

    labels = ["PV", "Wind", "Heat Pump", "Solarthermie"]
    values = [avg_pv, avg_wind, avg_heatpump, avg_solarthermie]

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
    ax2.tick_params(colors=text_color, labelleft=False)

    bars = ax2.bar(
        labels, values, color=bar_colors, edgecolor=text_color, linewidth=1.5
    )

    ax2.set_title("Investment Technology Sizes", color=text_color, fontsize=14)
    ax2.set_ylabel("Average Value", color=text_color, fontsize=14)

    fig.suptitle(
        "Dispatch vs. Invest-Optimization", color=text_color, fontsize=16
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # save plots
    if mode == "dark":

        plt.savefig("plot_dispatch_invest_dark.png")
    if mode == "light":

        plt.savefig("plot_dispatch_invest_light.png")


# uncomment he needed funczion to redraw the icons

# draw_lin_vs_mixed_int('light')
# draw_lin_vs_mixed_int('dark')

# draw_timeline("dark")  # Speichert als "timeline_dark.png"
# draw_timeline("light")  # Speichert als "timeline_light.png"

file_name = os.path.realpath(
    os.path.join(
        __file__,
        "..",
        "..",
        "..",
        "..",
        "tests/test_outputlib/input_data.csv",
    )
)
plot_dispatch_invest(file_name, mode="light")
plot_dispatch_invest(file_name, mode="dark")
