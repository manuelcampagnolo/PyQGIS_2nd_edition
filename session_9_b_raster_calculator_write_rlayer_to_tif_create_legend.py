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
fn=os.path.join(myfolder,'input','Cropped_S2A-T29SNB-B2348-2021-8-22.tif')
ln='S2SR-B2348'
# bands of fn (in order):
bandNames=['band2','band3','band4','band8']

# Legend for NDVI
mydict={
'no vegetation': (QColor('brown'),0),
'sparse vegetation': (QColor('yellow'),0.25), 
'vegetation': (QColor('green'),0.45),
'dense vegetation': (QColor('dark green'),1)}

# output file name
fn_ndvi=os.path.join(myfolder,'temp','ndvi.tif')

####################################### read raster from file name
# read raster 
rlayer=my_add_raster_layer(fn,ln)

#######################################  parameters to compute NDVI
# expression to compute NDVI
idxNIR=bandNames.index('band8')+1
calcBandNIR=ln+'@'+str(idxNIR)
idxRED=bandNames.index('band4')+1
calcBandRED=ln+'@'+str(idxRED)
exp_ndvi='("'+calcBandNIR+'"-"'+calcBandRED+'")/("'+calcBandNIR+'"+"'+calcBandRED+'")'

# Average cell size
cellsize=(rlayer.rasterUnitsPerPixelX()+rlayer.rasterUnitsPerPixelY())/2

# Extent
xMin=rlayer.extent().xMinimum()
xMax=rlayer.extent().xMaximum()
yMin=rlayer.extent().yMinimum()
yMax=rlayer.extent().yMaximum()
myEPSG=rlayer.crs().authid()
exp_extent=str(xMin)+','+str(xMax)+','+str(yMin)+','+str(yMax)+' ['+myEPSG+']'

fn_ndvi_output=processing.run("qgis:rastercalculator", 
{'EXPRESSION':exp_ndvi,
'LAYERS':None,
'CELLSIZE': cellsize,
'EXTENT':exp_extent,
'CRS':rlayer.crs(),
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

# add ndvi layer to canvas with 
ndvilayer=my_add_raster_layer(fn=fn_ndvi_output,ln='ndvi')

# Create legend
create_raster_ramp_legend(lyr=ndvilayer,dict=mydict, type='Discrete')

## Save raster layer as geotiff file
pipe = QgsRasterPipe()
pipe.set(ndvilayer.dataProvider().clone())
file_writer = QgsRasterFileWriter(fn_ndvi)
file_writer.writeRaster(pipe, ndvilayer.width(), ndvilayer.height(), ndvilayer.extent(), rlayer.crs())
