import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set page config for a professional mobile utility look
st.set_page_config(page_title="Bowling Vector App", layout="centered")

# 1. CORE VECTOR CALCULATION & PLOTTING ENGINE
def run_vector_app(target_arrow, breakpoint_dist, breakpoint_board, personal_offset):
    approach_start = -5
    foul_line = 0
    arrows_dist = 15
    pins_dist = 60
    
    # Core calculations stay 100% accurate with floating point numbers
    slope = (breakpoint_board - target_arrow) / (breakpoint_dist - arrows_dist)
    intercept = target_arrow - (slope * arrows_dist)
    
    ball_at_foul_line = intercept
    calculated_slide_board = ball_at_foul_line + personal_offset
    ball_at_pins = (slope * pins_dist) + intercept
    
    ball_y = np.linspace(foul_line, pins_dist, 100)
    ball_x = slope * ball_y + intercept

    # ULTRA-COMPACT CANVAS
    fig, ax = plt.subplots(figsize=(2.4, 3.8)) 
    ax.set_aspect(3.0, adjustable='box')
    
    # Transparency layer so it adapts cleanly to Light/Dark mobile system themes
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    # Lane elements (Fine lines)
    ax.plot([0.5, 0.5], [foul_line, pins_dist], color='black', linewidth=1.0)
    ax.plot([39.5, 39.5], [foul_line, pins_dist], color='black', linewidth=1.0)
    ax.axhline(y=foul_line, color='black', linestyle='-', linewidth=1.0)
    ax.axhline(y=arrows_dist, color='blue', linestyle='--', linewidth=0.5)
    ax.axhline(y=pins_dist, color='black', linestyle='-', linewidth=1.0)
    ax.fill_between([0.5, 39.5], approach_start, foul_line, color='lightgray', alpha=0.2)
    ax.plot([0.5, 39.5], [breakpoint_dist, breakpoint_dist], color='purple', linestyle='-', linewidth=0.8, alpha=0.6)
    
    for board in range(1, 40): ax.axvline(x=board, color='gray', linestyle='-', linewidth=0.1, alpha=0.08)
    for board in range(5, 40, 5): ax.axvline(x=board, color='gray', linestyle='-', linewidth=0.3, alpha=0.25)
    
    # Path & Markers
    ax.plot(ball_x, ball_y, color='red', linewidth=1.4, zorder=4)
    
    # Slide Stance (Orange)
    ax.scatter([calculated_slide_board], [approach_start + 2], color='orange', marker='^', s=35, zorder=8)
    ax.plot([calculated_slide_board, calculated_slide_board], [approach_start, foul_line], color='orange', linestyle='-.', linewidth=0.6)
    
    # Release Point, Target Arrow, and Breakpoint Markers
    ax.scatter([ball_at_foul_line], [foul_line], color='red', s=25, zorder=5)
    ax.scatter([target_arrow], [arrows_dist], color='blue', marker='o', s=20, zorder=7)
    ax.scatter([breakpoint_board], [breakpoint_dist], color='purple', marker='X', s=30, zorder=7)
    
    # Visual indicator at 60ft pins
    if 0.5 <= ball_at_pins <= 39.5:
        ax.scatter([ball_at_pins], [pins_dist], color='darkgreen', marker='v', s=25, zorder=7)
    else:
        ax.scatter([ball_at_pins], [pins_dist], color='darkred', marker='x', s=25, zorder=7)
    
    ax.set_xlim(45, -5) 
    ax.set_ylim(-6, 62)
    
    # Fixed board tick values
    ax.set_xticks([0, 20, 40])
    
    # Ultra-shrunk Typography for mobile viewport
    ax.set_xlabel('Lane Boards', fontsize=7, labelpad=2)
    ax.set_ylabel('Distance (ft)', fontsize=7, labelpad=2)
    ax.tick_params(axis='both', which='major', labelsize=6, pad=2)
    ax.grid(False)
    
    plt.tight_layout()
    return calculated_slide_board, ball_at_pins, fig

# 2. MOBILE-FIRST UI LAYOUT
st.markdown("## 🎳 Vector Calculator")

# Inputs expander
# FIXED: Kept min/max/value as floats, set step to 1.0. This preserves background decimal precision while format="%d" hides it visually without warning.
with st.expander("📥 CHANGE TARGET INPUTS", expanded=False):
    arrow_val = st.number_input('Target Arrow (Board):', min_value=1.0, max_value=39.0, value=15.0, step=1.0, format="%d")
    dist_val = st.number_input('Breakpoint Distance (ft):', min_value=16.0, max_value=60.0, value=44.0, step=1.0, format="%d")
    board_val = st.number_input('Breakpoint Target (Board):', min_value=-5.0, max_value=45.0, value=7.0, step=1.0, format="%d")
    offset_val = st.number_input('Personal Offset (Boards):', min_value=0.0, max_value=25.0, value=10.0, step=1.0, format="%d")

# Calculate Engine Metrics (runs with high-precision floats)
slide_num, pins_num, fig_asset = run_vector_app(arrow_val, dist_val, board_val, offset_val)

# Target results inside visual card container
with st.container(border=True):
    st.markdown("### 📋 TARGET RESULTS")
    
    # Values are strictly rounded ONLY at the final display step
    if pins_num < 0.5 or pins_num > 39.5:
        st.markdown(f"**FOCAL POINT:** Gutter ({int(round(pins_num))}) ❌")
    else:
        st.markdown(f"**FOCAL POINT:** Board {int(round(pins_num))}")

    st.markdown(f"**BREAKPOINT:** Board {int(round(board_val))}")
    st.markdown(f"**TARGET:** Board {int(round(arrow_val))}")
    st.markdown(f"**SLIDE POSITION:** Board {int(round(slide_num))}")

# Compact visual graph path map
st.markdown("### 🗺️ VISUAL PATH MAP")
st.pyplot(fig_asset, width="content")
plt.close(fig_asset)

st.markdown("---")

# Next Line Adjustments
st.markdown("### 🎯 Next Line Adjustments")
if dist_val < 60:
    table_data = []
    for step in range(1, 5):
        alt_arrow = arrow_val + step
        if alt_arrow <= 39.5:
            alt_slope = (board_val - alt_arrow) / (dist_val - 15)
            alt_intercept = alt_arrow - (alt_slope * 15)
            alt_pins = (alt_slope * 60) + alt_intercept
            alt_slide = alt_intercept + offset_val
            
            pin_label = f"Gutter ({int(round(alt_pins))})" if (alt_pins < 0.5 or alt_pins > 39.5) else f"{int(round(alt_pins))}"
            
            table_data.append({
                "Target Line": f"{int(round(alt_arrow))}",
                "Slide Stand": f"Board {int(round(alt_slide))}",
                "Focal Pin": pin_label
            })
            
    if table_data:
        st.table(table_data)
    else:
        st.markdown("`No legal adjustments available`")
else:
    st.markdown("`None`")

st.markdown("---")

# Pin Reference Deck Map (Unchanged clean view)
st.markdown("### 📋 Pin Reference Deck (60 FT)")
with st.container(border=True):
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**7 Pin:** Board 37\n\n**4 Pin:** Board 31\n\n**2 Pin:** Board 26")
    with col_right:
        st.markdown("**3 Pin:** Board 15\n\n**6 Pin:** Board 9\n\n**10 Pin:** Board 4")
