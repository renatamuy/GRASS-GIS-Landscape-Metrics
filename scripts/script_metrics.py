### script landscape metrics ###

# Maurício Humberto Vancine - mauricio.vancine@gmail.com
# 04/09/2017

###----------------------------------------------------------------------------------------###

# start python
python 

# import modules
import os
import grass.script as grass

###----------------------------------------------------------------------------------------###

# directory
fo = r"E:\mega\_dissertacao_v02\product\RIO_CLARO\USO"
os.chdir(fo)
print os.listdir(fo)

# addons
grass.run_command("g.extension", extension = "r.area", operation = "add")
grass.run_command("g.extension", extension = "r.diversity", operation = "add")

# import vector of land use
grass.run_command("v.in.ogr", input = "SP_3543907_USO.shp", output = "SP_3543907_USO", \
	overwrite = True)

# define region and resolution
grass.run_command("g.region", flags = "p", vector = "SP_3543907_USO", res = 30)

# vector to raster
grass.run_command("v.to.rast", input = "SP_3543907_USO", output = "SP_3543907_USO_raster", \
	type = "area", use = "cat", label_column = "CLASSE_USO", overwrite = True)

# select forest class
grass.mapcalc("SP_3543907_USO_raster_forest = if(SP_3543907_USO_raster == 4, 1, 0)")

###----------------------------------------------------------------------------------------###

## 1. percentage of forest

