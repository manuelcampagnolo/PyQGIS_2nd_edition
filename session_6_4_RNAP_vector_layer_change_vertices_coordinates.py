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
lnoriginal='RNAP'
ndigits=2 # we are going to change the number of digits of each feature
ln=lnoriginal+'_'+str(ndigits)+'_digits'

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# read data
vlayer=my_add_vector_layer(fn,lnoriginal)

################### make a deep copy of vlayer, so we don't alter the original data set
vlayer.selectAll()
mylayer=my_processing_run("native:saveselectedfeatures",lnoriginal,{},ln)
vlayer.removeSelection()
my_remove_layer(lnoriginal)

##################### from now on, we just work with the deep copy "mylayer"

#https://gis.stackexchange.com/questions/377513/filtering-layers-by-geometry-type-using-pyqgis

# Check layer geometry 
mylayertype=QgsWkbTypes.geometryDisplayString(mylayer.geometryType()) 
print(QgsWkbTypes.wkbDimensions(mylayer.wkbType()))
if QgsWkbTypes.isSingleType(mylayer.wkbType()):
    mylayermult='single type'

if QgsWkbTypes.isMultiType(mylayer.wkbType()):
    mylayermult='multi type'

QMessageBox.information(parent,'Info',"{} is {} {}".format(ln,mylayermult,mylayertype))

# MUltipolygon data structure
# Since it is a MultiPolygon, the list has 3 levels (2 for D=2, and 1 for Multi)

###########################################################################Create wkt string
# Edit layer and round vertices to ndigits (Problem suggested by Miguel)
# use function "round_vertices_coordinates_multipolygon(vlayer,ndigits)"
D=QgsWkbTypes.wkbDimensions(feat.geometry().wkbType())
if feat.geometry().isMultipart() and D==2:
    mylayer=round_vertices_coordinates_multipolygon(mylayer,ndigits)
    mylayer.setName(ln)
    QgsProject.instance().addMapLayer(mylayer)

# look at some vertex
feat=mylayer.getFeature(1) # 1st feature
f=feat.geometry().asMultiPolygon()
v=f[0][0][0]
print('coordinates of some vertex: ',v.toString())

