"""Graphic depicting change in fuel standards over time.

Graphic depicting change in fuel standards over time using the data first
provided in "Fuel Economy Standards for Autos" by New York Times, 1978.

Part of https://interactivedatascience.courses.

Author: A Samuel Pottinger
License: BSD-3-Clause
"""

import sketchingpy

# Range of variables (year and standards)
START_YEAR = 1978
END_YEAR = 1985
MIN_STANDARD = 0  # mpg
MAX_STANDARD = 27.5  # mpg

# Text to display within the visualization
TITLE = 'Fuel Standards from 1978 to 1985'
START_YEAR_ANNOTATION = 'First year of standards'
END_YEAR_ANNOTATION = 'Goal'
MIN_ANNOTATION = "%.1f mpg"
GOAL_ANNOTATION = '%.1f mpg ECPA target'

# Colors for text and background
DARK_COLOR = '#000000'
LIGHT_COLOR = '#606060'
BACKGROUND_COLOR = '#F0F0F0'

# Constants for fonts
HUGE_SIZE = 24  # px
LARGE_SIZE = 18  # px
SMALL_SIZE = 12  # px
FONT = 'PublicSans-Regular'

# Constants for sizing
WIDTH = 600  # px
HEIGHT = 400  # px
LEFT_PAD = 10  # px
RIGHT_PAD = 10  # px
BOTTOM_PAD = 15  # px
TOP_PAD = 55  # px


class FuelStandardChange:
    """Object representing a change in fuel standards.

    Record of a change in fuel standards with a year in which that standard came
    into force and the standard level.
    """

    def __init__(self, year, standard):
        """Make a new record of a standard change.

        Args:
            year: The year like 1985 in which the standard came into force.
            standard: The standard starting in the year as miles per gallon.
        """
        self._year = year
        self._standard = standard

    def get_year(self):
        """Get the year in which the standard came into force.

        Returns:
            The year like 1985 in which the standard came into force.
        """
        return self._year

    def get_standard(self):
        """Get the new fuel economy standard.

        Returns:
            The standard starting in this year as miles per gallon.
        """
        return self._standard


