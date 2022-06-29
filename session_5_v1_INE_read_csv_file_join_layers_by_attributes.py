# Read and pre-process non-spatial INE data set 
# Read and pre-process spatial CAOP map
# Join both table
# Create a map to display spatially values in the INE table.

#################################### import
import qgis # already loaded
import processing # idem
import os # file management
import numpy as np # numpy, for arrays, etc
from urllib.parse import urljoin #path2uri
import urllib.request
from qgis.PyQt.QtCore import QVariant # types for attributes in vector layers
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel)


# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
fn_caop = os.path.join(myfolder,'input','Cont_AAD_CAOP2020.gpkg')
ln_caop ='CAOP' # 3-level administrative units for Portugal 
an_caop_dicofre='Dicofre' # attribute of the 3-level code
# Milk production for 2020
fn_ine = os.path.join(myfolder,'input','Milk_production_2020_INE.csv')
ln_ine='Milk_2020'
an_nuts_code='NUTS_2013' # to select lowest level (LAU)
# Milk production only at the LAU level
ln_ine_lau='Milk_2020_LAU'
an_ine_lau='lau_code'
num_digits_codes=4
# new attribute name to add to CAOP
an_new_caop_code='dico'
# 2-level administrative units for Portugal (after dissolve)
ln_caop_dico='Concelhos_dico'

# output map: choose milk type with dialog box
myoptions=["Cow","Sheep","Goat"] #alternatively, vlayer.dataProvider().fields().names()
myoption, ok = QInputDialog.getItem(parent, "select:", "milk types", myoptions, 0, False)
my_legend_att=myoption
colormap='viridis'
myopacity=0.7

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

######################  read and process a non-spatial table
#
# convert data to utf-8 if they use a different encoding 
convert_encoding_to_utf8(os.path.join(myfolder,'input',fn_ine))

# parameters to read csv file (some options)
params='?delimiter=%s&xField=%s&yField=%s' % (",", "Lon", "Lat")
sep=';'
params="?delimiter={}&detectTypes=yes&geomType=none".format(sep)
params="?delimiter=;&detectTypes=yes&geomType=none"

# uri for reading the file as "delimitedtext"
uri='file:///'+fn_ine+params
mylayer = QgsVectorLayer(uri, '', "delimitedtext")
mylayer.setName(ln_ine)
myproject.addMapLayer(mylayer)

# However, we cannot use dataProvider to add attributes to this layer
print(mylayer.dataProvider().capabilitiesString())

# instead, we use a Toolbox function to create a new attribute with NULL values
dict_params={'FIELD_NAME':an_ine_lau,'FIELD_TYPE':2,'FIELD_LENGTH':10,'FIELD_PRECISION':0}
mylayer=my_processing_run("native:addfieldtoattributestable",ln_ine,dict_params,ln_ine_lau)
print(mylayer.dataProvider().capabilitiesString())

# remove previous layer
my_remove_layer(ln_ine)

# Lets edit the text layer and make some changes to it
# 1st determine which features have the longest code
# and how many digits it does have

maxDigits=0
for f in mylayer.getFeatures():
    if len(f[an_nuts_code]) > maxDigits:
       maxDigits=len(f[an_nuts_code])
print(maxDigits)

# for those, compute and store new 4-digit code (last 4 digits)
with edit(mylayer):
    for f in mylayer.getFeatures():
        if len(f[an_nuts_code]) == maxDigits:
            #print(f[an_nuts_code])
            f[an_ine_lau] = f[an_nuts_code][-num_digits_codes:] # last 4 digits
            res=mylayer.updateFeature(f) # to be silent

################################################ LAU map
# import LAU map and create a foreign key to be able to join with the 
mylayer=my_add_vector_layer(fn_caop,ln_caop)

# create new attribute with dataProvider
# checks if attribute already exists
pr=mylayer.dataProvider()
if an_new_caop_code not in pr.fields().names(): 
    pr.addAttributes([QgsField(an_new_caop_code,QVariant.String,len=num_digits_codes)])
    mylayer.updateFields()

# compute new 4-digit code (first 4 digits)
with edit(mylayer):
    for f in mylayer.getFeatures():
        f[an_new_caop_code] = f[an_caop_dicofre][:num_digits_codes] # last 4 digits
        res=mylayer.updateFeature(f) # to be silent

# dissolve by "dico"
dict_params={'FIELD':['dico']}
mylayer=my_processing_run("native:dissolve",ln_caop,dict_params,ln_caop_dico)

# remove previous layer
my_remove_layer(ln_caop)

###################################### join layers by attribute
# join layer CAOP and INE (milk) 
ln_caop_ine='caop_ine'
dict_params={'FIELD': an_new_caop_code,'INPUT_2': ln_ine_lau, 'FIELD_2':an_ine_lau}
mylayer=my_processing_run("native:joinattributestable",ln_caop_dico,dict_params,ln_caop_ine)

##################################### legend
# legends for cow, sheep and goat milk production

# determine what is the range of values for the legend
idx = mylayer.fields().indexOf(my_legend_att)
myListValues = list(mylayer.uniqueValues(idx)) # uniqueValues returns a "set"

# or, as and alternative, get values from field with the QgsVectorLayerUtils class
myListValues,selected=QgsVectorLayerUtils.getValues(mylayer, my_legend_att,selectedOnly=False)

# create dictionary for legend
myDict=create_sturges_graduated_legend_dict(myListValues,colormap,myopacity,'kl')

# create legend using attribute my_legend_att
create_graduated_legend(mylayer,my_legend_att,myDict)

# Information message box
QMessageBox.information(parent,'2020 production', '{} milk in 1000 l'.format(my_legend_att))
