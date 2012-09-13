import pygame

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

    def checkMousePress(self):
        pass

class WorldFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "World frame"

class MapFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "Map frame"

class TreeFrame(BasicFrame):
    def __init__(self, size):
        BasicFrame.__init__(self, size)
        self.text = "Tree frame"