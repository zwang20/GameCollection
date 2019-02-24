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

# creat window
WIDTH = 1280
HEIGHT = 800
DISPLAY = pygame.display.set_mode([WIDTH, HEIGHT])

# data
sounds = {}
images = {}
data = {}
music = {}

# colours
BLACK = (0, 0, 0)

WHITE = (255, 255, 255); GREY = (128, 128, 128)

RED = (255, 0, 0); DARK_RED = (128, 0, 0)
GREEN = (0, 255, 0); DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255); DARK_BLUE = (0, 0, 128)

CYAN = (0, 255, 255); DARK_CYAN = (0, 128, 128)
MAGENTA = (255, 0, 255); DARK_MAGENTA = (128, 0, 128)
YELLOW = (255, 255, 0); DARK_YELLOW = (128, 128, 0)

SKY_BLUE = (0, 128, 255); PALE_GREEN = (0, 225, 128)
PURPLE = (128, 0, 255); PINK = (255, 0, 128)
USELESS_GREEN = (128, 255, 0); ORANGE = (255, 128, 0)

# fonts
smallFont = pygame.font.SysFont("arial", 25)
medFont = pygame.font.SysFont("arial", 40)
largeFont = pygame.font.SysFont("arial", 80)

# Load Everything
os.chdir('assets')
os.chdir('data')
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.qgd' in file:
        data[file.split('.')[0]] = open(file).read()
os.chdir('..')
os.chdir('images')
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.png' in file:
        images[file.split('.')[0]] = pygame.image.load(file)
os.chdir('..')
os.chdir('music')
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.wav' in file:
        music[file.split('.')[0]] = pygame.mixer.music.load(file)
os.chdir('..')
os.chdir('sounds')
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.wav' in file:
        sounds[file.split('.')[0]] = pygame.mixer.Sound(file)
os.chdir('..')
os.chdir('..')