class FuelStandardVizPresenter:
    """Object representing the fuel standard visualization."""

    def __init__(self, changes):
        """Create a new fuel standards visualization.

        Args:
            changes: List of FuelStandardChanges to visualize.
        """
        self._changes = changes

    def draw(self, sketch):
        """Draw the visualization.

        Args:
            sketch: The sketch in which to draw the visualization.
        """
        self._draw_title(sketch)
        self._draw_axis(sketch)

        for change in self._changes:
            year = change.get_year()

            align = self._determine_align(year)
            highlight = self._determine_highlight(year)
            annotation = self._determine_annotation(year)

            self._draw_change(sketch, change, align, highlight, annotation)

    def _determine_align(self, year):
        """Determine how the text should be aligned for a year.

        Args:
            year: The year for which alignment should be determined.

        Returns:
            One of the following horizontal alignment options: left, right, or
            center.
        """
        if year == START_YEAR:
            return 'left'
        elif year == END_YEAR:
            return 'right'
        else:
            return 'center'

    def _determine_highlight(self, year):
        """Determine if a year should be given a highlight style treatment.

        Args:
            year: The year for which highlight status should be determined.

        Returns:
            True if higher contrast styling should be used to "highlight" the
            results of this year. False otherwise.
        """
        if year == START_YEAR:
            return True
        elif year == END_YEAR:
            return True
        else:
            return False

    def _determine_annotation(self, year):
        """Determine what annotation if any should be added for the given year.
        
        Args:
            year: The year for which an annotation should be returned.

        Returns:
            Annotation text to display next to results for the given year or
            None if no annotation should be added.
        """
        if year == START_YEAR:
            return START_YEAR_ANNOTATION
        elif year == END_YEAR:
            return END_YEAR_ANNOTATION
        else:
            return None

    def _draw_title(self, sketch):
        """Draw the visualization title.

        Args:
            sketch: The sketch in which the title should be drawn.
        """
        sketch.push_style()

        sketch.clear_stroke()
        sketch.set_fill(DARK_COLOR)
        sketch.set_text_align('left', 'bottom')
        sketch.set_text_font(FONT, HUGE_SIZE)
        sketch.draw_text(LEFT_PAD, TOP_PAD - 18, TITLE)

        sketch.pop_style()

    def _draw_axis(self, sketch):
        """Draw the left side axis which clarifies start / end standards.

        Args:
            sketch: The sketch in which to draw the axis.
        """
        sketch.push_style()
        
        sketch.set_text_font(FONT, SMALL_SIZE)

        min_y = self._get_y(MIN_STANDARD)

        sketch.clear_stroke()
        sketch.set_fill(LIGHT_COLOR)
        sketch.set_text_align('left', 'top')
        min_str = MIN_ANNOTATION % MIN_STANDARD
        sketch.draw_text(LEFT_PAD, min_y, min_str)

        sketch.set_stroke(LIGHT_COLOR)
        sketch.clear_fill()
        sketch.draw_line(LEFT_PAD, min_y, LEFT_PAD + 20, min_y)

        max_y = self._get_y(MAX_STANDARD)

        sketch.clear_stroke()
        sketch.set_fill(LIGHT_COLOR)
        sketch.set_text_align('left', 'bottom')
        goal_str = GOAL_ANNOTATION % MAX_STANDARD
        sketch.draw_text(LEFT_PAD, max_y - 1, goal_str)

        sketch.set_stroke(LIGHT_COLOR)
        sketch.clear_fill()
        sketch.draw_line(LEFT_PAD, max_y, LEFT_PAD + 20, max_y)

        sketch.pop_style()

    def _draw_change(self, sketch, change, align, highlight, annotation):
        """Draw an individual change in fuel economy standards.

        Args:
            sketch: The sketch in which the change should be drawn.
            change: The FuelStandardChange to draw.
            align: String describing the horizontal alignment to use when
                drawing this change.
            highlight: Flag that indicates if this year should be drawn in
                high contrast "highlight" styling. True if highlight should be
                used and false otherwise.
            annotation: The annotation to display next to this year's results
                or None if no annotation should be added.
        """
        sketch.push_style()

        sketch.clear_stroke()
        if highlight:
            sketch.set_fill(DARK_COLOR)
        else:
            sketch.set_fill(LIGHT_COLOR)

        year = change.get_year()
        standard = change.get_standard()
        x = self._get_x(year)
        y = self._get_y(standard)

        sketch.set_text_font(FONT, SMALL_SIZE)
        sketch.set_text_align(align, 'bottom')
        sketch.draw_text(x, y - LARGE_SIZE / 2 - 2, year)

        sketch.set_text_font(FONT, LARGE_SIZE)
        sketch.set_text_align(align, 'center')
        sketch.draw_text(x, y, '%.1f' % standard)
        
        if annotation:
            sketch.set_text_font(FONT, SMALL_SIZE)
            sketch.set_text_align(align, 'top')
            sketch.draw_text(x, y + SMALL_SIZE / 2 + 2, annotation)

        sketch.pop_style()

    def _get_x(self, year):
        """Get horizontal position at which a year's results should be drawn.
        
        Get horizontal position at which a year's results should be drawn where
        the minimum year is at the left side (LEFT_PAD) and the maximum year is
        at the right side (WIDTH - RIGHT) which corresponds to the minimum and
        maximum x coordinate of the chart body respectively.

        Args:
            year: The integer year for which an x position is requested.

        Returns:
            The x position in pixels at which the year should be drawn.
        """
        year_range = END_YEAR - START_YEAR
        percent_offset = (year - START_YEAR) / year_range
        working_width = WIDTH - LEFT_PAD - RIGHT_PAD
        pixel_offset = percent_offset * working_width
        return LEFT_PAD + pixel_offset

    def _get_y(self, standard):
        """Get vertical position at which a year's results should be drawn.
        
        Get vertical position at which standard's results should be drawn where
        the minimum standard is at the bottom side (HEIGHT - BOTTOM_PAD) and the
        maximum standard is at the top side (TOP_PAD) which corresponds to the
        maximum and minimum y coordinate of the chart body respectively.

        Note that, to have larger values at higher positions, the smallest
        standards in mpg are at the largest y coordinates.

        Args:
            year: The float standard (mpg) for which a y position is requested.

        Returns:
            The y position in pixels at which the standard should be drawn.
        """
        standard_range = MAX_STANDARD - MIN_STANDARD
        percent_offset = (standard - MIN_STANDARD) / standard_range
        percent_offset_reverse = 1 - percent_offset
        working_height = HEIGHT - TOP_PAD - BOTTOM_PAD
        pixel_offset = percent_offset_reverse * working_height
        return TOP_PAD + pixel_offset


def parse_fuel_standard_change(raw_datum):
    """Parse a raw CSV row as a FuelStandardChange.

    Args:
        raw_datum: Raw CSV row to parse.

    Returns:
        The row represented as a FuelStandardChange.
    """
    year = int(raw_datum['year'])
    standard = float(raw_datum['fuelStandardMpg'])
    return FuelStandardChange(year, standard)


def main():
    """Entrypoint to the visualization script."""
    sketch = sketchingpy.Sketch2D(WIDTH, HEIGHT)
    sketch.clear(BACKGROUND_COLOR)
    
    data_layer = sketch.get_data_layer()
    data_raw = data_layer.get_csv('fuel_standards.csv')
    changes = [parse_fuel_standard_change(x) for x in data_raw]

    viz = FuelStandardVizPresenter(changes)
    viz.draw(sketch)
    
    sketch.show()
    

main()
