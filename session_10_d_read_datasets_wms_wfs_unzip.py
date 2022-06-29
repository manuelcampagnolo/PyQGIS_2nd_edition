import os
from osgeo import gdal, osr
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


# my folders 
folder=r'C:\Users\mlc\Documents\PyQGIS'
subfolder='temp'

def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)

####################################################  DATA and PARAMETERS
# street maps
uri_StreetMap = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'

# COS 2018
fn_COS2018='COS2018-V1-PT150_Algarve.shp'
if fn_COS2018 not in os.listdir(os.path.join(folder,subfolder)):
    url_cos2018='http://mapas.dgterritorio.pt/DGT-ATOM-download/COS_Final/COS2018v1.0-NUT3/COS2018-V1-PT150_Algarve.zip'
    download_and_unzip(url_cos2018, extract_to=os.path.join(folder,subfolder))

# Sub regiões PROF
fn_PROF_SC='PROF_SerraCaldeirao.gpkg'
if fn_PROF_SC not in os.listdir(os.path.join(folder,subfolder)):
    uri_PROF2019='http://si.icnf.pt/wfs/prof_srh?service=wfs&version=2.0.0&request=GetCapabilities'
    vlayer=QgsVectorLayer(uri_PROF2019,'','ogr')
    # seleccionar Serra Caldeirão
    processing.run("native:extractbyexpression", \
    {'INPUT':vlayer,
    'EXPRESSION':' \"srh\" =  \'Serra do Caldeirao\' ',
    'OUTPUT':os.path.join(folder,subfolder,fn_PROF_SC)})

# create a project instance
myproj = QgsProject.instance() # does not write to file
canvas = iface.mapCanvas()
parent=iface.mainWindow() # necessary for QMessageBox

#remove layers and refresh canvas
for layer in myproj.mapLayers():  # myproj.mapLayers() is a dictionary
   myproj.removeMapLayer(layer)

canvas.refresh()

# set project CRS
my_crs=QgsCoordinateReferenceSystem(3763)
myproj.setCrs(my_crs)

#### read COS, select features that intersect Serra do Caldeirão 
cos2018original=QgsVectorLayer(os.path.join(folder,subfolder,fn_COS2018),'','ogr')

# populate canvas
iface.addRasterLayer(uri_StreetMap, "OpenStreetMap", "wms")
myproj.addMapLayer(cos2018original)
SC=iface.addVectorLayer(os.path.join(folder,subfolder,fn_PROF_SC),'','ogr')
SC.setName('SC')
my_symbol=QgsSymbol.defaultSymbol(SC.geometryType())
my_symbol.setColor(QColor('red'))
my_symbol.setOpacity(0.5)
SC.renderer().setSymbol(my_symbol)
SC.triggerRepaint()

# extent
canvas.setExtent(SC.extent())
canvas.refresh()

