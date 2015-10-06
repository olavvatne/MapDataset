__author__ = 'Olav'

import os, sys
from PIL import Image
import msvcrt as m

dataset ='../dataset/dataset1'

def get_image_files(path):
    included_extenstions = ['jpg','png'];
    return [fn for fn in os.listdir(path) if any([fn.endswith(ext) for ext in included_extenstions])]

images = get_image_files(dataset + '/data')
label = get_image_files(dataset + '/label')

for i in range(len(images)):
    background = Image.open(dataset + '/data/' + images[i])
    overlay = Image.open(dataset + '/label/' + label[i])

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.blend(background, overlay, 0.5)
    new_img.show()
    input('Proceed?')
