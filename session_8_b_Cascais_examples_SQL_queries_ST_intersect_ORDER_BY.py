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

# Determine 10 largest areas (in ha) in LandUse, needs join to list LandUseTypes
myselect= 'SELECT LandUseTypes.Use as land_use, ST_area(LandUse.geom)/10000 AS area_ha, LandUse.geom '
myfrom=   'FROM "LandUse", "LandUseTypes"'
mywhere=  'WHERE "LandUse"."codeUse"="LandUseTypes"."Code" '
myorderby='ORDER BY ST_area(LandUse.geom) DESC LIMIT 10'
myquery=   myselect+myfrom+mywhere+myorderby
myoutputdict={
'land_use':QgsField('land use',QVariant.String), 
'area_ha': QgsField('area_ha',QVariant.Double),
'geom':'MULTIPOLYGON'}

# Select by location and count number of features
myquery='SELECT Count(*) FROM LandUse, Streams WHERE ST_Intersects(LandUse.geom, Streams.geom)'
myoutputdict={}

### Select by location LandUse features that intersect Streams: returns geometry
myselect=" SELECT LandUse.codeUse, LandUse.geom"
myfrom=  " FROM LandUse, Streams"
mywhere="  WHERE ST_intersects (LandUse.geom,Streams.geom)"
myorderby="ORDER BY ST_area(LandUse.geom);"
myquery= myselect+myfrom+mywhere+myorderby
myoutputdict={'use':QgsField('use',QVariant.String,len=20),'geom':'MULTIPOLYGON'}

################################################################# Open connection to geopackage
# For info, if GPKG, use "ogr", if spatialite, use "spatialite"
md = QgsProviderRegistry.instance().providerMetadata("ogr")
conn = md.createConnection( fn, {})

################################################################# Execute query
result = conn.executeSql(myquery) # returns list

##################################################################Output result as new layer
mylayer=create_layer_from_sql_spatial_result(result,myoutputdict,mycrs)

# add mylayer to the project
myproject.addMapLayer(mylayer)
