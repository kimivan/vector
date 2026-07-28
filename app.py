import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set page layout
st.set_page_config(page_title="3-Point Targeting Calculator", layout="wide")

st.title("🎳 3-Point Targeting & Lane Calculator")
st.write(
    "Based on Del Warren's Kegel 3-Point Targeting System ($3:1$ Expansion Ratio)"
)

# --- SIDEBAR INPUTS ---
st.sidebar.header("Target Inputs")

arrow_target = st.sidebar.number_input(
    "Target at Arrows (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=15.0,
    step=0.5,
)

focal_target = st.sidebar.number_input(
    "Target at Pins / Focal Point (Board #)",
    min_value=1.0,
    max_value=39.0,
    value=9.0,
    step=0.5,
    help="e.g., Center of 6-Pin = 9, Center of 10-Pin = 4, Headpin = 20",
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
board_diff = arrow_target - focal_target
laydown_offset = board_diff / 3.0
laydown_board = arrow_target + laydown_offset
slide_board = laydown_board + slide_foot_offset

# --- MAIN DISPLAY: CALCULATED LINE ---
st.subheader("Your Calculated Line")

col1, col2, col3, col4 = st.columns(4)
col1.metric("1. Slide Board (Foot)", f"{slide_board:.1f}")
col2.metric("2. Laydown Board", f"{laydown_board:.1f}")
col3.metric("3. Target Arrow", f"{arrow_target:.1f}")
col4.metric("4. Pin / Focal Target", f"{focal_target:.1f}")

st.info(
    f"**Full Line Summary:** Slide **{slide_board:.1f}** ➔ Laydown **{laydown_board:.1f}** ➔ Arrow **{arrow_target:.1f}** ➔ Pins **{focal_target:.1f}**"
)

# --- VISUALIZATION (LANE DIAGRAM) ---
st.subheader("Scaled Lane Trajectory Diagram")


def plot_lane_trajectory(slide, laydown, arrow, focal):
    # Lane dimensions in feet and board units (39 boards wide, 60 ft long)
    fig, ax = plt.subplots(figsize=(10, 4))

    # X-axis = Length in feet (0 = Foul line, 60 = Pins)
    # Y-axis = Board number (1 = Right gutter edge, 39 = Left gutter edge)

    # Key longitudinal coordinates (Feet)
    x_foul = 0
    x_arrow = 15  # Arrows at 15ft
    x_pins = 60  # Pins at 60ft

    # Y coordinates (Boards)
    y_laydown = laydown
    y_arrow = arrow
    y_focal = focal

    # Draw Lane Background
    ax.set_facecolor("#f3e5ab")  # Maple/Pine wood tone
    ax.axhspan(0, 1, color="#8b0000", alpha=0.3)  # Right Gutter
    ax.axhspan(39, 40, color="#8b0000", alpha=0.3)  # Left Gutter

    # Draw Arrows zone (15ft marker line)
    ax.axvline(
        x=x_arrow,
        color="gray",
        linestyle="--",
        alpha=0.5,
        label="Arrows (15 ft)",
    )

    # Draw Pin Deck zone (60ft line)
    ax.axvline(x=x_pins, color="black", linestyle="-", alpha=0.7)

    # Draw Dots / Target Markers at 15ft
    for b in range(5, 40, 5):
        ax.plot(x_arrow, b, "^", color="saddlebrown", markersize=6, alpha=0.6)

    # Plot the Trajectory Line (Laydown -> Arrow -> Focal Point)
    x_line = [x_foul, x_arrow, x_pins]
    y_line = [y_laydown, y_arrow, y_focal]

    ax.plot(
        x_line,
        y_line,
        color="#0055ff",
        linewidth=2.5,
        label="Ball Path",
        zorder=4,
    )

    # Highlight Key Points
    ax.scatter(
        [x_foul],
        [y_laydown],
        color="crimson",
        s=80,
        zorder=5,
        label=f"Laydown ({y_laydown:.1f})",
    )
    ax.scatter(
        [x_arrow],
        [y_arrow],
        color="orange",
        s=80,
        zorder=5,
        label=f"Arrow ({y_arrow:.1f})",
    )
    ax.scatter(
        [x_pins],
        [y_focal],
        color="green",
        s=80,
        zorder=5,
        label=f"Pin Target ({y_focal:.1f})",
    )

    # Plot Slide Foot Position (at Foul Line)
    ax.scatter(
        [x_foul],
        [slide],
        color="black",
        marker="s",
        s=60,
        zorder=5,
        label=f"Inside Foot ({slide:.1f})",
    )

    # Formatting axes
    ax.set_xlim(-2, 62)
    ax.set_ylim(0, 40)
    ax.set_xlabel("Lane Length (Feet from Foul Line)", fontsize=10)
    ax.set_ylabel("Board Number (Right to Left)", fontsize=10)
    ax.set_yticks(range(0, 45, 5))
    ax.grid(True, which="both", linestyle=":", alpha=0.4)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), borderaxespad=0)

    plt.tight_layout()
    return fig


# Render Plot
fig = plot_lane_trajectory(
    slide_board, laydown_board, arrow_target, focal_target
)
st.pyplot(fig)
