import sketchingpy

sketch = sketchingpy.Sketch2D(500, 500)

sketch.set_ellipse_mode("radius")

sketch.draw_ellipse(0, 0, 5, 5)

# sketch.translate(100, 100)

# sketch.draw_ellipse(0, 0, 10, 10)

# sketch.translate(50, 50)
# sketch.translate(50, 50)

# sketch.draw_ellipse(0, 0, 15, 15)

# sketch.translate(100, 100)

# sketch.draw_ellipse(0, 0, 20, 20)

# sketch.translate(200, 200)

# sketch.draw_ellipse(0, 0, 5, 5)

# # sketch.push_transform()
# sketch.translate(100, 100)
# sketch.draw_ellipse(0, 0, 10, 10)

# sketch.translate(50, 0)
# sketch.push_transform()
# sketch.translate(50, 0)
# sketch.draw_ellipse(0, 0, 15, 15)
# sketch.pop_transform()

# sketch.translate(50, 50)
# sketch.draw_ellipse(0, 0, 20, 20)

sketch.clear('#505050')
sketch.set_stroke_weight(3)

sketch.set_fill('#B2DF8A50')
sketch.set_stroke('#F0F0F0')
sketch.draw_ellipse(150, 250, 20, 20)

sketch.push_style()
sketch.clear_fill()
sketch.draw_ellipse(250, 250, 20, 20)
sketch.pop_style()

sketch.draw_ellipse(350, 250, 20, 20)

sketch.show()
input("Press Enter to close the sketch...")
