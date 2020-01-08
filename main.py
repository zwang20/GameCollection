# initialise complex game engine
from games.cge import *


# import main menu
from main_menu import main_menu


# tell the compiler to include packages
# the compiler is too smart for its own good
# DO NOT DELETE THIS UNLESS YOU ARE STUPID
if False:
    import games.crazy_spin_pvc
    import games.crazy_spin_pvp
    import games.information
    import games.simple_shooter
    import games.chaos
    import games.craft_battle
    import games.snake
    import games.more
    import games.minesweeper
    import games.tetris
    import games.crazy_spin_2


# start the main menu
main_menu()


# exit the program if the main menu stops
sys.exit()
