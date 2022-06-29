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
# my color composite
myRGB={'R':'band8', 'G':'band4','B':'band3'}
K=2 # number of standard deviations

##############################################################
# read raster with iface: creates QgsRaterLayer instance
# rlayer=iface.addRasterLayer(fn)
rlayer=my_add_raster_layer(fn,ln)

# get the total band count of the raster
nbands=rlayer.bandCount()

# get the band name 
for idx in range(0,nbands): 
    print(rlayer.bandName(idx+1)) 

# dataProvider and no value
print(rlayer.dataProvider().sourceNoDataValue(1)) # band 1
type(rlayer.dataProvider().sourceNoDataValue(1))
# save nodatavalue as a variable
nodatavalue=rlayer.dataProvider().sourceNoDataValue(1)
if np.isnan(nodatavalue):
    print('Nodatavalue is numpy.nan')

# size and extent
print("Width: {} px".format(rlayer.width()))
print("Height: {} px".format(rlayer.height()))
print("Extent: {}".format(rlayer.extent().toString()))

# To get the minimum and maximum values of a single-band raster, we can access its data provider’s band statistics:
for idx in range(0,nbands): 
    stats = rlayer.dataProvider().bandStatistics(idx+1)
    print("Band {} Min value: {}".format(idx+1,stats.minimumValue))
    print("Band {} Max value: {}".format(idx+1,stats.maximumValue))

# renderer
# When a raster layer is loaded, it gets a default renderer based on its type. It can be altered either in the layer properties or programmatically.
# get the raster type: 0 = GrayOrUndefined (single band), 1 = Palette (single band), 2 = Multiband
print(rlayer.rasterType())
# To query the current renderer:
print(rlayer.renderer().type())

##############################################################################
# create a renderer and plot the map
# create color composit
idxBandR=bandNames.index(myRGB['R'])+1 # +1 since bands indices start at 1
idxBandG=bandNames.index(myRGB['G'])+1 # +1 since bands indices start at 1
idxBandB=bandNames.index(myRGB['B'])+1 # +1 since bands indices start at 1
rlayer.renderer().setRedBand(idxBandR)
rlayer.renderer().setGreenBand(idxBandG)
rlayer.renderer().setBlueBand(idxBandB)
rlayer.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(rlayer.id())

######################################################################################
# simple way of stretching to min max in each band:
rlayer.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum)
rlayer.triggerRepaint()

######################################################################################
# more detailed approach: define min and max in each band, as mean-K*std and mean+K*std

for channel, band in myRGB.items():
    print(channel,band)
    # the band of the original multiband raster that corresponds to 'channel' (R,G, or B)
    idxBand=bandNames.index(myRGB[channel])+1 # +1 since bands indices start at 1
    stats = rlayer.dataProvider().bandStatistics(idxBand)
    band_type = rlayer.renderer().dataType(idxBand) # not sure why is necessary, but it is
    enhancement = QgsContrastEnhancement(band_type)
    enhancement.setMaximumValue(stats.mean+K*stats.stdDev)
    enhancement.setMinimumValue(stats.mean-K*stats.stdDev)
    enhancement.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
    if channel=='R': rlayer.renderer().setRedContrastEnhancement(enhancement)
    if channel=='G': rlayer.renderer().setGreenContrastEnhancement(enhancement)
    if channel=='B': rlayer.renderer().setBlueContrastEnhancement(enhancement)

# if we want to set opacity
rlayer.renderer().setOpacity(0.9)
rlayer.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(rlayer.id())
