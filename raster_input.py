import arcpy
from arcpy import env
from arcpy.sa import *

# Check out Spatial Analyst license
arcpy.CheckOutExtension("spatial")

class RasterInput:
    """
    A single data input to the combination process, consisting of:
      - a raster file
      - a weighting coefficient (value between 0 and 1)
      - flag indicating whether to invert values before processing
    """
    def __init__(self, raster, weighting=0.125, inverse_required=False, overlay_method='SUM'):
        self.raster = raster
        self.weighted_raster = None
        self.weighting = float(weighting) # must be numeric
        self.inverse_required = inverse_required
        self.overlay_method = overlay_method

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

