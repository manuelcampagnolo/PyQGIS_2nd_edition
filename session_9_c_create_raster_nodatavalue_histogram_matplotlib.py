from osgeo import gdal, osr # raster input/output
import numpy as np # The fundamental package for scientific computing with Python
import matplotlib.pyplot as plt
import os

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# file name
fn=os.path.join(myfolder,'input','ndvi.tif')

##############################################################
# read file (e.g. geopackage or shapefile)
dataset = gdal.Open(fn, gdal.GA_ReadOnly) # osgeo.gdal.Dataset object

# create array of raster values
my_array=dataset.ReadAsArray()
print(my_array.shape)
print(np.prod(my_array.shape))

############################################################# no data values
# determine no data value with sourceNoDataValue
rlayer=QgsRasterLayer(fn)
nodatavalue=rlayer.dataProvider().sourceNoDataValue(1)

print(nodatavalue) # -3.4028234663852886e+38

# nodatavalue is a float, but can be a nan, identified with np.isnan
if np.isnan(nodatavalue):
    print('Nodatavalue is numpy.nan')
    # delete no data values
    idx=np.where(np.isnan(my_array.flatten()))
    my_clean_array = np.delete(my_array, idx)
else:
    print('Nodatavalue is ', nodatavalue)
    # delete no data values
    idx=np.where(my_array.flatten()==nodatavalue)
    my_clean_array = np.delete(my_array, idx)

print('nodatavalue',nodatavalue,'; no nodata values:',len(my_clean_array),'; nodata values:',len(my_array.flatten())-len(my_clean_array))

#determine min and max after cleaning array
print(np.max(my_clean_array))
print(np.min(my_clean_array))

# build histogram with matplotlib.pyplot
plt.hist(my_clean_array,np.linspace(-0.1,1,22))
plt.title("NDVI") 
plt.show()


