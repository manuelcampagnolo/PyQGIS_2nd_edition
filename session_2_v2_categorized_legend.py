# session 2: legends
# single symbol legend

import qgis # already loaded
import processing # idem
import os # file management

# my constants
myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_intext = os.path.join(myfolder,'temp','IntExt_20.gpkg')
ln_intext='IntExt' # layer name

# attribute to use for the legend
my_legend_att='layer'

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

# check that the legend attribute exists in mylayer
myattribs= mylayer.dataProvider().fields().names()
if my_legend_att not in myattribs: stop

######################################################################### renderer
#vlayer.renderer() gives us access to the vector layers renderer object. 
#There are different types of renderers: Single Symbol (QgsSingleSymbolRenderer), 
#Categorized (QgsCategorizedSymbolRenderer), Graduated (QgsGraduatedSymbolRenderer), and so on.
print(mylayer.renderer().dump())

############################################################
# categorizedSymbols
mysymbol1=QgsSymbol.defaultSymbol(mylayer.geometryType())
mysymbol2=QgsSymbol.defaultSymbol(mylayer.geometryType())

mysymbol1.setColor(QColor('light green'))
mysymbol2.setColor(QColor('dark green'))

cat1=QgsRendererCategory('interior', mysymbol1, 'Clear all') # value, symbol, label
cat2=QgsRendererCategory('exterior', mysymbol2, 'Clear understory')

categories=[cat1,cat2]

renderer = QgsCategorizedSymbolRenderer(my_legend_att, categories)
mylayer.setRenderer(renderer)
# Refresh layer
mylayer.triggerRepaint()

# Challenge: Try to change the StrokeWidth to 0.7 for the exterior feature