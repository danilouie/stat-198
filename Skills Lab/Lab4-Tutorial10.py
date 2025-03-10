"""Simulation which rotates wheels of colors to combine channels.

Simulation which rotates wheels with one wheel per color channel (red, green,
blue). These wheels overlap to show combinations of colors.

Part of https://interactivedatascience.courses.

Author: A Samuel Pottinger
License: BSD-3-Clause
"""

import sketchingpy

WHEEL_RADIUS = 70
WHEEL_ORTH_OFFSET = 49.497
RED_COLORS = [
    "#fff5f080",
    "#fee0d280",
    "#fcbba180",
    "#fc927280",
    "#fb6a4a80",
    "#ef3b2c80",
    "#cb181d80",
    "#99000d80"
]
BLUE_COLORS = [
    "#f7fbff80",
    "#deebf780",
    "#c6dbef80",
    "#9ecae180",
    "#6baed680",
    "#4292c680",
    "#2171b580",
    "#08459480"
]
GREEN_COLORS = [
    "#f7fcf580",
    "#e5f5e080",
    "#c7e9c080",
    "#a1d99b80",
    "#74c47680",
    "#41ab5d80",
    "#238b4580",
    "#005a3280"
]
ROTATE_SPEED = 0.5


class Wheel:
    """Wheel representing a single channel like red."""

    def __init__(self, x, y, colors, radius):
        """Create a new wheel.
        
        Args:
            x: The x position where the center of the wheel should be drawn.
            y: The y position where the center of the wheel should be drawn.
            colors: List of string hex codes to use. This should be single hue
                and decreasing in luminance.
            radius: The size of the spokes on the wheel in pixels.
        """
        self._x = x
        self._y = y
        self._colors = colors
        self._radius = radius
        self._cur_rotation = 0
        self._was_rotating = False

    def draw(self, sketch, mouse_x, mouse_y):
        """Draw this wheel in its current rotation.
        
        Args:
            sketch: The Sketch2D in which to draw the wheels.
            mouse_x: The current mouse x position.
            mouse_y: The current mouse y position.
        """
        sketch.push_transform()
        sketch.push_style()

        sketch.translate(self._x, self._y)
        sketch.set_angle_mode('degrees')
        sketch.set_ellipse_mode('radius')
        
        rotation_per_circle = 360 / len(self._colors)
        
        mouse_rel_x = mouse_x - self._x
        mouse_rel_y = mouse_y - self._y
        hovering_x = abs(mouse_rel_x) < self._radius
        hovering_y = abs(mouse_rel_y) < self._radius
        hovering = hovering_x and hovering_y
        
        if hovering:
            self._cur_rotation += ROTATE_SPEED
            self._cur_rotation %= 360
            self._was_rotating = True
        
        stopped_rotating = not hovering and self._was_rotating
        if stopped_rotating:
            self._was_rotating = False
            snap_num = round(self._cur_rotation / rotation_per_circle)
            self._cur_rotation = snap_num * rotation_per_circle

        sketch.rotate(self._cur_rotation)

        for color in self._colors:
            sketch.set_stroke('#999999')

            sketch.clear_fill()
            sketch.draw_line(0, 0, 0, self._radius - 10)

            sketch.set_fill(color)
            sketch.draw_ellipse(0, self._radius, 10, 10)

            sketch.rotate(rotation_per_circle)

        sketch.pop_style()
        sketch.pop_transform()


class Simulation:
    """Simulation which manages the three color channel wheels."""

    def __init__(self, center_x, center_y):
        """Create a new simluation with three new wheels.
        
        Args:
            center_x: The center where the overlap between the three wheels
                should be drawn.
            center_y: The center where the overlap between the three wheels
                should be drawn.
        """
        self._wheels = [
            Wheel(
                center_x,
                center_y - WHEEL_RADIUS,
                RED_COLORS,
                WHEEL_RADIUS
            ),
            Wheel(
                center_x - WHEEL_ORTH_OFFSET,
                center_y + WHEEL_ORTH_OFFSET,
                BLUE_COLORS,
                WHEEL_RADIUS
            ),
            Wheel(
                center_x + WHEEL_ORTH_OFFSET,
                center_y + WHEEL_ORTH_OFFSET,
                GREEN_COLORS,
                WHEEL_RADIUS
            )
        ]
    
    def draw(self, sketch, mouse_x, mouse_y):
        """Draw the three wheels in their current rotation.
        
        Args:
            sketch: The Sketch2D in which to draw.
            mouse_x: The current mouse x position.
            mouse_y: The current mouse y position.
        """
        sketch.push_transform()
        sketch.push_style()

        for wheel in self._wheels:
            wheel.draw(sketch, mouse_x, mouse_y)

        sketch.clear_fill()
        sketch.set_stroke("#333333")
        sketch.set_ellipse_mode('radius')
        sketch.draw_ellipse(250, 250, 15, 15)

        sketch.pop_style()
        sketch.pop_transform()


sketch = sketchingpy.Sketch2D(500, 500)
simulation = Simulation(250, 250)

def update_and_draw(sketch):
    """Update the state of the visualization and redraw.
    
    Args:
        sketch: The sketch to update and draw.
    """
    mouse = sketch.get_mouse()
    mouse_x = mouse.get_pointer_x()
    mouse_y = mouse.get_pointer_y()

    sketch.clear('#FFFFFF')
    simulation.draw(sketch, mouse_x, mouse_y)

sketch.on_step(update_and_draw)
sketch.show()
