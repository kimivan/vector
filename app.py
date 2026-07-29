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


def draw_lane():
    fig, ax = plt.subplots(figsize=(10, 3.5), facecolor="#111827")
    ax.set_facecolor("#1f2937")

    # Lane boundaries (0 to 60 ft, 1 to 39 boards)
    ax.set_xlim(-2, 62)
    ax.set_ylim(0, 40)

    # Fill Lane Wood Background
    ax.axhspan(1, 39, xmin=2 / 64, xmax=62 / 64, color="#d97706", alpha=0.15)

    # Draw Gutters
    ax.axhspan(0, 1, color="#374151", alpha=0.8)
    ax.axhspan(39, 40, color="#374151", alpha=0.8)

    # Key Landmarks
    # Foul Line (0 ft)
    ax.axvline(0, color="#ef4444", linewidth=2.5, label="Foul Line")

    # Arrows (15 ft) - Key arrow markers at boards 5, 10, 15, 20, 25, 30, 35
    ax.axvline(15, color="#f59e0b", linestyle="--", alpha=0.4)
    for b in [5, 10, 15, 20, 25, 30, 35]:
        ax.plot(15, b, "^", color="#f59e0b", markersize=6)

    # Oil Pattern End / Breakpoint Marker
    ax.axvline(
        st.session_state.breakpoint_dist,
        color="#3b82f6",
        linestyle=":",
        alpha=0.6,
    )

    # Head Pin Position (60 ft, Board 20)
    ax.plot(60, 20, "o", color="#ffffff", markersize=8, markeredgecolor="#ef4444")

    # --- TRAJECTORY LINE ---
    x_oil = [0, st.session_state.breakpoint_dist]
    y_oil = [laydown_board, breakpoint_board]

    x_hook = [st.session_state.breakpoint_dist, 60]
    y_hook = [breakpoint_board, st.session_state.focal_target]

    # Oil Trajectory (Straight)
    ax.plot(x_oil, y_oil, color="#60a5fa", linewidth=2.5, label="Skid Phase")

    # Hook Trajectory (Backend)
    ax.plot(
        x_hook,
        y_hook,
        color="#f43f5e",
        linewidth=2.5,
        linestyle="--",
        label="Hook Phase",
    )

    # Key Target Points
    ax.plot(0, laydown_board, "s", color="#38bdf8", markersize=6, label="Laydown")
    ax.plot(
        15,
        st.session_state.arrow_target,
        "D",
        color="#fbbf24",
        markersize=6,
        label="Arrow",
    )
    ax.plot(
        st.session_state.breakpoint_dist,
        breakpoint_board,
        "X",
        color="#a855f7",
        markersize=7,
        label="Breakpoint",
    )
    ax.plot(
        60,
        st.session_state.focal_target,
        "o",
        color="#22c55e",
        markersize=7,
        label="Focal Target",
    )

    # Axis Labels & Styling
    ax.set_xlabel("Distance Down Lane (Feet)", color="#9ca3af", fontsize=9)
    ax.set_ylabel("Board Number (1 to 39)", color="#9ca3af", fontsize=9)
    ax.tick_params(colors="#9ca3af", labelsize=8)

    # Invert Y axis so Board 1 (Right Gutter for Righties) is on the bottom
    ax.set_yticks([1, 10, 20, 30, 39])
    ax.set_xticks([0, 15, 30, st.session_state.breakpoint_dist, 60])

    # Styling grid & frame
    ax.grid(True, linestyle=":", alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#374151")

    # Compact Dark Legend
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=5,
        frameon=False,
        fontsize=8,
        labelcolor="#e5e7eb",
    )

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
