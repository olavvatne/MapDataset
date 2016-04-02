__author__ = 'Olav'

'''
Simpler version of the creator. The pickle files became very large.
Formatter will instead process all tiles by putting them into a single folder, which can be loaded
and processed by CNN
'''

import os, sys
import random
import shutil


dataset_dir = '../result/dataset/tiles/'
vector_dir = '../result/dataset/vector/'
output_folder ='./Norwegian_roads_dataset'

class DatasetCreator:
    ARRAY_FORMAT = 'float32'

    def __init__(self, images, vector, output):
        self.images_dir = images
        self.vector_dir = vector
        self.output_dir = output

    def create(self):
        print('Transforming dataset and vector into suitable dataset representation might take a few minutes depending'
              'on the number of tiles')

        os.makedirs(self.output_dir)
        os.makedirs(self.output_dir + '/data')
        os.makedirs(self.output_dir + '/labels')
        index = 0
        examples = []

        tile_path = self.images_dir
        vector_path = self.vector_dir
        tiles = self.get_image_files(tile_path)
        vectors = self.get_image_files(vector_path)

        if len(tiles) != len(vectors):
            raise Exception('Tile folder does not contain the same amount of images as vector folder. '
                            'Are you sure the QGIS render process worked?')

        tiles.sort()
        vectors.sort()
        print('==============Processing ======================')

        example_range = [i for i in range(len(tiles))]
        random.shuffle(example_range)
        print(example_range)
        for j in example_range:

            tile_file = self.output_dir + '/data/' + str(index) + '.png'
            vector_file = self.output_dir + '/labels/' + str(index) + '.png'

            #Copies to output directory and split each tile into 64x64 chunks.
            self.create_copy(os.path.join(vector_path, vectors[j]), vector_file )
            self.create_copy(os.path.join(tile_path, tiles[j]), tile_file )

            index = index +1

            if j % 200 == 0:
                print("Tile: ", j, '/', len(tiles))


    def create_copy(self, path, output):
        shutil.copy(path, output)


    def get_image_files(self, path):
        included_extenstions = ['jpg','png'];
        return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

creator = DatasetCreator(dataset_dir, vector_dir, output_folder)
creator.create()
print("Job done")

