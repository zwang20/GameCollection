import pygame
import os
import random
import sys
import math
import time

print('Complex Game Engine by Michael Wang Imported')

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
TINY_FONT = pygame.font.SysFont("arial", 10)
SMALL_FONT = pygame.font.SysFont("arial", 20)
MEDUIUM_FONT = pygame.font.SysFont("arial", 40)
LARGE_FONT = pygame.font.SysFont("arial", 80)
HUGE_FONT = pygame.font.SysFont("arial", 100)

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
    elif '.wav' in file or '.ogg' in file:
        # music[file.split('.')[0]] = pygame.mixer.music.load(file)
        music[file] = os.path.abspath(file)
os.chdir('..')
os.chdir('sounds')
for file in os.listdir():
    if file[0] == '.':
        continue
    elif '.wav' in file or '.ogg' in file:
        sounds[file.split('.')[0]] = pygame.mixer.Sound(file)
os.chdir('..')
os.chdir('..')

# Classes

# Basic Game Object
class GameObj(pygame.sprite.Sprite):

    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self)

# button class
class Button(GameObj):

    family = pygame.sprite.Group()

    def __init__(self, rect, text, text_size, unfocus_colour, focus_colour, text_colour, action):
        super().__init__()
        self.x, self.y, self.width, self.height = rect
        self.image = pygame.Surface((self.width, self.height))
        self.text = str(text)
        self.text_size = text_size
        self.unfocus_colour = unfocus_colour
        self.focus_colour = focus_colour
        self.text_colour = text_colour
        self.action = action
        self.image.fill(self.unfocus_colour)
        self.rect = self.image.get_rect()
        self.text_render = text_size.render(text, True, text_colour)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.width / 2, self.height / 2
        self.image.blit(self.text_render, self.text_rect)
        self.rect.topleft = (self.x, self.y)
        Button.family.add(self)

    def update(self):
        if self.x + self.width > mouse_pos[0] > self.x and self.y + self.height > mouse_pos[1] > self.y:
            self.image.fill(self.focus_colour)
            if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            # pygame.event.get()
            # if pygame.mouse.get_pressed()[0]:
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                pygame.event.clear()
                exec(self.action)
                # self.action()
        else:
            self.image.fill(self.unfocus_colour)
        if random.randint(0, 99) == 69:
            pygame.event.clear()
        self.image.blit(self.text_render, self.text_rect)

# functions

mouse_pos = pygame.mouse.get_pos()
keys = pygame.key.get_pressed()
mouse = pygame.mouse.get_pressed()

def launch(name):
    try:
        __import__(name)
    except KeyboardInterrupt:
        pass
    try:
        del name
    except NameError:
        pass
    refresh()

def refresh():
    GameObj.family.empty()
    DISPLAY.fill(WHITE)
    text = HUGE_FONT.render(str('Games Collection'), True, BLACK)
    DISPLAY.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/5 - text.get_height()/2))
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvC', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.crazy_spin_pvc")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvP', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.crazy_spin_pvp")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 60, 500, 50), 'Simple Shooter', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.simple_shooter")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 60, 500, 50), 'Chaos', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.chaos")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 0, 500, 50), 'Craft Battle', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.craft_battle")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 0, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.snake")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 240, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 240, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, '')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 300, 500, 50), 'Information', SMALL_FONT, YELLOW, DARK_YELLOW, BLACK, 'launch("games.information")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 300, 500, 50), 'Quit', SMALL_FONT, RED, DARK_RED, BLACK, 'sys.exit()')
    text = SMALL_FONT.render(str('Version 1.2.5'), True, BLACK)
    DISPLAY.blit(text, (0, HEIGHT - 10 - text.get_height()/2))
    pygame.display.set_caption("Games Collection")
    pygame.display.set_icon(images['game_icon'])
    pygame.mouse.set_visible(True)

# get input
def get_input():
    global mouse_pos
    global keys
    global mouse
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if pygame.event.peek(pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
        pygame.quit()
        sys.exit()

def game_quit():
    GameObj.family.empty()
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    raise KeyboardInterrupt

def useless_func():
    pass
