'''
Splice the 64x64 tiles to bigger images.
Beneficial for rotation etc.
'''

import os, sys
import numpy as np
import random
from PIL import Image
import _pickle as pickle
import gzip

imagedir_dir = '../tiles/Oslo1'
class TileCombiner:
    ARRAY_FORMAT = 'float32'

    def __init__(self, images):
        self.images_dir = images

    def create(self):
        print('Transforming dataset and vector into suitable dataset representation might take a few minutes depending'
              'on the number of tiles')
        image_files = self.get_image_files(self.images_dir)



        for i in range(len(image_files)):
            print(image_files)
            if i % 200 == 0:
                print("Tile: ", i, '/', len(image_files))

        return None

    def get_image_files(self, path):
        included_extenstions = ['jpg','png'];
        return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

t = TileCombiner(imagedir_dir)
t.create()