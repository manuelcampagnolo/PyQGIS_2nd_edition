#################################### import
import qgis # already loaded
import processing # idem
import os # file management
import numpy as np # numpy, for arrays, etc
from qgis.PyQt.QtCore import QVariant # types for attributes in vector layers

parent=iface.mainWindow() # necessary for QMessageBox

# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
fn=os.path.join(myfolder,'input',"landUse_invalid_features.gpkg") # data set with invalid feature
lnoriginal='LandUse'
ln=lnoriginal+'_copy'

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# read data
vlayer=my_add_vector_layer(fn,lnoriginal)

#https://gis.stackexchange.com/questions/377513/filtering-layers-by-geometry-type-using-pyqgis

###########################################Make layer clone (to edit the clone)
vlayer.selectAll()
mylayer=my_processing_run("native:saveselectedfeatures",lnoriginal,{},ln)
vlayer.removeSelection()

print('distinct ids: ', id(vlayer),id(mylayer))

########################################################################################
# check validity of features with method isGeosValid()
feats=mylayer.getFeatures()
not_valid_ids=[]
for feat in feats:
    if not feat.geometry().isGeosValid():
        not_valid_ids.append(feat.id())

QMessageBox.information(parent,'Info','There are {} not valid features'.format(len(not_valid_ids)))

# print list of ids of not valid features
if len(not_valid_ids)>0: print('invalid ids: ',not_valid_ids)

# Select invalid features 
mylayer.select(not_valid_ids)

QMessageBox.information(parent,'Info','Not valid features')


############################################################## Fixing invalid features
# Try to fix invalid geometries with GEOS method .makeValid()
with edit(mylayer):
    feats=mylayer.selectedFeatures() # just selected 
    for feat in feats:
        geom=feat.geometry().makeValid()
        feat.setGeometry(geom)
        mylayer.updateFeature(feat)

# Clear Selection
mylayer.removeSelection()

# Check result by identifying invalid features again
feats=mylayer.getFeatures()
not_valid_ids=[]
for feat in feats:
    if not feat.geometry().isGeosValid():
        not_valid_ids.append(feat.id())

QMessageBox.information(parent,'Info','There are {} not valid features'.format(len(not_valid_ids)))

mylayer.select(not_valid_ids) # if none are selected, there are no invalid features any more.

