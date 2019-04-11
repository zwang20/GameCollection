from games.cge import *

GameObj.family.empty()

DISPLAY.fill(WHITE)

text = ''
DISPLAY.blit(LARGE_FONT.render('Load Game', True, BLACK), (0, 0))
DISPLAY.blit(SMALL_FONT.render(text, True, BLACK), (0, 100))

Button((WIDTH/2 - 300, HEIGHT/2 + 300, 600, 50), 'Back', SMALL_FONT, GREEN, DARK_GREEN, BLACK, 'game_quit()')
wait = 0

while True:
    clock.tick(60)

    get_input()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if 'games' in text:
                    try:
                        launch(text)
                    except ModuleNotFoundError:
                        DISPLAY.blit(SMALL_FONT.render('Module Not Found', True, BLACK), (0, 150))
                        wait = 50
                else:
                    DISPLAY.blit(SMALL_FONT.render('Incorrect Format', True, BLACK), (0, 150))
                    wait = 50
                text = ''
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    pygame.draw.rect(DISPLAY, WHITE, (0, 100, 1280, 50))
    DISPLAY.blit(SMALL_FONT.render(text, True, BLACK), (0, 100))

    if wait > 0:
        wait -= 1

    if wait == 0:
        pygame.draw.rect(DISPLAY, WHITE, (0, 150, 1280, 50))

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
