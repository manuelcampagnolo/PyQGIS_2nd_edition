from osgeo import gdal, osr # raster input/output
import numpy as np # The fundamental package for scientific computing with Python
import matplotlib.pyplot as plt
import os
import sklearn

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# file name
fn=os.path.join(myfolder,'input','Cropped_S2A-T29SNB-B2348-2021-8-22.tif')
ln='S2SR-B2348'
fn_new=os.path.join(myfolder,'temp','k_means.tif')
ln_new='Clusters_from_bands'
# bands of fn (in order):
bandNames=['band2','band3','band4','band8']
# my color composite
myRGB={'R':'band8', 'G':'band4','B':'band3'}
# Clusters (k-means)
my_dict={
'cluster1': (QColor('red'),0),
'cluster2': (QColor('yellow'),1),
'cluster3': (QColor('black'),2),
'cluster4': (QColor('blue'),3),
'cluster5': (QColor('green'),4),
'cluster6': (QColor('pink'),5),
}
# number of clusters
Nclusters=len(my_dict)

##############################################################
# read raster with iface: creates QgsRaterLayer instance
# rlayer=iface.addRasterLayer(fn)
rlayer=my_add_raster_layer(fn,ln)

# read and define multiband renderer
rlayer=set_mean_std_color_composite(rlayer,bandNames,myRGB,K=2,myopacity=0.9)

###################################################### gdal & numpy

# access multi band Landsat 8 data with gdal.Open
gdal_layer = gdal.Open(fn, gdal.GA_ReadOnly) 

# fetch parameters from rlayer (that will be needed to convert processed data back to QgsRasterLayer)
# determine coordinate transformation with gdal
geotransform = gdal_layer.GetGeoTransform()   # from osgeo.gdal.Dataset object
# determine no data value from data provider (use 1st band)
if not np.isnan(rlayer.dataProvider().sourceNoDataValue(1)):
    nodatavalue=int(rlayer.dataProvider().sourceNoDataValue(1)) # from QgsRasterLayer object
else:
    nodatavalue=np.nan
# determine raster size
W=rlayer.width() # from QgsRasterLayer object
H=rlayer.height() # from QgsRasterLayer object
# determine CRS
EPSGcode=int(rlayer.crs().authid()[5:]) # from QgsRasterLayer object

# create empty raster with gdal using parameters above and with only 1 band
my_new_raster=None
my_new_raster = gdal.GetDriverByName('GTiff').Create(fn_new,W,H,1,gdal.GDT_Float32)
my_new_raster.SetGeoTransform(geotransform)
srs=osr.SpatialReference()
srs.ImportFromEPSG(EPSGcode)
my_new_raster.SetProjection(srs.ExportToWkt())

# process data with numpy and write results to new raster
# (1) convert data to numpy array and process
# Reading a chunk of a GDAL band into a numpy array. https://gdal.org/python/osgeo.gdal.Dataset-class.html#ReadAsArray
# real original raster as numpy array
my_array=gdal_layer.ReadAsArray() 
# convert nodatavalues into numpy.nan
if not np.isnan(nodatavalue):
    my_array[my_array==nodatavalue]=np.nan

############################## example: process data with KMeans from package sklearn
# K: number of clusters
# sample rate: proportion of pixels used to train KMeans
result=my_kmeans(my_array,k=Nclusters,sample_rate=0.1)
##########################################

# convert nan values back to nodatavalue
if not np.isnan(nodatavalue):
    result[np.isnan(result)]=nodatavalue

# (2) write processed data to my_raster
my_new_raster.GetRasterBand(1).WriteArray(result)
# assign original nodatavalue to my_new_raster
my_new_raster.GetRasterBand(1).SetNoDataValue(nodatavalue)

# close connection
my_new_raster = None

# load and render new raster
rlayer=my_add_raster_layer(fn_new,ln_new)
create_raster_ramp_legend(lyr=rlayer,dict=my_dict, type='Discrete')
