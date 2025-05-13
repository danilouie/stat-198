import sketchingpy

sketch = sketchingpy.Sketch2DA(500, 500)

# sets background to white as default
sketch.clear("#ffffff")

# sketch.set_stroke_weight(3)
# # Adding FF (full opaque) or 00 (full transparent) to the color code to the end
# # sketch.set_fill("#a6cee3FF")
# sketch.set_stroke("#1f78b4")
# sketch.clear_fill()
# sketch.draw_ellipse(150, 250, 100, 100)

# sketch.set_stroke_weight(10)
# sketch.set_fill("#C0C0C0")
# sketch.clear_stroke()
# sketch.draw_ellipse(250, 250, 100, 100)

# sketch.set_stroke_weight(6)
# # sketch.set_fill("#b2df8a00")
# sketch.set_stroke("#33a02c")
# sketch.clear_fill()
# sketch.draw_ellipse(350, 250, 100, 100)


sketch.set_ellipse_mode("radius")

def draw_circles(y):
    sketch.set_stroke("#000000")

    sketch.set_fill("#edf8fb")
    sketch.draw_ellipse(150, y, 20, 20)

    sketch.set_fill("#b2e2e2")
    sketch.draw_ellipse(200, y, 20, 20)

    sketch.set_fill("#66c2a4")
    sketch.draw_ellipse(250, y, 20, 20)

    sketch.set_fill("#2ca25f")
    sketch.draw_ellipse(300, y, 20, 20)

    sketch.set_fill("#006d2c")
    sketch.draw_ellipse(350, y, 20, 20)

draw_circles(125)

sketch.set_rect_mode("corner")
sketch.clear_stroke()
sketch.set_fill("#555555")
sketch.draw_rect(0, 250, 500, 250)

draw_circles(375)

sketch.show()