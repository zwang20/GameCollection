from games.cge import *
from games.simple_shooter_2.classes import *
from games.simple_shooter_2.init import *
# TODO: decrease reliance on sge
# from games.sge import *


print(player_img)
def menu():

    player = Player()
    # ss2 menu
    while True:
        DISPLAY.fill(GREY)

        # get input
        get_input()

        player.display()

        pygame.display.update()
        # last thing in the loop


menu()
