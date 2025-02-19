import sketchingpy

sketch = sketchingpy.Sketch2D(500, 500)

sketch.set_stroke_weight(3)

# sketching circles
# sketch.set_ellipse_mode('corners')
# sketch.draw_ellipse(250, 250, 20, 20)

# sketch.set_ellipse_mode('radius')
# sketch.draw_ellipse(250, 250, 20, 20)

# sketch.set_ellipse_mode('center')
# sketch.draw_ellipse(250, 250, 20, 20)

# sketch.set_ellipse_mode('corner')
# sketch.draw_ellipse(250, 250, 20, 20)

# sketching rectangles
# sketch.set_rect_mode('corners')
# sketch.draw_rect(250, 250, 20, 20)

# sketch.set_rect_mode('radius')
# sketch.draw_rect(250, 250, 20, 20)

# sketch.set_rect_mode('center')
# sketch.draw_rect(250, 250, 20, 20)

# sketch.set_rect_mode('corner')
# sketch.draw_rect(250, 250, 20, 20)

# sketching lines
sketch.draw_line(230, 270, 270, 270)

# shape = sketch.start_shape(230, 270)
# shape.add_line_to(270, 270)
# shape.add_line_to(250, 230)
# shape.end()
# sketch.draw_shape(shape)

# sketching curves
shape = sketch.start_shape(230, 270)
shape.add_line_to(270, 270)
shape.add_bezier_to(60, 110, 140, 190, 150, 200)
shape.end()
sketch.draw_shape(shape)

# sketching shapes
sketch.set_ellipse_mode('radius')
sketch.draw_ellipse(150, 250, 20, 20)

shape = sketch.start_shape(230, 270)
shape.add_line_to(270, 270)
shape.add_line_to(250, 230)
# shape.end() does not fill in the shape
shape.close()
sketch.draw_shape(shape)

sketch.set_rect_mode('radius')
sketch.draw_rect(350, 250, 20, 20)

sketch.show()