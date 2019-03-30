from games.cge import *

pygame.display.set_caption('Snake')

DISPLAY.fill(WHITE)

class Cell(GameObj):

    family = pygame.sprite.Group()

    WIDTH = 10
    HEIGHT = 10

    def __init__(self, x, y):
        pass


def main():
    while True:
        get_input()


        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop
