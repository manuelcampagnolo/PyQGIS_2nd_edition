# session 1: version 1
# just copy/paste from history

import qgis # already loaded
import processing # idem
import os # file management

processing.run("native:buffer", 
{'INPUT':'C:/Users/mlc/Documents/PyQGIS/input/RVFundamental.gpkg',
'DISTANCE':12.5,
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':False,
'OUTPUT':'C:/Users/mlc/Documents/PyQGIS/temp/Buffer.gpkg'})

processing.run("native:buffer", 
{'INPUT':os.path.join(myfolder,'input',fn_RV),
'DISTANCE':D,
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':True,
'OUTPUT':os.path.join(myfolder,'input','Buffer.gpkg')})

processing.run("native:clip", 
{'INPUT':'C:/Users/mlc/Documents/PyQGIS/temp/Buffer.gpkg',
'OVERLAY':'C:/Users/mlc/Documents/PyQGIS/input/RPFGC_PPSM.gpkg',
'OUTPUT':'C:/Users/mlc/Documents/PyQGIS/temp/Interior.gpkg'})

processing.run("native:difference", 
{'INPUT':'C:/Users/mlc/Documents/PyQGIS/input/RPFGC_PPSM.gpkg',
'OVERLAY':'C:/Users/mlc/Documents/PyQGIS/temp/Interior.gpkg',
'OUTPUT':'C:/Users/mlc/Documents/PyQGIS/temp/Exterior.gpkg'})

processing.run("native:mergevectorlayers", 
{'LAYERS':['C:/Users/mlc/Documents/PyQGIS/temp/Exterior.gpkg','C:/Users/mlc/Documents/PyQGIS/temp/Interior.gpkg'],
'CRS':None,
'OUTPUT':'C:/Users/mlc/Documents/PyQGIS/temp/FaixasIntExt.gpkg'})


