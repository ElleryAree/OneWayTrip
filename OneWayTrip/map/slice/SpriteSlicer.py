from OneWayTrip.Utils import load_tile_table

__author__ = 'elleryaree'

import pygame
import pygame.locals

if __name__=='__main__':
    pygame.init()
    screen = pygame.display.set_mode((630, 590))
    screen.fill((255, 255, 255))
#    table = load_tile_table("scr4scifi.jpeg", 32, 32)
    table = load_tile_table("fan.png", 32, 32)
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            screen.blit(tile, (x*37, y*37))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
