__author__ = 'olav'

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.utils
from qgis.utils import iface
from qgis.gui import *

import sys

import os
import os.path
import shutil
import math

'''
Reads a folder under tiles, where each file have it's bounding box in the filename.
The bbox is extracted from filename and a tile is rendered from QGIS.

The goals of the tile_writer is to create label data for the image data.
For example road vectors shown as black lines in the images etc.

'''

dir = os.listdir('C:/Users/olav/git/MapDataset/tiles/Oslo2')
output_dir = 'C:/Users/olav/git/MapDataset/vector/Oslo2/'
elements = len(dir)

mapRenderer = iface.mapCanvas().mapRenderer()
QDir().mkpath(output_dir)

def delay( millisecondsToWait ):
    dieTime = QTime().currentTime().addMSecs( millisecondsToWait )
    while ( QTime.currentTime() < dieTime ):
        QCoreApplication.processEvents( QEventLoop().AllEvents, 100 )
        
def get_name(file):
    EXTENSION = -4
    name = file.split('-')[1]
    name = name[:EXTENSION]
    return name

def get_bbox(name):
    bbox =[float(x) for x in name.split(',')]
    return bbox

def render(bbox, output_dir):
    lat_min, lon_min, lat_max, lon_max = bbox
    width = 256
    height = 256
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
                
    settings = QgsMapSettings()
    settings.setCrsTransformEnabled(True)
    settings.setOutputDpi(109.0)
    settings.setOutputImageFormat(QImage.Format_ARGB32_Premultiplied)
    settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:32632'))
    settings.setOutputSize(QSize(width, height))
    settings.setLayers(mapRenderer.layerSet())
    #settings.setFlag(QgsMapSettings.DrawLabeling, True)
    settings.setMapUnits(QGis.Meters)
    #settings.setBackgroundColor(QColor(127, 127, 127, 0))
    
    tileRect = QgsRectangle(lat_min, lon_min, lat_max, lon_max)
    settings.setExtent(tileRect)
    
    job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    delay(10)
    image = job.renderedImage()
    QgsVectorLayer
    image.save(output_dir, "PNG")
    
for idx, file in enumerate(dir):
    if not file.endswith('.jpg'):
        continue
    if idx % 50 == 0:
        print('progress:', str(idx), '/', str(elements))
    name = get_name(file)
    bbox = get_bbox(name)
    render(bbox, output_dir + file[:-4] + '.png')
print('Finished')
    
    