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
# bands of fn (in order):
bandNames=['band2','band3','band4','band8']
# my color composite
myRGB={'R':'band8', 'G':'band4','B':'band3'}
# new raster where clusters will be stored
fn_new=os.path.join(myfolder,'temp','k_means_3.tif')
ln_new='Clusters_from_bands_and_ndvi'
nbands=1 # bands in the output raster 
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

############################################################# requires gdal and osr
# (1) Create from fn new empty raster in file ln_new, with nbands number of bands
create_new_empty_raster_from_filename(fn,fn_new,nbands)

# (2) Create array from file fn
(my_array , nodatavalue) = create_array_from_raster_file_name(fn)

#######################################################################
# New: Create new 'ndvi' band with numpy
# indices in numpy arrays start at 0 
idxNIR=bandNames.index('band8') # NIR
idxRED=bandNames.index('band4') # RED

# (3) create array of ndvi values
ndvi=(my_array[idxNIR,:,:]-my_array[idxRED,:,:])/(my_array[idxNIR,:,:]+my_array[idxRED,:,:])
#resize to have the same number of dimensions than my_array
ndvi_shape=(1,my_array.shape[1],my_array.shape[2])
new_ndvi=np.resize(ndvi,ndvi_shape)
# append ndvi to my_array
my_array=np.append(my_array,new_ndvi,axis=0)
# remove nan, posinf (infinite values) and neginf with "nan_to_num"
my_array=np.nan_to_num(my_array, copy=False, nan=0.0, posinf=0.0, neginf=0.0)

print(my_array.shape)

# (4) process data with KMeans from package sklearn
# K: number of clusters
# sample rate: proportion of pixels used to train KMeans
result=my_kmeans(my_array,k=Nclusters,sample_rate=0.1)

# (5) convert nan values back to nodatavalue
if not np.isnan(nodatavalue):
    result[np.isnan(result)]=nodatavalue

# (6) write processed data to file fn_new
# see https://gdal.org/tutorials/raster_api_tut.html#opening-the-file
my_new_raster = gdal.Open(fn_new, gdal.GA_Update) # open connection
my_new_raster.GetRasterBand(1).WriteArray(result)
# assign original nodatavalue to my_new_raster
my_new_raster.GetRasterBand(1).SetNoDataValue(nodatavalue)
# close connection
my_new_raster = None

# (7) load and render new raster
rlayer=my_add_raster_layer(fn_new,ln_new)
create_raster_ramp_legend(lyr=rlayer,dict=my_dict, type='Discrete')
