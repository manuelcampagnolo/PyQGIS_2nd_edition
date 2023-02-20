# PyQGIS_2nd_edition

Instructor: Manuel Campagnolo, ISA/ULisboa

Notice: the local organization of files should be as described below for Windows (please adapt the paths for MasOS). Data are organized in sub-folders, to be just under an arbitrary "working folder" (e.g. C:\users\my_user\Documents\PyQGIS):

- input: input data sets for class exercises (e.g. `C:\users\my_user\Documents\PyQGIS\input`): where input files should be stored
- scripts: where python scripts should go (e.g. `C:\users\my_user\Documents\PyQGIS\scripts`): where Python scripts should be stored
- temp: temporary folder for outputs (e.g. `C:\users\my_user\Documents\PyQGIS\temp`): where intermediate and output files should be written

# Session 1: First example; using processing and history to obtain commands for the script; using variables and file paths

* Input data: Vector geografic data sets representing a road (RVFundamental.gpkg) and a protection area for wild fires (RPFGC_PPSM.gkpk). See this map and the intended vegetation profile from Manual da Rede Primária.
* Problem: determine two road buffers: one interior buffer within distance D of the road; one exterior buffer to fill the rest of the protection area. Both buffers need to be contained within the protection area. Then, create a single data set containing both buffers with an attribute that takes value "interior" and "exterior". See operations diagram for the problem.
* Extensions of the problem: (1) Use a variable for D instead of a fixed value; (2) use variables for the folder and file names; (3) add output to interface as a QGIS layer; (4) clear QGIS layers; (5) Solve the more realistic problem with 3 regions instead of 2.
  * Extra reading:
    - See "Using processing algorithms from the console" from QGIS documentation
    - The QgsProject class from QGIS documentation

# Session 2: Create layers in memory; Export a layer to file; Symbology; Renderer; Change symbol in Single Symbol (color, opacity, stroke width); Create Categorized legend; List attribute names for the layer (access attribute table).

* Problem: Write new solution for the problem of session 1 using temporary layers: see script in the scripts folder
* Change symbology for the resulting layer:
   - Input data: The layer that is the input of this new problem can be found in the Input folder
   - The scripts can be found in the scripts folder: `session_2_v1_single_symbol_legend.py` and `session_2_v2_graduated_legend.py`

# Session 3:
## Part 1: Use dictionary to define legend 

Create function with arguments layer, legend (a dictionary) and an attribute (the attribute name on which the legend is based)

* Input data: As before, The layer that is the input for this  problem can be found in the Input folder Scripts in the scripts folder: `session_2_v3_graduated_legend_with dictionary.py`, `session_2_v4_define_function_for_legend_with_dictionary_as_argument.py` and `session_2_v5_load_auxiliary_functions.py` (For keeping auxiliary functions in separate file)

## Part 2: Re-use the auxiliary functions above for a new data set

The data is the NUTS (Nomenclature of territorial units for statistics) map for Europe. The script allows to choose the NUTS level that one wants to draw. All features with the same country name will be represented with the same color in the legend. Colors are random, but the user can choose the range of RGB to create lighter or darker colors.

* Input data: NUTS map from https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts. The shapefile files are available in  the Input folder.
* Scripts in in the scripts folder: `session_3_v1_NUTS_create_dictionary_apply_legend_function.py`
* There is a challenge at the end of the script: define new function that creates the dictionary and the symbology

## Part 3: Re-write the script `session_1_v4_use_temporary_outputs.py`

Simplify the script by creating new functions in `auxiliary_functions.py` and creating new script `session_1_v6_simplify_s1v4_by_calling_functions.py`. 

* The added functions are: `my_clean_project`; `my_add_vector_layer`; `my_processing_run`; `my_remove_layer`
* Exercise suggestion: replace the code below in script `session_3_v1_NUTS_create_dictionary_apply_legend_function.py` by calls to the new functions in `auxiliary_functions.py`: you should be able to do that with 3 or 4 lines of code to replace the whole code below.

```         
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
```

# Session 4: Converting blocks of code into functions; modularity. Exemple with a function to build a dictionary and another function to apply that dictionary to create a graduated symbology for the NUTS data set. Using a matplotlib colormap. Miscelaneous: script to find strings in files (os module and regular expressions: re module). Message boxes in PyQGIS.

