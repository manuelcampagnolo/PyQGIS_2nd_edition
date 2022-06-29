import os
from PyQt5.QtWidgets import QInputDialog # dialog boxes

# my working folder
myfolder=r'C:/Users/mlc/Documents/PyQGIS' # CHANGE
# source auxiliary functions (instead of importing module)
exec(open(os.path.join(myfolder,'scripts','auxiliary_functions.py').encode('utf-8')).read())

# my remaining constants
# e.g. SNIG / Registo Nacional de Dados Geográficos
# examples:
# uri='http://si.icnf.pt/wfs/ardida_2016?service=wfs&version=2.0.0&request=GetCapabilities' # Área ardida_2016
uri=r'http://si.icnf.pt/wfs/rnap?service=wfs&version=2.0.0&request=GetCapabilities' # RNAP
ln='RNAP' # layer name
an='nome_ap' # one attribute name

#clear layer tree and canvas and creates instance of project
myproject,mycanvas = my_clean_project()

# access data with WFS (feature service)
mylayer=iface.addVectorLayer(uri,'','ogr')
mylayer.setName(ln)

# test if characters in RNAP are being read correctly
N=8
count=0
feats=mylayer.getFeatures()
for feat in feats:
    print(feat[an])
    count+=1
    if (count>N): break

# Select encoding:
myoptions=['utf-8','ISO-8859-1', 'latin1','System']
myoption, ok = QInputDialog.getItem(parent, "Select (hint: utf-8)", "Options", myoptions, 0, False)
    
# Set the encoding of loaded layers to UTF-8:
# Methods setEncoding() Set encoding used for accessing data from layer. 
# An empty encoding string indicates that the provider should automatically select the most appropriate encoding for the data source.
# in alternative, one can use e.g.  mylayer.setProviderEncoding('utf-8')
mylayer.dataProvider().setEncoding(myoption)
print('My encoding option: {}'.format(myoption))

# now, are the characters correctly read?
count=0
feats=mylayer.getFeatures()
for feat in feats:
    print(feat[an])
    count+=1
    if (count>N): break


# Ask Yes/No question
res=QMessageBox.question(parent,'Question', 'Do you want to export data set locally?' )

if res==QMessageBox.Yes:
    # information box
    QMessageBox.information(parent,'Info','The file will be stored in the "temp" subfolder')
    # question box
    text, ok = QInputDialog.getText(parent,'input dialog', 'Type filename.gpkg')
    if ok:
        fn_output=os.path.join(myfolder,'temp',text)
        # export mylayer as a geopackage file
        QgsVectorFileWriter.writeAsVectorFormat(mylayer,fn_output, "utf-8", mylayer.crs(), "GPKG")




