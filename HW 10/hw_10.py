import sketchingpy
import data_model
import math
import pandas as pd
from collections import defaultdict

WIDTH = 1500
HEIGHT = 800

IS_ONLINE = False

TITLE = 'The Different Factors of Wages'

PATH = '/Users/daniellelouie/Documents/Berkeley/2024-2025/stat-198/HW 9/data.csv'

def age_group_to_midpoint(age_group):
    age_ranges = {
        '<25 yr': 20,
        '25-35 yr': 30,
        '35-45 yr': 40,
        '45-55 yr': 50,
        '55-65 yr': 60,
        '65+ yr': 70
    }
    return age_ranges.get(age_group, 0) 

def scale_value(value, min_value, max_value, min_canvas, max_canvas):
    return ((value - min_value) / (max_value - min_value)) * (max_canvas - min_canvas) + min_canvas

def scale_proportion(proportion):
    # Exponential scaling for more drastic size differences
    min_size = 0.1
    max_size = 1
    return min_size + ((proportion - 0.2) ** 2) * (max_size - min_size) / ((0.5 - 0.2) ** 2)


class GenderColor:
    def __init__(self, dataset):
        self.dataset = dataset

    def gender_color(self, is_female):
        if is_female:
            color = '#9d8cd6' # light purple
        else:
            color = '#a6c36f' # light green
        return color
    

class HoursColor:
    def __init__(self, dataset):
        self.dataset = dataset
    
    def hours_color(self, hours):
        if hours == 'At Least 35 Hours':
            color = '#e09f8f' # salmon pink
        elif hours == 'Less than 35 Hours':
            color = '#a17d49' # brown
        elif hours == 'Varies or Other':
            color = '#506587'  # navy blue
        else:
            color = None  # No color if it doesn't match any condition
        return color
    

class BarGraph:
    """Creates a bargraph on the left side of the plot. Plots the difference in 
    wages for different races based on the hours worked."""
    def __init__(self, dataset, canvas):
        self.dataset = dataset
        self.canvas = canvas
        self.hours_color = HoursColor(dataset)
        self.hours_order = ['At Least 35 Hours', 'Less than 35 Hours', 'Varies or Other']

    def draw(self):
        min_wage = 0
        max_wage = 40

        self.draw_hours_legend()
        self.draw_race_title('Race')

        avg_wages = defaultdict(lambda: defaultdict(list))

        for record in self.dataset._records_by_id.values():
            race = record.get_wbhaom()
            hours_data = record.get_hoursuint()
            wage = float(record.get_wageotc()[0].get_wage())
            avg_wages[race][hours_data].append(wage)

        bar_width = 12
        bar_spacing = 10
        bar_group_spacing = 20
        chart_height = 300
        x_offset = 120
        y_offset = 374

        self.canvas.push_style()
        self.canvas.translate(x_offset, y_offset)
        self.canvas.set_text_font('Arial', 12)
        self.canvas.set_text_align('center', 'top')
        self.canvas.set_fill('#000000')

        races = list(avg_wages.keys())
        for i, race in enumerate(races):
            x = i * (bar_width + bar_spacing) * len(self.hours_order) + i * bar_group_spacing
            self.canvas.push_transform()
            self.canvas.translate(x + (bar_width + bar_spacing) * len(self.hours_order) / 2, chart_height + 20)
            self.canvas.rotate(-30)
            self.canvas.set_stroke_weight(0)
            self.canvas.set_fill('#000000')
            self.canvas.draw_text(-20, 2, race)
            self.canvas.pop_transform()
            for hours in self.hours_order:
                wages = avg_wages[race][hours]
                if wages:
                    avg_wage = sum(wages) / len(wages)
                    scaled_wage = scale_value(avg_wage, min_wage, max_wage, 0, chart_height)
                    color = self.hours_color.hours_color(hours)
                    if color:
                        self.canvas.set_fill(color)
                        self.canvas.draw_rect(x, chart_height - scaled_wage, bar_width, scaled_wage)
                x += bar_width + bar_spacing

        self.canvas.pop_style()

    def draw_race_title(self, title):
        """Draw the title for race."""
        self.canvas.push_transform()
        self.canvas.push_style()
       
        self.canvas.set_text_font('Arial', 20)
        self.canvas.set_text_align('center', 'top')
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.draw_text(340, 750, title)

        self.canvas.pop_style()
        self.canvas.pop_transform()

    def draw_hours_legend(self):
        """Draw the legend for the bar graph."""
        self.canvas.push_transform()
        self.canvas.push_style()

        self.canvas.translate(50, 100)  

        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('left', 'center')
        self.canvas.set_fill('#000000')
        
        # Title for Hours
        self.canvas.set_fill('#000000')
        self.canvas.set_text_font('Arial', 16)
        self.canvas.draw_text(0, 0, 'Hours Worked')

        # Legend for At Least 35 Hours
        self.canvas.set_text_font('Arial', 14)
        self.canvas.translate(0, 30)
        self.canvas.set_fill('#e09f8f')  
        self.canvas.draw_rect(0, 0, 10, 10)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(20, 7, 'At Least 35 Hours')

        # Legend for Less than 35 Hours
        self.canvas.translate(0, 30)
        self.canvas.set_fill('#a17d49') 
        self.canvas.draw_rect(0, 0, 10, 10)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(20, 7, 'Less than 35 Hours')

        # Legend for Varies or Other
        self.canvas.translate(0, 30)
        self.canvas.set_fill('#506587') 
        self.canvas.draw_rect(0, 0, 10, 10)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(20, 7, 'Varies or Other')

        self.canvas.pop_style()
        self.canvas.pop_transform()

