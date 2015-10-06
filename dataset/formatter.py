__author__ = 'Olav'

'''
Simpler version of the creator. The pickle files became very large.
Formatter will instead process all tiles by putting them into a single folder, which can be loaded
and processed by CNN
'''

import os, sys
import random
import shutil
import image_slicer
#python -m pip install image_slicer


dataset_dir = '../tiles/'
vector_dir = '../vector/'
output_folder ='dataset1'

class DatasetCreator:
    ARRAY_FORMAT = 'float32'

    def __init__(self, images, vector, output):
        self.images_dir = images
        self.vector_dir = vector
        self.output_dir = output

    def create(self):
        print('Transforming dataset and vector into suitable dataset representation might take a few minutes depending'
              'on the number of tiles')
        tile_folders = self.get_folders_in_dir(self.images_dir)
        vector_folders = self.get_folders_in_dir(self.vector_dir)
        tile_folders.sort()
        vector_folders.sort()

        #Assume that each tile_folder have a corresponding vector_folder
        if len(tile_folders) is not len(vector_folders):
            raise Exception('Number of tile and vector folders does not match. '
                            'Are you sure you have generated vectors for every tile folder?')

        os.makedirs(self.output_dir)
        os.makedirs(self.output_dir + '/data')
        os.makedirs(self.output_dir + '/label')
        index = 0
        examples = []
        for i in range(len(tile_folders)):
            if(tile_folders[i] != vector_folders[i]):
                print(tile_folders[i], ' does not have a corresponding vector folder. Vector folder:',
                      vector_folders[i])
                raise Exception('Create vector files for ', tile_folders[i])

            tile_path = self.images_dir + tile_folders[i]
            vector_path = self.vector_dir + vector_folders[i]
            tiles = self.get_image_files(tile_path)
            vectors = self.get_image_files(vector_path)

            if len(tiles) != len(vectors):
                raise Exception('Tile folder does not contain the same amount of images as vector folder. '
                                'Are you sure the QGIS render process worked?')

            tiles.sort()
            vectors.sort()
            print('==============Processing ', tile_folders[i], '======================')
            slicing = True

            #TODO: Correct format for CNN. Still not sure if the images should be a 1D matrix of some sort. Who knows
            for j in range(len(tiles)):
                tile_file = self.output_dir + '/data/' + str(index) + '.png'
                vector_file = self.output_dir + '/label/' + str(index) + '.png'

                #Copies to output directory and split each tile into 64x64 chunks.
                self.create_copy(os.path.join(vector_path, vectors[j]), vector_file )
                self.create_copy(os.path.join(tile_path, tiles[j]), tile_file )
                if slicing:
                    self.split(tile_file)
                    self.split(vector_file)

                index = index +1

                if j % 200 == 0:
                    print("Tile: ", j, '/', len(tiles))


    def create_copy(self, path, output):
        shutil.copy(path, output)

    def split(self, path):
        image_slicer.slice(path, 16)
        os.remove(path)

    def get_image_files(self, path):
        included_extenstions = ['jpg','png'];
        return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

    def get_folders_in_dir(self, path):
        folders = []
        for file in os.listdir(path):
            if os.path.isdir(path + file):
                folders.append(file)
        return folders

creator = DatasetCreator(dataset_dir, vector_dir, output_folder)
creator.create()
print("Job done")

