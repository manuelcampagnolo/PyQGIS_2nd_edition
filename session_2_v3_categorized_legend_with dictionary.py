# session 2: legends
# sdefine categorized legend from dictionary

import qgis # already loaded
import processing # idem
import os # file management

# my constants
myfolder=r'C:/Users/mlc/Documents/PyQGIS'
fn_intext = os.path.join(myfolder,'temp','IntExt_20.gpkg')
ln_intext='IntExt' # layer name

# attribute to use for the legend
my_legend_att='layer'

# legend options
mylegend={
'interior':('Clear all','light green', 0.7), # label, color, opacity
'exterior': ('Clear understory','dark green', 0.5)
}
print(mylegend.items())

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

############################################################
# categorizedSymbols

categories=[] # empty list
for myvalue, (mylabel,mycolor, myopacity) in mylegend.items():
    print(myvalue,mylabel, mycolor, myopacity)
    mysymbol=QgsSymbol.defaultSymbol(mylayer.geometryType())
    mysymbol.setColor(QColor(mycolor))
    mysymbol.setOpacity(myopacity)
    cat=QgsRendererCategory(myvalue, mysymbol, mylabel)
    categories.append(cat)

renderer = QgsCategorizedSymbolRenderer(my_legend_att, categories)
mylayer.setRenderer(renderer)
# Refresh layer
mylayer.triggerRepaint()

# Challenge: Try to change the StrokeWidth to 0.7 for both legend levels