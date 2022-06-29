# session 1: v6
# Simplifying session_1_v4 by using functions:
# my_clean_project
# my_add_vector_layer
# my_processing_run
# my_remove_layer

import qgis # already loaded
import processing # idem
import os # file management
from osgeo import ogr # connection to geopackage

myfolder=r'C:\Users\mlc\Documents\PyQGIS'
# load auxiliary functions
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my constants
fn=os.path.join(myfolder,'input','CascaisZoning.gpkg')
slopes = 'Slopes'
soilType = 'SoilType'
landUse = 'LandUse'
roads = 'Roads'
streams = 'Streams'
# tables
landUseTypes = 'LandUseTypes' 
roadProt='RoadProtection'
soilProd='SoilProductivity'

# keys for joins
key_landUse='codeUse'
key_landUseTypes='Code'
key_roadProt='Type'
key_roads='roadType'
key_soilType='COD1'
key_soilProd='code'

# some expressions and attributes
exp_soil=' "Productivt" = \'low\' OR  "Productivt" = \'medium\' ' # table SoilProductivity
exp_use=' "Use" IN (\' agriculture\',\' forest and bush\',\' bush\' ,\' bare ground\')' # table LandUseTypes
exp_slopes = '("Use" <> \' forest and bush\' AND  "SlopeType" = \'up to 5%\' ) OR ( "Use" = \' forest and bush\' )'
exp_streams = ' "strType" = \'main\' ' # table Streams
exp_area = ' \"area\" >300000 '  
an_distance='Distance' # table RoadProtection

##################################################### project; add layers
# Create project
myproject,mycanvas= my_clean_project()

# load layers into project with name equal to geopackage layer name
gpkg_layers = [l.GetName() for l in ogr.Open(fn)]
for ln in gpkg_layers:
    my_add_vector_layer(fn + "|layername=" + ln,ln)

##################################################### data analysis

# join layers about Land Use
dict_params={'FIELD': key_landUse,'INPUT_2': 'LandUseTypes', 'FIELD_2':key_landUseTypes}
mylayer=my_processing_run("native:joinattributestable",'LandUse',dict_params,'LandUse_Join')
my_remove_layer('LandUse')
my_remove_layer('LandUseTypes')

# select suitable land use
dict_params={'EXPRESSION': exp_use}
mylayer=my_processing_run("native:extractbyexpression",'LandUse_Join',dict_params,'suitableLandUse')
my_remove_layer('LandUse_Join')

# join layers about Soil
dict_params={'FIELD': key_soilType,'INPUT_2': 'SoilProductivity', 'FIELD_2':key_soilProd}
mylayer=my_processing_run("native:joinattributestable",'SoilType',dict_params,'soilType_Join')
my_remove_layer('SoilType')
my_remove_layer('SoilProductivity')

# select suitable soil type 
dict_params={'EXPRESSION': exp_soil}
mylayer=my_processing_run("native:extractbyexpression",'soilType_Join',dict_params,'suitableSoilType')
my_remove_layer('soilType_Join')

# clip suitable Land Use with suitable Soil Type
dict_params={'OVERLAY':'suitableSoilType'}
mylayer=my_processing_run("native:clip",'suitableLandUse',dict_params,'suitable_Use_and_Type')
my_remove_layer('suitableSoilType')

# Intersection of suitable Land Use with Slopes
dict_params={'OVERLAY':'Slopes'}
mylayer=my_processing_run("native:intersection",'suitableLandUse',dict_params,"Use_and_Slopes")
my_remove_layer('Slopes')
my_remove_layer('suitableLandUse')

# Select suitable slopes
dict_params={'EXPRESSION': exp_slopes}
mylayer=my_processing_run("native:extractbyexpression",'Use_and_Slopes',dict_params,'suitable_Use_and_Slopes')
my_remove_layer('Use_and_Slopes')

# Clip suitable Land Use and Soil Type with suitable Slopes
dict_params={'OVERLAY':'suitable_Use_and_Slopes'}
mylayer=my_processing_run("native:clip",'suitable_Use_and_Type',dict_params,'suitable_Use_Type_Slope')
my_remove_layer('suitable_Use_and_Slopes')
my_remove_layer('suitable_Use_and_Type')

# join layers about Roads
dict_params={'FIELD': key_roads,'INPUT_2': 'RoadProtection', 'FIELD_2':key_roadProt}
mylayer=my_processing_run("native:joinattributestable",'Roads',dict_params,'roads_Join')
my_remove_layer('RoadProtection')

# Create buffer around Roads
dict_params={'DISTANCE':QgsProperty.fromExpression('"Distance"'),'DISSOLVE':True}
mylayer=my_processing_run("native:buffer",'roads_Join',dict_params,'roadsBuffer')
my_remove_layer('roads_Join')

# Remove roads buffer from suitable areas
dict_params={'OVERLAY':'roadsBuffer'}
mylayer=my_processing_run("native:difference",'suitable_Use_Type_Slope',dict_params,'suitable')
my_remove_layer('roadsBuffer')
my_remove_layer('suitable_Use_Type_Slope')

# Dissolve suitable areas
dict_params={}
mylayer=my_processing_run("native:dissolve",'suitable',dict_params,'suitableDissolved')
my_remove_layer('suitable')

# Convert to singlepart (spatially connected)
dict_params={}
mylayer=my_processing_run("native:multiparttosingleparts",'suitableDissolved',dict_params,'suitableSinglepart')
my_remove_layer('suitableDissolved')

# Select main streams slopes
dict_params={'EXPRESSION': exp_streams}
mylayer=my_processing_run("native:extractbyexpression",'Streams',dict_params,'mainStreams')
my_remove_layer('Streams')

# Select by location suitable areas that are intersected by main streams
dict_params={'PREDICATE':[0], 'INTERSECT':'mainStreams'}
mylayer=my_processing_run("native:extractbylocation",'suitableSinglepart',dict_params,'suitable_with_mainStreams')
my_remove_layer('suitableSinglepart')

# Calculate areas
dict_params={'CALC_METHOD':2}
mylayer=my_processing_run("qgis:exportaddgeometrycolumns",'suitable_with_mainStreams',dict_params,'suitable_with_area_m2')
my_remove_layer('suitable_with_mainStreams')

# Select  areas with more than 30 ha = 300000 m2
dict_params={'EXPRESSION': exp_area}
mylayer=my_processing_run("native:extractbyexpression",'suitable_with_area_m2',dict_params,'final')
my_remove_layer('suitable_with_area_m2')