* Input data: NUTS data
* Scripts in the scripts folder
   - For the graduated legend for the NUTS units' area: see in scripts folder: `session_4_v1_NUTS_graduated_legend_color_ramp_from_matplotlib_no_dict.py` `session_4_v2_NUTS_graduated_legend_color_ramp_from_matplotlib_with_dict.py`, `session_4_v3_NUTS_graduated_legend_color_ramp_from_matplotlib_with_functions.py`, `auxiliary_functions.py`
   - Other: `search_string_in_files.py` ; `remove_files_message_boxes.py` ; `basic_example_matplotlib.py`

Exercise suggestions:
* (easy) create dictionary for the NUTS data set to define a graduated legend with 4 classes and respective labels that you choose "by hand". Then, call function `create_graduated_legend` (in `auxiliary_functions.py`) to create the legend.
* (more complex) Create a new function, in alternative to `create_graduated_legend_dict`, but with the same arguments `values,colormap,myopacity` that uses Sturges rule to determine the approximate number of classes to consider and define classes of equal amplitude for the legend. The output of this new function should be a dictionary (analogous to the output of `create_graduated_legend_dict`)

# Session 5: Dialog boxes to interact with the user; Read simple tables (csv, txt);  Iterate through features; Create new attributes (aka fields); Compute new attributes; Join by attribute
* Data sets: CAOP map (Portuguese administrative units), Milk production table from INE (Portuguese official statistics institute) , all in the Input folder
* Scripts in the scripts folder: `basic_examples_QInputDialog_and_QMessageBox.py`; `session_5_v1_INE_read_csv_file_join_layers_by_attributes.py`; `revised auxiliary_functions.py`

Exercise suggestion:
* (easy) Create a scritp that reads the NUTS data set and confirms that for all features, the attribute `LEVL_CODE` is the number of characters in the attribute `NUTS_ID` plus 2. Use iterator over `mylayer.getFeatures()` to check that this is true for all features.


# Session 6: Access data sets with WFS protocol; Vector layer geometry; Create a layer from scratch using wkt strings (well known text); Determine geometry of layers; Edit coordinates of vertices and create new layer.

* Documents. Description of geometry of features and wkt strings: singlepart and multipart.
* Data:
   - RNAP (protected areas in Portugal) to access with WFS (but the file is also available in the Input folder)
   - Streams.gpkg to test result of assignment
* Scripts in the scripts folder
```
session_6_read_WFS_from_uri_check_modify_encoding_QInputDialog_Export_as_local_file.py
session_6_1_small_example_create layer with one point feature
session_6_2_RNAP_read_WFS_from_uri_check_modify_encoding_QInputDialog_Export_as_local_file.py
session_6_3_b_RNAP_vector_determine_geometry.py
session_6_3_c_RNAP_vector_layer_geometry_access_vertices_with_accessor_function.py
session_6_4_RNAP_vector_layer_change_vertices_coordinates.py
revised auxiliary_functions.py
```

Exercise suggestion: 
* Adapt the function `round_vertices_coordinates_multipolygon` (which is in the current version of auxiliary_functions.py) and is called from the script `session_6_4_RNAP_vector_layer_change_vertices_coordinates.py` to create a new function, say, `round_vertices_coordinates_multilinestring` which has as input a MultiLineString layer. You can test it using a data set in `inputs` called `Streams.gpkg`.

# Session 7: Regular expressions and file management to search for the location of a given string among all files in a folder; Vector layer geometry to  and fix validity of layers; Geopackage -- create and populate geopackage; Read layers from geopackage; Query Geopackage with SQL

* Data in the Input folder:
   - landUse_invalid_features.gpkg : data set with invalid features
   - Data base CascaisZoning.gpkg
* Scripts
```
my_index_search_strings_in_files_regex.py
session_6_3_a_vector_layer_clone_check_and_fix_features_validity.py
session_7-a_create_geopackage_from_files.py
session_7_b_Cascais_simple_example_of_SQL_query_over_geopackage.py
revised auxiliary_functions.py
```

# Session 8: Doing SQL queries within Python script; Converting SQL query result into a new vector layer; Adding new layer to existing geopackage; Solving a zoning problem over Cascais

