from osgeo import ogr # connection to geopackage
import os
from qgis.PyQt.QtCore import QVariant # types for attributes in vector layers QVariant.String, QVariant.Int, QVariant.Double

parent=iface.mainWindow() # for message box

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# Constants and SQL queries
# geopackage name
fn = os.path.join(myfolder,'input','CascaisZoning.gpkg')
mycrs=3763

## Create buffer around Roads using distance in RoadProtection.Distance
myselect="SELECT RoadProtection.Distance as buffer, ST_buffer(Roads.geom, RoadProtection.Distance) as geom"
myfrom="  FROM Roads, RoadProtection"
mywhere=" WHERE Roads.roadType=RoadProtection.Type"
myquery=myselect+myfrom+mywhere
myoutputdict={'buffer':QgsField('buffer',QVariant.Int), 'geom':'MultiPolygon'}
ln='BufferRoads'

################################################################# Open connection to geopackage
# For info, if GPKG, use "ogr", if spatialite, use "spatialite"
md = QgsProviderRegistry.instance().providerMetadata("ogr")
conn = md.createConnection( fn, {})

################################################################# Execute query
result = conn.executeSql(myquery) # returns list

##################################################################Output result as new layer
#
mylayer=create_layer_from_sql_spatial_result(result,myoutputdict,mycrs)
myproject.addMapLayer(mylayer)
mylayer.setName(ln)

# Optional: add new layer to geopackage (necessary for new queries involving the new layer)
res=QMessageBox.question(parent,'Question', 'Do you want to add the new layer to the geopackage ?' )
if res==QMessageBox.Yes:
    add_layer_to_geopackage(fn,ln)

