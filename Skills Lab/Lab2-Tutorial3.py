import sketchingpy
import time

WIDTH = 500  # pixels
HEIGHT = 400  # pixels

sketch = sketchingpy.Sketch2D(WIDTH, HEIGHT)

class Ball:
    
    def __init__(self, position_x, position_y, velocity_x, velocity_y):
        self.position_x = position_x
        self.position_y = position_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    
    # bouncing behavior
    def reverse_x(self):
        self.velocity_x = self.velocity_x * -1
        
    def reverse_y(self):
        self.velocity_y = self.velocity_y * -1
    
    def get_is_near_mouse(self, mouse_x, mouse_y):
        x_near = abs(mouse_x - self.position_x) < 10
        y_near = abs(mouse_y - self.position_y) < 10
        return x_near and y_near

    def get_hit_mouse_in_direction(self, coordinate, mouse, velocity):
        if mouse > coordinate and velocity > 0:
            distance = mouse - coordinate
            return distance < 10
        elif mouse < coordinate and velocity < 0:
            distance = mouse - coordinate
            return distance > -10
        else:
            return False
        
    # update ball
    def update(self, duration, mouse_x, mouse_y):
        self.position_x = self.position_x + self.velocity_x * duration
        self.position_y = self.position_y + self.velocity_y * duration

        if self.position_x > WIDTH:
            self.position_x = WIDTH
            self.reverse_x()       
        elif self.position_x < 0:
            self.position_x = 0
            self.reverse_x()
        
        if self.position_y > HEIGHT:
            self.position_y = HEIGHT
            self.reverse_y()
        elif self.position_y < 0:
            self.position_y = 0
            self.reverse_y()
            
        if self.get_is_near_mouse(mouse_x, mouse_y):
            if self.get_hit_mouse_in_direction(self.position_x, mouse_x, self.velocity_x):
                self.reverse_x()
            elif self.get_hit_mouse_in_direction(self.position_y, mouse_y, self.velocity_y):
                self.reverse_y()
            
class Simulation:
    
    def __init__(self):
        self.balls = [
            Ball(WIDTH / 2, HEIGHT / 2, -10, -10),
            Ball(WIDTH / 2, HEIGHT / 2, -10, -10),
            Ball(WIDTH / 2, HEIGHT / 2, 10, 0)
        ]
        self.last_time = time.time()
        
    # def update(self):
    #     new_time = time.time()
    #     duration = new_time - self.last_time
    #     self.last_time = new_time
        
    #     for ball in self.balls:
    #         ball.update(duration)
    
    # update for mouse
    def update(self, mouse_x, mouse_y):
        new_time = time.time()
        duration = new_time - self.last_time
        self.last_time = new_time

        for ball in self.balls:
            ball.update(duration, mouse_x, mouse_y)
            
simulation = Simulation()

# def update_and_draw_balls(self):
#     simulation.update()
#     for ball in simulation.balls:
#         sketch.draw_ellipse(ball.position_x, ball.position_y, 2, 2)

# Mouse interaction
def update_and_draw_balls(self):
    mouse = sketch.get_mouse()
    mouse_x = mouse.get_pointer_x()
    mouse_y = mouse.get_pointer_y()

    simulation.update(mouse_x, mouse_y)

    for ball in simulation.balls:
        sketch.draw_ellipse(ball.position_x, ball.position_y, 2, 2)
        
sketch.on_step(update_and_draw_balls)
sketch.show()
        