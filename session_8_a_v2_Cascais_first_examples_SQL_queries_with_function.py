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

# Note: to list tables, useful to know the table name in the sql query
gpkg_layers = [l.GetName() for l in ogr.Open(fn)]
#print(gpkg_layers)

# QUERY:
# Determine how many features Roads has
myquery="SELECT COUNT(*) from Roads"
myoutputdict={}

# Determine which values Roads.roadType takes
myquery="SELECT DISTINCT Roads.roadType from Roads"
myoutputdict={}

# Determine Roads which Type is not 'P': returns geometry
myquery="SELECT roadType,Roads.geom FROM Roads WHERE NOT roadType='P' "
myoutputdict={'roadType': QgsField('roadType',QVariant.String),'geom':'MULTILINESTRING'}

# Join attribute tables (LandUse and LandUseTypes). No "join clause": equivalent to "INNER JOIN"
myselect=  ' SELECT LandUse.codeUse, LandUseTypes.Use, LandUse.geom '
myfrom =   ' FROM LandUse, LandUseTypes '
mywhere=   ' WHERE LandUse.codeUse=LandUseTypes.Code'
myquery=   myselect+myfrom+mywhere
myoutputdict={'code':QgsField('code',QVariant.String), 'use':QgsField('use',QVariant.String),'geom':'MULTIPOLYGON'}

################################################################ Open connection to geopackage
# For info, if GPKG, use "ogr", if spatialite, use "spatialite"
md = QgsProviderRegistry.instance().providerMetadata("ogr")
conn = md.createConnection( fn, {})

################################################################# Execute query
result = conn.executeSql(myquery) # returns list

##################################################################Output result as new layer
mylayer=create_layer_from_sql_spatial_result(result,myoutputdict,mycrs)

# add mylayer to the project
myproject.addMapLayer(mylayer)
