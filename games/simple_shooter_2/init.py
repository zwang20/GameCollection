import pygame
from engine.main import *

# load colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (204, 51, 0)
YELLOW = (255, 153, 0)
DARK_GREEN = (51, 204, 51)
GREEN = (0, 128, 0)
DARK_BLUE = (0, 102, 255)
GREY = (40, 40, 50)
BLUE = (0, 0, 128)


# load images
player_img = images['ss2_ship1blue']


# stop music
pygame.mixer.music.stop()


# Set caption to ss2
pygame.display.set_caption('Simple Shooter 2')
