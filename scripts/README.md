# Description 
Zonal statistics based on LS_metrics outputs. The already implemented procedures are the calculation of habitat proportion and patch number in series of rasters, perfect for time series analysis.
The output of generalized zonal stats is a shapefile or csv file containing all polygons (zone input for zonal statistics) and columns containing the landscape metrics chosen. The inner function proportion_habitat calculates the number of pixels of habitat divided by the total number of pixels in the zones). The number_patches function calculates the number of unique patches inside each polygon, considering each patch limits independently of the zone extent.

# Scripts

###generalized_zonal_stats.py: Script to test generalized zonal stats in GRASS GIS

###test_gen_zonal_stats.py: Test script for generalized zonal stats

### Last version of LSmetrics tested available at
https://github.com/LEEClab/LS_METRICS

### Original scripts
https://github.com/mauriciovancine/GRASS-GIS-Landscape-Metrics/tree/master/scripts

#### Comments

- The script which calculates patch number in zonal statistics (GeneralizedZonalStats() in generalized_zonal_stats.py) depends on a raster containing patch id (pid) information. This can be easily done with LSmetrics; 
- LSmetrics gui works well for a single raster and also for multiple rasters, but fot running the option for a sequence of rasters with a string common pattern in raster file name, you must use the symbol "*": 
for example, if the file names' common pattern is all that starts with BR, put: BR *;
if it is all that has "forest" in the middle of file name, put: * forest *;
if it's all that ends with forest_albers, type: * forest_albers in the white box of LSmetrics (Pattern).

#### Some important tips for running a python script in GRASS-GIS without copying and pasting code from a code editor

- Always type code in the black terminal screen. The python shell in GRASS GIS DO NOT run well all the defs created!!!
- Use an auxiliary set of five lines as a starter, so you don´t need to type anything else on the terminal
- Remove the command python from inner called script. If you let it there, the code will stop, since  the auxiliary code already starts python inside GRASS command line. However, if you could call a python code from GRASS command line without calling python first, then the auxiliary code would change. But I don´t know how to start a large script differently.

### The auxiliary starter code has five lines

- python # calls python in GRASS 
- import os # allows changing directory
- import grass.script as grass # allows importing scripts
- os.chdir('WORKDIR') # set directory where the script was saved
- import SCRIPT # imports the script and make your life easier
- After that, if everything is correctly written in the script, you can wait for the results and rest.



