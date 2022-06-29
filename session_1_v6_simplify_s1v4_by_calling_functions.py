# session 1: v6
# Simplifying session_1_v4 by using functions:
# my_clean_project
# my_add_vector_layer
# my_processing_run
# my_remove_layer

import qgis # already loaded
import processing # idem
import os # file management

myfolder=r'C:/Users/mlc/Documents/PyQGIS'
# load auxiliary functions
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my constants
D=25

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
myproject,mycanvas= my_clean_project()

# Add input as project layer
mylayer=my_add_vector_layer(fn_FGC,layer_FGC)
mylayer=my_add_vector_layer(fn_RV,layer_RV)

# run qgis functions from Processing Toolbox
dict_params={'DISTANCE':D,'DISSOLVE':True}
mylayer=my_processing_run("native:buffer",layer_RV,dict_params,layer_buffer)

dict_params={'OVERLAY':layer_FGC}
mylayer=my_processing_run("native:clip",layer_buffer,dict_params,layer_interior)

dict_params={'OVERLAY':layer_interior}
mylayer=my_processing_run("native:difference",layer_FGC,dict_params,layer_exterior)

dict_params={'LAYERS':[layer_interior,layer_exterior],'OVERLAY':layer_interior}
mylayer=my_processing_run("native:mergevectorlayers",'',dict_params,layer_output)

# export mylayer as a geopackage file
QgsVectorFileWriter.writeAsVectorFormat(mylayer,
fn_output, "UTF-8", mylayer.crs(), "GPKG",attributes=[1])

# delete input and intermediate layers
my_remove_layer(layer_RV)
my_remove_layer(layer_FGC)
my_remove_layer(layer_buffer)
my_remove_layer(layer_interior)
my_remove_layer(layer_exterior)
