import os
import pygame
from pygame.compat import geterror
from pygame.constants import RLEACCEL
from OneWayTrip.bmpfont import BmpFont

__author__ = 'elleryaree'
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, '../data')

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_font(name="font.idx", bmp_name="font.bmp"):
    fullname = os.path.join(data_dir, name)
    fullname_bmp = os.path.join(data_dir, bmp_name)
    font_2 = BmpFont(fullname, fullname_bmp)

    return font_2

def load_tile_table(filename, width, height, colorkey = -1):
    image, image_rect = load_image(filename, colorkey)
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

