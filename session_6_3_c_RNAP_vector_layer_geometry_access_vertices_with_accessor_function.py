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
fn=os.path.join(myfolder,'input',"RNAP.gpkg")
ln='RNAP'

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# read data
mylayer=my_add_vector_layer(fn,ln)

# Get the first feature from the layer
feat=mylayer.getFeature(1) # 1st feature

############################################################################ Accessor functions
# To extract information from a geometry there are accessor functions 
# for every vector type.
# asPoint(), asPolyline(), asPolygon(), asMultiPoint(), asMultiPolyline() and asMultiPolygon().
# Check from wkbType what is the accessor function
D=QgsWkbTypes.wkbDimensions(feat.geometry().wkbType())
if feat.geometry().isMultipart() and D==2:
    print(feat.geometry().asMultiPolygon()) # Returns a list

# Challenge: Build a function such that:
# input: feature (any kind of geometry)
# applies the correct accessor function to the feature and returns a list
# Test with layers of different types.

################################################################# Access coordinates of vertices
# MUltipolygon data structure
# let's look at the feature feat 
# Since it is a MultiPolygon, the list has 3 levels (2 for D=2, and 1 for Multi)
f=feat.geometry().asMultiPolygon() # feature f as list 
f[0] # 1st part of feature f
f[0][0] # 1st ring (exterior ring) of the 1st part of feature feat
f[0][0][0] # 1st vertex of that ring : QgsPointXY object
# x and y coordinates of the 1st vertex of the 1st ring of the 1st part of feature "feat"
v=f[0][0][0]
print(v.toString(2)) # string
print(v.x()) # float
print(v.y()) # float