import pygame
import os
import random
import sys
import math
import time

# init pygame
pygame.init()

# create clock
clock = pygame.time.Clock()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255); GREY = (128, 128, 128)
RED = (255, 0, 0); DARK_READ = (128, 0, 0)
GREEN = (0, 255, 0); DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255); DARK_BLUE = (0, 0, 128)
CYAN = (0, 255, 255); DARK_CYAN = (0, 128, 128)
MAGENTA = (255, 0, 255); DARK_MAGENTA = (128, 0, 128)
YELLOW = (255, 255, 0); DARK_YELLOW = (128, 128, 0)

# creat window
display_width = 1280
display_height = 800
display = pygame.display.set_mode([display_width, display_height], pygame.NOFRAME)

# set caption
pygame.display.set_caption('Chaos')

# set icon
pygame.display.set_icon(
    pygame.image.load(os.path.join('assets', '32x32_project_nont.png'))
)

# Load images
rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_rifle.png'))
sniper_rifle_img = pygame.image.load(os.path.join('Assets', 'guns', 'gun_sniper.png'))

# load sounds
pistol_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M1911.ogg'))
rifle_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'M16.ogg'))
reload_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'Reload.ogg'))

# sound channels
CHANNELS = 100
pygame.mixer.set_num_channels(CHANNELS)


class GameObj(pygame.sprite.Sprite):

    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)
