import sketchingpy
import random
import math

WIDTH = 1600
HEIGHT = 900

TITLE = "California Energy Data (2022)"

SECTOR_COLORS = {
    "Residential": "#99a85c", # Green
    "Commercial": "#cac1d9",  # Light Purple
    "Industrial": "#f2d584",  # Yellow
    "Transportation": "#597da5",  # Blue
}

# Darker shades of corresponding sector colors
CAPITA_COLORS = {
    "Residential": "#6b7540", # Green
    "Commercial": "#a19aad",  # Light Purple
    "Industrial": "#c1aa69",  # Yellow
    "Transportation": "#3e5773",  # Blue
}


sketch = sketchingpy.Sketch2DApp(WIDTH, HEIGHT)
sketch.clear('#FFFFFF')


class LoadData:
    """Class for loading and managing data from CSV files."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.data = {}

    def load_ranked_data(self, filepath):
        """Load data from the use_tot_realgdp_2022 CSV file and return a dictionary."""
        csv_data = sketch.get_data_layer().get_csv(filepath)
        
        data = {}
        for row in csv_data[0:]:
            
            try:
                state = row["Full Names"].strip() 
                total_energy = row[" Total Energy Consumption (BTU) "].replace(',', '').strip()
                real_gdp = row[" Real GDP "].replace(',', '').strip()
                energy_per_gdp = row[" Energy Consumption per real GDP "].strip()

                total_energy = float(total_energy) if total_energy else 0
                real_gdp = float(real_gdp) if real_gdp else 0
                energy_per_gdp = float(energy_per_gdp) if energy_per_gdp else 0

                data[state] = {
                    "Total Energy Consumption (BTU)": total_energy,
                    "Real GDP": real_gdp,
                    "Energy Consumption per Real GDP": energy_per_gdp
                }
            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                continue  

        return data
    
    def load_sector_data(self, filepath):
        """Load sector data from the sector_2022 CSV file and return a dictionary."""
        csv_data = sketch.get_data_layer().get_csv(filepath)
        
        data = {}
        for row in csv_data[0:]:  
            try:
                sector = row["\ufeffSector"].strip()  
                value = row["2022"].replace(',', '').strip()

                value = float(value) if value else 0
                data[sector] = value

            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                continue
            except KeyError as e:
                print(f"Missing column in the CSV file: {e}")
                continue

        return data
    
    def load_renewable_data(self, filepath):
        """Load renewable energy data from the renewable_2022 CSV file and return a dictionary."""
        csv_data = sketch.get_data_layer().get_csv(filepath)
        
        data = {}
        for row in csv_data[0:5]:
            try:
                sector = row["\ufeffType"].strip()  
                value = row["2022"].replace(',', '').strip()

                value = float(value) if value else 0
                data[sector] = value

            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                continue
            except KeyError as e:
                print(f"Missing column in the CSV file: {e}")
                continue

        return data
    
    def load_ff_data(self, filepath):
        """Load fossil fuel data from the fossil_fuel CSV file and return a dictionary."""
        csv_data = sketch.get_data_layer().get_csv(filepath)
        
        data = {"Years": [], "Natural Gas": [], "Petroleum": []}
        for row in csv_data:
            try:
                if row["\ufeffType"].strip() == "Natural Gas":
                    data["Natural Gas"] = [float(row[year].replace(',', '').strip()) for year in row if year.isdigit()]
                elif row["\ufeffType"].strip() == "Petroleum":
                    data["Petroleum"] = [float(row[year].replace(',', '').strip()) for year in row if year.isdigit()]

            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                continue

            except KeyError as e:
                print(f"Missing column in the CSV file: {e}")
                continue

        # Extract years from the first row
        data["Years"] = [int(year) for year in csv_data[0] if year.isdigit()]
        return data
    
    def get_data(self):
        """Return the loaded data."""
        return self.data


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

    def draw_x_axis_title(self, x, y, title):
        """Draw the x-axis title."""
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('center', 'center')
        self.canvas.set_text_font('Arial', 18)
        self.canvas.draw_text(x, y, title)

    def draw_y_axis(self, y_start, y_end, x_base):
        """Draw the y-axis with optional tick marks and labels."""
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.draw_line(x_base, y_start, x_base, y_end)

    def draw_y_axis_title(self, x, y, title):
        """Draw the y-axis title."""
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('right', 'center')
        self.canvas.set_text_font('Arial', 16)
        self.canvas.draw_text(x, y, title)
    
    def draw_y_title_rotate(self, x, y, title):
        """Draw the y-axis title with rotation."""
        self.canvas.push_transform() 
        self.canvas.translate(x, y)  
        self.canvas.rotate(-90)  
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('center', 'center') 
        self.canvas.set_text_font('Arial', 16)
        self.canvas.draw_text(0, 0, title)  
        self.canvas.pop_transform()  
       

class Sector:
    """Creates a bar graph on the upper left side of the plot."""
    def __init__(self, canvas, width, height, data):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.data = data

    def draw(self):
        categories = ["Residential", "Commercial", "Industrial", "Transportation"]
        values = [self.data[category] for category in categories]

        # Bar graph dimensions
        bar_width = 50
        spacing = 40
        x_start = 95
        y_base = self.height - 419
        max_value = max(values)
        scale_factor = 300 / max_value

        # Draw the bar chart
        for i, (category, value) in enumerate(zip(categories, values)):
            x = x_start + i * (bar_width + spacing)
            bar_height = value * scale_factor  
            y = y_base - bar_height

            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill(SECTOR_COLORS[category])
            self.canvas.draw_rect(x, y, bar_width, bar_height)

        # Draw the legend
        self.canvas.set_stroke_weight(0)
        self.draw_legend(categories)

        # Draw the y-axis ticks
        self.draw_y_axis_ticks(y_base, y_base - 300, max_value)

    def draw_legend(self, categories):
        """Draw a horizontal legend at the top left."""
        legend_x_start = 40
        legend_y_start = 70
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

    def draw_y_axis_ticks(self, y_base, y_max, max_value):
        """Draw ticks and labels on the y-axis."""
        tick_spacing_value = 500000
        num_ticks = int(max_value / tick_spacing_value) + 1
        tick_spacing = (y_base - y_max) / num_ticks  
        
        for i in range(num_ticks + 1):
            y = y_base - i * tick_spacing
            value = i * tick_spacing_value

            # Draw the tick mark
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(450, y, 470, y)  

            # Draw the tick label
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("left", "center")
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(485, y, f"{int(value)}")  


class PerCapita:
    """Creates a bar graph on the lower left side of the plot."""
    def __init__(self, canvas, width, height, data):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.data = data
        
    def draw(self):
        categories = ["Residential", "Commercial", "Industrial", "Transportation"]
        values = [self.data[category] for category in categories]

        # Bar graph dimensions
        bar_width = 50
        spacing = 40
        x_start = 95
        y_base = self.height - 419
        max_value = max(values)
        scale_factor = 300 / max_value

        # Draw the bars upside down
        for i, (category, value) in enumerate(zip(categories, values)):
            x = x_start + i * (bar_width + spacing)
            bar_height = value * scale_factor 
            y = y_base + bar_height

            # Draw the bar upside down
            self.canvas.set_stroke("#000000")
            self.canvas.set_fill(CAPITA_COLORS[category])  # Use the same colors as Sector
            self.canvas.draw_rect(x, y - bar_height, bar_width, bar_height)  
        
        # Draw the y-axis ticks
        self.draw_y_axis_ticks(y_base, 75, max_value)
        
    def draw_y_axis_ticks(self, y_base, y_max, max_value):
        """Draw ticks and labels on the y-axis."""
        tick_spacing_value = 5  # Increment by 5
        num_ticks = int(max_value / tick_spacing_value) + 1
        tick_spacing = (y_max - y_base + 100) / max_value * tick_spacing_value  # Pixel spacing for each tick

        for i in range(num_ticks + 1):
            y = y_base - i * tick_spacing
            value = i * tick_spacing_value

            # Draw the tick mark
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(450, y, 470, y)  

            # Draw the tick label
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("left", "center")
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(485, y, f"{int(value)}")  


class RankedBar:
    """Creates a bar graph in the middle that ranks the states based on their total energy consumption."""
    def __init__(self, canvas, width, height, data):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.data = data
        self.criteria = "Total Energy Consumption (BTU)"  # Default criteria

    def set_criteria(self, criteria):
        """Set the criteria for ranking the states based on user selection."""
        self.criteria = criteria   

        # Clear and redraw ranked chart
        x_base = 1150
        y_start = 115
        bar_area_width = 400
        bar_area_height = self.height 
        self.canvas.set_fill('#FFFFFF')
        self.canvas.draw_rect(x_base - 10, y_start - 10, bar_area_width, bar_area_height)
        self.draw() 

        # Redraw the x and y axes
        bar_axis = Axis(self.canvas, self.width, self.height)
        bar_axis.draw_x_axis(1150, 1500, self.height - 75)  
        bar_axis.draw_y_axis(132, self.height - 75, 1150)  
        stacked_axis.draw_x_axis_title(1325, 870, "Consumption Estimates (billion BTU)")

    def draw(self):
        # Sort states by the selected criteria
        sorted_states = sorted(self.data.items(), key=lambda x: x[1][self.criteria], reverse=True)
        max_value = max([values[self.criteria] for _, values in sorted_states])
        scale_factor = 315 / max_value

        # Bar graph dimensions
        bar_height = 6
        spacing = 7.25
        x_base = 1150
        y_start = 132
        y_end = self.height - 50

        # Draw the bars
        for i, (state, values) in enumerate(sorted_states):
            y = y_start + i * (bar_height + spacing)
            x = x_base 
            value = values[self.criteria] * scale_factor

            # Make California stand out compared to other states
            if state == "California" or state == "CA":
                self.canvas.set_fill("#fa0b0b")  # Red for California
            else:
                self.canvas.set_fill("#d0d0d0")  # Gray for other states

            # Draw the bar
            self.canvas.set_stroke("#000000")  
            self.canvas.set_stroke_weight(0)
            self.canvas.draw_rect(x, y + 10, value, bar_height)

             # Draw the state label to the right of the bar
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("left", "center")  # Align text to the left
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(x + value + 10, y + bar_height / 2 + 10, state)  
    
        self.draw_x_axis_counts(x_base, y_end, bar_height, spacing, max_value, scale_factor)

    # Draw the x-axis labels
    def draw_x_axis_counts(self, x_base, y_end, bar_height, spacing, max_value, scale_factor):
        """Draw counts on the x-axis for the RankedBar graph."""
        # Draw the ticks and labels
        num_ticks = 4  
        tick_spacing = 315 / num_ticks  
        tick_spacing_value = max_value / num_ticks

        for i in range(num_ticks + 1):
            x = x_base + i * tick_spacing
            value = i * tick_spacing_value

            # Draw the tick
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(x, y_end - 30, x, y_end - 20)

            # Draw the tick label
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("center", "top")
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(x, y_end - 15, f"{value:,.2f}" if isinstance(value, float) else f"{int(value):,}")

        # Draw the x-axis label
        self.canvas.set_stroke_weight(0)
        self.canvas.set_fill("#000000")
        self.canvas.set_text_align("center", "bottom")
        self.canvas.set_text_font("Arial", 12)


class RadarChart:
    """Creates a radar chart for visualizing the renewable energy consumption."""
    def __init__(self, canvas, width, height, data):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.data = data

    def draw(self):
        renewables = list(self.data.keys())
        values = list(self.data.values())
        max_value = max(values)
        
        # Radar chart dimensions
        center_x = self.width / 2 + 10
        center_y = 350
        radius = 180
        axis_extension = 10

        # Pentagon grid
        num_vertices = 5  
        increment =  125000
        num_levels = int(max_value / increment) + 1
        
        for level in range(1, num_levels + 1):
            r = (level / num_levels) * radius
            points = []
            for i in range(num_vertices):
                angle = (2 * math.pi / num_vertices) * i - math.pi / 2  # Start at the top
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
                points.append((x, y))
            # Connect the vertices
            self.canvas.set_stroke("#cccccc")  # Light gray for the grid
            self.canvas.set_stroke_weight(2)
            for j in range(len(points)):
                x1, y1 = points[j]
                x2, y2 = points[(j + 1) % len(points)]  # Wrap around to the first point
                self.canvas.draw_line(x1, y1, x2, y2)
        
            # Add number labels for each layer
            layer_value = level * increment
            label_x = center_x + 20
            label_y = center_y - r - 5  # Position the label next to the vertical axis
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("center", "center")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(label_x, label_y, f"{int(layer_value)}")


        # Draw the radar axes
        num_renewables = len(renewables)
        for i in range(num_renewables):
            angle = (2 * math.pi / num_renewables) * i - math.pi / 2  
            x = center_x + (radius + axis_extension) * math.cos(angle)
            y = center_y + (radius + axis_extension) * math.sin(angle)
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(center_x, center_y, x, y)

            # Add category labels
            label_x = center_x + (radius + 40) * math.cos(angle)
            label_y = center_y + (radius + 40) * math.sin(angle)
            self.canvas.set_fill("#000000")
            self.canvas.set_text_align("center", "center")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_font("Arial", 14)
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
        self.canvas.set_stroke("#0ec30e")  # Green
        self.canvas.set_stroke_weight(2)
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)] 
            self.canvas.draw_line(x1, y1, x2, y2)

        # Draw the data points
        for x, y in points:
            self.canvas.set_fill("#0ec30e")
            self.canvas.draw_ellipse(x, y, 3, 3) 


class LineGraph:
    """Creates a line graph for visualizing the petroleum and natural gas consumption over the years."""
    def __init__(self, canvas, width, height, data):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.data = data

    def draw(self):
        years = self.data["Years"]
        natural_gas = self.data["Natural Gas"]
        petroleum = self.data["Petroleum"]
        max_value = max(max(natural_gas), max(petroleum))

        # Line graph dimensions
        graph_x_start = 605
        graph_x_end = 1050
        graph_y_start = 800
        graph_y_end = 500

        # Scale the data to fit within the graph dimensions
        x_spacing = (graph_x_end - graph_x_start) / (len(years) - 1)
        y_scale = (graph_y_start - graph_y_end) / max_value * 0.7

        # Plot the data points and connect them with lines
        points_ng = []
        for i, value in enumerate(natural_gas):
            x = graph_x_start + i * x_spacing
            y = graph_y_start - value * y_scale
            points_ng.append((x, y))

            # Draw the data point
            self.canvas.set_fill("#e87e2b") # Orange
            self.canvas.draw_ellipse(x, y, 1, 1)  

        # Connect the points with lines
        self.canvas.set_stroke("#e87e2b")
        self.canvas.set_stroke_weight(2)
        for i in range(len(points_ng) - 1):
            x1, y1 = points_ng[i]
            x2, y2 = points_ng[i + 1]
            self.canvas.draw_line(x1, y1, x2, y2)
        
        # Draw the data points
        for x, y in points_ng:
            self.canvas.set_fill("#e87e2b")
            self.canvas.draw_ellipse(x, y, 1, 1) 

        # Plot the data points and connect them with lines
        points_p = []
        for i, value in enumerate(petroleum):
            x = graph_x_start + i * x_spacing
            y = graph_y_start - value * y_scale
            points_p.append((x, y))

            # Draw the data point
            self.canvas.set_fill("#a649a6") # Orange
            self.canvas.draw_ellipse(x, y, 1, 1)  

        # Connect the points with lines
        self.canvas.set_stroke("#a649a6")
        self.canvas.set_stroke_weight(2)
        for i in range(len(points_p) - 1):
            x1, y1 = points_p[i]
            x2, y2 = points_p[i + 1]
            self.canvas.draw_line(x1, y1, x2, y2)
        
        # Draw the data points
        for x, y in points_p:
            self.canvas.set_fill("#a649a6")
            self.canvas.draw_ellipse(x, y, 1, 1) 
        
        # Draw x-axis ticks for every 20 years
        start_year = years[0]
        end_year = years[-1]
        for year in range(start_year, end_year + 1, 10):
            index = years.index(year)  
            x = graph_x_start + index * x_spacing
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(x, graph_y_start + 20, x, graph_y_start + 30)  

            # Draw the year label
            self.canvas.set_fill("#000000")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_align("center", "top")
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(x, graph_y_start + 35, str(year))

        # Draw y-axis labels
        tick_spacing_value = 20
        max_value = ((max_value // tick_spacing_value) + 1) * tick_spacing_value  
        num_ticks = int(max_value / tick_spacing_value) 
        tick_spacing = (graph_y_start - graph_y_end - 15) / num_ticks

        for i in range(num_ticks):
            y = graph_y_start + 25 - i * tick_spacing
            value = i * tick_spacing_value

            # Draw the tick mark
            self.canvas.set_stroke("#000000")
            self.canvas.set_stroke_weight(2)
            self.canvas.draw_line(graph_x_start - 10, y, graph_x_start, y)  # Tick mark

            # Draw the value label
            self.canvas.set_fill("#000000")
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_align("right", "center")
            self.canvas.set_text_font("Arial", 10)
            self.canvas.draw_text(graph_x_start - 15, y, f"{int(value)}")
    

class DropdownRank:
    """Creates a dropdown menu for selecting ranking criteria."""
    def __init__(self, canvas, x, y, width, height, options, callback):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options  
        self.callback = callback  
        self.selected_option = options[0]  # Default to the first option
        self.is_expanded = False  # Track if the dropdown is expanded

    def draw(self):
        """Draws the dropdown box and the selected option."""
        # Draw the dropdown box
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.set_fill('#FFFFFF')
        self.canvas.draw_rect(self.x, self.y, self.width, self.height)

        # Draw the selected option
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('center', 'center')
        self.canvas.set_text_font('Arial', 12)
        self.canvas.draw_text(self.x + self.width / 2, self.y + self.height / 2, self.selected_option)

        # If expanded, draw the dropdown options
        if self.is_expanded:
            for i, option in enumerate(self.options):
                option_y = self.y + (i + 1) * self.height
                self.canvas.set_stroke('#000000')
                self.canvas.set_stroke_weight(2)
                self.canvas.set_fill('#FFFFFF')
                self.canvas.draw_rect(self.x, option_y, self.width, self.height)

                # Draw the option text
                self.canvas.set_fill('#000000')
                self.canvas.set_stroke_weight(0)
                self.canvas.set_text_align('center', 'center')
                self.canvas.set_text_font('Arial', 12)
                self.canvas.draw_text(self.x + self.width / 2, option_y + self.height / 2, option)
        
        elif self.is_expanded == False:
            self.canvas.set_fill('#000000')
            self.canvas.set_stroke_weight(0)
            self.canvas.set_text_align('center', 'center')
            self.canvas.set_text_font('Arial', 12)
            self.canvas.draw_text(self.x + self.width / 2, self.y + self.height / 2, self.selected_option)

    def on_click(self, x, y):
        """Handle mouse click events."""
        # Check if the click is within the dropdown box
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            # Toggle the dropdown expansion
            self.is_expanded = not self.is_expanded
        elif self.is_expanded:
            # Check if an option is clicked
            for i, option in enumerate(self.options):
                option_y = self.y + (i + 1) * self.height
                if self.x <= x <= self.x + self.width and option_y <= y <= option_y + self.height:
                    # Update the selected option and collapse the dropdown
                    self.selected_option = option
                    self.is_expanded = False
                    self.callback(self.selected_option) 
                    break
        else:
            # Collapse the dropdown if clicked outside
            self.is_expanded = False


def draw_title(title):
    """Draw the title for the bar graph."""
    sketch.set_text_font('Arial', 36)
    sketch.set_text_align('center', 'bottom')
    sketch.set_fill('#000000')
    sketch.draw_text(WIDTH/2, 60, title)

def draw_explanation(x, y, title):
    """Draw any explanations needed for the visualization"""
    sketch.set_text_font('Arial', 12)
    sketch.set_text_align('right', 'center')
    sketch.set_fill('#000000')
    sketch.set_stroke_weight(0)
    sketch.draw_text(x, y, title)

# Load the data
load_data = LoadData(sketch)

USE_TOT_REALGDP_2022 = load_data.load_ranked_data('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/Final Project/data/csv/use_tot_realgdp_2022.csv')
SECTOR_T0T_2022 = load_data.load_sector_data('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/Final Project/data/csv/sector_2022.csv')
SECTOR_PRICES_2022 = load_data.load_sector_data('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/Final Project/data/csv/sector_prices_2022.csv')
RENEWABLE_2022 = load_data.load_renewable_data('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/Final Project/data/csv/renewable_2022.csv')
FOSSIL_FUEL = load_data.load_ff_data('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/Final Project/data/csv/fossil_fuel.csv')

# Draw the title
draw_title(TITLE)

# Draw the explanation
BTU_EXPLANATION = "BTU: British Thermal Unit"
draw_explanation(477, 870, BTU_EXPLANATION)

# Draw the graphs
sector = Sector(sketch, WIDTH, HEIGHT, SECTOR_T0T_2022)
sector.draw()

perCapita = PerCapita(sketch, WIDTH, HEIGHT, SECTOR_PRICES_2022)
perCapita.draw()

rankedBar = RankedBar(sketch, WIDTH, HEIGHT, USE_TOT_REALGDP_2022)
rankedBar.draw()

radar = RadarChart(sketch, WIDTH, HEIGHT, RENEWABLE_2022)
radar.draw()

lineGraph = LineGraph(sketch, WIDTH, HEIGHT, FOSSIL_FUEL)
lineGraph.draw()

# Create the dropdown
dropdown = DropdownRank(sketch, 1225, 85, 200, 20, [
    'Total Energy Consumption (BTU)',
    'Real GDP',
    'Energy Consumption per Real GDP'
], rankedBar.set_criteria)

dropdown.draw()

# Handle mouse button presses
def on_click(button):
    """Handle mouse button presses."""
    mouse = sketch.get_mouse()
    x, y = mouse.get_pointer_x(), mouse.get_pointer_y()
    dropdown.on_click(x, y)  
    dropdown.draw()

# Set up the sketch to handle mouse button presses
sketch.get_mouse().on_button_press(on_click)

# Draw the axes
bar_axis = Axis(sketch, WIDTH, HEIGHT)
bar_axis.draw_x_axis(60, 460, HEIGHT - 419)
bar_axis.draw_y_axis(137, HEIGHT - 75, 460)
bar_axis.draw_y_axis_title(475, 120, "Energy Consumption (billion BTU)")
bar_axis.draw_y_axis_title(475, 840, "Average Energy Prices ($/million BTU)")

radar_axis = Axis(sketch, WIDTH, HEIGHT)
radar_axis.draw_x_axis_title(800, 95, "Renewable Energy Consumption (billion BTU)")

line_axis = Axis(sketch, WIDTH, HEIGHT)
line_axis.draw_x_axis(600, 1070, HEIGHT - 75)
line_axis.draw_x_axis_title(800, 870, "Years")
line_axis.draw_y_axis(550, HEIGHT - 75, 600)
line_axis.draw_y_title_rotate(550, 690, "Consumption Per Capita (million BTU)")

stacked_axis = Axis(sketch, WIDTH, HEIGHT)
stacked_axis.draw_x_axis(1150, 1500, HEIGHT - 75)
stacked_axis.draw_x_axis_title(1325, 870, "Consumption Estimates (billion BTU)")
stacked_axis.draw_y_axis(137, HEIGHT - 75, 1150)
stacked_axis.draw_y_title_rotate(1120, 481, "States")

# Show the sketch
sketch.show()
