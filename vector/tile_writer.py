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

The goals of the tile_writer is to create label result for the image result.
For example road vectors shown as black lines in the images etc.

'''
from random import shuffle
dir = os.listdir('C:/Users/olav/git/MapDataset/result/dataset/tiles')
output_dir = 'C:/Users/olav/git/MapDataset/result/dataset/vector/'
elements = len(dir)

mapRenderer = iface.mapCanvas().mapRenderer()
QDir().mkpath(output_dir)

def delay( millisecondsToWait ):
    dieTime = QTime().currentTime().addMSecs( millisecondsToWait )
    while ( QTime.currentTime() < dieTime ):
        QCoreApplication.processEvents( QEventLoop().AllEvents, 100 )
        
def get_name(file):
    EXTENSION = -4
    idx = file.index('-')
    name = file[idx+1:EXTENSION]
    return name

def get_bbox(name):
    bbox =[float(x) for x in name.split(',')]
    return bbox

def render(bbox, output_dir):
    lat_min, lon_min, lat_max, lon_max = bbox
    print(lat_min, lon_min, lat_max, lon_max)
    width = 1536
    height = 1536
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
                
    settings = QgsMapSettings()
    settings.setCrsTransformEnabled(True)
    settings.setOutputDpi(109.0)
    settings.setOutputImageFormat(QImage.Format_ARGB32_Premultiplied)
    settings.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:32633'))
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
    
    