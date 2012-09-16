import pygame
from OneWayTrip.Pathfinder import PathFinder
from OneWayTrip.TileSet import *
from OneWayTrip.Things import *
from OneWayTrip.Talk import *

__author__ = 'elleryaree'

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

ITEMS = ItemsTileSet()

class BasicFrame(pygame.sprite.Sprite):
    def __init__(self, size, pointer, big_pointer):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.font = pygame.font.Font(None, 36)
        self.text = "Basic frame"
        self.surface = pygame.Surface(size)
        self.pointer = pointer
        self.big_pointer = big_pointer

        self.all_Items = {}
        self.items1 = {(4, 1): Item(10, "First.png", (4, 1), [UP, DOWN, RIGHT, LEFT], "1 credit", 1)}
        self.items2 = {(3, 0): Item(3, "Ficus.png", (3, 0), [UP, DOWN, RIGHT, LEFT], "Funny ficus", 10),
                       (2, 8): Item(10, "First.png", (2, 8), [UP, DOWN, RIGHT, LEFT], "1 credit", 1),
                       (4, 11): Item(10, "First.png", (4, 11), [UP, DOWN, RIGHT, LEFT], "1 credit", 1)}
        self.items3 = {(11, 8): Item(10, "First.png", (11, 8), [UP, DOWN, RIGHT, LEFT], "1 credit", 1),
                       (12, 4): Item(10, "First.png", (12, 4), [UP, DOWN, RIGHT, LEFT], "1 credit", 1),
                        (16, 12): Item(10, "First.png", (16, 12), [LEFT], "Last", 1)}
        for item in self.items1.values():
            self.all_Items[item.id] = item
        for item in self.items2.values():
            self.all_Items[item.id] = item
        for item in self.items3.values():
            self.all_Items[item.id] = item

        self.all_Items[4] = Item(4, "embrion.png", (16, 10), [UP, DOWN, RIGHT, LEFT], "Proof of nobless", 1)


        self.all_chars = {}
        self.chars1 = {(3, 12): Char([3, 12, "U", 1], [UP], "Rocket ticket seller", "kurosu"),
                       (16, 10): Char([16, 10, "L", 1], [LEFT, UP], "Mad scientist", "suka")}
        self.chars2 = {(5, 6): Char([5, 6, "R", 1], [DOWN, LEFT], "A noble man", "kaito")}
        self.chars3 = {(9, 5): Char([9, 5, "D", 1], [DOWN, LEFT, UP, RIGHT], "Noble zombie", "miruru")}

        for char in self.chars1.values():
            self.all_chars[char.name] = char
        for char in self.chars2.values():
            self.all_chars[char.name] = char
        for char in self.chars3.values():
            self.all_chars[char.name] = char

        self.dialog_texts = TalkParser().parse()

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

        self.hero_position = [1, 0, "D", 1]

        street1 =  [["W", "S", "W", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "D", "S"],
                    ["W", "S", "W", "S", "I", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "S", "W", "D", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "S", "W", "W", "S", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "S", "W", "W", "S", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "W", "S", "S", "S", "S", "S", "S", "S", "W", "D", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
                    ["W", "W", "W", "S", "S", "W", "W", "W", "S", "S", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "W", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],
                    ["W", "S", "S", "S", "S", "S", "W", "S", "S", "S", "W", "W", "W", "W", "W", "S", "C"],
                    ["W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "W", "C", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"]]


        street2 =  [["W", "S", "S", "I", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W"],
                    ["W", "S", "W", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W"],
                    ["W", "S", "W", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "S", "S", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "S", "S", "W", "W"],
                    ["W", "W", "W", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "S", "S", "W", "W"],
                    ["W", "W", "W", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "C", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W", "W"],
                    ["W", "S", "I", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "S", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "S", "S", "S", "I", "S", "W", "W", "W", "D", "W", "W", "W", "D", "W", "W", "W"],
                    ["W", "S", "W", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S"]]

        street3 =  [["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "W", "W", "W", "D", "W", "W", "S", "S", "S", "S", "S", "I", "S", "S", "W", "W"],
                    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "C", "S", "S", "S", "W", "S", "W", "W"],
                    ["W", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["W", "S", "S", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "W", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "I", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "S", "S", "W", "W"],
                    ["S", "S", "W", "W", "W", "W", "W", "W", "S", "S", "S", "S", "S", "W", "S", "S", "I"]]

        doors1 = {(8, 3): Door((8, 3), [13, 12, "D", 1], 1, [DOWN], "garden"),
                  (11, 6): Door((11, 6), [13, 0, "L", 1], 0, [DOWN], "somewhere"),
                  (15, 0): Door((15, 0), [11, 7, "D", 1], 0, [LEFT], "sewers")}
        doors2 = {(13, 11): Door((9, 6), [8, 4, "D", 1], 0, [DOWN], "near the rocket"),
                  (9, 11): Door((9, 11), [4, 5, "D", 1], 2, [DOWN], "to the road")}
        doors3 = {(4, 4): Door((4, 4), [13, 0, "D", 1], 0, [DOWN], "near the rocket")}

        self.location_grids = [WorldSet(size, street1, DarkWorldTileSet(), doors1, self.items1, self.chars1),
                               WorldSet(size, street2, GreenWorldTileSet(), doors2, self.items2, self.chars2),
                               WorldSet(size, street3, LightWorldTileSet(), doors3, self.items3, self.chars3)]
        self.current_street = 0
        add = (self.location_grids[self.current_street].add_x, self.location_grids[self.current_street].add_y)

        hero_tile_set = HeroTileSet()
        hero_image, self.hero_position = hero_tile_set.get_sprite(self.hero_position)
        hero_sprite = HeroTile(hero_image, (self.hero_position[0], self.hero_position[1]), add, hero_tile_set)

        self.dialog = None

        self.hero_sprite = pygame.sprite.GroupSingle(hero_sprite)
        self.click_sprite = pygame.sprite.GroupSingle()
        self.dialog_group = pygame.sprite.GroupSingle()

        self.tick = 0

    def update(self):
        self.surface.fill((0, 0, 0))
        self.tick += 1

        street_ = self.location_grids[self.current_street]
        sprites = street_.tiles()
        items = street_.items_sprites
        chars = street_.characters_sprites

        sprites.update()
        items.update()
        chars.update()

        if len(self.click_sprite.sprites()) and not len(self.click_sprite.sprites()[0].tiles):
            for sprite in self.click_sprite.sprites():
                sprite.kill()
        self.click_sprite.update()

        if self.tick >= 4:
            self.hero_sprite.update()
            self.tick = 0

        sprites.draw(self.surface)
        items.draw(self.surface)
        chars.draw(self.surface)

        self.click_sprite.draw(self.surface)
        self.hero_sprite.draw(self.surface)

        if self.dialog:
            if self.dialog.validate(self.hero_sprite.sprites()[0].position):
                self.dialog.update()
                self.dialog_group.draw(self.surface)
            else:
                self.dialog.kill()
                self.dialog = None


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

        if len(pygame.sprite.spritecollide(self.pointer, self.dialog_group, 0)):
            self.dialog.checkMousePress()
            return

        for clicked_menu in pygame.sprite.spritecollide(self.pointer, sprites, 0):
            if clicked_menu.key == "S":
                self.hero_sprite.sprites()[0].route = self.__find_route(clicked_menu.position)
            if clicked_menu.key == "D":
                door = current_set.doors[clicked_menu.position]

                door_near = False
                adjacent_places = door.action_positions
                x = 0
                y = 0
                for place in adjacent_places:
                    x = clicked_menu.position[0] + place[0]
                    y = clicked_menu.position[1] + place[1]
                    if (x, y) == self.hero_sprite.sprites()[0].position:
                        self.__change_street(door)
                        door_near = True
                        break
                if not door_near:
                    self.hero_sprite.sprites()[0].route = self.__find_route((x, y))


        for clicked_menu in pygame.sprite.spritecollide(self.pointer, current_set.items_sprites, 0):
            if clicked_menu.key in ["I", "C"]:
                if clicked_menu.key == "I":
                    thing = current_set.items[clicked_menu.position]
                elif clicked_menu.key == "C":
                    thing = current_set.characters[clicked_menu.position]
                else:
                    continue

                thing_near = False
                adjacent_places = thing.action_positions
                x = 0
                y = 0
                for place in adjacent_places:
                    x = clicked_menu.position[0] + place[0]
                    y = clicked_menu.position[1] + place[1]
                    if (x, y) == (self.hero_sprite.sprites()[0].position[0], self.hero_sprite.sprites()[0].position[1]):
                        if clicked_menu.key == "I":
                            self.__take_item(clicked_menu, thing, current_set)
                        if clicked_menu.key == "C":
                            self.dialog = DialogFrame(self.main,
                                (500, 500), (self.surface.get_width() / 2 - 250, 0),
                                self.pointer, self.big_pointer, thing, self.dialog_texts[thing.name], self.all_Items, self.all_chars)
                            self.dialog_group.add(self.dialog)

                        thing_near = True
                        break
                if not thing_near:
                    self.hero_sprite.sprites()[0].route = self.__find_route((x, y))

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

        self.main.add_item(item_info.id, item_info.cost)

class MapFrame(BasicFrame):
    def __init__(self, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.text = "Map frame"

class TreeFrame(BasicFrame):
    def __init__(self, size, pointer, big_pointer):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.chars = {}
        for char in self.all_chars:
            self.chars[char] = self.all_chars[char].get_image()

    def update(self):
        self.surface.fill((0, 0, 0))

        i = 0
        j = 1

        text = self.font.render("Items to collect: ", 1, (250, 250, 250))
        self.surface.blit(text, (40 * i + 20, 20))

        for item in self.all_Items.values():
            x = 40 * i + 20
            y = 40 * j + 20

            item_image = ITEMS.get_tile(item)
            self.surface.blit(item_image, (x, y))

            i += 1
            if j > 2:
                j += 1
                i = 0

        text = self.font.render("Vital characters: ", 1, (250, 250, 250))
        self.surface.blit(text, (20, 40 * (j + 1) + 20))
        j += 2
        i = 0

        for char_name in self.dialog_texts:
            draw = False
            char = self.dialog_texts[char_name]
            for phrase in char.phrases.values():
                if phrase.item is not None:
                    draw = True
                    break

            if draw:
                x = 40 * i + 20
                y = 40 * j + 20

                item_image = self.chars[char_name]
                self.surface.blit(item_image, (x, y))

                i += 1
                if j > 2:
                    j += 1
                    i = 0


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


class DialogFrame(BasicFrame):
    def __init__(self, main, size, position, pointer, big_pointer, char, phrases, all_items, all_chars):
        BasicFrame.__init__(self, size, pointer, big_pointer)
        self.__main = main
        self.__char = char
        self.__needs_closing = False
        self.__position = position
        self.__phrases = phrases
        self.__current_id = 0
        self.__all_items = all_items
        self.__all_chars = all_chars

        self.__close_group = pygame.sprite.GroupSingle()
        self.__answer_group = pygame.sprite.RenderPlain()

        self.rect = pygame.Rect(position, size)
        self.image = self.surface

        text_r_close = self.font.render("Close", 1, (250, 100, 100))
        text_pos_r_close = text_r_close.get_rect(centerx=self.surface.get_width() - 30, centery=10)
        close_sprite = DialogTextSprite(text_r_close, text_pos_r_close)
        self.__close_group.add(close_sprite)

        tile_set = RandomTileSet()
        self.background = pygame.sprite.RenderPlain()
        for i in range(size[1] / 32):
            for j in range(size[0] / 32):
                tile_image = tile_set.get_tile()
                tile = Tile(tile_image, (j, i), (0, 0))
                self.background.add(tile)

        self.redraw()

    def checkMousePress(self):
        self.__needs_closing = len(pygame.sprite.spritecollide(self.pointer, self.__close_group, 0, self.collideTest))

        for chosen_ans in pygame.sprite.spritecollide(self.pointer, self.__answer_group, 0):
            self.__current_id = chosen_ans.next_id
            self.redraw()

    def collideTest(self, rect1, rect2):
        rect1.rect.topleft = (rect1.rect.topleft[0] - self.__position[0], rect1.rect.topleft[1] - self.__position[1])
        return pygame.sprite.collide_rect(rect1, rect2)

    def __get_image_from_chars(self, answer):
        for char_name in self.dialog_texts:
            char = self.dialog_texts[char_name]
            for phrase in char.phrases.values():
                if phrase.item == answer.required:
                    return self.__all_chars[char_name].get_image()
        return None

    def redraw(self):
        self.surface.fill((0, 0, 0))
        self.background.draw(self.surface)

        phrase = self.__phrases.phrases[self.__current_id]

        if phrase.item is not None:
            self.__main.add_item(phrase.item, phrase.cost)

        i = 1

        for text in phrase.text:
            if i == 1:
                text_ = "%s: %s" % (self.__phrases.display_name, text)
            else:
                text_ = text
            text_r_1 = self.font.render(text_, 1, (250, 250, 250))
            text_pos_r_1 = text_r_1.get_rect()
            text_pos_r_1.topleft = (20, (40 * i + 20))
            self.surface.blit(text_r_1, text_pos_r_1)
            i += 1


        self.__answer_group.empty()
        for answer in phrase.answers:
            cnt = 0
            if answer.count is not None and answer.required is not None:
                for itm in self.__main.inventory:
                    if itm == answer.required:
                        cnt += 1

            if answer.required is None or (answer.required in self.__main.inventory and
                                           (answer.count is None or answer.count == cnt)):
                enabled = True
                color = (150, 250, 150)
            else:
                enabled = False
                color = (150, 150, 150)

            ans = self.font.render("> %s" % answer.text, 1, color)
            ans_pos = ans.get_rect()
            y = (40 * i + 20)
            ans_pos.topleft = (40, y)
            self.surface.blit(ans, ans_pos)

            if enabled:
                ans_sprite = AnswerSprite(ans, ans_pos, answer.next_id)
                self.__answer_group.add(ans_sprite)
            if answer.required:
                if answer.required in self.__all_items:
                    item_image = ITEMS.get_tile(self.__all_items[answer.required])
                else:
                    item_image = self.__get_image_from_chars(answer)

                if item_image:
                    self.surface.blit(item_image, (5, y))

            i += 1

        self.__close_group.draw(self.surface)

    def update(self):
        pass

    def validate(self, hero_pos):
        if self.__needs_closing:
            return False

        adjacent_places = self.__char.action_positions
        for place in adjacent_places:
            x = self.__char.position[0] + place[0]
            y = self.__char.position[1] + place[1]
            if (x, y) == hero_pos:
                return True

        return False

class WorldSet(object):
    def __init__(self, size, map, tile_set, doors, items = None, characters = None):
        self.map = map
        self.__tiles = None
        self.__tile_set = tile_set
        self.doors = doors
        self.add_x = 10
        self.add_y = 10

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
                tile_image = self.__tile_set.get_tile(i, j)
                tile = Tile(tile_image, (j, i), (self.add_x, self.add_y), self.map[i][j])
                self.__tiles.add(tile)
                if self.map[i][j] == "D":
                    self.mouse_overable.add(tile)
                if self.map[i][j] in ["I", "C"]:
                    if self.map[i][j] == "I":
                        item_image = ITEMS.get_tile(self.items[(j, i)])
                    else:
                        item_image = self.characters[(j, i)].get_image()
                    item_tile = Tile(item_image, (j, i), (self.add_x, self.add_y), self.map[i][j])
                    self.items_sprites.add(item_tile)
                    self.mouse_overable.add(item_tile)
        return self.__tiles


class DialogTextSprite(pygame.sprite.Sprite):
    def __init__(self, text_r, text_r_pos):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = text_r
        self.rect = text_r_pos

class AnswerSprite(DialogTextSprite):
    def __init__(self, text_r, text_r_pos, next_id):
        DialogTextSprite.__init__(self, text_r, text_r_pos)
        self.next_id = next_id