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
display = pygame.display.set_mode([display_width, display_height])

# Load Everything
os.chdir('assets')
directories = []
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.' not in file:
        directories.append(file)
    else:
        print(file)
