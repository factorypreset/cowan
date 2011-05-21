Raster Multi-Criteria Analysis Tools
====================================

This is intended to be a set of tools for performing linear weighted multi-
criteria analysis on rasters describing different features of a given
geographical area.

Technical requirements
----------------------

1. Currently requires ArcGIS 10.0 and arcpy with a valid license for the Spatial
Analyst extensions. Sadly this means the script will only run on Windows. A
future version might be able to remove this dependency on ArcGIS.

2. arcpy is available in your PYTHONPATH. To verify, open a python shell and
type the following command::

  import arcpy

If this executes without error then you're in the clear. If not, ensure that
PATH and PYTHONPATH are set correctly. This ESRI help page might be of
assistance:

   http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//002z00000008000000.htm

combine_fuzzies.py
------------------

This script assumes you have a number of fuzzified raster files covering the
same geographic extent, with the same spatial reference system and projection.
These should have been normalised to a scale with values between 0 and 1,
based on whatever fuzzy membership function you choose (most likely a
monotonic, trapezoidal, triangular or gaussian function). At present we do not
provide a script for generating these fuzzified rasters, although that would
have been awesome.

The combine_fuzzies.py script itself enables a linear weighted multi-criteria
analysis to be performed on the resulting fuzzified raster files.

To use it:

1. Copy raster files into position

In this version the raster files must be in the same directory as the
combine_fuzzies.py script (possibly not a very good assumption).

2. Configure source raster files

Open source_files.py. This defines a list called SOURCE_FILES. Each element in
the list is a dictionary representing one fuzzified raster file, and having
the following members (i.e. key/value pairs):

  * name: an arbitrary name
  * file_name: name of the raster file on your file system
  * overlay: name of the fuzzy overlay method to be used. Currently supports
    'SUM' and 'AND'. Possibly others too, but they are untested.
  * invert: a flag indicating whether the fuzzified raster should be inverted
    prior to processing. This is useful in cases where ideal values are 0
    rather than 1.

For example::

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

3. Configure scenarios

A scenario defines a set of subjective preferences for the values described in
each raster file. These preferences are encapsulated in a list called
SCENARIOS. This list contains one or more dictionaries, each of which must
contain this member:

  * name: an arbitrary name for the scenario

After that, each dictionary in SCENARIOS must have one member for each of the
source rasters described in SOURCE_FILES. These data members are key/value
pairs and must be of the following form:

  * key: must match the name of a source file defined in SOURCE_FILES
  * value: a weighting value between 0 and 1

Ideally all weighting values in a scenario should add up to 1, although
this is not enforced in the script.

For example::

  SCENARIOS = [{
      'name': 'conserv',
      'fauna': 0.3,
      'flora': 0.3,
      'mangroves': 0.3,
      'creeks': 0.02,
      'slope': 0,
      'fire': 0.04,
      'ftrail': 0.02,
      'erosion': 0.02
  }, {
      'name': 'min_cost',
      'fauna': 0.01,
      'flora': 0.01,
      'mangroves': 0.03,
      'creeks': 0.1,
      'slope': 0.3,
      'fire': 0.1,
      'ftrail': 0.25,
      'erosion': 0.2
  }]


4. Execute script

To start the process just run the following command::

  PATH_TO_YOUR_ESRIFIED_PYTHON\python.exe combine_fuzzies.py

Or on systems with PATH and PYTHONPATH correctly configured, you can instead
just double-click on the combine_fuzzies.py file from Windows Explorer.

One output raster will be calculated for each scenario, based on the
preferences you defined. They will be found in the output/ directory
(which is a subfolder of the directory containing combine_fuzzies.py).

5. Re-running the script

combine_fuzzies.py does not attempt to re-generate output rasters if an
output file for a given scenario already exists. If you want to rerun the
script with different values you must first delete or move the relevant output
file(s).


TODO
----

* Make input and output paths configurable, or pass them in via command
  line options.

* Properly handle fuzzy overlay methods other than 'SUM'. At present the
  script only works when 'AND' sources files are listed after the 'SUM'
  files.

* Optimise the fuzzy overlay step. sa.FuzzyOverlay() allows an arbitrary
  number of rasters to be passed in at once. We should make use of that.

* Write a script to generate (fuzzify) the source rasters.

* Handle different geographic extents, spatial references and/or projections.

* Automatically identify positions or areas with the highest overall score
  across multiple scenarios.

* Need to write some unit tests. Of course.

* Rework this to use open source tools rather than relying on proprietary
  ESRI software. Ideally before my student evaluation of ArcGIS expires.

