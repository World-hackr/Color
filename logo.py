# If you're in Jupyter, you may need one of these:
# %matplotlib notebook
# %matplotlib widget

import matplotlib
# If running as a standalone script, you can force an interactive backend, for example:
# matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt
import numpy as np
import itertools

# ------------------ COLOR SETUP ------------------
# Include “Radient Green” (#00FF7F) and other vibrant colors
colors = [
    "#FF0000", "#FFFF00", "#FF4500", "#0000FF", "#FF69B4", "#00FFFF",
    "#CCFF00", "#1F51FF", "#BF00FF", "#FFFF66", "#FF00FF", "#00CED1",
    "#FF355E", "#7F00FF", "#FF6EC7", "#BFFF00", "#00FF7F"  # Radient Green
]

# Generate all unique 2-color combinations
color_combinations = list(itertools.combinations(colors, 2))

# ------------------ PLOTTING ALL LOGOS IN A ROW ------------------
fig, ax = plt.subplots(figsize=(15, 6), facecolor="black")

# Draw every logo side by side
for i, (left_color, right_color) in enumerate(color_combinations):
    # Define hexagon shape
    theta = np.linspace(0, 2 * np.pi, 7)
    x_hex = np.cos(theta)
    y_hex = np.sin(theta)

    # X offset so each logo sits side by side, 3 units apart
    x_offset = i * 3

    # Black circular background
    circle = plt.Circle((x_offset, 0), 1.1, color="black", zorder=0)
    ax.add_patch(circle)

    # Fill left and right halves
    ax.fill_betweenx(y_hex, x_hex + x_offset, x_offset, where=(x_hex <= 0), color=left_color)
    ax.fill_betweenx(y_hex, x_hex + x_offset, x_offset, where=(x_hex >= 0), color=right_color)

    # Show color codes above each logo
    ax.text(x_offset, 1.3, f"{left_color}\n{right_color}", color="white",
            fontsize=8, ha='center', va='center')

# ------------------ VIEW / SCROLL SETTINGS ------------------
logos_per_view = 6
initial_left = -2
view_width = logos_per_view * 3  # 6 logos * 3 units each = 18 wide
initial_right = initial_left + view_width

ax.set_xlim(initial_left, initial_right)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis("off")

# Calculate how far we can scroll
max_x_offset = (len(color_combinations) - 1) * 3  # rightmost logo center
min_x = -2
max_x = max_x_offset + 2  # some padding
current_left = initial_left
current_right = initial_right

def on_scroll(event):
    """
    Handles mouse scroll events for a 'webpage-like' horizontal scroll:
    - Scrolling down => move view to the right
    - Scrolling up => move view to the left
    """
    global current_left, current_right

    # Define scroll speed in x-units
    scroll_speed = 2

    if event.step < 0:
        # Scrolling down => SHIFT VIEW TO THE RIGHT
        new_left = current_left + scroll_speed
        new_right = current_right + scroll_speed
    else:
        # Scrolling up => SHIFT VIEW TO THE LEFT
        new_left = current_left - scroll_speed
        new_right = current_right - scroll_speed

    # Clamp so we don't scroll beyond the row
    if new_left < min_x:
        new_left = min_x
        new_right = min_x + view_width
    if new_right > max_x:
        new_right = max_x
        new_left = max_x - view_width

    # Update
    current_left, current_right = new_left, new_right
    ax.set_xlim(current_left, current_right)
    plt.draw()

# Bind mouse scroll event
fig.canvas.mpl_connect("scroll_event", on_scroll)

plt.show()
