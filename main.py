from cge import *

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

def refresh():
    GameObj.family.empty()
    DISPLAY.fill(WHITE)
    text = HUGE_FONT.render(str('Games Collection'), True, BLACK)
    DISPLAY.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/5 - text.get_height()/2))
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvC', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvc)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvP', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_crazy_spin_pvp)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 60, 500, 50), 'Simple Shooter', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_simple_shooter)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 60, 500, 50), 'Chaos', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_chaos)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 0, 500, 50), 'Craft Battle', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_craft_battle)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 0, 500, 50), 'Snake', SMALL_FONT, GREEN, DARK_GREEN, BLACK, launch_snake)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 240, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 240, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, useless_func)
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 300, 500, 50), 'Information', SMALL_FONT, YELLOW, DARK_YELLOW, BLACK, launch_information)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 300, 500, 50), 'Quit', SMALL_FONT, RED, DARK_RED, BLACK, sys.exit)
    text = SMALL_FONT.render(str('Version 1.2.3'), True, BLACK)
    DISPLAY.blit(text, (0, HEIGHT - 10 - text.get_height()/2))
    pygame.display.set_caption("Games Collection")
    pygame.display.set_icon(images['game_icon'])
    pygame.mouse.set_visible(True)

def launch(name):
    try:
        exec(' '.join(['import', name]))
    except KeyboardInterrupt:
        pass
    try:
        del name
    except NameError:
        pass
    refresh()

def launch_crazy_spin_pvc():
    launch('crazy_spin_pvc')

def launch_crazy_spin_pvp():
    launch('crazy_spin_pvp')

def launch_information():
    launch('information')

def launch_simple_shooter():
    launch('simple_shooter')

def launch_chaos():
    launch('chaos')

def launch_craft_battle():
    launch('craft_battle')

def launch_snake():
    launch('snake')

main_menu()

sys.exit()
