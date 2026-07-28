import streamlit as st

# Page Configuration - Set to centered to optimize for mobile screens
st.set_page_config(
    page_title="3-Point Targeting", page_icon="🎳", layout="centered"
)

st.title("🎳 3-Point Targeting")
st.caption("Del Warren's Kegel 3-Point System ($3:1$ Ratio)")

# --- DEFAULT VALUES / SESSION STATE INITIALIZATION ---
if "arrow_target" not in st.session_state:
    st.session_state.arrow_target = 15.0
if "focal_target" not in st.session_state:
    st.session_state.focal_target = 9.0
if "breakpoint_dist" not in st.session_state:
    st.session_state.breakpoint_dist = 42.0
if "slide_foot_offset" not in st.session_state:
    st.session_state.slide_foot_offset = 5.0

# --- CALCULATIONS ---
board_diff = st.session_state.arrow_target - st.session_state.focal_target
laydown_offset = board_diff / 3.0
laydown_board = st.session_state.arrow_target + laydown_offset
slide_board = laydown_board + st.session_state.slide_foot_offset

slope = (st.session_state.focal_target - laydown_board) / 60.0
breakpoint_board = laydown_board + (slope * st.session_state.breakpoint_dist)

# --- 1. TOP RESULT CARD (ALWAYS VISIBLE AT TOP) ---
st.subheader("Your Calculated Line")

# Stack metrics into two mobile-friendly rows
row1_col1, row1_col2, row1_col3 = st.columns(3)
row1_col1.metric("1. Slide Foot", f"B{slide_board:.1f}")
row1_col2.metric("2. Laydown", f"B{laydown_board:.1f}")
row1_col3.metric("3. Arrow (15')", f"B{st.session_state.arrow_target:.1f}")

row2_col1, row2_col2 = st.columns(2)
row2_col1.metric(
    f"4. Break ({st.session_state.breakpoint_dist:.0f}')",
    f"B{breakpoint_board:.1f}",
)
row2_col2.metric("5. Focal (60')", f"B{st.session_state.focal_target:.1f}")

st.info(
    f"**Full Trajectory:**\n\n"
    f"Foot **{slide_board:.1f}** ➔ Laydown **{laydown_board:.1f}** ➔ Arrow **{st.session_state.arrow_target:.1f}** ➔ Break **{breakpoint_board:.1f}** (@{st.session_state.breakpoint_dist:.0f}') ➔ Pin **{st.session_state.focal_target:.1f}**"
)

st.markdown("---")

# --- 2. MAIN PAGE INPUT CONTROLS (EXPANDABLES FOR MOBILE SCROLLING) ---
st.subheader("Adjust Your Targets")

# INPUT GROUP 1: BOARD TARGETS
with st.expander("🎯 Target Boards (Arrow & Focal)", expanded=True):
    st.number_input(
        "Target at Arrows (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=0.5,
        key="arrow_target",
        help="Distance = 15 feet from foul line",
    )

    st.number_input(
        "Focal Target at Pins (Board #)",
        min_value=1.0,
        max_value=39.0,
        step=0.5,
        key="focal_target",
        help="Target at 60 feet. e.g., Board 9 = Center of 6-Pin",
    )

    # Quick Reference Box inside the expander
    st.markdown(
        """
        > **📌 Focal Pin Board Guide (Left - Center - Right):**
        > * **10 Pin:** 6 — **4** — 2
        > * **6 Pin:** 11 — **9** — 7
        > * **3 Pin:** 16 — **14** — 12
        """
    )

# INPUT GROUP 2: BREAKPOINT & STANCE
with st.expander("📏 Breakpoint & Stance Settings", expanded=False):
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
        step=0.5,
        key="slide_foot_offset",
        help="Standard distance from inside of sliding foot to ball laydown is 5 boards.",
    )
