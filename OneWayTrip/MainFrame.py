import pygame
from OneWayTrip.GameFrames import *
from OneWayTrip.Utils import load_image

__author__ = 'elleryaree'

class MainFrame:
    def __init__(self, screen, days_left = 10):
        frame_size = (screen.get_width(), screen.get_height() - 64)
        self.menu_list = {"World": WorldFrame(frame_size),
                          "Map": MapFrame(frame_size),
                          "Tree": TreeFrame(frame_size),
                          "Score": None, "Days_left": None}
        self.selected = "World"

        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.days_left = days_left

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.menu_sprites = pygame.sprite.RenderPlain()
        self.pointer = Pointer()
        self.pointer_group = pygame.sprite.GroupSingle(self.pointer)

        item_x = (self.background.get_width()/2) - (70 * len(self.menu_list) / 2)
        item_y = self.background.get_height() - 65
        for menu_item in self.menu_list:
            if menu_item == "Score":
                text_value = "%s" % self.score
            elif menu_item == "Days_left":
                text_value = "-%s" % self.days_left
            else:
                text_value = menu_item

            item = MenuItem(menu_item, text_value, (item_x, item_y), self.font)
            if menu_item == "World":
                item.selected = True

            self.menu_sprites.add(item)

            item_x += 70


    def update(self):
        frame = self.menu_list[self.selected]
        frame.update()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(frame.surface, (0, 0))

        self.menu_sprites.update()
        self.pointer_group.update()

        self.menu_sprites.draw(self.screen)
        self.pointer_group.draw(self.screen)

    def checkMousePress(self):
        for clicked_menu in pygame.sprite.spritecollide(self.pointer, self.menu_sprites, 0):
            if not self.menu_list[clicked_menu.name]:
                continue

            for sprite in self.menu_sprites:
                sprite.selected = False
            clicked_menu.selected = True
            self.selected = clicked_menu.name

        self.menu_list[self.selected].checkMousePress()


class Pointer(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('pointer.bmp', pygame.Color("#454e5b"))

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
#        if self.punching:
#            self.rect.move_ip(5, 10)


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, name, text_value, position, font):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.name = name
        self.selected = False
        self.image_selected, self.rect_selected = load_image("menuSelected.png", -1)
        self.image_simple, self.rect_simple = load_image("menuBackground.png", -1)

        self.rect_simple.topleft = position
        self.rect_selected.topleft = position

        self.image = self.image_simple
        self.rect = self.rect_simple

        self.text = font.render(text_value, 1, (250, 250, 250))
        self.text_pos = self.text.get_rect(centerx=self.image.get_width()/2, centery = self.image.get_height()/2)

    def update(self):
        if self.selected:
            self.image = self.image_selected
            self.rect = self.rect_selected
        else:
            self.image = self.image_simple
            self.rect = self.rect_simple

        self.image.blit(self.text, self.text_pos)
