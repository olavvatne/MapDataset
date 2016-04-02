__author__ = 'Olav'

import os, sys, random
from PIL import Image

'''
Tool for examining the tiles and vectors. It opens a random tile and label. Superimpose label onto tile, and displays
the resulting image to the user. The user can choose to proceed by clicking enter in console.
'''
tiles_dir ='../result/dataset/tiles/'
vector_dir ='../result/dataset/vector/'

def get_image_files(path):
    included_extenstions = ['jpg','png'];
    return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

def make_transparent(img):
    pixdata = img.load()
    BG = 0
    FG = 255
    for y in range(img.size[1]):
        for x in range(img.size[0]):

            if pixdata[x, y] == (BG, BG, BG, 255):
                pixdata[x, y] = (BG, BG, BG, 0)

            if pixdata[x, y] == (FG, FG, FG, 255):
                pixdata[x, y] = (200, 200, 0, 100)

images = get_image_files(tiles_dir)
label = get_image_files(vector_dir)

for i in range(len(images)):
    rand_idx = random.randint(0, len(images)-1)
    background = Image.open(tiles_dir + images[rand_idx])
    overlay = Image.open(vector_dir + label[rand_idx])

    print(images[rand_idx])

    print(label[rand_idx])
    #background.show()
    #overlay.show()
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    make_transparent(overlay)
    background.paste(overlay, (0, 0), overlay)
    background.show()
    input('Proceed?')
