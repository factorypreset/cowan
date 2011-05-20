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
from raster_input import RasterInput
from scenarios import SCENARIOS
from source_files import import SOURCE_FILES

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

def overlay(fuzzies):
    """
    Overlays a set of rasters using fuzzy overlay
    """
    result_raster = None
    for fuzzy in fuzzies:
        fuzzy.weigh()
        try:
            result_raster = FuzzyOverlay([result_raster, fuzzy.weighted_raster], fuzzy.overlay_method)
        except:
            result_raster = fuzzy.weighted_raster


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
            fuzzies = []
            for source_file in SOURCE_FILES:
                overlay = source_file.get('overlay')
                input_raster = RasterInput(source_file.get('file_name'),
                                    scenario[source_file.get('name')],
                                    source_file.get('invert'),
                                    source_file.get('overlay'))
                fuzzies.append(input_raster)

            final_raster = overlay(fuzzies)
            final_raster.save(output_file)


# Main script execution block
create_output_path()
process()
