from osgeo import ogr # connection to geopackage
import os
from qgis.PyQt.QtCore import QVariant # types for attributes in vector layers QVariant.String, QVariant.Int, QVariant.Double

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# Constants and SQL queries
# geopackage name
fn = os.path.join(myfolder,'input','CascaisZoning.gpkg')
mycrs=3763

# SQL query: Determine which values LandUse takes
myquery="SELECT DISTINCT LandUse.codeUse FROM LandUse"

################################################################# Open connection to geopackage
# For info, if GPKG, use "ogr", if spatialite, use "spatialite"
md = QgsProviderRegistry.instance().providerMetadata("ogr")
conn = md.createConnection( fn, {})

################################################################# Execute query
result = conn.executeSql(myquery) # returns list

print(result)