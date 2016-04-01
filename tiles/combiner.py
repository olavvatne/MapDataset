'''
Splice the 64x64 tiles to bigger images.
Beneficial for rotation etc.
Hacky implementation but so what!
'''

import os, sys
import numpy as np
from PIL import Image
import math
imagedir_dir = '../result/Randaberg/'
imagesave_dir = '../result/dataset/tiles'

class TileCombiner:
    ARRAY_FORMAT = 'float32'

    def __init__(self, images, save):
        self.images_dir = images
        self.output_dir = save


    def create(self):
        print('Transforming dataset and vector into suitable dataset representation might take a few minutes depending'
              'on the number of tiles')
        image_files = self.get_image_files(self.images_dir)


        stuff = {}
        for i in range(len(image_files)):
            coords = self._file_to_coords(image_files[i])

            if coords[0] not in stuff:
                stuff[coords[0]] = [];
            stuff[coords[0]].append((coords[1],image_files[i]))
            if i % 200 == 0:
                print("Tile: ", i, '/', len(image_files))

        l = list(stuff.items())
        l.sort(key=lambda k: k[0])
        matrix = [i[1] for i in l]

        #Puts all tile in a matrix in correct order
        longest_row = 0
        images = []
        for m in matrix:
            m.sort(key=lambda k: k[0])
            row = []
            for j in range(len(m)):
                a = m[j]
                #print(a[1])
                name = self.images_dir + a[1]
                image = Image.open(name, 'r')
                data = np.asarray(image)
                row.append((name, data))
            images.append(row)
            if longest_row < len(row):
                longest_row = len(row)

        img_dim = 6 #With res of 256 result in 256 *6 dim img
        h = math.floor(len(images)/img_dim)
        w = math.floor(longest_row/img_dim)

        for i in range(h):
            for j in range(w):
                sub = images[i*6:(i*6)+6]
                sub = [arr[j*6:(j*6)+6] for arr in sub]
                self._create_image(sub)

        return None

    def _file_to_coords(self, file):
        #Index seperated by a '-'
        idx = file.index('-')
        temp = file[idx+1:-4]
        coords = [float(x) for x in temp.split(',')]
        return coords

    def _create_image(self, subarr):
        #TODO: Magic numbers
        minx = float('inf')
        maxx = 0
        miny = float('inf')
        maxy = 0

        #Build image array from patches.
        arr = np.zeros((6*256, 6*256, 3), dtype=np.uint8)
        for i in range(len(subarr)):
            row = subarr[i]

            for j in range(len(row)):
                name, data = subarr[i][j]
                coords = self._file_to_coords(name)
                #print(len(row)-j-1, len(row)-j, i, i+1 )
                #Each patch replace certain spot in image.
                arr[(len(row)-j-1)*256:  (len(row)-j)*256,  (i)*256: (i+1)*256, :] = data[:,:, :]
                print(coords)
                if minx > abs(coords[0]):
                    minx = coords[0]
                if maxx < abs(coords[2]):
                    maxx = coords[2]
                if miny > abs(coords[1]):
                    miny = coords[1]
                if maxy < abs(coords[3]):
                    maxy = coords[3]
        #print(minx, maxx, miny, maxy)
        self.save_image([minx,miny, maxx, maxy], arr)

    def get_image_files(self, path):
        included_extenstions = ['jpg','png'];
        return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

    def save_image(self, c, data):
        if(data.shape[0] >1500 and data.shape[1]> 1500):
            image = Image.fromarray(data)
            name = 'I-' + str(c).strip('[]')
            image.save(self.output_dir + '/' +name + '.jpg')
            image.close()


t = TileCombiner(imagedir_dir, imagesave_dir)
t.create()