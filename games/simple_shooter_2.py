from games.cge import *
# TODO: decrease reliance on sge
# from games.sge import *



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


# player class
class Player:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.cooldown = 0
        self.health = 100


def menu():
    # ss2 menu
    while True:
        DISPLAY.fill(GREY)

        # get input
        get_input()

        pygame.display.update()
        # last thing in the loop


menu()
