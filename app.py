import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Page Configuration - Mobile First
st.set_page_config(
    page_title="3-Point Targeting",
    page_icon="🎳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM MOBILE STYLING ---
st.markdown(
    """
    <style>
    /* Style container cards */
    [data-testid="stForm"], [data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
    /* Compact headers */
    h3 {
        margin-top: 0rem !important;
        padding-bottom: 0.25rem !important;
        font-size: 1.15rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DEFAULT VALUES / SESSION STATE INITIALIZATION ---
if "arrow_target" not in st.session_state:
    st.session_state.arrow_target = 15.0
if "focal_target" not in st.session_state:
    st.session_state.focal_target = 9.0
if "breakpoint_dist" not in st.session_state:
    st.session_state.breakpoint_dist = 42.0
if "slide_foot_offset" not in st.session_state:
    st.session_state.slide_foot_offset = 5.0
if "true_scale" not in st.session_state:
    st.session_state.true_scale = False

# --- 1. INPUT CONTROLS ---
st.subheader("Targets")

with st.container(border=True):
    st.number_input(
        "Target at Arrows (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=1.0,
        key="arrow_target",
        help="Distance = 15 feet from foul line",
    )

    st.number_input(
        "Focal Target at Pins (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=1.0,
        key="focal_target",
        help="Target at 60 feet. e.g., Board 9 = Center of 6-Pin",
    )

    st.slider(
        "Breakpoint Distance (Feet)",
        min_value=30.0,
        max_value=55.0,
        step=1.0,
        key="breakpoint_dist",
        help="Distance down the lane where the oil ends / ball hooks.",
    )

    st.slider(
        "Inside Foot Offset (Boards)",
        min_value=3.0,
        max_value=7.0,
        step=1.0,
        key="slide_foot_offset",
        help="Standard distance from inside of sliding foot to ball laydown is 5 boards.",
    )

# --- CALCULATIONS ---
board_diff = st.session_state.arrow_target - st.session_state.focal_target
laydown_offset = board_diff / 3.0
laydown_board = st.session_state.arrow_target + laydown_offset
slide_board = laydown_board + st.session_state.slide_foot_offset

slope = (st.session_state.focal_target - laydown_board) / 60.0
breakpoint_board = laydown_board + (slope * st.session_state.breakpoint_dist)

# --- 2. FULL TRAJECTORY RESULTS ---
st.success(
    f"Slide **{slide_board:.1f}** ➔ "
    f"Laydown **{laydown_board:.1f}** ➔ "
    f"Arrow **{st.session_state.arrow_target:.0f}** ➔ "
    f"Break **{breakpoint_board:.1f}** ➔ "
    f"Focal **{st.session_state.focal_target:.0f}**"
)

st.markdown("---")

# --- 3. VISUAL LANE DIAGRAM ---
st.subheader("Lane Trajectory")

# Scale Toggle
st.toggle(
    "True Spatial Ratio (1:1 Geometry)",
    key="true_scale",
    help="When enabled, renders exact 60ft x 41.5in physical proportions (extremely thin on phones).",
)


def draw_lane(true_scale=False):
    # Width of 1 board in feet = (41.5 inches / 39 boards) / 12 inches per foot
    BOARD_TO_FEET = (41.5 / 39.0) / 12.0

    fig, ax = plt.subplots(
        figsize=(10, 2.5 if true_scale else 3.8), facecolor="#111827"
    )
    ax.set_facecolor("#1f2937")

    if true_scale:
        # Physical feet dimensions
        y_min, y_max = 0.0, 40.0 * BOARD_TO_FEET
        ax.set_ylim(y_min, y_max)
        ax.set_xlim(-2, 62)
        ax.set_aspect("equal")  # 1:1 Physical Spatial Geometry

        def b2y(b):
            return b * BOARD_TO_FEET

    else:
        # Board units dimensions (Exaggerated board width for readability)
        ax.set_ylim(0, 40)
        ax.set_xlim(-2, 62)

        def b2y(b):
            return b

    # Fill Lane Wood Area (Boards 1 to 39)
    ax.axhspan(
        b2y(1), b2y(39), xmin=2 / 64, xmax=62 / 64, color="#d97706", alpha=0.15
    )

    # Draw Gutters
    ax.axhspan(b2y(0), b2y(1), color="#374151", alpha=0.8)
    ax.axhspan(b2y(39), b2y(40), color="#374151", alpha=0.8)

    # Foul Line (0 ft)
    ax.axvline(0, color="#ef4444", linewidth=2.0, label="Foul Line")

    # Arrows (15 ft) - Key arrows at boards 5, 10, 15, 20, 25, 30, 35
    ax.axvline(15, color="#f59e0b", linestyle="--", alpha=0.3)
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(15, b2y(b), "^", color="#f59e0b", markersize=5 if not true_scale else 3)

    # Breakpoint Distance Line
    ax.axvline(
        st.session_state.breakpoint_dist,
        color="#3b82f6",
        linestyle=":",
        alpha=0.5,
    )

    # Head Pin Position (60 ft, Board 20)
    ax.plot(
        60,
        b2y(20),
        "o",
        color="#ffffff",
        markersize=7 if not true_scale else 4,
        markeredgecolor="#ef4444",
    )

    # --- TRAJECTORY LINES ---
    x_oil = [0, st.session_state.breakpoint_dist]
    y_oil = [b2y(laydown_board), b2y(breakpoint_board)]

    x_hook = [st.session_state.breakpoint_dist, 60]
    y_hook = [b2y(breakpoint_board), b2y(st.session_state.focal_target)]

    # Oil/Skid Phase Trajectory Line
    ax.plot(x_oil, y_oil, color="#60a5fa", linewidth=2.0, label="Skid Phase")

    # Hook Phase Trajectory Line
    ax.plot(
        x_hook,
        y_hook,
        color="#f43f5e",
        linewidth=2.0,
        linestyle="--",
        label="Hook Phase",
    )

    # Key Target Marker Points
    ms = 6 if not true_scale else 3.5
    ax.plot(0, b2y(laydown_board), "s", color="#38bdf8", markersize=ms, label="Laydown")
    ax.plot(
        15,
        b2y(st.session_state.arrow_target),
        "D",
        color="#fbbf24",
        markersize=ms,
        label="Arrow",
    )
    ax.plot(
        st.session_state.breakpoint_dist,
        b2y(breakpoint_board),
        "X",
        color="#a855f7",
        markersize=ms + 1,
        label="Breakpoint",
    )
    ax.plot(
        60,
        b2y(st.session_state.focal_target),
        "o",
        color="#22c55e",
        markersize=ms + 1,
        label="Focal Target",
    )

    # Styling Axes
    ax.set_xlabel("Distance Down Lane (Feet)", color="#9ca3af", fontsize=9)
    ax.set_ylabel(
        "Width (Feet)" if true_scale else "Board Number (1-39)",
        color="#9ca3af",
        fontsize=9,
    )
    ax.tick_params(colors="#9ca3af", labelsize=8)

    # Set Y-Ticks
    if true_scale:
        ax.set_yticks([b2y(1), b2y(10), b2y(20), b2y(30), b2y(39)])
        ax.set_yticklabels(["B1", "B10", "B20", "B30", "B39"])
    else:
        ax.set_yticks([1, 10, 20, 30, 39])

    ax.set_xticks([0, 15, 30, st.session_state.breakpoint_dist, 60])

    ax.grid(True, linestyle=":", alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#374151")

    # Legend Alignment
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.35 if true_scale else -0.22),
        ncol=5,
        frameon=False,
        fontsize=8,
        labelcolor="#e5e7eb",
    )

    plt.tight_layout()
    return fig


st.pyplot(draw_lane(st.session_state.true_scale), use_container_width=True)

st.markdown("---")

# --- 4. FOCAL PIN BOARD GUIDE ---
st.markdown(
    """
    > **10 Pin:** 6 — **4** — 2  
    > **6 Pin:** 11 — **9** — 7  
    > **3 Pin:** 16 — **14** — 12
    """
)
