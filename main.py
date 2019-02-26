from cge import *

def main_menu():

    refresh()

    while True:
        clock.tick(60)

        get_input()

        if pygame.event.peek(pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
            pygame.quit()
            sys.exit()

        GameObj.family.update() # update sprites
        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop

def refresh():
    GameObj.family.empty()
    DISPLAY.fill(WHITE)
    text = HUGE_FONT.render(str('Games Collection'), True, BLACK)
    DISPLAY.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/5 - text.get_height()/2))
    Button((WIDTH/2 - 300, HEIGHT/2, 600, 50), 'Crazy Spin PvC', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvc)
    Button((WIDTH/2 - 300, HEIGHT/2 + 60, 600, 50), 'Crazy Spin PvP', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvp)
    Button((WIDTH/2 - 300, HEIGHT/2 + 120, 600, 50), 'Simple Shooter', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_simple_shooter)
    Button((WIDTH/2 - 300, HEIGHT/2 + 180, 600, 50), 'Information', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_information)
    Button((WIDTH/2 - 300, HEIGHT/2 + 240, 600, 50), 'Quit', SMALL_FONT, GREEN, DARK_GREEN, BLACK, sys.exit)


def launch_crazy_spin_pvc():
    try:
        import crazy_spin_pvc
    except KeyboardInterrupt:
        pass
    try:
        del crazy_spin_pvc
    except NameError:
        pass
    refresh()

def launch_crazy_spin_pvp():
    try:
        import crazy_spin_pvp
    except KeyboardInterrupt:
        pass
    try:
        del crazy_spin_pvp
    except NameError:
        pass
    refresh()

def launch_information():
    try:
        import information
    except KeyboardInterrupt:
        pass
    try:
        del information
    except NameError:
        pass
    refresh()

def launch_simple_shooter():
    try:
        import simple_shooter
    except KeyboardInterrupt:
        pass
    try:
        del simple_shooter
    except NameError:
        pass
    refresh()

main_menu()

sys.exit()
