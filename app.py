import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def plot_lane_trajectory(slide, laydown, arrow, focal):
    # --- DIMENSIONAL CONSTANTS (USBC Specifications) ---
    # 39 boards total across a 41.5 inch wide lane -> ~1.064 inches per board
    INCHES_PER_BOARD = 41.5 / 39.0
    FEET_PER_BOARD = INCHES_PER_BOARD / 12.0  # ~0.0887 feet per board

    # Convert board numbers to actual feet from right gutter edge (Board 1 = 1 * FEET_PER_BOARD)
    y_laydown_ft = laydown * FEET_PER_BOARD
    y_arrow_ft = arrow * FEET_PER_BOARD
    y_focal_ft = focal * FEET_PER_BOARD
    y_slide_ft = slide * FEET_PER_BOARD

    lane_width_ft = 39 * FEET_PER_BOARD  # ~3.46 ft
    gutter_width_ft = 9.25 / 12.0  # 9.25 inches -> 0.77 ft

    # Create tall figure for realistic lane proportion
    fig, ax = plt.subplots(figsize=(4, 12))

    # --- DRAW LANE STRUCTURE ---
    # Lane wood bed
    lane_bg = patches.Rectangle(
        (0, 0),
        lane_width_ft,
        60,
        linewidth=1.5,
        edgecolor="black",
        facecolor="#f5e6ca",
        zorder=1,
    )
    ax.add_patch(lane_bg)

    # Approach Area (-15 ft to 0 ft)
    approach_bg = patches.Rectangle(
        (-gutter_width_ft, -15),
        lane_width_ft + (2 * gutter_width_ft),
        15,
        linewidth=1,
        edgecolor="gray",
        facecolor="#d2b48c",
        alpha=0.5,
        zorder=1,
    )
    ax.add_patch(approach_bg)

    # Gutters
    r_gutter = patches.Rectangle(
        (-gutter_width_ft, 0),
        gutter_width_ft,
        60,
        facecolor="#708090",
        alpha=0.6,
        zorder=1,
    )
    l_gutter = patches.Rectangle(
        (lane_width_ft, 0),
        gutter_width_ft,
        60,
        facecolor="#708090",
        alpha=0.6,
        zorder=1,
    )
    ax.add_patch(r_gutter)
    ax.add_patch(l_gutter)

    # Foul Line
    ax.axhline(y=0, color="red", linewidth=2.5, zorder=3, label="Foul Line")

    # Oil Pattern End Line (42 ft)
    ax.axhline(
        y=42,
        color="#008b8b",
        linestyle="--",
        linewidth=1,
        alpha=0.7,
        zorder=2,
        label="Pattern End (42 ft)",
    )

    # --- TARGET MARKINGS ---
    # 7-foot dots
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(
            b * FEET_PER_BOARD,
            7,
            "o",
            color="saddlebrown",
            markersize=3,
            zorder=3,
        )

    # 15-foot arrows (Rangefinders)
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(
            b * FEET_PER_BOARD,
            15,
            "^",
            color="saddlebrown",
            markersize=7,
            zorder=3,
        )

    # --- PIN DECK (AT 60 FT) ---
    # Pin coordinates (Board #, Distance ft)
    pin_locations = {
        "1": (20, 60.0),
        "2": (15, 60.866),
        "3": (25, 60.866),
        "4": (10, 61.732),
        "5": (20, 61.732),
        "6": (30, 61.732),
        "7": (5, 62.598),
        "8": (15, 62.598),
        "9": (25, 62.598),
        "10": (35, 62.598),
    }

    for p_num, (p_board, p_dist) in pin_locations.items():
        ax.plot(
            p_board * FEET_PER_BOARD,
            p_dist,
            "o",
            color="white",
            markeredgecolor="black",
            markersize=7,
            zorder=4,
        )

    # --- BALL TRAJECTORY LINE ---
    # Straight trajectory line extending from Laydown through Arrow to Pin Deck
    ax.plot(
        [y_laydown_ft, y_arrow_ft, y_focal_ft],
        [0, 15, 60],
        color="#0055ff",
        linewidth=2.5,
        label="Ball Path",
        zorder=5,
    )

    # Mark Key Targets
    ax.scatter(
        [y_laydown_ft],
        [0],
        color="crimson",
        s=60,
        zorder=6,
        label=f"Laydown ({laydown:.1f})",
    )
    ax.scatter(
        [y_arrow_ft],
        [15],
        color="orange",
        s=60,
        zorder=6,
        label=f"Arrow Target ({arrow:.1f})",
    )
    ax.scatter(
        [y_focal_ft],
        [60],
        color="green",
        s=60,
        zorder=6,
        label=f"Focal Point ({focal:.1f})",
    )

    # Foot Position at Foul Line (-0.5 ft into approach)
    ax.scatter(
        [y_slide_ft],
        [-0.5],
        color="black",
        marker="s",
        s=50,
        zorder=6,
        label=f"Slide Foot ({slide:.1f})",
    )

    # --- AXIS & BOARD TICKS ---
    ax.set_ylim(-5, 64)
    ax.set_xlim(-gutter_width_ft - 0.2, lane_width_ft + gutter_width_ft + 0.2)

    # Secondary X-axis showing Board Numbers instead of feet
    board_ticks = [1, 5, 10, 15, 20, 25, 30, 35, 39]
    board_positions = [b * FEET_PER_BOARD for b in board_ticks]
    ax.set_xticks(board_positions)
    ax.set_xticklabels([str(b) for b in board_ticks])

    ax.set_xlabel("Lane Board Number (Right 1 ➔ Left 39)", fontsize=10)
    ax.set_ylabel("Distance from Foul Line (Feet)", fontsize=10)

    # Grid & Legend
    ax.grid(True, which="both", linestyle=":", alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=2)

    plt.tight_layout()
    return fig
