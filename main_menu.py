# import complex game engine
from games.cge import *

# define the main menu
def main_menu():


    # kill all objects
    GameObj.family.empty()

    # fill white background
    DISPLAY.fill(WHITE)

    # print title
    text = HUGE_FONT.render(str('Games Collection'), True, BLACK)
    DISPLAY.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/5 - text.get_height()/2))


    # create buttons
    # TODO: add scroll wheel
    # TODO: create smarter way
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvC', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.crazy_spin_pvc")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 120, 500, 50), 'Crazy Spin PvP', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.crazy_spin_pvp")')
    # SS --> SS2
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 60, 500, 50), 'Simple Shooter 2', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.simple_shooter_2")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 60, 500, 50), 'Chaos', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.chaos")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 - 0, 500, 50), 'Craft Battle', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.craft_battle")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 - 0, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'launch("games.snake")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 60, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 120, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 180, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 240, 500, 50), '', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'useless_func()')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 240, 500, 50), 'More', SMALL_FONT, BLUE, DARK_BLUE, BLACK, 'launch("games.more")')
    Button((WIDTH/2 - 250 - 255, HEIGHT/2 + 300, 500, 50), 'Information', SMALL_FONT, YELLOW, DARK_YELLOW, BLACK, 'launch("games.information")')
    Button((WIDTH/2 - 250 + 255, HEIGHT/2 + 300, 500, 50), 'Quit', SMALL_FONT, RED, DARK_RED, BLACK, 'sys.exit()')

    # version Information
    # very imortant
    text = SMALL_FONT.render(str('Version 1.3.0 Alpha'), True, BLACK)
    DISPLAY.blit(text, (0, HEIGHT - 10 - text.get_height()/2))

    # set caption of window
    pygame.display.set_caption("Games Collection")

    # set icon of program
    pygame.display.set_icon(images['game_icon'])

    # set mouse visibility to true
    pygame.mouse.set_visible(True)

    # main loop
    while True:

        # Advance clock
        clock.tick(60)

        # Detect input
        get_input()

        GameObj.family.update() # update sprites
        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop
