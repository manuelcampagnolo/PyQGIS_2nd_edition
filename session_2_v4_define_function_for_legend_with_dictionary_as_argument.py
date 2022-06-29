# session 2: legends
# define categorized legend from dictionary
# create function that adds legend

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
mylegend1={
'interior':('Clear all',QColor('light green'), 0.7), # label, color, opacity
'exterior': ('Clear understory',QColor('dark green'), 0.5)
}
mylegend2={
'interior':('Clear everything',QColor('#ff0000'), 0.7), 
'exterior': ('Clear understory',QColor('#ffff00'), 0.7)
}

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

# define function
# input: layer to render, attribute to use, dictionary for the legend
# no output
def create_categorized_legend(vlayer,attrib,dict):
    # create categories from mydict
    categories=[] # empty list
    for myvalue, (mylabel,mycolor, myopacity) in dict.items():
        print(myvalue,mylabel, mycolor, myopacity)
        mysymbol=QgsSymbol.defaultSymbol(vlayer.geometryType())
        mysymbol.setColor(mycolor)
        mysymbol.setOpacity(myopacity)
        cat=QgsRendererCategory(myvalue, mysymbol, mylabel)
        categories.append(cat)
    # create renderer
    renderer = QgsCategorizedSymbolRenderer(attrib, categories)
    vlayer.setRenderer(renderer)
    # Refresh layer
    vlayer.triggerRepaint()
    
# apply function to mylayer
create_categorized_legend(mylayer,my_legend_att,mylegend2)
create_categorized_legend(mylayer,my_legend_att,mylegend1)
