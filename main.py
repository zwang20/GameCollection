from cge import *

def main_menu():

    while True:
        clock.tick(60)
        DISPLAY.fill(WHITE)
        text = HUGE_FONT.render(str('Games Collection'), True, BLACK)
        DISPLAY.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/5 - text.get_height()/2))

        get_input()

        Button((WIDTH/2 - 300, HEIGHT/2, 600, 50), 'Crazy Spin PvC', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvc)
        Button((WIDTH/2 - 300, HEIGHT/2 + 60, 600, 50), 'Crazy Spin PvP', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvp)
        Button((WIDTH/2 - 300, HEIGHT/2 + 120, 600, 50), 'Information', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_information)
        Button((WIDTH/2 - 300, HEIGHT/2 + 180, 600, 50), 'Quit', SMALL_FONT, GREEN, DARK_GREEN, BLACK, sys.exit)

        if pygame.event.peek(pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
            pygame.quit()
            sys.exit()

        GameObj.family.update() # update sprites
        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop

def launch_crazy_spin_pvc():
    try:
        import crazy_spin_pvc
        try:
            del crazy_spin_pvc
        except NameError:
            pass
    except KeyboardInterrupt:
        pass

def launch_crazy_spin_pvp():
    try:
        import crazy_spin_pvp
        try:
            del crazy_spin_pvp
        except NameError:
            pass
    except KeyboardInterrupt:
        pass

def launch_information():
    try:
        import information
        try:
            del information
        except NameError:
            pass
    except KeyboardInterrupt:
        pass

main_menu()

sys.exit()
