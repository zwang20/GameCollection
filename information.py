from cge import *

GameObj.family.empty()

DISPLAY.fill(WHITE)

DISPLAY.blit(LARGE_FONT.render('Information', True, BLACK), (0, 0))
DISPLAY.blit(MEDUIUM_FONT.render('Crazy Spin PvC and Crazy Spin PvP', True, BLACK), (0, 100))
DISPLAY.blit(SMALL_FONT.render('\t Created by Edward Ji in early 2018', True, BLACK), (0, 150))
DISPLAY.blit(SMALL_FONT.render('\t Contributed by Michael Wang', True, BLACK), (0, 175))
DISPLAY.blit(SMALL_FONT.render('\t Ported to Games Collection by Michael Wang', True, BLACK), (0, 200))
DISPLAY.blit(SMALL_FONT.render('\t Playtested by Josh Chen', True, BLACK), (0, 225))

Button((WIDTH/2 - 300, HEIGHT/2 + 300, 600, 50), 'Back', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'game_quit()')

while True:
    clock.tick(60)

    get_input()

    # print(pygame.event.peek(pygame.MOUSEBUTTONDOWN))

    if (pygame.key.get_pressed()[pygame.K_q] and (pygame.key.get_pressed()[pygame.K_LMETA] or pygame.key.get_pressed()[pygame.K_RMETA])):
        pygame.quit()
        sys.exit()
    if pygame.key.get_pressed()[pygame.K_q]:
        raise KeyboardInterrupt

    GameObj.family.update() # update sprites
    GameObj.family.draw(DISPLAY) # draw sprites
    pygame.display.update()  # update
    # This should be the last thing in the loop
