# Script to calculate generalized zonal stats

# PS: After creating a location based on the input shapefile

# Open python
python

# Import modules
import os
import grass.script as grass
import subprocess

# Set folder where input files are
input_dir = r'/home/leecb/Github/GRASS-GIS-Landscape-Metrics/input_files'
os.chdir(input_dir)

# Import shape file
shape_name = 'mun_teste_wgs84'
grass.run_command('v.in.ogr', input = shape_name+'.shp', output = shape_name, overwrite = True)

# Import raster
raster_name = 'BR_2001_euca_9'
grass.run_command('r.in.gdal', input = raster_name+'.tif', output = raster_name, overwrite = True)

# Now, run LSMetrics and calculate the metrics "patch size"
# More info here: https://github.com/LEEClab/LS_METRICS/

# We can leave python, change to LSMetrics script dir and run the LSMetrics script there
# Or, here, we will call the script from within GRASS
lsmetrics_dir = r'/home/leecb/Github/LS_METRICS/_LSMetrics_v1_0_0_stable'
os.chdir(lsmetrics_dir)

# Run LSMetrics
subprocess.call('python LSMetrics_v1_0_0.py', shell=True) # runs and wait
# Here it is important to decide whether pixels on the diagonal will be considered as the same patch or not!!

# We will use the Patch ID map to calculate the number of patches within a shapefile feature
# We will use the binary eucaliptus map to calculate the proportion of eucaliputs within a shapefile feature

# Change to the script folder
script_dir = r'/home/leecb/Github/GRASS-GIS-Landscape-Metrics/scripts'
os.chdir(script_dir)

# Import generalized_zonal_stats class
from generalized_zonal_stats import generalized_zonal_stats, proportion_habitat, number_patches

#---------------
# Running for proportion of eucaliptus
input_shp = 'mun_teste_wgs84'
input_rast = ['BR_2001_euca_9']

# Initialize and select maps to be used in zonal stats
teststats = generalized_zonal_stats(input_shape = input_shp, input_rasters = input_rast, folder = input_dir)

# Create new cols
cols = ['prp_euca_2001']
col_type = ['float']

# WARNING! GRASS GIS does not like col names longer than 8-10 characters, so try to be very concise!!
# Or later you can do something like 
# grass.run_command('v.db.renamecolumn', map=shape_name, column='oldcolname,newcolname')
#grass.run_command('v.db.renamecolumn', map=shape_name, column='prp_euca_2001,p_eu_2001')

teststats.create_new_column(column_names = cols, type_col=col_type)

# Calculate proportion of eucaliptus in each feature using proportion_habitat function
teststats.run_zonal_stats(proportion_habitat)

# Export shapefile
os.chdir(input_dir)
# export shape file
#grass.run_command('v.out.ogr', input = shape_name, output = shape_name+'_prop_euca.shp', overwrite = True)
# export db in csv format
#grass.run_command('db.out.ogr', input = shape_name, output = shape_name+'_prop_euca.csv')

#-------------------
# Running for number of patches
input_shp = 'mun_teste_wgs84'
input_rast = ['BR_2001_euca_9_pid']

# Initialize and select maps to be used in zonal stats
test_np = generalized_zonal_stats(input_shape = input_shp, input_rasters = input_rast, folder = input_dir)

# Create new cols
cols = ['np_2001']
col_type = ['int']

# WARNING! GRASS GIS does not like col names longer than 8-10 characters, so try to be very concise!!

test_np.create_new_column(column_names = cols, type_col=col_type)

# Calculate number of patches (clumps) of eucaliptus in each feature using number_patches function
test_np.run_zonal_stats(number_patches, mask = True)

# Export shapefile
os.chdir(input_dir)
# export shape file
grass.run_command('v.out.ogr', input = shape_name, output = shape_name+'_prop_euca_np.shp', overwrite = True)

#-------------------------------------------------------------------------
# Do not run below!!!!
# Other tests
python 

import os
import grass.script as grass
import grass.script.vector as v
import grass.script.raster as r
import grass.script.db as db

cat = '20'

input_shape = 'mun_teste_wgs84'
input_raster = 'BR_2001_euca_9'
col = 'proportion_euca'

# Take resolution from raster map
rast_info = r.raster_info(input_raster)
ewres = rast_info['ewres']
nsres = rast_info['nsres']
ewres
nsres

# Create a raster for the feature
grass.run_command('g.region', vector = input_shape, ewres = ewres, nsres = nsres, align = input_raster)
grass.run_command('v.to.rast', input = input_shape, output = 'temp_rast', cats = cat, use='val', overwrite = True)

# Set region to the feature
grass.run_command('g.region', raster = 'temp_rast', zoom = 'temp_rast') 

# Run r.mask for the feature
grass.run_command('r.mask', vector = input_shape, cats = cat)

prop = proportion_habitat(input_raster)

grass.run_command('v.db.update', map = input_shape, column = col, value = str(prop), where='cat = '+cat)

grass.run_command('r.mask', flags = 'r')

#---------------
# test proportion_habitat function
# Open python
python

# Import modules
import os
import grass.script as grass

# Change to the script folder
script_dir = r'/home/leecb/Github/GRASS-GIS-Landscape-Metrics/scripts'
os.chdir(script_dir)

# Import generalized_zonal_stats class
from generalized_zonal_stats import generalized_zonal_stats, proportion_habitat

input_rast = ['BR_2001_euca_9']
proportion_habitat(input_rast)