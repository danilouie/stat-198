import sketchingpy
import math

# Initialize the sketch
sketch = sketchingpy.Sketch2DApp(500, 500)
sketch.clear('#FFFFFF')

# Radar chart data
categories = ['A', 'B', 'C', 'D', 'E']
values = [4, 3, 2, 5, 4]
max_value = 5  # Maximum value for scaling

# Center and radius of the radar chart
center_x, center_y = 250, 250
radius = 150

# Calculate angles for each category
num_vars = len(categories)
angles = [2 * math.pi * i / num_vars for i in range(num_vars)]

# Draw the radar chart
# Draw the grid
for i in range(1, max_value + 1):
    r = radius * i / max_value
    points = [(center_x + r * math.cos(angle), center_y + r * math.sin(angle)) for angle in angles]
    points.append(points[0])  # Close the polygon
    sketch.set_stroke('#CCCCCC')
    for j in range(len(points) - 1):
        sketch.draw_line(points[j][0], points[j][1], points[j + 1][0], points[j + 1][1])

# Draw the data
data_points = [(center_x + (radius * value / max_value) * math.cos(angle),
                center_y + (radius * value / max_value) * math.sin(angle))
               for value, angle in zip(values, angles)]
data_points.append(data_points[0])  # Close the polygon

sketch.set_fill('#87CEEB')
sketch.set_stroke('#4682B4')
for i in range(len(data_points) - 1):
    sketch.draw_line(data_points[i][0], data_points[i][1], data_points[i + 1][0], data_points[i + 1][1])

# Display the sketch
sketch.show()