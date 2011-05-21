# Define raster source files to be combined
# Note: dictionary indices must match properties in SCENARIOS
# Also note: ANDs must be positioned last in this list!
SOURCE_FILES = [
    {'name': 'fauna', 'file_name': 'fuz_fauna2', 'overlay': 'SUM', 'invert': False},
    {'name': 'flora', 'file_name': 'fuz_flora2', 'overlay': 'SUM', 'invert': False},
    {'name': 'slope', 'file_name': 'fuz_slopeper', 'overlay': 'SUM', 'invert': False},
    {'name': 'fire', 'file_name': 'fuz_fire1', 'overlay': 'SUM', 'invert': True},
    {'name': 'ftrail', 'file_name': 'fuz_firetrail', 'overlay': 'SUM', 'invert': False},
    {'name': 'erosion', 'file_name': 'fuz_erosion1', 'overlay': 'SUM', 'invert': True},
    {'name': 'mangroves', 'file_name': 'fuz_mangr2', 'overlay': 'AND', 'invert': False},
    {'name': 'creeks', 'file_name': 'fuz_creek4', 'overlay': 'AND', 'invert': False},
]