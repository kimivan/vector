import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set page config for mobile-friendly view
st.set_page_config(page_title="Bowling Vector App", layout="centered")

# 1. CORE VECTOR CALCULATION & PLOTTING ENGINE
def run_vector_app(target_arrow, breakpoint_dist, breakpoint_board, personal_offset):
    approach_start = -5
    foul_line = 0
    arrows_dist = 15
    pins_dist = 60
    
    # Core calculations for the primary line
    slope = (breakpoint_board - target_arrow) / (breakpoint_dist - arrows_dist)
    intercept = target_arrow - (slope * arrows_dist)
    
    ball_at_foul_line = intercept
    calculated_slide_board = ball_at_foul_line + personal_offset
    ball_at_pins = (slope * pins_dist) + intercept
    
    ball_y = np.linspace(foul_line, pins_dist, 100)
    ball_x = slope * ball_y + intercept

    # ULTRA-COMPACT CANVAS: Perfect for small mobile layouts
    fig, ax = plt.subplots(figsize=(2.4, 3.8)) 
    ax.set_aspect(3.0, adjustable='box')
    
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
    
    # Path & Markers (Scaled down to micro sizes)
    ax.plot(ball_x, ball_y, color='red', linewidth=1.4, zorder=4)
    
    # Slide Stance (Orange)
    ax.scatter([calculated_slide_board], [approach_start + 2], color='orange', marker='^', s=35, zorder=8)
    ax.plot([calculated_slide_board, calculated_slide_board], [approach_start, foul_line], color='orange', linestyle='-.', linewidth=0.6)
    
    # Release Point, Target Arrow, and Breakpoint Markers (Micro sizing)
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
st.title("🎳 Vector Calculator")

# Inputs expander
with st.expander("📥 CHANGE TARGET INPUTS", expanded=False):
    arrow_val = st.number_input('Target:', min_value=1.0, max_value=39.0, value=15.0, step=0.5)
    dist_val = st.number_input('BP Distance:', min_value=16, max_value=60, value=44, step=1)
    board_val = st.number_input('BP Board:', min_value=-5.0, max_value=45.0, value=7.0, step=0.1)
    offset_val = st.number_input('Offset:', min_value=0.0, max_value=25.0, value=10.0, step=0.5)

# Calculate Engine Metrics
slide_num, pins_num, fig_asset = run_vector_app(arrow_val, dist_val, board_val, offset_val)

st.markdown("### 📋 TARGET RESULTS")

# FIXED: Removed st.metric and used unified font sizing markdown strings
if pins_num < 0.5 or pins_num > 39.5:
    st.markdown(f"🔴 **❌ FOCAL POINT:** ({pins_num:.1f})")
else:
    st.markdown(f"🟢 **🎳 FOCAL POINT:** {pins_num:.1f}")

st.markdown(f"🟠 **👟 SLIDE:**  {int(round(slide_num))}")
st.markdown(f"🟣 **📍 BREAKPOINT:**  {board_val:.1f}")
st.markdown(f"🔵 **🎯 TARGET:**  {int(round(arrow_val))}")

st.markdown("---")

# Compact visual graph path map
st.markdown("### 🗺️ VISUAL PATH MAP")
st.pyplot(fig_asset, width="content")
plt.close(fig_asset)

st.markdown("---")

# FIXED: Moved "Next line adjustments" down below the graph canvas
st.markdown("### 🎳 Next line adjustments")
if dist_val < 60:
    matrix_html = '<div style="font-family: monospace; line-height: 1.8; font-size: 11px; background-color: #f0f2f6; padding: 10px; border-radius: 5px;">'
    for step in range(1, 5):
        alt_arrow = arrow_val + step
        if alt_arrow <= 39.5:
            alt_slope = (board_val - alt_arrow) / (dist_val - 15)
            alt_intercept = alt_arrow - (alt_slope * 15)
            alt_pins = (alt_slope * 60) + alt_intercept
            alt_slide = alt_intercept + offset_val
            
            color = "darkred" if (alt_pins < 0.5 or alt_pins > 39.5) else "green"
            label_suffix = f" (+{step})"
            
            matrix_html += (
                f"🎯 Target: <span style='color:blue; font-weight:bold;'>{alt_arrow:4.1f}</span>{label_suffix:<4} | "
                f"👟 Slide: <span style='color:orange; font-weight:bold;'>{int(round(alt_slide)):2d}</span> | "
                f"🏁 Focal Point: <span style='color:{color}; font-weight:bold;'>B {alt_pins:.1f}</span><br>"
            )
    matrix_html += '</div>'
    st.html(matrix_html)
else:
    st.markdown("`None`")

st.markdown("---")

# FIXED: Removed expander dropdown container; completely open code window block
st.markdown("### 📋 PIN REFERENCE (60 FT)")
st.html("""
<div style="font-family: monospace; line-height: 1.6; font-size: 13px; background-color: #f0f2f6; padding: 10px; border-radius: 5px;">
  <b>7 Pin:</b>  Board 36.5 &nbsp;&nbsp; <b>3 Pin:</b> Board 14.5<br>
  <b>4 Pin:</b>  Board 31.0 &nbsp;&nbsp; <b>6 Pin:</b>  Board 9.0<br>
  <b>2 Pin:</b>  Board 25.5 &nbsp;&nbsp; <b>10 Pin:</b> Board 3.5<br>
</div>
""")
