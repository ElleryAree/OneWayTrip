import pygame
from OneWayTrip.Utils import load_tile_table, load_image
from random import Random

__author__ = 'elleryaree'

class BasicTileSet(object):
    def _getKeyAndSurroundings(self, set, i, j):
        if (i - 1) < 0:
            key_up = "W"
        else:
            key_up = set[i - 1][j]

        if i + 1 > len(set) - 1:
            key_down = "W"
        else:
            key_down = set[i + 1][j]

        if j - 1 < len(set[i]):
            key_left = "W"
        else:
            key_left = set[i][j - 1]

        if j + 1 > len(set[i]) - 1:
            key_right = "W"
        else:
            key_right = set[i][j + 1]

        return key_up, key_down, key_left, key_right

    def _floor(self, key):
        return key in ["S", "I", "C"]

class DarkWorldTileSet(BasicTileSet):
    def __init__(self):
        self.tile_width = 32
        self.tile_height = 32
        self.tiles = load_tile_table("scr4scifi.jpeg", self.tile_width, self.tile_height)

    def get_tile(self, i, j):
        return self.tiles[j][i]

class LightWorldTileSet(BasicTileSet):
    def __init__(self):
        self.tile_width = 32
        self.tile_height = 32
        self.tiles = load_tile_table("scr3scifi.jpeg", self.tile_width, self.tile_height)

    def get_tile(self, i, j):
        return self.tiles[j][i]

class GreenWorldTileSet(BasicTileSet):
    def __init__(self):
        self.tile_width = 32
        self.tile_height = 32
        self.tiles = load_tile_table("scr2scifi.jpeg", self.tile_width, self.tile_height)

    def get_tile(self, i, j):
        return self.tiles[j][i]

class RandomTileSet(BasicTileSet):
    def __init__(self):
        self.tile_width = 32
        self.tile_height = 32
        self.tiles = load_tile_table("AbyssTileA5.png", self.tile_width, self.tile_height)

    def get_tile(self):
        random = Random()

        return self.tiles[int(random.random() * len(self.tiles))][int(random.random() * len(self.tiles[0]))]

class ItemsTileSet(BasicTileSet):
    def get_tile(self, item):
        return load_image(item.name, -1)[0]

class CharacterTileSet(object):
    def __init__(self, name):
        self.tile_width = 32
        self.tile_height = 32
        self.tiles = load_tile_table(name, 32, 32)

    def get_sprite(self, hero_position):
        if hero_position[2] == "L":
            y = 1
        elif hero_position[2] == "R":
            y = 2
        elif hero_position[2] == "U":
            y = 3
        else:
            y = 0

        x = hero_position[3]
        if x >= 2:
            x = 0

        tile = self.tiles[x][y]

        hero_position[3] += 1
        if hero_position[3] >= 3:
            hero_position[3] = 0

        return tile, hero_position

class HeroTileSet(CharacterTileSet):
    def __init__(self):
        super(HeroTileSet, self).__init__("fan.png")

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position, additional, key = None):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = image
        self.position = position
        self.rect = image.get_rect()
        self.rect.topleft = (position[0] * 32 + additional[0], position[1] * 32 + additional[1])
        self.key = key
        self.additional = additional

class ExplodeTileSet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.tile_width = 24
        self.tile_height = 24
        self.tiles = load_tile_table("Explode1.bmp", 24, 24)
        self.position = position
        self.__set_image()

    def __set_image(self):
        self.image = self.tiles.pop(0)[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.position[0] - 8
        self.rect.centery = self.position[1]

    def update(self):
        self.__set_image()

class HeroTile(Tile):
    def __init__(self, image, position, additional, tile_set):
        Tile.__init__(self, image, position, additional)
        self.route = []
        self.step = 0
        self.tile_set = tile_set

    def update(self):
        if len(self.route):
            route_part = self.route.pop(0)
            tile, pos = self.tile_set.get_sprite([route_part[0][0], route_part[0][1], route_part[1], self.step])
            self.position = route_part[0]
            self.image = tile
            self.step = pos[3]
        self.rect.topleft = (self.position[0] * 32 + self.additional[0], self.position[1] * 32 + self.additional[1])