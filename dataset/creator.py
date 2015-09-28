__author__ = 'olav'
'''
Creator loads both dataset and vector folder and, run through
all of them. Combines data X with label y into a dataset structure.
The structure will be similar to the way mnist.pkl.gz is structured.

The goal of the creator is to reduce the amount of computation and work that has to
be done by the CNN module.
'''
import os, sys
import numpy as np
import random
from PIL import Image
import _pickle as pickle
import gzip

dataset_dir = '../tiles/'
vector_dir = '../vector/'
output_file ='test'

class DatasetCreator:
    ARRAY_FORMAT = 'float32'

    def __init__(self, images, vector, testset=0.1, validationset=0.1):
        self.images_dir = images
        self.vector_dir = vector

        self.p_test = testset
        self.p_valid = validationset
        self.p_train = 1 - testset - validationset

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

            #TODO: Correct format for CNN. Still not sure if the images should be a 1D matrix of some sort. Who knows
            for j in range(len(tiles)):
                label = self.create_image_label(os.path.join(vector_path, vectors[j]))
                image = self.create_image_data(os.path.join(tile_path, tiles[j]))
                examples.append((image, label))

                if j % 200 == 0:
                    print("Tile: ", j, '/', len(tiles))

        dataset = self._split_dataset(examples)
        return dataset


    def _split_dataset(self, examples):
        random.shuffle(examples) #Shuffle all tiles to avoid similar tiles being lumped together
        nr = len(examples)
        nr_train = int(nr*self.p_train)
        nr_valid = int(nr*self.p_valid)

        train = self._split_label_data(examples[:nr_train])
        valid = self._split_label_data(examples[nr_train:nr_train + nr_valid])
        test = self._split_label_data(examples[nr_train + nr_valid:])
        return (train, valid, test)

    def _split_label_data(self, examples):
        data = [i[0] for i in examples]
        label =[i[1] for i in examples]
        return (data, label)

    def create_image_data(self, path):
        image = Image.open(path, 'r')
        arr =  np.asarray(image, dtype=DatasetCreator.ARRAY_FORMAT) / 255
        arr = np.rollaxis(arr, 2, 0)
        image.close()
        return arr

    def create_image_label(self, path):
        image = Image.open(path, 'r')
        label = np.invert(np.asarray(image))
        label = np.divide(label, 255 , dtype=DatasetCreator.ARRAY_FORMAT)
        image.close()
        return label

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
dataset = creator.create()
print('Final dataset size: ', len(dataset[0][0]) + len(dataset[1][0]) + len(dataset[2][0]))
print('Train set size:', len(dataset[0][0]),' Validation set size:', len(dataset[1][0]), ' Test set size:', len(dataset[2][0]))
print('Will pickle and gzipping dataset. This might take a while!')

f =  open('tiles.pkl ', 'wb')
pickle.dump(dataset, f)
f.close()
