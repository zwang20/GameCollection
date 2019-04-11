# imports
import pygame
import sys
import os

pygame.init()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255); GREY = (128, 128, 128)
RED = (255, 0, 0); DARK_READ = (128, 0, 0)
GREEN = (0, 255, 0); DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255); DARK_BLUE = (0, 0, 128)
CYAN = (0, 255, 255); DARK_CYAN = (0, 128, 128)
MAGENTA = (255, 0, 255); DARK_MAGENTA = (128, 0, 128)
YELLOW = (255, 255, 0); DARK_YELLOW = (128, 128, 0)


# screen
WIDTH = 1200
HEIGHT = 600
display = pygame.display.set_mode((WIDTH, HEIGHT))


# name the window
pygame.display.set_caption("Crazy Spin 2")


AI = True


class GameObj(pygame.sprite.Sprite):

    family = pygame.sprite.RenderUpdates()

    def __init__(self):
        super().__init__()
        GameObj.family.add(self) # EDWARD!!!! YOU CAN NOT USE self.family.add(self) !!!!!!!!!!!!!!!!!!!!!!!!


class Ball(GameObj):
    radius = 10

    family = pygame.sprite.GroupSingle() # pygame.sprite.GroupSingle()

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.circle(self.image, RED, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        Ball.family.add(self)
        self.x = 8
        self.y = 8

    def update(self):
        if self.rect.y - self.radius * 2 < 0 or self.rect.y + self.radius * 2 > HEIGHT:
            self.y = -self.y
        if pygame.sprite.collide_rect(self, PlayerPad.family.sprite) or pygame.sprite.collide_rect(self, EnemyPad.family.sprite):
            self.x = -self.x
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.respawn()
            # self.x += 0.1 if self.x >=0 else -0.1
            # self.y += 0.1 if self.y >=0 else -0.1
        self.rect.x += self.x
        self.rect.y += self.y

    def respawn(self):
        self.rect.center = WIDTH/2, HEIGHT/2
        PlayerPad.family.sprite.reset()
        EnemyPad.family.sprite.reset()


class BallFuture(GameObj):
    radius = 10

    family = pygame.sprite.GroupSingle()

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius))
        pygame.draw.circle(self.image, BLUE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        BallFuture.family.add(self)

    def update(self):
        self.rect.x = Ball.family.sprite.rect.x + Ball.family.sprite.x
        self.rect.y = Ball.family.sprite.rect.y + Ball.family.sprite.y


class PlayerPad(GameObj):

    height = 100
    width = 20

    family = pygame.sprite.GroupSingle()

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (self.width / 2, HEIGHT / 2)
        PlayerPad.family.add(self)

    def move(self, y):
        self.rect.y += y
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + PlayerPad.height >= HEIGHT:
            self.rect.y = HEIGHT - PlayerPad.height


    def update(self):
        pass

    def reset(self):
        self.rect.center = (self.width / 2, HEIGHT / 2)


class EnemyPad(GameObj):

    height = 100
    width = 20

    family = pygame.sprite.GroupSingle()

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - self.width / 2, HEIGHT / 2)
        EnemyPad.family.add(self)

    def move(self, y):
        self.rect.y += y
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + self.height >= HEIGHT:
            self.rect.y = HEIGHT - self.height


    def update(self):
        if AI:
            self.ai()


    def ai(self):
        if Ball.family.sprite.rect.y > self.rect.y:
            self.move(8)
        elif Ball.family.sprite.rect.y < self.rect.y:
            self.move(-8)
        else:
            pass

    def reset(self):
        self.rect.center = (WIDTH - self.width / 2, HEIGHT / 2)


def game():
    Ball()
    BallFuture()
    PlayerPad()
    EnemyPad()
    while True:
        display.fill(BLACK)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and (keys[pygame.K_LMETA] or keys[pygame.K_RMETA]) or pygame.event.peek(pygame.QUIT):  # Quit
            pygame.quit()
            sys.exit()
        if keys[pygame.K_w]:
            PlayerPad.family.sprite.move(-5)
        if keys[pygame.K_s]:
            PlayerPad.family.sprite.move(5)
        if not AI:
            if keys[pygame.K_UP]:
                EnemyPad.family.sprite.move(-5)
            if keys[pygame.K_DOWN]:
                EnemyPad.family.sprite.move(5)

        GameObj.family.draw(display)
        GameObj.family.update()

        pygame.display.update()


game()
