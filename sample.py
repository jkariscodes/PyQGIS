"""
/**********************************************************************************
Description         Generate Map from Layers (csv and shapefile)
Date                   7/May/2018
references          Python QGIS Cookbook
***********************************************************************************/
"""

# defining paths to root and working directories
root_dir = "/home/youruser/dev/pyqgis/"
data_dir="/home/youruser/dev/pyqgis/data/"

# importing required libraries
import sys
from qgis.core import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(root_dir)

# required for map objects (legend, scale etc) rendering
import MapComposer

# defining location path for csv file
uri =  data_dir + "points.csv?crs=epsg:4326&type=csv&xField=X&yField=Y"
layer = QgsVectorLayer(uri, 'points', "delimitedtext")

# loading shapefile
layer2 = QgsVectorLayer('/home/youruser/dev/pyqgis/data/Rwanda.shp','Rwanda','ogr')

# validating if layer exists
if not layer.isValid():
    print "Layer %s did not load" % layer.name()


#adding layer1 to the Registry
myRegistry = QgsMapLayerRegistry.instance()
myRegistry.addMapLayer(layer2)
myRegistry.addMapLayer(layer)

# labelling the points layer to display NN field values
layer_label = iface.activeLayer()
layer_label = QgsPalLayerSettings()
layer_label.readFromLayer(layer)
layer_label.drawLabels = True
layer_label.enabled = True
layer_label.fieldName = 'NN'
layer_label.writeToLayer(layer)
iface.mapCanvas().refresh()
iface.mapCanvas().resize(QSize(1920,1080))

# accessing the map renderer
mapRend = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRend)
c.setPlotStyle(QgsComposition.Print)

# create a map composer object
qcomp = MapComposer.MapComposer(qmlr=myRegistry, qmr=mapRend)

### LEGEND ###

# The layers in the map cap canvas goes to the legend of the map
qcomp.legend = QgsComposerLegend(qcomp.c)
qcomp.legend.model().setLayerSet(qcomp.qmr.layerSet())

# defining the position of the legend and adding it to the c(composition) object defined in the MapComposer class
qcomp.legend.setItemPosition(5, qcomp.y)
qcomp.c.addItem(qcomp.legend)

### MAP ###

x, y = 0, 0
w, h = c.paperWidth(), c.paperHeight()
# define map
composerMap = QgsComposerMap(c, x, y, w,h)
c.addItem(composerMap)

# map dimensions
mcw = qcomp.composerMap.rect().width()
mch = qcomp.composerMap.rect().height()
ax = qcomp.x + mcw + 20
ay = (qcomp.y + mch) + 10
afy = ay - 30

### NORTH ARROW ###

# Defining the position of the North Arrow
qcomp.arrow = QgsComposerArrow(QPointF(ax, ay), QPointF(ax,afy),
qcomp.c)

#adding the north arrow to the c (composition) object
qcomp.c.addItem(qcomp.arrow)

#Defining how the properties of the label for the North arrow
f = QFont()
f.setBold(True)
f.setFamily("Times New Roman")
f.setPointSize(30)
qcomp.labelNorth = QgsComposerLabel(qcomp.c)
qcomp.labelNorth.setText("N")
qcomp.labelNorth.setFont(f)
qcomp.labelNorth.adjustSizeToText()
qcomp.labelNorth.setFrameEnabled(False)
qcomp.labelNorth.setItemPosition(ax - 5, ay)

# Adding the label to the composition object
qcomp.c.addItem(qcomp.labelNorth)


### LABEL ###

# create a label object, setting the label text and size
qcomp.label = QgsComposerLabel(qcomp.c)
qcomp.label.setText("ASSIGNMENT")
qcomp.label.adjustSizeToText()

# add frame around label
qcomp.label.setFrameEnabled(True)

# add label to map composition
qcomp.c.addItem(qcomp.label)

### SCALEBAR ### 

#defining the properties of the scale bar and adding it to the composition object
qcomp.scalebar = QgsComposerScaleBar(qcomp.c)
qcomp.scalebar.setStyle('Double Box')
qcomp.scalebar.setComposerMap(qcomp.composerMap)
qcomp.scalebar.applyDefaultSize()
sbw = qcomp.scalebar.rect().width()
sbh = qcomp.scalebar.rect().height()
mcw = qcomp.composerMap.rect().width()
mch = qcomp.composerMap.rect().height()
sbx = qcomp.x + (mcw - sbw)
sby = qcomp.y + mch
qcomp.scalebar.setItemPosition(sbx, sby)
qcomp.c.addItem(qcomp.scalebar)

### MAP LABEL ###

#defining the properties of the map label and adding it to the composition object
qcomp.label = QgsComposerLabel(qcomp.c)
qcomp.label.setText("Rwanda NN")
qcomp.label.adjustSizeToText()
qcomp.label.setFrameEnabled(False)
qcomp.label.setItemPosition(qcomp.x,qcomp.y-10)
qcomp.c.addItem(qcomp.label)

# saving the map as JPEG
qcomp.output("/home/youruser/dev/pyqgis/myMap.jpg", "jpg")
# End Of Script
