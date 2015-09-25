from tiles.mapcrawler import MapCrawler

'''
Contains a lot of configurable variables for the map crawler.

Retrieves all image tiles inside bbox from url.
The wms service often needs url parameters which can be added under url_params.
'''
#SETTINGS
output_dir = './Oslo2'
step = 169.25
index = (0, 0, 0) #Index, tilex, tiley. If program stops working during run.
bbox = [592571.5,6641787.75,599341.5,6649065.5]
resolution = 256
url = 'http://gatekeeper3.geonorge.no/BaatGatekeeper/gk/gk.nibcache'
url_params = {
    'SERVICE': 'WMS',
    'VERSION': '1.1.1',
    'FORMAT': 'image%2Fjpeg',
    'LAYERS':'NiB',
    'GKT':'CE0BB18FE2615C06F0BD9CA5F9AB693A9A617FE62EE601FD590533E5B4303485E1CB71120F36F9FE324EDA7FBA0D09268312C1D8C5FB020EAB579AAE6F8C5E79',
    'REQUEST':'GetMap',
    'SRS':'EPSG%3A32632',
    'STYLES': '',
    'WIDTH':'256',
    'HEIGHT':'256'
}


crawler = MapCrawler(bbox, step, index=index)
crawler.set_dir(output_dir)
crawler.set_url(url, url_params)
crawler.start()

