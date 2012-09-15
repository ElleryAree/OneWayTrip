import pygame
from pygame.constants import  QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from OneWayTrip.MainFrame import MainFrame
from OneWayTrip.Utils import *
from OneWayTrip.bmpfont import BmpFont

__author__ = 'elleryaree'

def main():
    if not pygame.font: print ('Warning, fonts disabled')
    if not pygame.mixer: print ('Warning, sound disabled')

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.mouse.set_visible(0)

#    sound = load_sound("Theme.ogg")
#    sound.play()

    pygame.display.set_caption('Last rocket')
    image, rect = load_image("invader_1.jpeg", -1)
    pygame.display.set_icon(image)

    mainFrame = MainFrame(screen)
    clock = pygame.time.Clock()

    score = 0
    days_left = 2

    mainFrame.score = score
    mainFrame.days_left = days_left

    while True:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return -1
            elif event.type == MOUSEBUTTONDOWN:
                mainFrame.checkMousePress()
            elif event.type == KEYDOWN:
                return 1

        mainFrame.update()

        pygame.display.flip()