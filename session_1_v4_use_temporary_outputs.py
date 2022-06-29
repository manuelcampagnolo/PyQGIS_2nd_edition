# session 1: version 4
# create variables for distance and for file names
# interface, project, layers and canvas 
# use temporary outputs instead of writing outputs to files

import qgis # already loaded
import processing # idem
import os # file management

# my constants
D=20

myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_FGC = os.path.join(myfolder,'input','RPFGC_PPSM.gpkg')
layer_FGC='RPFGC_PPSM'
fn_RV = os.path.join(myfolder,'input','RVFundamental.gpkg')
layer_RV='RVFundamental'
layer_buffer='buffer'
layer_interior = 'interior'
layer_exterior = 'exterior'
fn_output= os.path.join(myfolder,'temp','IntExt_'+str(D)+'.gpkg')
layer_output='IntExt_'+str(D)

# Create project
myproject = QgsProject.instance() # does not write to file
myproject.removeAllMapLayers()

# add input as project layer
mylayer=QgsVectorLayer(fn_FGC,"", "ogr")
mylayer.setName(layer_FGC)
myproject.addMapLayer(mylayer)

mylayer=QgsVectorLayer(fn_RV,"", "ogr")
mylayer.setName(layer_RV)
myproject.addMapLayer(mylayer)

# run qgis functions
# input layer_RV; output: temporary layer to be named layer_buffer
mylayer=processing.run("native:buffer", 
{'INPUT':layer_RV, # string with the layer name
'DISTANCE':D,
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':True,
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
mylayer.setName(layer_buffer)
myproject.addMapLayer(mylayer)

mylayer=processing.run("native:clip", 
{'INPUT':layer_buffer,
'OVERLAY':layer_FGC,
'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
mylayer.setName(layer_interior)
myproject.addMapLayer(mylayer)

mylayer=processing.run("native:difference", 
{'INPUT':layer_FGC,
'OVERLAY':layer_interior,
'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
mylayer.setName(layer_exterior)
myproject.addMapLayer(mylayer)

mylayer=processing.run("native:mergevectorlayers", 
{'LAYERS':[layer_interior,layer_exterior],
'CRS':None,
'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']
mylayer.setName(layer_output)
myproject.addMapLayer(mylayer)

# export mylayer as a geopackage file
QgsVectorFileWriter.writeAsVectorFormat(mylayer,
fn_output, "UTF-8", mylayer.crs(), "GPKG",attributes=[1])

# delete input and intermediate layers
to_be_deleted = myproject.mapLayersByName(layer_RV)[0]
myproject.removeMapLayer(to_be_deleted.id())
to_be_deleted = myproject.mapLayersByName(layer_FGC)[0]
myproject.removeMapLayer(to_be_deleted.id())
to_be_deleted = myproject.mapLayersByName(layer_buffer)[0]
myproject.removeMapLayer(to_be_deleted.id())
to_be_deleted = myproject.mapLayersByName(layer_interior)[0]
myproject.removeMapLayer(to_be_deleted.id())
to_be_deleted = myproject.mapLayersByName(layer_exterior)[0]
myproject.removeMapLayer(to_be_deleted.id())