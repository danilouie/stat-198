import sketchingpy

sketch = sketchingpy.Sketch2D(500, 500)

sketch.set_rect_mode('radius')
sketch.set_angle_mode('degrees')

def draw_at(x, y, color):
    sketch.push_transform()
    sketch.push_style()

    sketch.translate(x, y)

    sketch.set_fill(color)

    size = 5
    for rotation in range(0, 12):
        sketch.draw_rect(100, 0, size, size)
        sketch.rotate(30)
        size += 2

    sketch.pop_style()
    sketch.pop_transform()

sketch.translate(250, 250)

draw_at(0, -100, "#1b9e7750")
draw_at(-100, 100, "#d95f0250")
draw_at(100, 100, "#7570b350")

# sketch.set_rect_mode('radius')
# sketch.set_angle_mode('degrees')

# # translate before sketch to change the origin of rotation
# sketch.translate(250, 250)

# size = 5
# for rotation in range(0, 12):
#     sketch.draw_rect(200, 0, size, size)
#     sketch.rotate(30)
#     size += 5


sketch.show()