* Scripts
```
session_8_a_v1_Cascais_first_examples_SQL_queries_.py
session_8_a_v2_Cascais_first_examples_SQL_queries_with_function.py
session_8_b_Cascais_exaamples_SQL_queries_ST_intersect_ORDER_BY.py
session_8_c_Cascais_example_ST_buffer_create_new_layer_add_layer_to_geopackage.py
revised auxiliary_functions.py
 ```
 
* Documents in 'Figures and other course documentation': Spatial Analysis Problem Cascais; Cascais Zoning Diagram Soil Productivity : diagram describing SQL query; Cascais Zoning Diagram Road Buffer: diagram describing SQL query

Assignement: the Cascais Zoning Problem. The problem is described in this document. The goal is to solve the Zoning problem for Cascais using the information in the CascaisZoning.gpkg geopackage available in the 'input' folder.

Suggestions:
1. Look at the script `session_1_v6_simplify_s1v4_by_calling_functions.py` to see how you can use the functions that are already defined to run tools of processing toolbox and make your code short and clear;
2. First run the function you need in the QGIS interface from Processing toolbox, and then look at "History" and copy the script that is there and adapt it to look something like this -- the functions you need are in `auxiliary_functions.py`:
```
dict_params={'OVERLAY':'my overlay layer name'}
mylayer=my_processing_run("native:clip",'my input layer name',dict_params,'my output layer name')
```
3. You can remove layers you don't need anymore with `my_remove_layer('name of the layer to be removed')`

4. You should be able to solve the whole problem just with operations from the Processing toolbox, but you can use other options if you want
5. Since the data are all in a geopackage, to open simple tables you don't need to go through the more complicated details needed to open a csv or txt file: you just load the layer from the geopackage as discussed in the script `session_7_a_create_geopackage_from_files.py`

# Session 9: A resolution for the Cascais Zoning problem just using operations from the processing Toolbox; New script replacing some operations by one SQL query; Raster data: (1) Read and render multiband rasters with a script; Export raster; (2) Operate on bands with raster calculator and create a legend; (3) Convert data into a numpy array and analize; (4) Identify no-data values.

* Data:
    - Multiband raster `Cropped_S2A-T29SNB-B2348-2021-8-22.tif` a Sentinel 2 surface reflectance stack of bands 2, 3, 4 and 8, over tile T29SNB (Algarve)
    - `ndvi.tif`: a single band raster derived from the data set above
* Scripts
```
Scripts for the Cascais Zoning problem
session_9_a_read_and_render_multiband_raster.py
session_9_b_raster_calculator_write_rlayer_to_tif_create_legend.py
session_9_c_create_raster_nodatavalue_histogram_matplotlib.py
revised auxiliary_functions.py
```
* Documents in the 'Figures and other course documentation' folder:
    - Overview of procedures to read/write vector data and raster data with PyQGIS scripts
    - Overview of PyQGIS objects for legends of vector and raster datasets.


# Session 10: Extract raster pixel values as a numpy array with gdal; Replace raster nodata value by numpy.nan (not a number);  Use MatPlotLib to build an histogram of raster values;  Manipulate numpy array using numpy and other packages (e.g. sklearn, a package for machine learning);  Convert array back to raster layer and tif file with gdal;  Access on-line data (download and unzip files, access with XYZ, WMS and WFS protocols) using a Python script in QGIS.

* Data:
    - Multiband raster `Cropped_S2A-T29SNB-B2348-2021-8-22.tif` a Sentinel 2 surface reflectance stack of bands 2, 3, 4 and 8, over tile T29SNB (Algarve)
    - `ndvi.tif`: a single band raster derived from the data set above
* Scripts
```
        session_9_c_create_raster_nodatavalue_histogram_matplotlib.py
        session_10_a_read_multiband_convert_to_array.py
        session_10_b_v1_read_multiband_convert_to_array_k_means_export_as_raster.py
        session_10_b_v2_read_multiband_convert_to_array_k_means_export_as_raster_with functions.py
        session_10_c_read_multiband_convert_to_array_add_ndvi_k_means_export_as_raster.py
        session_10_d_read_datasets_wms_wfs_unzip.py
        revised auxiliary_functions.py
```
