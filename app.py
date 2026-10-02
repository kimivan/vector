import math
import streamlit as st

# Page Configuration - Wide Layout for Full Screen Width
st.set_page_config(
    page_title="3-Point Targeting",
    page_icon=" bowling ",
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
    st.session_state.arrow_target = 13.0
if "breakpoint_board" not in st.session_state:
    st.session_state.breakpoint_board = 8.0
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
            help="Target distance = 15 feet from foul line",
        )

        st.number_input(
            "Breakpoint Board #",
            min_value=1.0,
            max_value=39.0,
            step=1.0,
            key="breakpoint_board",
            help="Target board where the ball exits the oil pattern.",
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
            "Slide / Laydown Gap (Boards)",
            min_value=3.0,
            max_value=7.0,
            step=1.0,
            key="slide_foot_offset",
            help="Distance from inside of sliding foot to ball laydown (Standard is 5 boards).",
        )

# --- CALCULATIONS ---
# 1. Delta between target board and breakpoint board
board_delta = st.session_state.arrow_target - st.session_state.breakpoint_board

# 2. Delta between breakpoint distance and 15ft arrows
dist_delta = st.session_state.breakpoint_dist - 15.0

# 3. Ratio per foot multiplied by 15ft
foul_line_offset = (board_delta / dist_delta) * 15.0

# 4. Laydown Board (at 0 ft)
laydown_board = st.session_state.arrow_target + foul_line_offset

# 5. Slide Position
slide_board = laydown_board + st.session_state.slide_foot_offset

# 6. Focal Board Projection at 60 feet
focal_board = laydown_board + (
    (st.session_state.breakpoint_board - laydown_board)
    / st.session_state.breakpoint_dist
) * 60.0

# 7. Launch Angle (Degrees)
# 1 board = 1.067 inches = 0.0889 feet
board_width_ft = 0.0889
board_diff_ft = (
    st.session_state.breakpoint_board - laydown_board
) * board_width_ft
launch_angle = math.degrees(
    math.atan(board_diff_ft / st.session_state.breakpoint_dist)
)

# --- 2. TRAJECTORY & FOCAL METRICS RESULTS ---
st.success(
    f"Slide **{slide_board:.1f}** ➔ "
    f"Laydown **{laydown_board:.1f}** ➔ "
    f"Arrow **{st.session_state.arrow_target:.0f}** ➔ "
    f"Break **{st.session_state.breakpoint_board:.0f}** (@ {st.session_state.breakpoint_dist:.0f}')"
)

# Render Launch Angle and Focal Point Metrics
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    st.metric("Slide Board", f"{slide_board:.1f}")
with metric_col2:
    st.metric("Arrow Board", f"{st.session_state.arrow_target:.1f}")
with metric_col3:
    st.metric("Focal Board (60')", f"{focal_board:.1f}")
with metric_col4:
    st.metric("Launch Angle", f"{launch_angle:.2f}°")
