import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Page Configuration - Wide Layout for Full Screen Width
st.set_page_config(
    page_title="3-Point Targeting",
    page_icon="🎳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM STYLING ---
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

# --- 1. INPUT CONTROLS ---
st.subheader("Targets")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
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

# --- 3. VISUAL LANE DIAGRAM (TRUE 1:1 GEOMETRY) ---
st.subheader("Lane Trajectory (True Spatial Proportions)")


def draw_lane():
    # Board to Feet Conversion Factor: (41.5 inches / 39 boards) / 12 inches per foot
    BOARD_TO_FEET = (41.5 / 39.0) / 12.0

    fig, ax = plt.subplots(figsize=(15, 2.0), facecolor="#111827")
    ax.set_facecolor("#1f2937")

    # True 1:1 Physical Geometry
    ax.set_ylim(0.0, 40.0 * BOARD_TO_FEET)
    ax.set_xlim(-2, 62)
    ax.set_aspect("equal")

    def b2y(b):
        return b * BOARD_TO_FEET

    # Fill Lane Wood Area (Boards 1 to 39)
    ax.axhspan(
        b2y(1), b2y(39), xmin=2 / 64, xmax=62 / 64, color="#d97706", alpha=0.15
    )

    # Draw Gutters
    ax.axhspan(b2y(0), b2y(1), color="#374151", alpha=0.8)
    ax.axhspan(b2y(39), b2y(40), color="#374151", alpha=0.8)

    # Foul Line (0 ft)
    ax.axvline(0, color="#ef4444", linewidth=1.5)

    # Arrows Distance Indicator (15 ft)
    ax.axvline(15, color="#f59e0b", linestyle="--", alpha=0.3)

    # Breakpoint Distance Marker
    ax.axvline(
        st.session_state.breakpoint_dist,
        color="#3b82f6",
        linestyle=":",
        alpha=0.4,
    )

    # Head Pin Position (60 ft, Board 20)
    ax.plot(60, b2y(20), "o", color="#ffffff", markersize=4, markeredgecolor="#ef4444")

    # --- TRAJECTORY LINES ---
    x_oil = [0, st.session_state.breakpoint_dist]
    y_oil = [b2y(laydown_board), b2y(breakpoint_board)]

    x_hook = [st.session_state.breakpoint_dist, 60]
    y_hook = [b2y(breakpoint_board), b2y(st.session_state.focal_target)]

    # Skid Phase Line
    ax.plot(x_oil, y_oil, color="#60a5fa", linewidth=1.5)

    # Hook Phase Line
    ax.plot(x_hook, y_hook, color="#f43f5e", linewidth=1.5, linestyle="--")

    # Key Target Points
    ax.plot(0, b2y(laydown_board), "s", color="#38bdf8", markersize=3.5)
    ax.plot(15, b2y(st.session_state.arrow_target), "D", color="#fbbf24", markersize=3.5)
    ax.plot(st.session_state.breakpoint_dist, b2y(breakpoint_board), "X", color="#a855f7", markersize=4.5)
    ax.plot(60, b2y(st.session_state.focal_target), "o", color="#22c55e", markersize=4.5)

    # Axes Formatting
    ax.set_xlabel("Distance Down Lane (Feet)", color="#9ca3af", fontsize=8)
    ax.set_ylabel("Width (Feet)", color="#9ca3af", fontsize=8)
    ax.tick_params(colors="#9ca3af", labelsize=8)

    ax.set_yticks([b2y(1), b2y(10), b2y(20), b2y(30), b2y(39)])
    ax.set_yticklabels(["B1", "B10", "B20", "B30", "B39"])
    ax.set_xticks([0, 15, 30, st.session_state.breakpoint_dist, 60])

    ax.grid(True, linestyle=":", alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#374151")

    plt.tight_layout()
    return fig


st.pyplot(draw_lane(), use_container_width=True)

st.markdown("---")

# --- 4. FOCAL PIN BOARD GUIDE ---
st.markdown(
    """
    > **10 Pin:** 6 — **4** — 2  
    > **6 Pin:** 11 — **9** — 7  
    > **3 Pin:** 16 — **14** — 12
    """
)
