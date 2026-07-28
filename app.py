import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set page configuration
st.set_page_config(page_title="3-Point Targeting Calculator", layout="wide")

st.title("🎳 3-Point Targeting & Lane Calculator")
st.write(
    "Based on Del Warren's Kegel 3-Point Targeting System ($3:1$ Expansion Ratio)"
)

# --- SIDEBAR INPUTS ---
st.sidebar.header("Target Inputs")

arrow_target = st.sidebar.number_input(
    "Target at Arrows (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=15.0,
    step=0.5,
)

focal_target = st.sidebar.number_input(
    "Target at Pins / Focal Point (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=9.0,
    step=0.5,
    help="e.g., Center of 6-Pin = 9, Center of 10-Pin = 4, Headpin = 20",
)

slide_foot_offset = st.sidebar.slider(
    "Inside Foot Offset (Boards)",
    min_value=3.0,
    max_value=7.0,
    value=5.0,
    step=0.5,
    help="Standard distance from inside of sliding foot to ball laydown is 5 boards.",
)

# --- CALCULATIONS ---
board_diff = arrow_target - focal_target
laydown_offset = board_diff / 3.0
laydown_board = arrow_target + laydown_offset
slide_board = laydown_board + slide_foot_offset

# --- MAIN DISPLAY: CALCULATED LINE ---
st.subheader("Your Calculated Line")

col1, col2, col3, col4 = st.columns(4)
col1.metric("1. Slide Board (Foot)", f"{slide_board:.1f}")
col2.metric("2. Laydown Board", f"{laydown_board:.1f}")
col3.metric("3. Target Arrow", f"{arrow_target:.1f}")
col4.metric("4. Pin / Focal Target", f"{focal_target:.1f}")

st.info(
    f"**Full Line Summary:** Slide **{slide_board:.1f}** ➔ Laydown **{laydown_board:.1f}** ➔ Arrow **{arrow_target:.1f}** ➔ Pins **{focal_target:.1f}**"
)

# --- VISUALIZATION FUNCTION ---
def plot_lane_trajectory(slide, laydown, arrow, focal):
    # --- DIMENSIONAL CONSTANTS (USBC Specifications) ---
    INCHES_PER_BOARD = 41.5 / 39.0
    FEET_PER_BOARD = INCHES_PER_BOARD / 12.0  # ~0.0887 feet per board

    y_laydown_ft = laydown * FEET_PER_BOARD
    y_arrow_ft = arrow * FEET_PER_BOARD
    y_focal_ft = focal * FEET_PER_BOARD
    y_slide_ft = slide * FEET_PER_BOARD

    lane_width_ft = 39 * FEET_PER_BOARD  # ~3.46 ft
    gutter_width_ft = 9.25 / 12.0  # 9.25 inches -> 0.77 ft

    fig, ax = plt.subplots(figsize=(4, 11))

    # --- DRAW LANE STRUCTURE ---
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

    ax.axhline(y=0, color="red", linewidth=2.5, zorder=3, label="Foul Line")
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
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(
            b * FEET_PER_BOARD,
            7,
            "o",
            color="saddlebrown",
            markersize=3,
            zorder=3,
        )
        ax.plot(
            b * FEET_PER_BOARD,
            15,
            "^",
            color="saddlebrown",
            markersize=6,
            zorder=3,
        )

    # --- PIN DECK AT 60 FT ---
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
            markersize=6,
            zorder=4,
        )

    # --- TRAJECTORY LINE ---
    ax.plot(
        [y_laydown_ft, y_arrow_ft, y_focal_ft],
        [0, 15, 60],
        color="#0055ff",
        linewidth=2.5,
        label="Ball Path",
        zorder=5,
    )

    ax.scatter(
        [y_laydown_ft],
        [0],
        color="crimson",
        s=50,
        zorder=6,
        label=f"Laydown ({laydown:.1f})",
    )
    ax.scatter(
        [y_arrow_ft],
        [15],
        color="orange",
        s=50,
        zorder=6,
        label=f"Arrow ({arrow:.1f})",
    )
    ax.scatter(
        [y_focal_ft],
        [60],
        color="green",
        s=50,
        zorder=6,
        label=f"Focal ({focal:.1f})",
    )

    ax.scatter(
        [y_slide_ft],
        [-1.0],
        color="black",
        marker="s",
        s=40,
        zorder=6,
        label=f"Slide Foot ({slide:.1f})",
    )

    # --- AXES & LABELS ---
    ax.set_ylim(-5, 64)
    ax.set_xlim(-gutter_width_ft - 0.2, lane_width_ft + gutter_width_ft + 0.2)

    board_ticks = [1, 5, 10, 15, 20, 25, 30, 35, 39]
    board_positions = [b * FEET_PER_BOARD for b in board_ticks]
    ax.set_xticks(board_positions)
    ax.set_xticklabels([str(b) for b in board_ticks])

    ax.set_xlabel("Board Number (Right 1 ➔ Left 39)", fontsize=9)
    ax.set_ylabel("Distance from Foul Line (Feet)", fontsize=9)

    ax.grid(True, which="both", linestyle=":", alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=8)

    plt.tight_layout()
    return fig

# --- RENDER DIAGRAM ---
st.subheader("Scaled Lane Diagram")
fig = plot_lane_trajectory(
    slide_board, laydown_board, arrow_target, focal_target
)
st.pyplot(fig)
