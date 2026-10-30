import math
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
if "breakpoint_board" not in st.session_state:
    st.session_state.breakpoint_board = 5.0
if "breakpoint_dist" not in st.session_state:
    st.session_state.breakpoint_dist = 45.0
if "slide_foot_offset" not in st.session_state:
    st.session_state.slide_foot_offset = 5.0

# --- PRESET SELECTION CALLBACK ---
def apply_preset():
    preset = st.session_state.preset_selection
    if preset == "Fresh House Benchmark (15 → BP5 @ 45')":
        st.session_state.arrow_target = 15.0
        st.session_state.breakpoint_board = 5.0
        st.session_state.breakpoint_dist = 45.0
    elif preset == "Outside Friction Line (13 → BP5 @ 45')":
        st.session_state.arrow_target = 13.0
        st.session_state.breakpoint_board = 5.0
        st.session_state.breakpoint_dist = 45.0
    elif preset == "First Transition Inside (17 → BP5 @ 45')":
        st.session_state.arrow_target = 17.0
        st.session_state.breakpoint_board = 5.0
        st.session_state.breakpoint_dist = 45.0
    elif preset == "Deep Inside Swing Line (19 → BP5 @ 45')":
        st.session_state.arrow_target = 19.0
        st.session_state.breakpoint_board = 5.0
        st.session_state.breakpoint_dist = 45.0
    elif preset == "Heavy Oil / Major Breakdown (21 → BP5 @ 45')":
        st.session_state.arrow_target = 21.0
        st.session_state.breakpoint_board = 5.0
        st.session_state.breakpoint_dist = 45.0

# --- 1. QUICK PRESETS & INPUT CONTROLS ---
st.subheader("Quick Presets")
st.selectbox(
    "Select a Common Benchmark Line:",
    options=[
        "Custom Inputs",
        "Fresh House Benchmark (15 → BP5 @ 45')",
        "Outside Friction Line (13 → BP5 @ 45')",
        "First Transition Inside (17 → BP5 @ 45')",
        "Deep Inside Swing Line (19 → BP5 @ 45')",
        "Heavy Oil / Major Breakdown (21 → BP5 @ 45')",
    ],
    key="preset_selection",
    on_change=apply_preset,
    help="Selecting a preset instantly sets your arrow target, breakpoint, and distance.",
)

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
            min_value=0.0,
            max_value=7.0,
            step=1.0,
            key="slide_foot_offset",
            help="Distance from inside of sliding foot to ball laydown.",
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
        return "6-Pin Right
