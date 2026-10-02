import math
import streamlit as st

# Page Configuration
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
    [data-testid="stForm"], [data-testid="stVerticalBlock"] > div > div[data-testid="stBlock"] {
        border-radius: 12px;
    }
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

# --- INPUT CONTROLS ---
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

# --- PIN REFERENCE HELPER ---
def get_focal_description(board):
    b = round(board, 1)
    if b >= 19.5:
        return "Headpin / Pocket (20+)"
    elif 16.5 <= b < 19.5:
        return "3-Pin Left Edge (17)"
    elif 14.5 <= b < 16.5:
        return "3-Pin Center (15)"
    elif 12.5 <= b < 14.5:
        return "3-Pin Right Edge (13)"
    elif 11.5 <= b < 12.5:
        return "6-Pin Left Base (12)"
    elif 10.5 <= b < 11.5:
        return "6-Pin Left Shoulder (11)"
    elif 9.5 <= b < 10.5:
        return "6-Pin Base Center (10)"
    elif 8.5 <= b < 9.5:
        return "6-Pin Center (9)"
    elif 7.5 <= b < 8.5:
        return "6-Pin Right Base (8)"
    elif 6.5 <= b < 7.5:
        return "10-Pin Left Edge (7)"
    elif 5.5 <= b < 6.5:
        return "10-Pin Left Shoulder (6)"
    elif 4.5 <= b < 5.5:
        return "10-Pin Base Left (5)"
    elif 3.5 <= b < 4.5:
        return "10-Pin Center (4)"
    elif 2.5 <= b < 3.5:
        return "10-Pin Base Right (3)"
    elif 1.5 <= b < 2.5:
        return "10-Pin Right Shoulder (2)"
    else:
        return "Gutter (< 2)"

# --- CALCULATION FUNCTION ---
def calculate_line(arrow_board, break_board, break_dist, slide_gap):
    board_delta = arrow_board - break_board
    dist_delta = break_dist - 15.0
    
    foul_line_offset = (board_delta / dist_delta) * 15.0
    laydown_board = arrow_board + foul_line_offset
    slide_board = laydown_board + slide_gap
    
    focal_board = laydown_board + ((break_board - laydown_board) / break_dist) * 60.0
    
    board_width_ft = 0.0889
    board_diff_ft = (break_board - laydown_board) * board_width_ft
    launch_angle = math.degrees(math.atan(board_diff_ft / break_dist))
    
    return {
        "slide": slide_board,
        "arrow": arrow_board,
        "focal": focal_board,
        "angle": launch_angle,
        "landmark": get_focal_description(focal_board),
    }

# Compute 3 lines
current_arrow = st.session_state.arrow_target
bp_board = st.session_state.breakpoint_board
bp_dist = st.session_state.breakpoint_dist
gap = st.session_state.slide_foot_offset

line_current = calculate_line(current_arrow, bp_board, bp_dist, gap)
line_move_1 = calculate_line(current_arrow + 1.0, bp_board, bp_dist, gap)
line_move_2 = calculate_line(current_arrow + 2.0, bp_board, bp_dist, gap)

# --- RESULTS DISPLAY ---
st.subheader("Trajectory & Moves")

col_curr, col_m1, col_m2 = st.columns(3)

with col_curr:
    with st.container(border=True):
        st.markdown("### Current Line")
        st.metric("Slide Board", f"{line_current['slide']:.1f}")
        st.metric("Arrow Board", f"{line_current['arrow']:.0f}")
        st.metric("Focal Board (60')", f"{line_current['focal']:.1f}")
        st.caption(f"🎯 **Target:** {line_current['landmark']}")
        st.metric("Launch Angle", f"{line_current['angle']:.2f}°")

with col_m1:
    with st.container(border=True):
        st.markdown("### Move +1 Left")
        st.metric("Slide Board", f"{line_move_1['slide']:.1f}")
        st.metric("Arrow Board", f"{line_move_1['arrow']:.0f}")
        st.metric("Focal Board (60')", f"{line_move_1['focal']:.1f}")
        st.caption(f"🎯 **Target:** {line_move_1['landmark']}")
        st.metric("Launch Angle", f"{line_move_1['angle']:.2f}°")

with col_m2:
    with st.container(border=True):
        st.markdown("### Move +2 Left")
        st.metric("Slide Board", f"{line_move_2['slide']:.1f}")
        st.metric("Arrow Board", f"{line_move_2['arrow']:.0f}")
        st.metric("Focal Board (60')", f"{line_move_2['focal']:.1f}")
        st.caption(f"🎯 **Target:** {line_move_2['landmark']}")
        st.metric("Launch Angle", f"{line_move_2['angle']:.2f}°")

# --- REFERENCE IMAGE EXPANDER ---
st.write("")
with st.expander("📸 **View Pin Deck Focal Board Diagram**", expanded=False):
    # Save your reference image as 'focal_map.jpg' or 'focal_map.png' in the same folder
    st.image("focal_map.jpg", caption="Quiet Eye / 3-Point Targeting Focal Landmarks at 60 Feet", use_container_width=True)
