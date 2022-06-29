# session 1: version 3
# create variables for distance and for file names
# interface, project, layers and canvas 

import qgis # already loaded
import processing # idem
import os # file management

# my constants
D=20

myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_FGC = 'RPFGC_PPSM.gpkg'
fn_RV = 'RVFundamental.gpkg'
fn_buffer='Buffer.gpkg'
fn_interior = 'interior.gpkg'
fn_exterior = 'exterior.gpkg'
fn_output= 'faixasIntExt.gpkg'

# Create project
myproject = QgsProject.instance() # does not write to file
#myproject.write(os.path.join(myfolder,'temp','myproject.qgs')) # (optional: write to file)

# Remove all layers in project
# myproject.mapLayers()
myproject.removeAllMapLayers()
    
# Canvas
# iface is set up to provide an object of the class QgisInterface to interact with the running QGIS 
# environment. This interface allows access to the map canvas, menus, toolbars and other 
# parts of the QGIS application.
canvas = iface.mapCanvas()
# Reload all layers, clears the cache and refreshes the canvas.
canvas.refreshAllLayers()

# Obs: one could bridge Canvas and LayerTree with QgsLayerTreeMapCanvasBridge

# run qgis functions
processing.run("native:buffer", 
{'INPUT':os.path.join(myfolder,'input',fn_RV),
'DISTANCE':D,
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':True,
'OUTPUT':os.path.join(myfolder,'temp',fn_buffer)})

processing.run("native:clip", 
{'INPUT':os.path.join(myfolder,'temp',fn_buffer),
'OVERLAY':os.path.join(myfolder,'input',fn_FGC),
'OUTPUT':os.path.join(myfolder,'temp',fn_interior)})

processing.run("native:difference", 
{'INPUT':os.path.join(myfolder,'input',fn_FGC),
'OVERLAY':os.path.join(myfolder,'temp',fn_interior),
'OUTPUT':os.path.join(myfolder,'temp',fn_exterior)})

processing.run("native:mergevectorlayers", 
{'LAYERS':[os.path.join(myfolder,'temp',fn_interior),os.path.join(myfolder,'temp',fn_exterior)],
'CRS':None,
'OUTPUT':os.path.join(myfolder,'temp',fn_output)})

# add output layer to QGIS interface
newlayer = iface.addVectorLayer(os.path.join(myfolder,'temp',fn_output),"", "ogr")
newlayer.setName('FaixasIntOut')

# or 
# create layer and add to project (same result)
mylayer=QgsVectorLayer(os.path.join(myfolder,'temp',fn_output),"", "ogr")
mylayer.setName('FaixasIntOut_2')
myproject.addMapLayer(mylayer)
