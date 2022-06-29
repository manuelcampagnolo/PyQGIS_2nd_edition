# session 3_v1: re-use create_categorized_legend for new data set

#################################### import
import qgis # already loaded
import processing # idem
import os # file management
import random # random numbers

# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE

# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
fn_nuts = os.path.join(myfolder,'input','NUTS_RG_20M_2021_3035.shp')
ln_nuts='NUTS' # layer name
# attribute to use for the legend
my_legend_att='CNTR_CODE'
nuts_level_attrib='LEVL_CODE'
nuts_level_value=2 # NUTS level: the higher the level, the more regions there are
# legend parameters
colorMin=100  # between 0 and 255
colorMax=255 # between 0 and 255
myOpacity=0.8 # from 0 (transparent) to 1 (opaque)

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

###########################################  process data
# read data and create layer
mylayer=QgsVectorLayer(fn_nuts,"", "ogr")
mylayer.setName(ln_nuts)
myproject.addMapLayer(mylayer)

# select only feature for the chosen NUTS_level
mylayer=processing.run("native:extractbyattribute", 
{'INPUT':ln_nuts,
'FIELD':nuts_level_attrib,
'OPERATOR':0,
'VALUE':nuts_level_value,
'OUTPUT':QgsProcessing.TEMPORARY_OUTPUT})['OUTPUT']

mylabel=ln_nuts+'_'+str(nuts_level_value)
mylayer.setName(mylabel)
myproject.addMapLayer(mylayer)

################################################### creates legend
# check that the legend attribute exists in vlayer
myattribs= mylayer.dataProvider().fields().names()
if my_legend_att not in myattribs: stop

# determine which unique values my_legend_att can take
idx = mylayer.fields().indexOf(my_legend_att)
myListValues = list(mylayer.uniqueValues(idx)) # uniqueValues returns a "set"

# define legend to use: creates dictionary
# 1. Create list of categories (one for each legend class)
myDict={} # initialize
# creates dictionary: one entry per value in myListValues
for val in myListValues:
    val = str(val) # to be sure it is a string
    myR=random.randint(colorMin,colorMax) 
    myG=random.randint(colorMin,colorMax)
    myB=random.randint(colorMin,colorMax)
    myQColor=QColor(myR,myG,myB)
    # insert a new entry to the dictionary
    myDict.update({val : (val,myQColor,myOpacity)})
    
# apply auxiliary function to build legend
create_categorized_legend(mylayer,my_legend_att,myDict)

print(myDict)

# challenge: define new function 'create_random_categorized_legend' 
# with arguments mylayer, my_legend_att, 
# colorMin, colorMax, myOpacity that creates legend: a call to this 
# function should replace all the code above after "creates legend"
# Note: this new function should include a call to 'create_categorized_legend'