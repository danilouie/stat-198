import sketchingpy
import math
import random

sketch = sketchingpy.Sketch2D(500, 500)

x_center = 250
y_center = 250
x_radius = 150
y_radius = 150

# draws base of the eye
def draw_base(x_center, y_center):
    sketch.clear("#ffffff")
    sketch.set_ellipse_mode("radius")
    sketch.set_fill("#7eb7bf")
    sketch.draw_ellipse(x_center, y_center, x_radius, y_radius)

# draw eye -> updates to where the cursor is
def draw_eye(x_center, y_center):
    draw_base(x_center, y_center)
    outer_ring(x_center, y_center)
    draw_iris_teal(x_center, y_center)
    draw_iris_darkteal(x_center, y_center)
    draw_iris_lightteal(x_center, y_center)
    outer_to_inner(x_center, y_center)   
    white_ring(x_center, y_center)
    draw_pupil_fuzz(x_center, y_center)
    draw_pupil(x_center, y_center)
    draw_shine(x_center, y_center)

#draw pupil
def draw_pupil(x_center, y_center):
    sketch.set_fill("#000000")
    sketch.draw_ellipse(x_center, y_center, 40, 40)
    
# draw pupil fuzz
def draw_pupil_fuzz(x_center, y_center):
    sketch.set_stroke("#000000")
    sketch.set_stroke_weight(1)
    
    for i in range(2000):
        angle = math.radians(i * (360 / 2000)) 
        outer_length = random.uniform(30, 40)
        inner_length = 30

        x_outer = x_center + outer_length * math.cos(angle)
        y_outer = y_center + outer_length * math.sin(angle)
        x_inner = x_center + inner_length * math.cos(angle)
        y_inner = y_center + inner_length * math.sin(angle)
        sketch.draw_line(x_outer, y_outer, x_inner, y_inner)

# draws outer ring
def outer_ring(x_center, y_center):
    sketch.set_stroke('#125359')
    sketch.set_stroke_weight(6)
    sketch.draw_ellipse(x_center, y_center, x_radius, y_radius)

def draw_iris_teal(x_center, y_center):
    sketch.set_stroke("#5099a3")
    sketch.set_stroke_weight(1)

    for i in range(1000):  
        angle = math.radians(random.uniform(0, 360)) 
        length = random.uniform(70, x_radius)
        x_end = x_center + length * math.cos(angle)  
        y_end = y_center + length * math.sin(angle)  
        sketch.draw_line(x_center, y_center, x_end, y_end)

def draw_iris_darkteal(x_center, y_center):
    sketch.set_stroke("#335861")
    sketch.set_stroke_weight(1)
    
    for i in range(500):
        angle = math.radians(i * (360 / 500)) 
        outer_length = x_radius - random.uniform(40, 80)
        inner_length = x_radius - random.uniform(40, 80)

        x_outer = x_center + outer_length * math.cos(angle)
        y_outer = y_center + outer_length * math.sin(angle)
        x_inner = x_center + inner_length * math.cos(angle)
        y_inner = y_center + inner_length * math.sin(angle)
        sketch.draw_line(x_outer, y_outer, x_inner, y_inner)

def draw_iris_lightteal(x_center, y_center):
    sketch.set_stroke("#8eb7d7")
    sketch.set_stroke_weight(1)
    outer_length = x_radius - 125
    
    for i in range(360):
        angle = math.radians(i * (360 / 360))
        inner_length = x_radius - random.uniform(70, 90)

        x_outer = x_center + outer_length * math.cos(angle)
        y_outer = y_center + outer_length * math.sin(angle)
        x_inner = x_center + inner_length * math.cos(angle)
        y_inner = y_center + inner_length * math.sin(angle)
        sketch.draw_line(x_outer, y_outer, x_inner, y_inner)
        
def outer_to_inner(x_center, y_center):
    sketch.set_stroke("#125359")
    sketch.set_stroke_weight(1)
    outer_length = x_radius 

    for i in range(1000):
        angle = math.radians(i * (360 / 1000)) 
        inner_length = random.uniform(130, 140)

        x_outer = x_center + outer_length * math.cos(angle)
        y_outer = y_center + outer_length * math.sin(angle)
        x_inner = x_center + inner_length * math.cos(angle)
        y_inner = y_center + inner_length * math.sin(angle)
        sketch.draw_line(x_outer, y_outer, x_inner, y_inner)

def white_ring(x_center, y_center):
    sketch.set_stroke("#ffffff")
    sketch.set_stroke_weight(1)
    
    for i in range(200):
        angle = math.radians(i * (360 / 200)) 
        outer_length = x_radius - random.uniform(30, 40)
        inner_length = x_radius - random.uniform(30, 40)

        x_outer = x_center + outer_length * math.cos(angle)
        y_outer = y_center + outer_length * math.sin(angle)
        x_inner = x_center + inner_length * math.cos(angle)
        y_inner = y_center + inner_length * math.sin(angle)
        sketch.draw_line(x_outer, y_outer, x_inner, y_inner)

def draw_shine(x_center, y_center):
    sketch.set_fill("#ffffff") 
    shine_x = x_center - 90  
    shine_y = y_center - 40  
    shine_width = 30  
    shine_height = 15 
    sketch.draw_ellipse(shine_x, shine_y, shine_width, shine_height)

def update(sketch):
    sketch.clear("#ffffff")
    global x_center, y_center
    mouse = sketch.get_mouse()
    x_center = mouse.get_pointer_x()
    y_center = mouse.get_pointer_y()
    draw_eye(x_center, y_center)

sketch.on_step(update)
draw_eye(x_center, y_center)
sketch.show()
