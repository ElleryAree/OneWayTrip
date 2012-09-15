import pygame
from OneWayTrip.Pathfinder import PathFinder
from OneWayTrip.TileSet import *
from OneWayTrip.map.Things import *

__author__ = 'elleryaree'

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

ITEMS = ItemsTileSet()

class BasicFrame(object):
    def __init__(self, size, pointer, big_pointer):
        self.font = pygame.font.Font(None, 36)
        self.text = "Basic frame"
        self.surface = pygame.Surface(size)
        self.pointer = pointer
        self.big_pointer = big_pointer

    def update(self):
        text = self.font.render(self.text, 1, (250, 250, 250))
        text_pos = text.get_rect(centerx=self.surface.get_width() / 2, centery=self.surface.get_height() / 2)

        self.surface.blit(text, text_pos)

    def render_hint(self, hint):
        text = self.font.render(hint, 1, (250, 250, 250))
        text_pos = text.get_rect(centerx=self.surface.get_width() / 2, centery=self.surface.get_height() - 30)
        self.surface.blit(text, text_pos)

    def checkMousePress(self):
        pass

class WorldFrame(BasicFrame):
    def __init__(self, main, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.text = "World frame"
        self.main = main

        self.hero_position = [0, 1, "L", 1]

        street1 = [["W", "S", "S", "S", "W", "W", "S", "S", "S", "W"],
                   ["S", "S", "W", "S", "W", "W", "W", "W", "W", "W"],
                   ["W", "S", "W", "S", "W", "D", "W", "S", "S", "W"],
                   ["W", "S", "S", "S", "S", "S", "S", "W", "W", "W"],
                    ["S", "S", "W", "S", "S", "W", "S", "S", "W", "W"],
                    ["W", "S", "D", "S", "S", "W", "S", "I", "S", "W"],
                    ["W", "S", "S", "S", "W", "W", "S", "S", "S", "W"]]


        street2 =  [["S", "S", "S", "S", "S", "S", "S", "S", "S", "W"],
                    ["W", "S", "W", "W", "W", "W", "W", "W", "S", "W"],
                    ["W", "S", "W", "S", "S", "S", "W", "W", "S", "W"],
                    ["W", "S", "W", "S", "W", "S", "W", "W", "W", "W"],
                    ["W", "S", "W", "S", "W", "S", "S", "S", "S", "W"],
                    ["W", "S", "W", "S", "W", "S", "S", "W", "S", "W"],
                    ["W", "S", "S", "S", "W", "S", "S", "W", "S", "D"]]

        street3 =  [["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "D", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "S", "S", "W", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["W", "S", "S", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "I", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "W", "S", "S", "I"],
        ]

        doors1 = {(5, 2): Door((5, 2), [0, 0, "U", 1], 1, [DOWN], "to second level"),
                  (2, 5): Door((2, 5), [0, 0, "U", 1], 2, [DOWN], "to the streets")}
        doors2 = {(9, 6): Door((9, 6), [5, 3, "D", 1], 0, [LEFT], "back to first level")}
        doors3 = {(4, 4): Door((4, 4), [2, 6, "D", 1], 0, [DOWN], "back in the dark")}

        items1 = {(7, 5): Item("First.png", (7, 5), [UP, DOWN, RIGHT, LEFT], "First item in the game", 10)}
        items3 = {(11, 8): Item("First.png", (11, 8), [UP, DOWN, RIGHT, LEFT], "Second item", 5),
                  (16, 12): Item("First.png", (16, 12), [LEFT], "Last", 30)}

        self.location_grids = [WorldSet(size, street1, DarkWorldTileSet(), doors1, items1),
                               WorldSet(size, street2, DarkWorldTileSet(), doors2),
                               WorldSet(size, street3, LightWorldTileSet(), doors3, items3)]
        self.current_street = 0
        add = (self.location_grids[self.current_street].add_x, self.location_grids[self.current_street].add_y)

        hero_tile_set = HeroTileSet()
        hero_image, self.hero_position = hero_tile_set.get_sprite(self.hero_position)
        hero_sprite = HeroTile(hero_image, (self.hero_position[0], self.hero_position[1]), add, hero_tile_set)


        self.hero_sprite = pygame.sprite.GroupSingle(hero_sprite)
        self.click_sprite = pygame.sprite.GroupSingle()

        self.tick = 0

    def update(self):
        self.surface.fill((0, 0, 0))
        self.tick += 1

        street_ = self.location_grids[self.current_street]
        sprites = street_.tiles()
        items = street_.items_sprites

        sprites.update()
        items.update()

        if len(self.click_sprite.sprites()) and not len(self.click_sprite.sprites()[0].tiles):
            for sprite in self.click_sprite.sprites():
                sprite.kill()
        self.click_sprite.update()

        if self.tick >= 10:
            self.hero_sprite.update()
            self.tick = 0

        sprites.draw(self.surface)
        items.draw(self.surface)

        self.click_sprite.draw(self.surface)
        self.hero_sprite.draw(self.surface)

        desc = None
        for overable in pygame.sprite.spritecollide(self.pointer, street_.mouse_overable, 0):
            if overable.position in street_.doors:
                desc = "Door: %s" % street_.doors[overable.position].description
            if overable.position in street_.items:
                desc = "Item: %s" % street_.items[overable.position].description
            if overable.position in street_.characters:
                desc = "Char: %s" % street_.characters[overable.position].description
        self.render_hint(desc)

    def checkMousePress(self):
        current_set = self.location_grids[self.current_street]
        sprites = current_set.tiles()
        self.click_sprite.add(ExplodeTileSet(pygame.mouse.get_pos()))

        for clicked_menu in pygame.sprite.spritecollide(self.pointer, sprites, 0):
            if clicked_menu.key == "S":
                self.hero_sprite.sprites()[0].route = self.__find_route(clicked_menu.position)
            if clicked_menu.key == "D":
                door = current_set.doors[clicked_menu.position]

                adjacent_places = door.action_positions
                for place in adjacent_places:
                    x = clicked_menu.position[0] + place[0]
                    y = clicked_menu.position[1] + place[1]
                    if (x, y) == self.hero_sprite.sprites()[0].position:
                        self.__change_street(door)
                        break

        for clicked_menu in pygame.sprite.spritecollide(self.pointer, current_set.items_sprites, 0):
            if clicked_menu.key in ["I", "C"]:
                if clicked_menu.key == "I":
                    thing = current_set.items[clicked_menu.position]
                elif clicked_menu.key == "C":
                    thing = current_set.characters[clicked_menu.position]
                else:
                    continue

                adjacent_places = thing.action_positions
                for place in adjacent_places:
                    x = clicked_menu.position[0] + place[0]
                    y = clicked_menu.position[1] + place[1]
                    if (x, y) == self.hero_sprite.sprites()[0].position:
                        if clicked_menu.key == "I":
                            self.__take_item(clicked_menu, thing, current_set)
                        if clicked_menu.key == "C":
                            pass
                        break

    def __find_route(self, goal):
        finder = PathFinder(self.location_grids[self.current_street].map, self.hero_sprite.sprites()[0].position, goal)
        return finder.find()[1]

    def __change_street(self, door):
        self.current_street = door.map_index
        current_set = self.location_grids[self.current_street]
        self.hero_sprite.sprites()[0].position = door.hero_position
        self.hero_sprite.sprites()[0].additional = (current_set.add_x, current_set.add_y)

    def __take_item(self, item, item_info, current_set):
        item.kill()
        current_set.map[item.position[1]][item.position[0]] = "S"

        self.main.add_item(item_info)

class MapFrame(BasicFrame):
    def __init__(self, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.text = "Map frame"

class TreeFrame(BasicFrame):
    def __init__(self, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.text = "Tree frame"

class TimeUpFrame(BasicFrame):
    def __init__(self, main, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.main = main

    def update(self):
        self.text_1 = "Time is out."
        self.text_2 = "You collected %s items and got a score of %s." % (len(self.main.inventory), self.main.score)
        self.text_3 = "Nice of you..."
        self.text_4 = "Press any key to leave..."

        text_r_1 = self.font.render(self.text_1, 1, (250, 250, 250))
        text_pos_r_1 = text_r_1.get_rect(centerx=self.surface.get_width() / 2, centery=self.surface.get_height() / 2)
        text_r_2 = self.font.render(self.text_2, 1, (250, 250, 250))
        text_pos_r_2 = text_r_2.get_rect(centerx=self.surface.get_width() / 2, centery=(self.surface.get_height() / 2) + 30)
        text_r_3 = self.font.render(self.text_3, 1, (250, 250, 250))
        text_pos_r_3 = text_r_3.get_rect(centerx=self.surface.get_width() / 2, centery=(self.surface.get_height() / 2) + 60)
        text_r_4 = self.font.render(self.text_4, 1, (250, 250, 250))
        text_pos_r_4 = text_r_4.get_rect(centerx=self.surface.get_width() / 2, centery=self.surface.get_height() - 30)

        self.surface.blit(text_r_1, text_pos_r_1)
        self.surface.blit(text_r_2, text_pos_r_2)
        self.surface.blit(text_r_3, text_pos_r_3)
        self.surface.blit(text_r_4, text_pos_r_4)


class WorldSet(object):
    def __init__(self, size, map, tile_set, doors, items = None, characters = None):
        self.map = map
        self.__tiles = None
        self.__tile_set = tile_set
        self.doors = doors
        self.add_x = (size[0] / (2 * 32) - (len(self.map) / 2)) * 32
        self.add_y = (size[1] / (2 * 32) - (len(self.map[0]) / 2)) * 32

        self.mouse_overable = pygame.sprite.RenderPlain()
        self.items_sprites = pygame.sprite.RenderPlain()
        self.characters_sprites = pygame.sprite.RenderPlain()

        self.items = []
        if items:
            self.items = items
        self.characters = []
        if characters:
            self.characters = characters

    def tiles(self):
        if self.__tiles:
            return self.__tiles

        self.__tiles = pygame.sprite.RenderPlain()
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                tile_image = self.__tile_set.get_tile(i, j, self.map)
                tile = Tile(tile_image, (j, i), (self.add_x, self.add_y), self.map[i][j])
                self.__tiles.add(tile)
                if self.map[i][j] == "D":
                    self.mouse_overable.add(tile)
                if self.map[i][j] in ["I", "C"]:
                    item_tile = Tile(ITEMS.get_tile(self.items[(j, i)]), (j, i), (self.add_x, self.add_y), self.map[i][j])
                    self.items_sprites.add(item_tile)
                    self.mouse_overable.add(item_tile)
        return self.__tiles