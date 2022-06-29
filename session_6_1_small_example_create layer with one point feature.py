# A-GPS tracker reading at the vertex in Tapada da Ajuda
Lon= -9.186650
Lat= 38.713770

# Create empty layer in memory
mylayer = QgsVectorLayer("Point", "Tapada Vertex", "memory")
# Set a Coordinate Reference System
crs=mylayer.crs()
crs.createFromId(4326) # latlon
mylayer.setCrs(crs)

# Access to provider
pr = mylayer.dataProvider()

# Create a point geometry
mygeometry = QgsGeometry.fromWkt( 'Point( %f %f)' % (Lon,Lat) )

#Create feature and add it to layer
feat=QgsFeature()
feat.setGeometry(mygeometry)
pr.addFeature(feat)

# Set layer extent
mylayer.updateExtents() 

# Add layer to project
myproject = QgsProject.instance()
myproject.addMapLayer(mylayer)