# combine_fuzzies.py
#
# Created: 2011-05-12
# Version: 0.1
# Author: Bo Daley <bo@factorypreset.com>
# Description: Combines arbitrary number of fuzzified rasters with given weights

import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Check out Spatial Analyst license
arcpy.CheckOutExtension("spatial")

# Allow overwriting of temporary rasters
env.overwriteOutput = True

# Location of input rasters - assume same path as current script
# (possibly not a very good assumption)
# TODO: try to avoid windows-style slashes
input_path = os.path.realpath(os.path.dirname(__file__)) + "\\"

# Location of output raster
output_path = input_path + "output2\\"

# Default input raster files
# TODO: allow these to be passed in via command line (these can be defaults)
FAUNA_FILE = "%sfuz_fauna2" % input_path
FLORA_FILE = "%sfuz_flora2" % input_path
MANGROVES_FILE = "%sfuz_mangr2" % input_path
CREEKS_FILE = "%sfuz_creek4" % input_path
SLOPE_FILE = "%sfuz_slopeper" % input_path
FIRE_FILE =  "%sfuz_fire1" % input_path
FTRAIL_FILE = "%sfuz_firetrail" % input_path
EROSION_FILE = "%sfuz_erosion1" % input_path

# Define scenarios
SCENARIOS = [{
    'name': 'firetrail', 'fauna': 0.05, 'flora': 0.05, 'mangroves': 0.15,
    'creeks': 0.15, 'slope': 0.1, 'fire': 0.15, 'ftrail': 0.25, 'erosion': 0.1
}, {
    'name': 'conserv_e', 'fauna': 0.3, 'flora': 0.3, 'mangroves': 0.3,
    'creeks': 0.02, 'slope': 0, 'fire': 0.04, 'ftrail': 0.02, 'erosion': 0.02
}, {
    'name': 'conserv_m', 'fauna': 0.2, 'flora': 0.2, 'mangroves': 0.25,
    'creeks': 0.28, 'slope': 0, 'fire': 0.01, 'ftrail': 0.01, 'erosion': 0.05
}, {
    'name': 'min_cost', 'fauna': 0.01, 'flora': 0.01, 'mangroves': 0.03,
    'creeks': 0.1, 'slope': 0.3, 'fire': 0.1, 'ftrail': 0.25, 'erosion': 0.2
}, {
    'name': 'fire_xtr1', 'fauna': 0.03, 'flora': 0.03, 'mangroves': 0.04,
    'creeks': 0.2, 'slope': 0.2, 'fire': 0.4, 'ftrail': 0.05, 'erosion': 0.05
}, {
    'name': 'edris', 'fauna': 0.05, 'flora': 0.05, 'mangroves': 0.1,
    'creeks': 0.15, 'slope': 0.10, 'fire': 0.2, 'ftrail': 0.20,'erosion': 0.15
}, {
    'name': 'edris3', 'fauna': 0.1, 'flora': 0.1, 'mangroves': 0.15,
    'creeks': 0.10, 'slope': 0.05, 'fire': 0.25, 'ftrail': 0.15, 'erosion': 0.10
}, {
    'name': 'conser_m2', 'fauna': 0.05, 'flora': 0.05, 'mangroves': 0.2,
    'creeks': 0.2, 'slope': 0.0, 'fire': 0.0, 'ftrail': 0.2, 'erosion': 0.3
}
]



class RasterInput:
    """
    A single data input to the combination process, consisting of:
      - a raster file
      - a weighting coefficient (value between 0 and 1)
      - flag indicating whether to invert values before processing
    """
    def __init__(self, raster, weighting=0.125, inverse_required=False):
        self.raster = raster
        self.weighted_raster = None
        self.weighting = float(weighting) # must be numeric
        self.inverse_required = inverse_required

    def invert_if_required(self):
        """
        Invert raster cell values if required
        To do this we just subtract the raster from 1
        """
        if self.inverse_required:
            self.raster = Minus(1,self.raster)
        return self.raster

    def weigh(self):
        """
        Multiply raster cell values by weighting coefficient
        """
        self.invert_if_required()
        self.weighted_raster = Times(self.raster, self.weighting)
        return self.weighted_raster

    def __unicode__(self):
        return self.raster



def sum(fuzzies):
    """
    Sums a collection of RasterInputs
    """
    result_raster = None
    for fuzzy in fuzzies:
        fuzzy.weigh()
        try:
            result_raster = Plus(result_raster, fuzzy.weighted_raster)
        except:
            result_raster = fuzzy.weighted_raster
    return result_raster


def create_output_path():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def process():
    """
    Combine all the fuzzified rasters
    """

    for scenario in SCENARIOS:
        output_file = output_path + "all_" + scenario['name']
        # calculate raster if we don't already have it
        if not os.path.exists(output_file):
            print "Calculating combined raster for " + scenario['name']
            fauna = RasterInput(FAUNA_FILE, scenario['fauna'])
            flora = RasterInput(FLORA_FILE, scenario['flora'])
            mangroves = RasterInput(MANGROVES_FILE, scenario['mangroves'])
            creeks = RasterInput(CREEKS_FILE, scenario['creeks'])
            slope = RasterInput(SLOPE_FILE, scenario['slope'])
            fire = RasterInput(FIRE_FILE, scenario['fire'], True)
            ftrail = RasterInput(FTRAIL_FILE, scenario['ftrail'])
            erosion = RasterInput(EROSION_FILE, scenario['erosion'], True)

            fuzzies = (fauna, flora, mangroves, creeks, slope, fire, ftrail, erosion)

            final_raster = sum(fuzzies)
            final_raster.save(output_file)


# Main script execution block
create_output_path()
process()
