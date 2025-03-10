import sketchingpy

sketch = sketchingpy.Sketch2D(500, 500)
sketch.clear("#FFFFFF")

sketch.set_text_font("PublicSans-Regular.otf", 14)
sketch.set_fill("#333333")
sketch.clear_stroke()
# sketch.draw_text(10, 240, "Interactive Data Science and Visualization")

# Horizontal align
# sketch.set_text_align('left')
# sketch.draw_text(10, 150, 'Interactive Data Science and Visualization')

# sketch.set_text_align('center')
# sketch.draw_text(250, 250, 'Interactive Data Science and Visualization')

# sketch.set_text_align('right')
# sketch.draw_text(490, 350, 'Interactive Data Science and Visualization')

# Vertical align
sketch.set_text_align('left', 'baseline')
sketch.draw_text(10, 250, 'Going on a journey.')

sketch.show()