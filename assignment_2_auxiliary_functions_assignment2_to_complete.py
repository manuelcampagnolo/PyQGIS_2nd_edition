# identify non valid features
# input: vector layer
# output: list of id's of features that do not have a valid geometry
def identify_not_valid_features(mylayer):
    feats=mylayer.getFeatures()
    not_valid_ids=[]
    for feat in feats:
        if not feat.geometry().isGeosValid():
            not_valid_ids.append(feat.id())
    return not_valid_ids

# input: vector layer and name of output layer
# output: copy of input vector layer, where non valid features are fixed with method makeValid
def fix_not_valid_features(vlayer,ln):
    # Make deep copy of vlayer called mylayer
    vlayer.selectAll()
    mylayer=my_processing_run("native:saveselectedfeatures",vlayer,{},ln)
    vlayer.removeSelection()
    # Determine not valid features in mylayer
    not_valid_ids=identify_not_valid_features(mylayer)
    # report result to user
    QMessageBox.information(parent,'Info','There are {} not valid features'.format(len(not_valid_ids)))
    # Select invalid features 
    mylayer.select(not_valid_ids)
    # Fix invalid features with makeValid
    with edit(mylayer):
        feats=mylayer.selectedFeatures() # just the selected ones
        for feat in feats:
            ---
    mylayer.removeSelection()
    # Identify non valid features after fix
    not_valid_ids=identify_not_valid_features(mylayer)
    # Report result to user
    QMessageBox.information(parent,'Info','After fix, there are {} not valid features'.format(len(not_valid_ids)))
    mylayer.setName(ln)
    return mylayer, not_valid_ids


# input: DEM, dictionary with val1, val2 and labels, output layer name
# output: vector layer with attribute myattrib, with values given by, e.g.,  mydict = {1: (10, 'up to 10%'), 2: (20, 'between 10 and 20%')}
def create_vector_slope_classes(fn_dem,mydict,myattrib,ln_out):
    val1=mydict[1][0]
    val2=mydict[2][0]
    # read DEM
    rlayer=my_add_raster_layer(fn_dem,'DEM')
    # compute slope in percentage (slope_pc)
    fn_slope=processing.run("grass7:r.slope.aspect", 
    {'elevation':'DEM',
    'format':1,
    'precision':0,
    '-a':True,
    '-e':False,
    '-n':False,
    'slope':'TEMPORARY_OUTPUT'})['slope']
    rlayer=my_add_raster_layer(fn_slope,'slope_pc')
    # reclassify slopes
    # 1, if slopes below val1
    # 2, if slopes between val1 and val2
    exp='("slope_pc@1" < '+str(val1)+')+2*("slope_pc@1" >= '+str(val1)+'AND "slope_pc@1" <'+str(val2)+')'
    dict_params={'EXPRESSION': exp, 'LAYERS':['slope_pc']}
    mylayer=my_processing_run("qgis:rastercalculator",{},dict_params,'slopes_reclass')
    # Polygonize slopes
    dict_params={'BAND':1,'FIELD':'DN','EIGHT_CONNECTEDNESS':True}
    mylayer=my_processing_run("gdal:polygonize",'slopes_reclass',dict_params,'slopes')
    # Select polygons with value 1 or 2
    dict_params={'EXPRESSION': ' "DN" = 1 OR "DN" = 2 '}
    mylayer=my_processing_run("native:extractbyexpression",'slopes',dict_params,ln_out)
    my_remove_layer('DEM')
    my_remove_layer('slopes')
    my_remove_layer('slope_pc')
    my_remove_layer('slopes_reclass')
    # Create new attribute myattrib 
    pr=mylayer.dataProvider()
    if myattrib not in pr.fields().names(): 
        pr.addAttributes([QgsField(myattrib,QVariant.String)])
        mylayer.updateFields()
    # Populate new attribute with the labels in mydict
    with edit(mylayer):
        ---
    return mylayer
