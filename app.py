import matplotlib.patches as patches
import matplotlib.pyplot as plt
import streamlit as st

# Page Configuration
st.set_page_config(page_title="3-Point Targeting Calculator", layout="wide")

st.title(" bowling 3-Point Targeting & Lane Calculator")
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
    help="Board 9 = Center of 6-Pin (Right), Board 31 = Center of 4-Pin (Left)",
)

slide_foot_offset = st.sidebar.slider(
    "Inside Foot Offset (Boards)",
    min_value=3.0,
    max_value=7.0,
    value=5.0,
    step=0.5,
    help="Standard offset from inside sliding foot to ball laydown is 5 boards.",
)

# --- CALCULATIONS ---
board_diff = arrow_target - focal_target
laydown_offset = board_diff / 3.0
laydown_board = arrow_target + laydown_offset
slide_board = laydown_board + slide_foot_offset

# --- METRIC SUMMARY DISPLAY ---
st.subheader("Your Calculated Line")

col1, col2, col3, col4 = st.columns(4)
col1.metric("1. Slide Foot Board", f"{slide_board:.1f}")
col2.metric("2. Laydown Board", f"{laydown_board:.1f}")
col3.metric("3. Arrow Target", f"{arrow_target:.1f}")
col4.metric("4. Focal Target", f"{focal_target:.1f}")

st.info(
    f"**Full Line:** Slide **{slide_board:.1f}** ➔ Laydown **{laydown_board:.1f}** ➔ Arrow **{arrow_target:.1f}** ➔ Focal Point **{focal_target:.1f}**"
)

# --- VISUALIZATION FUNCTION ---
def plot_lane_trajectory(slide, laydown, arrow, focal):
    # USBC Dimensional Specs
    INCHES_PER_BOARD = 41.5 / 39.0
    FEET_PER_BOARD = INCHES_PER_BOARD / 12.0  # ~0.0887 ft/board

    lane_width_ft = 39 * FEET_PER_BOARD
    gutter_width_ft = 9.25 / 12.0

    # Board X-Position Helper (Board 1 = Far Right, Board 39 = Far Left)
    def b2x(board_num):
        return (39.0 - board_num) * FEET_PER_BOARD

    fig, ax = plt.subplots(figsize=(5, 11))

    # --- LANE STRUCTURE ---
    lane_bg = patches.Rectangle(
        (0, 0),
        lane_width_ft,
        60,
        linewidth=1.2,
        edgecolor="black",
        facecolor="#fdf6e7",
        zorder=1,
    )
    ax.add_patch(lane_bg)

    approach_bg = patches.Rectangle(
        (-gutter_width_ft, -12),
        lane_width_ft + (2 * gutter_width_ft),
        12,
        linewidth=1,
        edgecolor="gray",
        facecolor="#e6d7c3",
        alpha=0.6,
        zorder=1,
    )
    ax.add_patch(approach_bg)

    r_gutter = patches.Rectangle(
        (-gutter_width_ft, 0),
        gutter_width_ft,
        60,
        facecolor="#788896",
        alpha=0.5,
        zorder=1,
    )
    l_gutter = patches.Rectangle(
        (lane_width_ft, 0),
        gutter_width_ft,
        60,
        facecolor="#788896",
        alpha=0.5,
        zorder=1,
    )
    ax.add_patch(r_gutter)
    ax.add_patch(l_gutter)

    ax.axhline(y=0, color="red", linewidth=2, zorder=3)
    ax.text(
        lane_width_ft / 2,
        0.5,
        "FOUL LINE",
        ha="center",
        va="bottom",
        fontsize=7,
        color="crimson",
        fontweight="bold",
    )

    # 60 ft line marker
    ax.axhline(y=60, color="black", linestyle="--", linewidth=1, zorder=3, alpha=0.5)
    ax.text(
        lane_width_ft / 2,
        59.2,
        "PIN DECK (60 FT)",
        ha="center",
        va="top",
        fontsize=7,
        color="black",
        fontweight="bold",
        alpha=0.6,
    )

    # --- TARGET DOTS & ARROWS ---
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(b2x(b), 7, "o", color="#8b5a2b", markersize=3, zorder=3)
        ax.plot(b2x(b), 15, "^", color="#8b5a2b", markersize=5, zorder=3)

    # --- TRAJECTORY LINE ---
    x_slide = b2x(slide)
    x_laydown = b2x(laydown)
    x_arrow = b2x(arrow)
    x_focal = b2x(focal)

    ax.plot(
        [x_laydown, x_arrow, x_focal],
        [0, 15, 60],
        color="#0055ff",
        linewidth=2.5,
        zorder=5,
    )

    # --- TARGET DOTS WITH IN-LINE BOARD CALLOUTS ---
    # 1. Slide Foot
    ax.scatter(
        [x_slide], [-2.0], color="black", marker="s", s=45, zorder=6
    )
    ax.annotate(
        f"Foot: B{slide:.1f}",
        (x_slide, -2.0),
        textcoords="offset points",
        xytext=(8, -3),
        fontsize=8,
        fontweight="bold",
        zorder=7,
    )

    # 2. Laydown
    ax.scatter([x_laydown], [0], color="crimson", s=55, zorder=6)
    ax.annotate(
        f"Laydown: B{laydown:.1f}",
        (x_laydown, 0),
        textcoords="offset points",
        xytext=(8, -3),
        fontsize=8,
        color="crimson",
        fontweight="bold",
        zorder=7,
    )

    # 3. Arrow
    ax.scatter([x_arrow], [15], color="darkorange", s=55, zorder=6)
    ax.annotate(
        f"Arrow: B{arrow:.1f}",
        (x_arrow, 15),
        textcoords="offset points",
        xytext=(8, -3),
        fontsize=8,
        color="darkorange",
        fontweight="bold",
        zorder=7,
    )

    # 4. Focal Point
    ax.scatter([x_focal], [60], color="green", s=55, zorder=6)
    ax.annotate(
        f"Focal: B{focal:.1f}",
        (x_focal, 60),
        textcoords="offset points",
        xytext=(8, -3),
        fontsize=8,
        color="green",
        fontweight="bold",
        zorder=7,
    )

    # --- AXIS FORMATTING & ASPECT RATIO LOCK ---
    ax.set_ylim(-6, 64)
    ax.set_xlim(-gutter_width_ft - 0.2, lane_width_ft + gutter_width_ft + 0.2)

    # Ticks setup (Board 1 on far Right, Board 39 on Left)
    board_ticks = [1, 5, 10, 15, 20, 25, 30, 35, 39]
    ax.set_xticks([b2x(b) for b in board_ticks])
    ax.set_xticklabels([str(b) for b in board_ticks])

    ax.set_xlabel("Board # (Right 1 ◄ 39 Left)", fontsize=9)
    ax.set_ylabel("Distance from Foul Line (Feet)", fontsize=9)
    ax.grid(True, which="both", linestyle=":", alpha=0.3)

    plt.tight_layout()
    return fig

# --- RENDER DIAGRAM ---
st.subheader("Lane Diagram with Live Board Readouts")
fig = plot_lane_trajectory(
    slide_board, laydown_board, arrow_target, focal_target
)
st.pyplot(fig)
