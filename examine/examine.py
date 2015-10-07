__author__ = 'Olav'

import os, sys
from PIL import Image
import msvcrt as m

tiles_dir ='../tiles/dataset/'
vector_dir ='../vector/dataset/'

def get_image_files(path):
    included_extenstions = ['jpg','png'];
    return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

def white_to_transparent(img):
    pixdata = img.load()
    print(pixdata)
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

images = get_image_files(tiles_dir)
label = get_image_files(vector_dir)

for i in range(len(images)):
    background = Image.open(tiles_dir + images[i])
    overlay = Image.open(vector_dir + label[i])

    print(images[i])

    print(label[i])
    background.show()
    overlay.show()
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    white_to_transparent(overlay)
    background.paste(overlay, (0, 0), overlay)
    background.show()
    input('Proceed?')
