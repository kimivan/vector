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
    /* Remove unnecessary top padding for mobile viewports */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }
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
    unsafe_allow_javascript=True,
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
st.subheader("🎯 Shot Targets & Settings")

with st.container(border=True):
    st.number_input(
        "Arrow Target (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=1.0,
        key="arrow_target",
        help="Target at 15 feet from foul line",
    )

    st.number_input(
        "Focal Target at Pins (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=1.0,
        key="focal_target",
        help="Target at 60 feet (e.g., Center of 6-Pin = Board 9)",
    )

    st.slider(
        "Breakpoint Distance (Feet)",
        min_value=30.0,
        max_value=55.0,
        step=1.0,
        key="breakpoint_dist",
        help="Distance down the lane where oil ends",
    )

    st.slider(
        "Inside Foot Offset (Boards)",
        min_value=3.0,
        max_value=7.0,
        step=1.0,
        key="slide_foot_offset",
        help="Distance from inside sliding foot to ball laydown (Default: 5)",
    )

# --- CALCULATIONS ---
board_diff = st.session_state.arrow_target - st.session_state.focal_target
laydown_offset = board_diff / 3.0
laydown_board = st.session_state.arrow_target + laydown_offset
slide_board = laydown_board + st.session_state.slide_foot_offset

slope = (st.session_state.focal_target - laydown_board) / 60.0
breakpoint_board = laydown_board + (slope * st.session_state.breakpoint_dist)

# --- 2. TRAJECTORY RESULT CARD ---
st.subheader("📍 Target Line")

st.success(
    f"Slide **{slide_board:.1f}** ➔ "
    f"Laydown **{laydown_board:.1f}** ➔ "
    f"Arrow **{st.session_state.arrow_target:.0f}** ➔ "
    f"Break **{breakpoint_board:.1f}** (@{st.session_state.breakpoint_dist:.0f}') ➔ "
    f"Focal **{st.session_state.focal_target:.0f}**"
)

# --- 3. PIN BOARD REFERENCE GUIDE ---
with st.container(border=True):
    st.markdown(
        """
        **📌 Focal Pin Board Guide** *(Left — Center — Right)*
        * **10 Pin:** `6` — **`4`** — `2`
        * **6 Pin:** `11` — **`9`** — `7`
        * **3 Pin:** `16` — **`14`** — `12`
        """
    )
