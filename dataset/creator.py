__author__ = 'olav'
'''
Creator loads both dataset and vector folder and, run through
all of them. Combines data X with label y into a dataset structure.
The structure will be similar to the way mnist.pkl.gz is structured.

The goal of the creator is to reduce the amount of computation and work that has to
be done by the CNN module.
'''
import os, sys
from PIL import Image


dataset_dir = '../tiles/'
vector_dir = '../vector/'
output_file ='test'

class DatasetCreator:

    def __init__(self, images, vector, testset=0.1, validationset=0.1):
        self.images_dir = images
        self.vector_dir = vector

    def create(self):
        tile_folders = self.get_folders_in_dir(self.images_dir)
        vector_folders = self.get_folders_in_dir(self.vector_dir)
        tile_folders.sort()
        vector_folders.sort()

        #Assume that each tile_folder have a corresponding vector_folder
        if len(tile_folders) is not len(vector_folders):
            raise Exception('Number of tile and vector folders does not match. '
                            'Are you sure you have generated vectors for every tile folder?')

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

            examples = []
            for j in range(len(tiles)):
                label = self.create_image_label(os.path.join(vector_path, vectors[j]))
                image = self.create_image_data(os.path.join(tile_path, tiles[j]))





    def create_image_data(self, path):
        #TODO: Load image, open it, do numpy magic, return
        pass

    def create_image_label(self, path):
        #TODO: Load image
        #TODO: Invert
        #TODO: Correct representation for theano
        #TODO: return
        
        print(path)
        pass

    def get_image_files(self, path):
        included_extenstions = ['jpg','png'];
        return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

    def get_folders_in_dir(self, path):
        folders = []
        for file in os.listdir(path):
            if os.path.isdir(path + file):
                folders.append(file)
        return folders

creator = DatasetCreator(dataset_dir, vector_dir)
creator.create()