class ScatterPlot:
    """Creates a scatterplot on the right side of the plot."""
    def __init__(self, dataset, width, height):
        self.dataset = dataset
        self.width = width
        self.height = height
        self.gender_color = GenderColor(dataset)
        self.canvas = sketchingpy.Sketch2D(width, height, TITLE)
        self.bar_graph = BarGraph(dataset, self.canvas)

    def draw(self):
        min_age = 20
        max_age = 70
        min_wage = 0
        max_wage = 40

        self.canvas.clear("#ffffff")
        self.draw_title(TITLE)
        self.draw_age_graph()
        self.draw_y_axis(min_wage, max_wage)
        self.draw_age_title('Age Group')
        self.draw_y_axis_title('Average Wage (Hourly)')
        self.draw_legend(min_wage, max_wage)

        avg_wages = defaultdict(lambda: {True: [], False: []})
        total_counts = defaultdict(lambda: {True: 0, False: 0})
        college_counts = defaultdict(lambda: {True: 0, False: 0})

        for record in self.dataset._records_by_id.values():
            age_group = record.get_age()
            wage = float(record.get_wageotc()[0].get_wage())
            is_female = record.get_female()
            avg_wages[age_group][is_female].append(wage)
            education_level = record.get_educ()
            total_counts[age_group][is_female] += 1
            if education_level in ['College', 'Advanced']:
                college_counts[age_group][is_female] += 1

        for age_group, gender_data in avg_wages.items():
            for is_female, wages in gender_data.items():
                avg_wage = sum(wages) / len(wages)
                age = scale_value(age_group_to_midpoint(age_group), min_age, max_age, 750, WIDTH - 350)
                wage = scale_value(avg_wage, min_wage, max_wage, HEIGHT - 150, 150)

                color = self.gender_color.gender_color(is_female)
                self.canvas.set_fill(color)

                # Adjust the size based on proportion of college+ in age + gender group
                proportion = college_counts[age_group][is_female] / total_counts[age_group][is_female]
                scaled_proportion = scale_proportion(proportion)
                ellipse_size = scale_value(scaled_proportion, 0, 1, 5, 30)  
                self.canvas.draw_ellipse(age, wage, ellipse_size, ellipse_size)
        
        self.bar_graph.draw()

        self.canvas.show()

    def draw_age_graph(self):
        """Draw the x-axis with age labels."""
        self.canvas.push_transform()
        self.canvas.push_style()

        # draw x-axis line
        self.canvas.set_stroke_weight(2)
        self.canvas.draw_line(100, self.height - 125, self.width - 275, self.height - 125)

        self.canvas.translate(0, self.height - 75)  

        self.canvas.set_text_font('Arial', 16)
        self.canvas.set_text_align('center', 'top')
        self.canvas.set_fill('#000000')

        # Draw age labels
        age_labels = ['<25 yr', '25-35 yr', '35-45 yr', '45-55 yr', '55-65 yr', '65+ yr']
        min_age = 20
        max_age = 70
        for label in age_labels:
            self.canvas.set_stroke_weight(1)
            x = scale_value(age_group_to_midpoint(label), min_age, max_age, 750, WIDTH - 350)
            self.canvas.set_stroke('#d3d3d3')  
            self.canvas.draw_line(x, -self.height + 200, x, -52)
            self.canvas.draw_text(x, -25, label)

        self.canvas.pop_style()
        self.canvas.pop_transform()

    def draw_age_title(self, title):
        """Draw the title for the x-axis."""
        self.canvas.push_transform()
        self.canvas.push_style()
       
        self.canvas.set_text_font('Arial', 20)
        self.canvas.set_text_align('center', 'top')
        self.canvas.set_fill('#000000')
        self.canvas.set_stroke_weight(0)
        self.canvas.draw_text(950, self.height - 50, title)

        self.canvas.pop_style()
        self.canvas.pop_transform()
    
    def draw_y_axis(self, min_wage, max_wage):
        """Draw the y-axis with wage labels."""
        self.canvas.push_transform()
        self.canvas.push_style()

        # draw y-axis line
        self.canvas.set_stroke('#000000')
        self.canvas.set_stroke_weight(2)
        self.canvas.draw_line(670, 125, 670, self.height - 125)

        self.canvas.translate(670, 0)  

        self.canvas.set_text_font('Arial', 16)
        self.canvas.set_text_align('right', 'center')
        self.canvas.set_fill('#000000')

        # Draw wage labels
        wage_interval = 5
        current_wage = (min_wage // wage_interval) * wage_interval
        while current_wage <= max_wage:
            self.canvas.set_stroke_weight(1)
            y = scale_value(current_wage, min_wage, max_wage, HEIGHT - 125, 150)
            self.canvas.set_stroke('#d3d3d3') 
            if current_wage == 0:
                # draw '0' at the origin
                self.canvas.draw_text(15, y + 30, f'{current_wage:.2f}') 
            else:
                self.canvas.draw_text(-10, y, f'{current_wage:.2f}')  
                self.canvas.draw_line(2, y, self.width - 950, y)
            current_wage += wage_interval

        self.canvas.pop_style()
        self.canvas.pop_transform()

    def draw_y_axis_title(self, title):
        """Draw the title for the y-axis."""
        self.canvas.push_transform()
        self.canvas.push_style()
    
        self.canvas.set_text_font('Arial', 18)
        self.canvas.set_text_align('center', 'center')
        self.canvas.set_stroke_weight(0)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(670, 100, title)

        self.canvas.pop_style()
        self.canvas.pop_transform()

    def draw_legend(self, min_wage, max_wage):
        """Draw the legend for the scatter plot."""
        self.canvas.push_transform()
        self.canvas.push_style()

        self.canvas.translate(self.width - 230, 70)  

        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_align('left', 'center')
        self.canvas.set_fill('#000000')
        
        # Title for Gender
        self.canvas.set_fill('#000000')
        self.canvas.set_text_font('Arial', 16)
        self.canvas.draw_text(0, 0, 'Gender')

        # Legend for female
        self.canvas.set_text_font('Arial', 14)
        self.canvas.translate(0, 30)
        self.canvas.set_fill('#9d8cd6')  
        self.canvas.draw_ellipse(0, 0, 10, 10)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(20, 0, 'Female')

        # Legend for male
        self.canvas.translate(0, 30)
        self.canvas.set_fill('#a6c36f') 
        self.canvas.draw_ellipse(0, 0, 10, 10)
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(20, 0, 'Male')

        # Legend for circle sizes
        self.canvas.translate(0, 60)
        self.canvas.set_fill('#000000')
        self.canvas.set_text_font('Arial', 16)
        self.canvas.draw_text(0, 0, 'Proportion of College or More')

        self.canvas.set_stroke_weight(0)
        self.canvas.set_text_font('Arial', 14)
        proportions = [0.2, 0.3, 0.4, 0.5]
        for proportion in proportions:
            self.canvas.translate(0, 50)
            scaled_proportion = scale_proportion(proportion)
            ellipse_size = scale_value(scaled_proportion, 0, 1, 5, 20)  # Increased max size to 100
            self.canvas.set_fill('#000000')
            self.canvas.draw_ellipse(0, 0, ellipse_size, ellipse_size)
            self.canvas.draw_text(30, 0, f'{proportion:.2f}')

        self.canvas.pop_style()
        self.canvas.pop_transform()

    def draw_title(self, title):
        """Draw the title for the scatter plot."""
        self.canvas.push_transform()
        self.canvas.push_style()

        self.canvas.set_text_font('Arial', 28)
        self.canvas.set_text_align('center', 'bottom')
        self.canvas.set_fill('#000000')
        self.canvas.draw_text(self.width / 2 - 65, 60, title)

        self.canvas.pop_style()
        self.canvas.pop_transform()


if IS_ONLINE:
    sketch = sketchingpy.Sketch2D(WIDTH, HEIGHT)
else:
    sketch = sketchingpy.Sketch2DStatic(WIDTH, HEIGHT)

sketch.clear("#ffffff")
dataset = data_model.load_from_file(PATH)

scatter_plot = ScatterPlot(dataset, WIDTH, HEIGHT)
scatter_plot.draw()

if IS_ONLINE:
    sketch.show()
else:
    sketch.save_image('assignment_9_scatter.png')
