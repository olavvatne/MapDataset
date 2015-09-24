__author__ = 'olav'

import os
#TODO: Program for QGIS to write vector tiles to disk.
#TODO: Takes a folder as input with files having filename scheme defined in tiles.
#Use bbox extracted from file name and write image vector image to disk as a raster image.
#Use python code

dir = os.listdir('C:/Users/olav/git/MapDataset/tiles/f')
output_dir = 'C:/Users/olav/git/MapDataset/vector'
QDir().mkpath(output_dir)
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
    settings.setFlag(QgsMapSettings.DrawLabeling, True)
    settings.setMapUnits(QGis.Meters)
    settings.setBackgroundColor(QColor(127, 127, 127, 0))
    
    tileRect = QgsRectangle(lat_min, lon_min, lat_max, lon_max)
    settings.setExtent(tileRect)
    
    job = QgsMapRendererSequentialJob(settings)
    job.start()
    job.waitForFinished()
    delay(10)
    image = job.renderedImage()
    print(image)
    print(output_dir)
    QgsVectorLayer
    image.save(output_dir + '/test3.png', "PNG")
    sys.stdout.write("*")
    
for file in dir:
    if not file.endswith('.jpg'):
        continue
    name = get_name(file)
    bbox = get_bbox(name)
    render(bbox, output_dir)
    raise Exception("NO MORE")
    
    