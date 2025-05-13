import sketchingpy
import random
import math

WIDTH = 1600
HEIGHT = 900

TITLE = "California Energy Data"

SECTOR_COLORS = {
    "Residential": "#99a85c", # Green
    "Commercial": "#cac1d9",  # Light Purple
    "Industrial": "#f2d584",  # Yellow
    "Transportation": "#597da5",  # Blue
    "Total": "#d7b4ad"  # Salmon
}

# Darker shades of corresponding sector colors
CAPITA_COLORS = {
    "Residential": "#6b7540", # Green
    "Commercial": "#a19aad",  # Light Purple
    "Industrial": "#c1aa69",  # Yellow
    "Transportation": "#3e5773",  # Blue
    "Total": "#ac908a"  # Salmon
}

# TODO: Add actual data and scale the values accordingly
# TODO: Add interactivity - priority is for the large bar chart, then for the different years

# Initialize the sketch
sketch = sketchingpy.Sketch2DApp(WIDTH, HEIGHT)
sketch.clear('#FFFFFF')


class Axis:
    """A general class for drawing x and y axes."""

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw_x_axis(self, x_start, x_end, y_base):
        """Draw the x-axis with optional tick marks and labels."""
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.draw_line(x_start, y_base, x_end, y_base)

    def draw_y_axis(self, y_start, y_end, x_base):
        """Draw the y-axis with optional tick marks and labels."""
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.draw_line(x_base, y_start, x_base, y_end)


class Sector:
    """Creates a bar graph on the upper left side of the plot."""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw(self):
        # Filler data for the bar graph
        categories = ["Residential", "Commercial", "Industrial", "Transportation", "Total"]
        values = [random.randint(50, 300) for _ in categories]

        # Bar graph dimensions
        bar_width = 50
        spacing = 20
        x_start = 90
        y_base = self.height - 419

        # Draw the bars
        for i, (category, value) in enumerate(zip(categories, values)):
            x = x_start + i * (bar_width + spacing)
            y = y_base - value

            # Draw the bar
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill(SECTOR_COLORS[category])
            self.canvas.draw_rect(x, y, bar_width, value)

        # Draw the legend
        self.canvas.set_stroke_weight(0)
        self.draw_legend(categories)

    def draw_legend(self, categories):
        """Draw a horizontal legend at the top left."""
        legend_x_start = 30
        legend_y_start = self.height - 810
        legend_box_size = 20
        spacing = 8

        for i, category in enumerate(categories):
            x = legend_x_start + i * (legend_box_size + spacing + 80)
            y = legend_y_start

            # Draw the legend color box
            self.canvas.set_fill(SECTOR_COLORS[category])
            self.canvas.draw_rect(x, y, legend_box_size, legend_box_size)

            # Draw the legend label
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("left", "center")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_font("Arial", 12)
            self.canvas.draw_text(x + legend_box_size + spacing - 5, y + legend_box_size / 2 + 1, category)


class PerCapita:
    """Creates a bar graph on the lower left side of the plot."""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw(self):
        # Filler data for the bar graph
        categories = ["Residential", "Commercial", "Industrial", "Transportation", "Total"]
        values = [random.randint(50, 300) for _ in categories]

        # Bar graph dimensions
        bar_width = 50
        spacing = 20
        x_start = 90
        y_base = self.height - 419

        # Draw the bars upside down
        for i, (category, value) in enumerate(zip(categories, values)):
            x = x_start + i * (bar_width + spacing)
            y = y_base + value 

            # Draw the bar upside down
            self.canvas.set_stroke("#000000")
            # self.canvas.set_stroke_weight(2)
            self.canvas.set_fill(CAPITA_COLORS[category])  # Use the same colors as Sector
            self.canvas.draw_rect(x, y - value, bar_width, value)  # Adjust y to start from the top of the bar


class RankedBar:
    """Creates a bar graph in the middle that ranks the states based on their total energy consumption."""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw(self):
        # Generate random data for 50 states
        states = ["State " + str(i) for i in range(1, 51)]
        states[4] = "California"  # Replace one state with California
        data = {state: random.randint(50, 300) for state in states}  # Single value per state

        # Sort states by total energy consumption in descending order
        sorted_states = sorted(data.items(), key=lambda x: x[1], reverse=True)

        # Bar graph dimensions
        bar_height = 6.5
        spacing = 7
        x_base = 1150
        y_start = 137

        # Draw the bars
        for i, (state, value) in enumerate(sorted_states):
            x = x_base
            y = y_start + i * (bar_height + spacing)

            # Make California stand out compared to other states
            if state == "California":
                self.canvas.set_fill("#fa0b0b")  # Red for California
            else:
                self.canvas.set_fill("#d0d0d0")  # Gray for other states

            # Draw the bar
            self.canvas.set_stroke("#000000")  # Black border
            self.canvas.set_stroke_weight(0)
            self.canvas.draw_rect(x, y + 10, value, bar_height)

             # Draw the state label to the right of the bar
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("left", "center")  # Align text to the left
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(x + value + 10, y + bar_height / 2 + 10, state)  # Position label to the right of the bar


