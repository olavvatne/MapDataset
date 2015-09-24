from tiles.mapcrawler import MapCrawler
#TODO: Make a txt file containing all indexes and bbox with a bit better formatting.

#SETTINGS
output_dir = './Trondheim'
step = 169.25
index = (576, 8, 49)
bbox = [565830,7028862.5,577000.5,7036309.5]
resolution = 256
url = 'http://gatekeeper2.geonorge.no/BaatGatekeeper/gk/gk.nibcache'
url_params = {
    'SERVICE': 'WMS',
    'VERSION': '1.1.1',
    'FORMAT': 'image%2Fjpeg',
    'LAYERS':'NiB',
    'GKT':'CE0BB18FE2615C06D3E16AC464ED39172AA4D4279856224D590533E5B4303485E1CB71120F36F9FE324EDA7FBA0D09268312C1D8C5FB020EAB579AAE6F8C5E79',
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

