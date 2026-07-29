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


# --- 4. FOCAL PIN BOARD GUIDE ---
st.markdown(
    """
    > **10 Pin:** 6 — **4** — 2  
    > **6 Pin:** 11 — **9** — 7  
    > **3 Pin:** 16 — **14** — 12
    """
)
