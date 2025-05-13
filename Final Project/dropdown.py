import sketchingpy

# Currently broken

# Initialize the sketch
sketch = sketchingpy.Sketch2DApp(500, 500)
sketch.clear('#FFFFFF')

# Set a font for text
sketch.set_text_font('Arial', 16)

# Dropdown data
dropdown_x, dropdown_y = 50, 50
dropdown_width, dropdown_height = 200, 30
options = ["Option 1", "Option 2", "Option 3"]
is_dropdown_open = False
selected_option = None

# Draw the dropdown
def draw_dropdown():
    global is_dropdown_open, selected_option
    sketch.clear('#FFFFFF')  # Clear the canvas

    # Draw the main dropdown box
    sketch.set_fill('#CCCCCC')
    sketch.draw_rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)

    # Draw the selected option or placeholder
    sketch.set_fill('#000000')
    if selected_option is None:
        sketch.draw_text("Select an option", int(dropdown_x + 10), int(dropdown_y + 20))
    else:
        sketch.draw_text(selected_option, int(dropdown_x + 10), int(dropdown_y + 20))

    # If the dropdown is open, draw the options
    if is_dropdown_open:
        for i, option in enumerate(options):
            option_y = dropdown_y + dropdown_height * (i + 1)
            sketch.set_fill('#FFFFFF')
            sketch.draw_rect(dropdown_x, option_y, dropdown_width, dropdown_height)
            sketch.set_fill('#000000')
            sketch.draw_text(option, int(dropdown_x + 10), int(option_y + 20))

# Handle mouse clicks
def handle_click(button):
    global is_dropdown_open, selected_option

    # Get mouse position
    mouse_x = sketch.get_pointer_x()
    mouse_y = sketch.get_pointer_y()

    # Check if the main dropdown box is clicked
    if dropdown_x <= mouse_x <= dropdown_x + dropdown_width and dropdown_y <= mouse_y <= dropdown_y + dropdown_height:
        is_dropdown_open = not is_dropdown_open
    elif is_dropdown_open:
        # Check if any option is clicked
        for i, option in enumerate(options):
            option_y = dropdown_y + dropdown_height * (i + 1)
            if dropdown_x <= mouse_x <= dropdown_x + dropdown_width and option_y <= mouse_y <= option_y + dropdown_height:
                selected_option = option
                is_dropdown_open = False
                break
        else:
            # Close the dropdown if clicked outside
            is_dropdown_open = False

    draw_dropdown()

# Bind the mouse click event
sketch.get_mouse().on_button_press(handle_click)

# Initial draw
draw_dropdown()

# Show the sketch
sketch.show()