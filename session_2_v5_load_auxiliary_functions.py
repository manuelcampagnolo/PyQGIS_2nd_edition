# session 2: categorized legend
# load auxiliary functions to make code more modular

#################################### import
import qgis # already loaded
import processing # idem
import os # file management

# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE

# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
fn_intext = os.path.join(myfolder,'temp','IntExt_20.gpkg')
ln_intext='IntExt' # layer name
# attribute to use for the legend
my_legend_att='layer'
# define legend to use: creates dictionary
mylegend={
'interior':('Clear everything',QColor('red'), 0.7), 
'exterior': ('Clear understory',QColor('green'), 0.7)
}

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()
    
# Read file and load layer into project
mylayer=QgsVectorLayer(fn_intext,"", "ogr")
mylayer.setName(ln_intext)
myproject.addMapLayer(mylayer)

# check that the legend attribute exists in vlayer
myattribs= mylayer.dataProvider().fields().names()
if my_legend_att not in myattribs: stop

# apply function to mylayer to build legend
create_categorized_legend(mylayer,my_legend_att,mylegend)
