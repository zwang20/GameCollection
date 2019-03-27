from cge import *

pygame.display.set_caption('Mine Sweeper')

GameObj.family.empty()

DISPLAY.fill(WHITE)

class Cell(GameObj):
    pass

def main():
    while True:
        get_input()

        

        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop
