from osgeo import ogr # connection to geopackage
import os

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# file name of new geopackage
fn_gpkg= os.path.join(myfolder,'temp','mygeopackage.gpkg')

# some (random) files to include in geopackage
# Simple table: Milk production for 2020
fn_ine = os.path.join(myfolder,'input','Milk_production_2020_INE.csv')
ln_ine='Milk_2020'
# Shapefile
fn_nuts = os.path.join(myfolder,'input','NUTS_RG_20M_2021_3035.shp')
ln_nuts='NUTS' # layer name
# Geopackage
fn_rnap=os.path.join(myfolder,'input',"RNAP.gpkg")
ln_rnap='RNAP'
# project CRS
mycrs=3763

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()
# set project CRS
crs=myproject.crs()
crs.createFromId(mycrs)
myproject.setCrs(crs)

# read sata sets and add each layer to project
params="?delimiter=;&detectTypes=yes&geomType=none"
uri='file:///'+fn_ine+params
mylayer = QgsVectorLayer(uri, '', "delimitedtext")
mylayer.setName(ln_ine)
myproject.addMapLayer(mylayer)
# vector layers
my_add_vector_layer(fn_nuts,ln_nuts)
my_add_vector_layer(fn_rnap,ln_rnap)

####################################### Create geopackage from layers
processing.run("native:package", 
{'LAYERS':[ln_rnap,ln_nuts,ln_ine],
'OUTPUT': fn_gpkg,
'OVERWRITE':True,
'SAVE_STYLES':True,
'SAVE_METADATA':True,
'SELECTED_FEATURES_ONLY':False})

# clear original layers
myproject,mycanvas = my_clean_project()

######################################### Inspect geopackage

# 1.  open the GeoPackage and get a a list of its layers:
gpkg_layers = [l.GetName() for l in ogr.Open(fn_gpkg)]
print(gpkg_layers)

# 2. load geopackage layers
def add_gpkg_layer(fn, ln):
    layers = [l.GetName() for l in ogr.Open(fn)]
    if ln in layers:
        fn_new=fn + "|layername=" + ln # layername within geopackage
        my_add_vector_layer(fn_new,ln)
    else: 
        print('Error: there is no layer named "{}" in {}!'.format(ln, gpkg))

add_gpkg_layer(fn_gpkg, ln_nuts)
add_gpkg_layer(fn_gpkg, ln_ine)
add_gpkg_layer(fn_gpkg, ln_rnap)

#3. in alternative, to load all layers:
for ln in gpkg_layers:
    add_gpkg_layer(fn_gpkg, ln)
