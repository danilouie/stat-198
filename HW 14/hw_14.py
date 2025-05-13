import sketchingpy
import sketchingpy.geo


sketch = sketchingpy.Sketch2DWeb(500, 500)
sketch.clear('#F0F0FF')

# Center the map on San Francisco and place in middle of sketch
center_longitude = -122.418343
center_latitude = 37.761842
center_x = 250
center_y = 250
map_scale = 100

# Create a geo transformation that ties pixel to geo coordinates
sketch.set_map_pan(center_longitude, center_latitude) # Where to center geographically
sketch.set_map_zoom(map_scale)  # How much zoom
sketch.set_map_placement(center_x, center_y)  # Where to center in terms of pixels

# Make and convert points
data_layer = sketch.get_data_layer()
geojson = data_layer.get_json('/Users/daniellelouie/Documents/Berkeley/2024-2025/STAT 198/stat-198/HW 14/bayarea.geojson')
geo_polgyons = sketch.parse_geojson(geojson)

# There is only one polygon
geo_polgyon = geo_polgyons[0]
shape = geo_polgyon.to_shape()

# Draw
sketch.set_fill('#333333')
sketch.clear_stroke()
sketch.draw_shape(shape)

sketch.show()