from cge import *

def main_menu():

    refresh()

    while True:
        # print(pygame.event.get())
        clock.tick(60)

        if pygame.event.peek(pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
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
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 300, 500, 50), 'Information', SMALL_FONT, YELLOW, DARK_YELLOW, BLACK, launch_information)
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 300, 500, 50), 'Quit', SMALL_FONT, RED, DARK_RED, BLACK, sys.exit)
    text = SMALL_FONT.render(str('Version 1.2.2'), True, BLACK)
    DISPLAY.blit(text, (0, HEIGHT - 10 - text.get_height()/2))
    pygame.display.set_caption("Games Collection")
    pygame.display.set_icon(images['game_icon'])
    pygame.mouse.set_visible(True)


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
    while True:
        try:
            import simple_shooter
        except KeyboardInterrupt:
            break
        except AttributeError:
            continue
    try:
        del simple_shooter
    except NameError:
        pass
    refresh()

def launch_chaos():
    try:
        import chaos
    except KeyboardInterrupt:
        pass
    try:
        del chaos
    except NameError:
        pass
    refresh()

def launch_craft_battle():
    try:
        import CraftBattle
    except KeyboardInterrupt:
        pass
    try:
        del CraftBattle
    except NameError:
        pass
    refresh()

main_menu()

sys.exit()