class RadarChart:
    """Creates a radar chart for visualizing the renewable energy consumption."""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw(self):
        # Placeholder for radar chart drawing logic
        renewables = ["Biomass", "Geothermal", "Hydroelectric Power", "Solar", "Wind"]
        values = [random.randint(50, 250) for _ in renewables]
        max_value = max(values)
        
        # Radar chart dimensions
        center_x = self.width / 2 
        center_y = 350
        radius = 180
        axis_extension = 10

        # Pentagon grid
        num_levels = 5 # Number of web levels
        num_vertices = 5  # Number of vertices for the pentagon
        for level in range(1, num_levels + 1):
            r = (level / num_levels) * radius
            points = []
            for i in range(num_vertices):
                angle = (2 * math.pi / num_vertices) * i - math.pi / 2  # Start at the top
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
                points.append((x, y))
            # Connect the vertices to form the pentagon
            self.canvas.set_stroke("#cccccc")  # Light gray for the grid
            self.canvas.set_stroke_weight(2)
            for j in range(len(points)):
                x1, y1 = points[j]
                x2, y2 = points[(j + 1) % len(points)]  # Wrap around to the first point
                self.canvas.draw_line(x1, y1, x2, y2)

        # Draw the radar axes
        num_renewables = len(renewables)
        for i in range(num_renewables):
            angle = (2 * math.pi / num_renewables) * i - math.pi / 2  # Start at the top
            x = center_x + (radius + axis_extension) * math.cos(angle)
            y = center_y + (radius + axis_extension) * math.sin(angle)
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(center_x, center_y, x, y)

            # Add category labels
            label_x = center_x + (radius + 30) * math.cos(angle)
            label_y = center_y + (radius + 30) * math.sin(angle)
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("center", "center")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_font("Arial", 12)
            self.canvas.draw_text(label_x, label_y, renewables[i])

        # Plot the data points
        points = []
        for i, value in enumerate(values):
            angle = (2 * math.pi / num_renewables) * i - math.pi / 2
            r = (value / max_value) * radius
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))

        # Connect the points to form the radar shape
        self.canvas.set_stroke("#FF0000")  # Red for the radar shape
        self.canvas.set_stroke_weight(2)
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]  # Connect to the next point, wrapping around
            self.canvas.draw_line(x1, y1, x2, y2)

        # Draw the data points
        for x, y in points:
            self.canvas.set_fill("#FF0000")
            self.canvas.draw_ellipse(x, y, 3, 3)  # Small circles for data points


class LineGraph:
    """Creates a line graph for visualizing the renewable energy consumption over the years."""
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def draw(self):
        # Generate random data for years and values
        years = list(range(2000, 2021))  # Years from 2000 to 2020
        values = [random.randint(50, 100) for _ in years]  # Random values for each year
        max_value = max(values)

        # Line graph dimensions
        graph_x_start = 550
        graph_x_end = 1025
        graph_y_start = 500
        graph_y_end = 800

        # Scale the data to fit within the graph dimensions
        x_spacing = (graph_x_end - graph_x_start) / (len(years) - 1)
        y_scale = (graph_y_start - graph_y_end) / max_value

        # Plot the data points and connect them with lines
        points = []
        for i, value in enumerate(values):
            x = graph_x_start + i * x_spacing
            y = graph_y_start - value * y_scale
            points.append((x, y))

            # Draw the data point
            self.canvas.set_fill("#FF0000")
            self.canvas.draw_ellipse(x, y, 3, 3)  # Small circle for the data point

        # Connect the points with lines
        self.canvas.set_stroke("#FF0000")
        self.canvas.set_stroke_weight(2)
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.draw_line(x1, y1, x2, y2)


class Dropdown:
    """Creates multiple dropdown for user interaction.

    First Dropdown: year

    Second Dropdown:
        - Total energy consumption estimates
        - Real gross domestic product (GDP)
        - Energy consumption estimates per real dollar of GDP""" 
    
    # Temporarily draws a rectangle where the dropodown will be
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    # Draws a rectangle for selecting the year
    def draw(self):
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.set_fill('#FFFFFF')
        self.canvas.draw_rect(WIDTH/2 - 100, 90, 200, 20)  # Placeholder for dropdown
        self.canvas.draw_rect(1225, 90, 200, 20)  # Placeholder for dropdown


def draw_title(title):
    """Draw the title for the bar graph."""
    sketch.set_text_font('Arial', 36)
    sketch.set_text_align('center', 'bottom')
    sketch.set_fill('#000000')
    sketch.draw_text(WIDTH/2, 60, title)


# Draw the title
draw_title(TITLE)

# Draw the sector bar graph
sector = Sector(sketch, WIDTH, HEIGHT)
sector.draw()

perCapita = PerCapita(sketch, WIDTH, HEIGHT)
perCapita.draw()

rankedBar = RankedBar(sketch, WIDTH, HEIGHT)
rankedBar.draw()

radar = RadarChart(sketch, WIDTH, HEIGHT)
radar.draw()

lineGraph = LineGraph(sketch, WIDTH, HEIGHT)
lineGraph.draw()

dropdown = Dropdown(sketch, 750, 100)
dropdown.draw()

# Draw the axes
bar_axis = Axis(sketch, WIDTH, HEIGHT)
bar_axis.draw_x_axis(60, 460, HEIGHT - 419)
bar_axis.draw_y_axis(137, HEIGHT - 75, 460)

line_axis = Axis(sketch, WIDTH, HEIGHT)
line_axis.draw_x_axis(550, 1050, HEIGHT - 75)
line_axis.draw_y_axis(550, HEIGHT - 75, 550)

stacked_axis = Axis(sketch, WIDTH, HEIGHT)
stacked_axis.draw_x_axis(1150, 1500, HEIGHT - 75)
stacked_axis.draw_y_axis(137, HEIGHT - 75, 1150)

# Show the sketch
sketch.show()
