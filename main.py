from games.cge import *

def main_menu():

    refresh()

    while True:
        # print(pygame.event.get())
        clock.tick(60)

        if (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
            pygame.quit()
            sys.exit()

        # print(pygame.event.peek(pygame.MOUSEBUTTONDOWN))

        get_input()
        GameObj.family.update() # update sprites
        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop

if False:  # DO NOT DELETE THIS UNLESS YOU ARE STUPID
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

main_menu()

sys.exit()
