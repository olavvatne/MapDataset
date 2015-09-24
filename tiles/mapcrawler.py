import requests
from PIL import Image
from io import BytesIO
import math
import time


class MapCrawler(object):

    def __init__(self, area,step, resolution=256, index=(0,0,0)):
        print("Step: ", step)
        self.x_tiles = math.floor(abs(area[0] - area[2]) /step)
        self.y_tiles = math.floor(abs(area[1] - area[3]) /step)
        self.area = area
        self.step = step
        self.res = resolution
        self.index = index;


    def set_url(self, url, params):
        self.base = url
        self.params = params

    def set_dir(self, output_directory):
        self.output = output_directory

    def start(self):
        if not self.base or not self.output:
            raise Exception('Set url and output directory')
        index, si ,sj = self.index
        start_x = self.area[0]
        start_y = self.area[1]
        print(start_x)
        print(start_y)
        params = self.params
        #BBOX Defined from bottom left to top right
        for i in range(si, self.y_tiles):
            for j in range(sj,self.x_tiles):
                bbox = [
                    str(start_x + (self.step * i)),
                    str(start_y + (self.step * j)),
                    str(start_x + (self.step * (i+1))),
                    str(start_y + (self.step * (j +1)))
                ]
                params['BBOX'] = ','.join(bbox)
                print(params['BBOX'])
                print("i: ", i , " j: ", j)
                self._request_and_store(self.params, index)
                index = index +1
                time.sleep(0.5)



    def _request_and_store(self, params, index):
        payload_str = "&".join("%s=%s" % (k,v) for k,v in params.items())
        r = requests.get(self.base, params = payload_str)
        print(r.url)

        #ENSURE image content
        try:
            i = Image.open(BytesIO(r.content))
            output_name = 'I' + str(index) + '-' + str(params['BBOX'])
            i.save(self.output + '/' +output_name + '.jpg')
            i.close()
        except OSError:
            print("IDX: ", index)
            print(r.content)