# diameter = 3 pixels
# moving window  
grass.run_command("r.neighbors", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_avg_3", method = "average", size = "3")

# percentage
grass.mapcalc("SP_3543907_USO_raster_forest_avg_3_pct = SP_3543907_USO_raster_forest_avg_3 * 100")

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_avg_3_pct", \
	output = "SP_3543907_USO_raster_forest_avg_3_pct" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 2. structural connectivity 

# clump
grass.run_command("r.clump", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_clump", overwrite = True)

# selection forest
ex = "SP_3543907_USO_raster_forest_clump_f = if((SP_3543907_USO_raster_forest_clump * SP_3543907_USO_raster_forest) > 0, \
(SP_3543907_USO_raster_forest_clump * SP_3543907_USO_raster_forest), null())"
grass.mapcalc(ex, overwrite = True)

# area - number of pixels
grass.run_command("r.area", input = "SP_3543907_USO_raster_forest_clump_f", \
	output = "SP_3543907_USO_raster_forest_clump_f_area", overwrite = True)

# area - square meters
ex2 = "SP_3543907_USO_raster_forest_clump_f_area_m2 = SP_3543907_USO_raster_forest_clump_f_area * 2 * 30"
grass.mapcalc(ex2, overwrite = True)

# area - hectares
ex3 = "SP_3543907_USO_raster_forest_clump_f_area_ha = SP_3543907_USO_raster_forest_clump_f_area_m2 * 0.0001"
grass.mapcalc(ex3, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_clump_f_area", \
	output = "SP_3543907_USO_raster_forest_clump_f_area" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

## 3. functional connectivity

# diameter 3 pixels = 60 m
# moving window  
grass.run_command("r.neighbors", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_max_3", method = "maximum", size = "3", overwrite = True)

# clump
grass.run_command("r.clump", input = "SP_3543907_USO_raster_forest_max_3", \
	output = "SP_3543907_USO_raster_forest_max_3_clump", overwrite = True)

# selection forest
ex = "SP_3543907_USO_raster_forest_max_3_clump_f = if((SP_3543907_USO_raster_forest_max_3_clump * SP_3543907_USO_raster_forest_max_3) > 0, \
(SP_3543907_USO_raster_forest_max_3_clump * SP_3543907_USO_raster_forest_max_3), null())"
grass.mapcalc(ex, overwrite = True)

# area - number of pixels
grass.run_command("r.area", input = "SP_3543907_USO_raster_forest_max_3_clump_f", \
	output = "SP_3543907_USO_raster_forest_max_3_clump_f_area", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_max_3_clump_f_area", \
	output = "SP_3543907_USO_raster_forest_max_3_clump_f_area" + ".tif", format = "GTiff", overwrite = True)


###----------------------------------------------------------------------------------------###

## 4. core

# diameter 3 pixels = 60 m
# moving window  
grass.run_command("r.neighbors", input = "SP_3543907_USO_raster_forest", \
	output = "SP_3543907_USO_raster_forest_min_3", method = "minimum", size = "3", overwrite = True)

# clump
grass.run_command("r.clump", input = "SP_3543907_USO_raster_forest_min_3", \
	output = "SP_3543907_USO_raster_forest_min_3_clump", overwrite = True)

# selection forest
ex = "SP_3543907_USO_raster_forest_min_3_clump_f = if((SP_3543907_USO_raster_forest_min_3_clump * SP_3543907_USO_raster_forest_min_3) > 0, \
(SP_3543907_USO_raster_forest_min_3_clump * SP_3543907_USO_raster_forest_min_3), null())"
grass.mapcalc(ex, overwrite = True)

# area - number of pixels
grass.run_command("r.area", input = "SP_3543907_USO_raster_forest_min_3_clump_f", \
	output = "SP_3543907_USO_raster_forest_min_3_clump_f_area", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_avg_3_pct", \
	output = "SP_3543907_USO_raster_forest_avg_3_pct" + ".tif", format = "GTiff", overwrite = True)


###----------------------------------------------------------------------------------------###

## 5. edge

# edge
ex = "SP_3543907_USO_raster_forest_min_3_edge = SP_3543907_USO_raster_forest - SP_3543907_USO_raster_forest_min_3"
grass.mapcalc(ex, overwrite = True)

# clump
grass.run_command("r.clump", input = "SP_3543907_USO_raster_forest_min_3_edge", \
	output = "SP_3543907_USO_raster_forest_min_3_edge_clump", overwrite = True)

# selection forest
ex = "SP_3543907_USO_raster_forest_min_3_edge_clump_f = if((SP_3543907_USO_raster_forest_min_3_edge_clump * SP_3543907_USO_raster_forest_min_3_edge) > 0, \
(SP_3543907_USO_raster_forest_min_3_edge_clump * SP_3543907_USO_raster_forest_min_3_edge), null())"
grass.mapcalc(ex, overwrite = True)

# area - number of pixels
grass.run_command("r.area", input = "SP_3543907_USO_raster_forest_min_3_edge_clump_f", \
	output = "SP_3543907_USO_raster_forest_min_3_edge_clump_f_area", overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_forest_min_3_edge_clump_f_area", \
	output = "SP_3543907_USO_raster_forest_min_3_edge_clump_f_area" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

# 6. diversity

# diversity
grass.run_command("r.diversity", input = "SP_3543907_USO_raster", prefix = "diversity", \
	size = 3, alpha = .5, overwrite = True)

# export
grass.run_command("r.out.gdal", flags = "c", input = "SP_3543907_USO_raster_diversity", \
	output = "SP_3543907_USO_raster_diversity" + ".tif", format = "GTiff", overwrite = True)

###----------------------------------------------------------------------------------------###

# clean
grass.run_command("g.remove", flags = "f", type = "raster", pattern = "*raster*")


###----------------------------------------------------------------------------------------###

# select forest class
grass.mapcalc("SP_3543907_USO_raster_forest_null = if(SP_3543907_USO_raster == 4, 1, null())")

# rlisetup
grass.run_command("g.gui.rlisetup")

# name: rio_claro
# raster: SP_3543907_USO_raster_forest_null
# sampling: whole map
# moving window
# method: keyboard
# type: rectangle
# size: 3 x 3


## indices based on patch number:
# calculates patch density index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.patchdensity", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_patchdensity", conf = "rio_claro", overwrite = True)

# calculates patch number index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.patchnum", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_patchnum", conf = "rio_claro", overwrite = True)

## indices based on patch dimension:
# calculates mean patch size index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.mps", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_mps", conf = "rio_claro", overwrite = True)

# calculates coefficient of variation of patch area on a raster map
grass.run_command("r.li.padcv", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padcv", conf = "rio_claro", overwrite = True)
 
# calculates range of patch area size on a raster map
grass.run_command("r.li.padrange", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padrange", conf = "rio_claro", overwrite = True)

# calculates standard deviation of patch area a raster map
grass.run_command("r.li.padsd", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_padsd", conf = "rio_claro", overwrite = True)


## indices based on patch shape
# calculates shape index on a raster map
grass.run_command("r.li.shape", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_shape", conf = "rio_claro", overwrite = True)
 

## indices based on patch edge:
# calculates edge density index on a raster map, using a 4 neighbour algorithm
grass.run_command("r.li.edgedensity", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity", conf = "rio_claro", overwrite = True)

grass.run_command("r.li.edgedensity", flags = "b", input = "SP_3543907_USO_raster_forest_null", \
	output = "SP_3543907_USO_raster_forest_null_edgedensity_b", conf = "rio_claro", overwrite = True)
 
 

## indices based on patch attributes:
# calculates contrast Weighted Edge Density index on a raster map
#grass.run_command("r.li.cwed", input = "SP_3543907_USO_raster_forest_null", \
#	output = "SP_3543907_USO_raster_forest_null_cwed", conf = "rio_claro", overwrite = True)
 
# calculates mean pixel attribute index on a raster map
grass.run_command("r.li.mpa", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_mpa", conf = "rio_claro", overwrite = True)
 

## diversity indices:
# calculates dominance diversity index on a raster map
grass.run_command("r.li.dominance", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_dominance", conf = "rio_claro", overwrite = True)

# calculates Pielou eveness index on a raster map
grass.run_command("r.li.pielou", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_pielou", conf = "rio_claro", overwrite = True) 

# calculates Renyi entropy on a raster map
grass.run_command("r.li.renyi", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_renyi_a06", alpha = "0.6", conf = "rio_claro", overwrite = True) 

# calculates richness diversity index on a raster map
grass.run_command("r.li.richness", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_richness", conf = "rio_claro", overwrite = True) 

# calculates Shannon diversity index on a raster map
grass.run_command("r.li.shannon", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_shannon", conf = "rio_claro", overwrite = True) 

# calculates Simpson diversity index on a raster map
grass.run_command("r.li.simpson", input = "SP_3543907_USO_raster", \
	output = "SP_3543907_USO_raster_simpson", conf = "rio_claro", overwrite = True)  

