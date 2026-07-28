import streamlit as st

# Page Configuration
st.set_page_config(page_title="3-Point Targeting Calculator", layout="centered")

st.title("3-Point Targeting & Breakpoint Calculator")
st.caption(
    "Based on Del Warren's Kegel 3-Point Targeting System ($3:1$ Expansion Ratio)"
)

st.markdown("---")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Target Inputs")

arrow_target = st.sidebar.number_input(
    "Target at Arrows (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=15.0,
    step=0.5,
    help="Distance = 15 feet from foul line",
)

focal_target = st.sidebar.number_input(
    "Focal Target at Pins (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=9.0,
    step=0.5,
    help="Target at 60 feet. e.g., Center of 6-Pin = 9, Center of 10-Pin = 4, Headpin = 20",
)

st.sidebar.header("2. Breakpoint & Stance")

breakpoint_dist = st.sidebar.slider(
    "Breakpoint Distance (Feet)",
    min_value=30.0,
    max_value=55.0,
    value=40.0,
    step=1.0,
    help="Distance down the lane where the oil ends / ball hooks.",
)

slide_foot_offset = st.sidebar.slider(
    "Inside Foot Offset (Boards)",
    min_value=3.0,
    max_value=7.0,
    value=5.0,
    step=0.5,
    help="Standard distance from inside of sliding foot to ball laydown is 5 boards.",
)

# --- CALCULATIONS ---
# 1. Standard Del Warren 3-Point Formula
board_diff = arrow_target - focal_target
laydown_offset = board_diff / 3.0
laydown_board = arrow_target + laydown_offset
slide_board = laydown_board + slide_foot_offset

# 2. Linear Interpolation for Breakpoint
# Trajectory line goes from (0 ft, laydown) to (15 ft, arrow) to (60 ft, focal)
# Slope (boards per foot) = (Focal Board - Laydown Board) / 60 ft
slope = (focal_target - laydown_board) / 60.0
breakpoint_board = laydown_board + (slope * breakpoint_dist)

# --- DISPLAY RESULTS ---
st.subheader("Your Line Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Slide Foot", f"Board {slide_board:.1f}")
col2.metric("Laydown (Foul Line)", f"Board {laydown_board:.1f}")
col3.metric("Arrow (15 ft)", f"Board {arrow_target:.1f}")

st.markdown("---")

# Breakpoint Highlights
st.subheader("Breakpoint Location")

st.success(
    f"At **{breakpoint_dist:.0f} feet** down the lane, your ball crosses **Board {breakpoint_board:.1f}**"
)

# Breakdown Card
with st.expander("See Complete Trajectory Milestones"):
    st.write(
        f"""
    * **Foul Line ($0\\text{{ ft}}$):** Laydown on **Board {laydown_board:.1f}** *(Feet on {slide_board:.1f})*
    * **Target Arrows ($15\\text{{ ft}}$):** Target **Board {arrow_target:.1f}**
    * **Breakpoint ({breakpoint_dist:.0f}$\\text{{ ft}}$):** Crosses **Board {breakpoint_board:.1f}**
    * **Pin Deck ($60\\text{{ ft}}$):** Hits **Board {focal_target:.1f}**
    """
    )
