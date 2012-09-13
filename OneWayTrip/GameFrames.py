import pygame
from OneWayTrip.Pathfinder import PathFinder
from OneWayTrip.TileSet import *

__author__ = 'elleryaree'

class BasicFrame:
    def __init__(self, size):
        self.font = pygame.font.Font(None, 36)
        self.text = "Basic frame"
        self.surface = pygame.Surface(size)

    def update(self):
        text = self.font.render(self.text, 1, (250, 250, 250))
        text_pos = text.get_rect(centerx=self.surface.get_width()/2, centery = self.surface.get_height()/2)

        self.surface.blit(text, text_pos)

    def checkMousePress(self, pointer):
        pass

class WorldFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "World frame"

        self.hero_position = [0, 1, "L", 1]

        street_1_sprites = pygame.sprite.RenderPlain()

        street1 = [["W", "S", "S", "S", "W", "W", "S", "S", "S", "W"],
                   ["S", "S", "W", "S", "W", "W", "W", "W", "W", "W"],
                   ["W", "S", "W", "S", "W", "W", "S", "S", "S", "W"],
                   ["W", "S", "S", "S", "S", "S", "S", "W", "W", "W"],
                    ["S", "S", "W", "S", "S", "W", "S", "S", "W", "W"],
                    ["W", "S", "W", "S", "S", "W", "S", "S", "S", "W"],
                    ["W", "S", "S", "S", "W", "W", "S", "S", "S", "W"]]

        dark_tile_set = DarkWorldTileSet()
        for i in range(len(street1)):
            for j in range(len(street1[i])):
                tile_image = dark_tile_set.get_tile(street1, i, j)
                tile = Tile(tile_image, (j, i), street1[i][j])
                street_1_sprites.add(tile)

        hero_tile_set = HeroTileSet()
        hero_image, self.hero_position = hero_tile_set.get_sprite(self.hero_position)
        hero_sprite = HeroTile(hero_image, (self.hero_position[0], self.hero_position[1]), hero_tile_set)

        self.locations = [street_1_sprites]
        self.location_grids = [street1]
        self.hero_sprite = pygame.sprite.GroupSingle(hero_sprite)

        self.current_street = 0
        self.tick = 0

    def update(self):
        self.tick += 1

        sprites = self.locations[self.current_street]

        sprites.update()
        if self.tick >= 10:
            self.hero_sprite.update()
            self.tick = 0

        sprites.draw(self.surface)
        self.hero_sprite.draw(self.surface)

    def checkMousePress(self, pointer):
        sprites = self.locations[self.current_street]
        for clicked_menu in pygame.sprite.spritecollide(pointer, sprites, 0):
            if clicked_menu.key == "S":
                print clicked_menu.position
                self.hero_sprite.sprites()[0].route = self.__find_route(clicked_menu.position)



    def __find_route(self, goal):
        finder = PathFinder(self.location_grids[self.current_street], self.hero_sprite.sprites()[0].position, goal)
        return finder.find()[1]

class MapFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "Map frame"

class TreeFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "Tree frame"