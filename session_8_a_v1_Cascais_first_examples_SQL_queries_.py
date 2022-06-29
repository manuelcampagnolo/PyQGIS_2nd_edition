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
myoutputdict={'roadType': QgsField('use',QVariant.String),'geom':'MULTILINESTRING'}

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
#
L=list(myoutputdict) # list of attributes for output layer (including 'geom')
if L==[] or 'geom' not in L:
    print(result)
    # Suggestion: convert "result" into a delimited text layer

# Create output spatial layer
if L!=[] and 'geom' in L:
    # Determine geometry for output layer
    idx_geom=L.index('geom') # index of 'geom' in "result"
    myoutputgeometry= myoutputdict['geom']
    # removes'geom' from output attributes
    myoutputdict.pop('geom')
    # Convert "result" into a new vector layer
    mylayer = QgsVectorLayer(myoutputgeometry, '', "memory")
    mylayer.setName('SQLqueryResult')
    pr = mylayer.dataProvider()
    # create new atributes (except 'geom')
    if not myoutputdict=={}:
        pr.addAttributes(list(myoutputdict.values())) # extract values from dict
        mylayer.updateFields() # “update-after-change”.
    # change CRS
    crs=mylayer.crs()
    crs.createFromId(mycrs)
    mylayer.setCrs(crs)
    
    # Populate mylayer with values in "result"
    with edit(mylayer):
        for row in result:
            # create new feature
            feat=QgsFeature()
            # feature's geometry
            mystr=row[idx_geom] # geometry
            mygeometry = QgsGeometry.fromWkt(mystr)
            feat.setGeometry(mygeometry)
            #feature's attributes # remainging values
            row.remove(mystr)
            if len(row)>0:
                feat.setAttributes(row) 
            # add feature to dataProvider
            ok=pr.addFeature(feat) 
            mylayer.updateExtents() # “update-after-change”.

    # add mylayer to the project
    myproject.addMapLayer(mylayer)
