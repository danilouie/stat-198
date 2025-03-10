import sketchingpy

sketch = sketchingpy.Sketch2D(500, 500)

image = sketch.get_image('reading.jpg')
image.resize(150, 150)

def draw(sketch):
    sketch.clear('#707070')

    mouse = sketch.get_mouse()

    sketch.clear_stroke()
    sketch.set_ellipse_mode('radius')
    sketch.set_fill('#A6CEE350')
    sketch.draw_ellipse(250, 250, 100, 100)

    sketch.set_image_mode('center')
    sketch.draw_image(mouse.get_pointer_x(), mouse.get_pointer_y(), image)

sketch.on_step(draw)

# save images
sketch = sketchingpy.Sketch2D(500, 500)
sketch.draw_ellipse(250, 250, 100, 100)
sketch.save_image('ellipse.png')

sketch.show()