import pygame
import random
from engine.launch import launch

def get_input():

    # ...
    global mouse_pos
    global keys
    global mouse
    global events


    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    # New way of detecting events
    events = pygame.event.get()
    for i in events:
        if (i == pygame.quit) or (keys[pygame.K_q] and keys[pygame.K_LMETA]):
            sys.exit()

    return events


def game_quit():
    GameObj.family.empty()
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    raise KeyboardInterrupt


def useless_func():
    pass


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
            if mouse[0]:
                exec(self.action)
        else:
            self.image.fill(self.unfocus_colour)

        # EXCUSE ME WHAT
        # if random.randint(0, 99) == 69:
        #     pygame.event.clear()

        self.image.blit(self.text_render, self.text_rect)
