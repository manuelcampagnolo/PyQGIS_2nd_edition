# session 2: legends
# single symbol legend

import qgis # already loaded
import processing # idem
import os # file management

# my constants
myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_intext = os.path.join(myfolder,'temp','IntExt_20.gpkg')
ln_intext='IntExt' # layer name

# project and canvas
myproject = QgsProject.instance() # does not write to file
canvas = iface.mapCanvas()

# clear layers in project
myproject.removeAllMapLayers()

# refresh canvas
canvas.refreshAllLayers()

# Load layer into project
mylayer=QgsVectorLayer(fn_intext,"", "ogr")
mylayer.setName(ln_intext)
myproject.addMapLayer(mylayer)

######################################################################### renderer
#vlayer.renderer() gives us access to the vector layers renderer object. 
#There are different types of renderers: Single Symbol (QgsSingleSymbolRenderer), 
#Categorized (QgsCategorizedSymbolRenderer), Graduated (QgsGraduatedSymbolRenderer), and so on.
print(mylayer.renderer().dump())

# Change single symbol

# color
mycolor=QColor('red')
#or
mycolor=QColor(12, 34, 56, 180)  #RGBA 0-255 (A is transparency between 0 to 255=opaque)
#or
mycolor=QColor('#ff0000')  #hexadecimal
mycolor=QColor("red")
mylayer.renderer().symbol().setColor(mycolor)
# reset map
mylayer.triggerRepaint()

# transparency/opacity
mylayer.renderer().symbol().setOpacity(0.9) # between 0 and 1=opaque
mylayer.triggerRepaint()

# other options in symbolLayer(0)
dir(mylayer.renderer().symbol().symbolLayer(0)) 
mylayer.renderer().symbol().symbolLayer(0).setStrokeWidth(.8)
mylayer.triggerRepaint()

# Refresh layer's symbology in Layer Tree
iface.layerTreeView().refreshLayerSymbology(mylayer.id())