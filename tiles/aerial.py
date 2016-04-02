from tiles.mapcrawler import MapCrawler

'''
Contains a lot of configurable variables for the map crawler.

Retrieves all image tiles inside bbox from url.
The wms service often needs url parameters which can be added under url_params.
'''
#SETTINGS
output_dir = '../result/Eidsfjord'
step = 169.25 #Also actual meters in image.
index = (0, 0, 0) #Index, tilex, tiley. If program stops working during run.
#Left east coordinate,  down north coordinate, right east coodinate,  up north coordinate
bbox = [
  63460.5,6723535.5,68199.5,6730474.75
]
#BBOX = Lower left corner, upper right corner
resolution = 256
url = 'http://gatekeeper1.geonorge.no/BaatGatekeeper/gk/gk.nibcache'
url_params = {
    'SERVICE': 'WMS',
    'VERSION': '1.1.1',
    'FORMAT': 'image%2Fjpeg',
    'LAYERS':'NiB',
    'gkt':'27B7618EDE6C7DE7FD53B98313E7BDBC06B6D3E687CEBDFD8DF829231A08590AA9678AB96D6E1FC113B57E5BAA3F284CBC8633929A70B5118D018F0853CD0DA1',
    'REQUEST':'GetMap',
    'SRS':'EPSG%3A32633',
    'STYLES': '',
    'WIDTH':'256',
    'HEIGHT':'256'
}


crawler = MapCrawler(bbox, step, index=index)
crawler.set_dir(output_dir)
crawler.set_url(url, url_params)
crawler.start()

