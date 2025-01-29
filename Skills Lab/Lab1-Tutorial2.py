import sketchingpy
import time

# build space
sketch = sketchingpy.Sketch2D(500, 400)
 
# DRAWING LINES
# sketch.draw_line(500 / 2, 400 / 2, 100, 50)

center_x = 500 / 2
center_y = 400 / 2
end_x = 100
end_y = 50
sketch.draw_line(center_x, center_y, end_x, end_y)

# start_time = time.time()

# def draw_moving_line(self):
#     seconds = time.time() - start_time
#     pixels_per_second = 5
#     offset = seconds * pixels_per_second
#     sketch.draw_line(250, 200, 100, 50 + offset)

# sketch.on_step(draw_moving_line)

def draw_moving_line(self):
    mouse = sketch.get_mouse()
    sketch.draw_line(250, 200, mouse.get_pointer_x(), mouse.get_pointer_y())

sketch.on_step(draw_moving_line)

sketch.show()
