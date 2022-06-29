# session 4_v2 graduated legend for NUTS using area and matplotlib colormap
# creates 1st dictionary with the classes
# then, uses dictionary to create graduated symbology

#################################### import
import qgis # already loaded
import processing # idem
import os # file management
import random # random numbers
import matplotlib # main python library for plots
import numpy as np # numpy, for arrays, etc

# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
fn_nuts = os.path.join(myfolder,'input','NUTS_RG_20M_2021_3035.shp')
ln_nuts='NUTS' # layer name
# attribute to use for the legend
my_legend_att='area' 
nuts_level_attrib='LEVL_CODE'
nuts_level_value=0 # NUTS level: the higher the level, the more regions there are
# legend parameters
colormap='viridis'
myopacity=0.8 # from 0 (transparent) to 1 (opaque)

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

###########################################  process data
# read data and create layer
my_add_vector_layer(fn_nuts,ln_nuts)

# select only feature for the chosen NUTS_level
dict_params={'FIELD':nuts_level_attrib, 'OPERATOR':0,'VALUE':nuts_level_value,}
ln_nuts_=ln_nuts+'_'+str(nuts_level_value)
mylayer=my_processing_run('native:extractbyattribute',ln_nuts,dict_params,ln_nuts_)

# remove original layer
my_remove_layer(ln_nuts)

# add area (m2) as a new attribute with Processing Toolbox and "add geometry attributes"
dict_params={'CALC_METHOD':2}
ln_nuts__=ln_nuts+'_'+str(nuts_level_value)+'_with_area'
mylayer=my_processing_run("qgis:exportaddgeometrycolumns",ln_nuts_,dict_params,ln_nuts__)

# remove intermediate layer
my_remove_layer(ln_nuts_)

################################################### creates legend
# check that the legend attribute exists in vlayer
myattribs= mylayer.dataProvider().fields().names()
if my_legend_att not in myattribs: stop

# determine what is the range of areas that we have in the map
idx = mylayer.fields().indexOf(my_legend_att)
myListValues = list(mylayer.uniqueValues(idx)) # uniqueValues returns a "set"
mymin=min(myListValues)
mymindigits=int(np.ceil(np.log10(mymin)))
mymax=max(myListValues)
mymaxdigits=int(np.ceil(np.log10(mymax)))
# number of classes
N=mymaxdigits+1-mymindigits

# Creates dictionary for the graduated legend
myDict={} # initialize
count=0
for i in range(mymindigits,mymaxdigits+1):
    # determine class minimum and maximum value
    if i==mymindigits: 
        classMin = 0
    else:
        classMin = classMax
    classMax = 10**i
    # label for the class:
    classMinKm2=int(classMin/10**6)
    classMaxKm2=int(classMax/10**6)
    mylabel = 'from {} to {} km2'.format(classMinKm2,classMaxKm2)
    # color using colormap defined in the header of the script
    mycolormap=matplotlib.cm.get_cmap(colormap,N) 
    mycolors=mycolormap.colors*255 # numpy.ndarray
    mycolor=mycolors[count]
    count +=1
    myQColor=QColor(mycolor[0],mycolor[1],mycolor[2])
    # insert a new entry to the dictionary
    myDict.update({mylabel : (classMin,classMax,myQColor,myopacity)})
print(myDict)

# creates object QgsRendererRange from myDict
myRangeList=[]
count=0
for mylabel, (classMin,classMax, myQColor, myopacity) in myDict.items():
    mySymbol = QgsSymbol.defaultSymbol(mylayer.geometryType())
    mySymbol.setColor(myQColor)
    mySymbol.setOpacity(myopacity)
    # new for graduated symbols:
    myRange = QgsRendererRange(classMin, classMax, mySymbol, mylabel)
    myRangeList.append(myRange)

# define GraduatedSymbol renderer and pass it to mylayer
renderer = QgsGraduatedSymbolRenderer(my_legend_att, myRangeList)
mylayer.setRenderer(renderer)
# Refresh layer
mylayer.triggerRepaint()