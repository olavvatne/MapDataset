import requests
from PIL import Image
from io import BytesIO
import math

#TODO: Make a map tile requester. That request tiles for a certain area and store them in a folder.
#TODO: index and bbox in filename
#TODO: Make a txt file containing all indexes and bbox with a bit better formatting.
#TODO: Store area bbox
#SETTINGS
output_dir = './'
step = 169.25
bbox = [-32842.75,6574426.25,-31996.5,6574087.75]
resolution = 256

url = 'http://gatekeeper3.geonorge.no/BaatGatekeeper/gk/gk.nibcache'
url_params = {
    'SERVICE': 'WMS',
    'VERSION': '1.1.1',
    'BGCOLOR': '0x000000',
    'FORMAT': 'image%2Fjpeg',
    'TRANSPARENT': '0',
    'LAYERS':'NiB',
    'gkt':'F866B061CA4062C1C55200B373F436B80FC759A18E1D6DF38DF829231A08590AA9678AB96D6E1FC113B57E5BAA3F284CBC8633929A70B5118D018F0853CD0DA1',
    'REQUEST':'GetMap',
    'SRS':'EPSG%3A32632',
    'BBOX':'-32504.25,6574426.25,-31996.5,6574087.75',
    'WIDTH':'256',
    'HEIGHT':'256'
}


class MapCrawler(object):

    def __init__(self, area, step, resolution=256):
        self.x_tiles = math.floor(abs(area[0] - area[2]) /step)
        self.y_tiles = math.floor(abs(area[1] - area[3]) /step)
        self.area = area
        self.step = step
        self.res = resolution


    def set_url(self, url, params):
        self.base = url
        self.params = params

    def set_dir(self, output_directory):
        self.output = output_directory

    def start(self):
        if not self.base or not self.output:
            raise Exception('Set url and output directory')
        index = 0
        start_x = self.area[0]
        start_y = self.area[1]
        print(start_x)
        print(start_y)
        params = self.params

        for i in range(self.y_tiles):
            for j in range(self.x_tiles):
                bbox = [
                    str(start_x + (self.step * i)),
                    str(start_y + (self.step * j)),
                    str(start_x + (self.step * (i+1))),
                    str(start_y + (self.step * (j +1)))
                ]
                params['BBOX'] = ','.join(bbox)
                print(params['BBOX'])
                self._request_and_store(self.params, index)
                index = index +1



    def _request_and_store(self, params, index):
        #TODO: Try catch
        payload_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
        cookies = {'_ga': 'GA1.2.285433025.1442827876'}
        r = requests.get(self.base, params = payload_str, cookies=cookies)
        print(r.url)
        #ENSURE image content
        i = Image.open(BytesIO(r.content))
        i.save(self.output + '/img ' + str(index) + '.jpg')
        print("saved")
        i.close()


crawler = MapCrawler(bbox, step)
crawler.set_dir(output_dir)
crawler.set_url(url, url_params)
crawler.start()

