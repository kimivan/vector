import streamlit as st

# Page Configuration
st.set_page_config(page_title="3-Point Targeting Calculator", layout="centered")


st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Target Inputs")

arrow_target = st.sidebar.number_input(
    "Target at Arrows (Board #)",
    min_value=1,
    max_value=39,
    value=15,
    step=1,
    help="Distance = 15 feet from foul line",
)

focal_target = st.sidebar.number_input(
    "Focal Target at Pins (Board #)",
    min_value=1,
    max_value=39,
    value=9,
    step=1,
    help="Target at 60 feet. e.g., Center of 6-Pin = 9, Center of 10-Pin = 4, Headpin = 20",
)

st.sidebar.header("2. Breakpoint & Stance")

breakpoint_dist = st.sidebar.slider(
    "Breakpoint Distance (Feet)",
    min_value=30,
    max_value=55,
    value=40,
    step=1,
    help="Distance down the lane where the oil ends / ball hooks.",
)

slide_foot_offset = st.sidebar.slider(
    "Inside Foot Offset (Boards)",
    min_value=3,
    max_value=7,
    value=5,
    step=1,
    help="Standard distance from inside of sliding foot to ball laydown is 5 boards.",
)

# --- CALCULATIONS ---
# 1. Standard Del Warren 3-Point Formula
board_diff = arrow_target - focal_target
laydown_offset = board_diff / 3.0
laydown_board = arrow_target + laydown_offset
slide_board = laydown_board + slide_foot_offset

# 2. Linear Interpolation for Breakpoint
# Trajectory slope (boards per foot) = (Focal Board - Laydown Board) / 60 ft
slope = (focal_target - laydown_board) / 60.0
breakpoint_board = laydown_board + (slope * breakpoint_dist)

# --- DISPLAY RESULTS ---
st.subheader("Your Line Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("1. Slide Foot", f"{slide_board:.1f}")
col2.metric("2. Laydown", f"{laydown_board:.1f}")
col3.metric("3. Arrow (15')", f"{arrow_target}")
col4.metric(f"4. Break ({breakpoint_dist}')", f"{breakpoint_board:.1f}")
col5.metric("5. Focal (60')", f"{focal_target}")

st.markdown("---")

st.info(
    f"**Quick Reference:** Slide **{slide_board:.1f}** ➔ Laydown **{laydown_board:.1f}** ➔ Arrow **{arrow_target}** ➔ Breakpoint **{breakpoint_board:.1f}** @ {breakpoint_dist}' ➔ Pins **{focal_target}**"
)
