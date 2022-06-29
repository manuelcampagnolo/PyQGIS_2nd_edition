# session 1: version 1
# create variables for distance and for file names

import qgis # already loaded
import processing # idem
import os # file management

# my constants
D=12.5

myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_FGC = 'RPFGC_PPSM.gpkg'
fn_RV = 'RVFundamental.gpkg'
fn_buffer='Buffer.gpkg'
fn_interior = 'interior.gpkg'
fn_exterior = 'exterior.gpkg'
fn_output= 'faixasIntExt.gpkg'

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


