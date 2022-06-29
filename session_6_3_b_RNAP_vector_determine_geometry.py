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
fn=os.path.join(myfolder,'input',"Streams.gpkg")
ln='streams'

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# read data
mylayer=my_add_vector_layer(fn,ln)

#https://gis.stackexchange.com/questions/377513/filtering-layers-by-geometry-type-using-pyqgis

########################################################################################
# https://opensourceoptions.com/blog/pyqgis-get-feature-geometry/
# editing the location of a feature requires you to access the feature’s geometry

###################################################### Determine features geometry type
# Determine layer's geometry: dimension and type (single part or multipart)
# it can be Point, LineString or Polygon
mylayertype=QgsWkbTypes.geometryDisplayString(mylayer.geometryType()) 
print(QgsWkbTypes.wkbDimensions(mylayer.wkbType()))
if QgsWkbTypes.isSingleType(mylayer.wkbType()):
    mylayermult='single type'

if QgsWkbTypes.isMultiType(mylayer.wkbType()):
    mylayermult='multi type'

QMessageBox.information(parent,'Info',"{} is {} {}".format(ln,mylayermult,mylayertype))

# Determine list of geometry types for the features
# The type() method which returns a value from the QgsWkbTypes.GeometryType enumeration.
# The wkbType() method is the one to use. It returns a value from the QgsWkbTypes.Type enumeration.
# Use displayString to get wkbTypes
mytypes=[]
for feat in mylayer.getFeatures():
    myfeattype=QgsWkbTypes.displayString(feat.geometry().wkbType())
    mytypes.append(myfeattype)

print(mytypes) # e.g. MultiSurface

# Note: some methods that can be applied to QgsWkbTypes to get geometry information about 1 feature
print('info about the last feature of the layer')
print('wkbType',QgsWkbTypes.displayString(feat.geometry().wkbType()))
print('Is multitype? ', QgsWkbTypes.isMultiType(feat.geometry().wkbType())) 
print('Is multitype? ', feat.geometry().isMultipart()) # simpler
print('Is singletype? ', QgsWkbTypes.isSingleType(feat.geometry().wkbType())) 
print("Feature's dimension", QgsWkbTypes.wkbDimensions(feat.geometry().wkbType()))
print('Has M coord? ',QgsWkbTypes.hasM(feat.geometry().wkbType())) 
print('Has Z coord? ',QgsWkbTypes.hasZ(feat.geometry().wkbType())) 
