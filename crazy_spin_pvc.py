from variables import *

pygame.display.set_caption("Crazy Spin PvC")

pygame.display.set_icon(images['crazy_spin_icon'])

backgroundMusic = music['background_music']

backgroundImg = images['background_image']

padBounceSound = sounds["pad_bounce"]
edgeBounceSound = sounds['edge_bounce']
cheerSound = sounds['cheer']
whistleSound = sounds['whistle']

# game wide constants
pad_length = int(HEIGHT / 6)  # 100
pad_width = int(WIDTH / 45)  # 17
ball_size = int(HEIGHT / 40)  # 15
effect_size = 30
pad_speed = int(HEIGHT / 45)  # 13
ball_speed_init = int(HEIGHT / 50)  # 12
ball_speed_rate = 1.05
ball_spin_effect = 1.1
ball_spin_fade = 0.008
edge_bounce_limit = 10
win_condition = 10
FPS = 45
# ball reflection lambdas


def x_reflect(x): return 360 - x


def y_reflect(x): return 180 - x


def dumb(): return random.randint(1, 10) == 1

# create text objects


def text_objects(msg, color, size):
    if size == "small":
        screen_text = SMALL_FONT.render(msg, True, color)
    elif size == "medium":
        screen_text = MEDUIUM_FONT.render(msg, True, color)
    elif size == "large":
        screen_text = LARGE_FONT.render(msg, True, color)
    return screen_text, screen_text.get_rect()

# display mmessage


def displayMsg(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (WIDTH / 2, HEIGHT / 2 + y_displace)
    DISPLAY.blit(textSurf, textRect)

# display score of players


def displayDetail(left_score, right_score, edge_bounce):
    scoreSurf, scoreRect = text_objects(
        str(left_score)+" : "+str(right_score), BLACK, "small")
    scoreRect.center = (WIDTH / 2, 30)
    DISPLAY.blit(scoreSurf, scoreRect)
    if right_score != win_condition and left_score != win_condition:
        if right_score == win_condition - 1:
            msg = "Game Point"
            bounceSurf, bounceRect = text_objects(msg,
                                                  BLACK,
                                                  "small")
            bounceRect.center = (WIDTH / 2 + 100, 30)
            DISPLAY.blit(bounceSurf, bounceRect)
        if left_score == win_condition - 1:
            msg = "Game Point"
            bounceSurf, bounceRect = text_objects(msg,
                                                  BLACK,
                                                  "small")
            bounceRect.center = (WIDTH / 2 - 100, 30)
            DISPLAY.blit(bounceSurf, bounceRect)
    if edge_bounce >= edge_bounce_limit - 3:
        msg = "Ball respawn after "+str(
            edge_bounce_limit-edge_bounce)+" edge bounce"
        bounceSurf, bounceRect = text_objects(msg, BLACK, "small")
        bounceRect.center = (WIDTH / 2, 60)
        DISPLAY.blit(bounceSurf, bounceRect)

# display text for buttons


def buttonText(msg, color, location, size="small"):
    button_x, button_y, button_width, button_height = location
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (
        (button_x + button_width/2), (button_y + button_height/2))
    DISPLAY.blit(textSurf, textRect)

# display responsive button


def displayButton(
        text,
        location, unfocus_color, focus_color, text_color=BLACK, action=None):
    bX, bY, bWidth, bHeight = location
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if bX + bWidth > cursor[0] > bX and bY + bHeight > cursor[1] > bY:
        pygame.draw.rect(DISPLAY, focus_color, location)
        if click[0]:
            action()
    else:
        pygame.draw.rect(DISPLAY, unfocus_color, location)
    buttonText(text, text_color, location)


def displayBackground():
    DISPLAY.fill(WHITE)
    DISPLAY.blit(backgroundImg, [0, 0])
    pygame.draw.rect(
        DISPLAY, BLUE, [0, 0, pad_width, HEIGHT])
    pygame.draw.rect(DISPLAY, BLUE, [WIDTH - pad_width,
                                               0,
                                               pad_width,
                                               HEIGHT])

# display player pads


def displayPad(x, y, length):
    pygame.draw.rect(DISPLAY, BLACK, [x, y, pad_width, length])

# display ball


def displayBall(x, y):
    pygame.draw.rect(DISPLAY, RED, [x, y, ball_size, ball_size])

# reset ball position and variables


def ballReset(side):
    if side == "left":
        ball_dir = random.randint(130, 230)
        x_adjust = 0.3
        ball_x = int((WIDTH - ball_size) / 2 + WIDTH * 0.3)
        ball_y = int((HEIGHT - ball_size) / 2)
        ball_speed = ball_speed_init
        ball_spin = 0
    elif side == "right":
        ball_dir = random.randint(-50, 50)
        ball_x = int((WIDTH - ball_size) / 2 - WIDTH * 0.3)
        ball_y = int((HEIGHT - ball_size) / 2)
        ball_speed = ball_speed_init
        ball_spin = 0
    time.sleep(2)
    return ball_x, ball_y, ball_dir, ball_speed, ball_spin

# reset pad position and variables


def padReset():
    temp = int((HEIGHT - pad_length) / 2)
    return temp, temp

# work out the coordination of the actual hit point


def hit_point(cur_x, cur_y, dir, hit_x=None, hit_y=None):
    if hit_x is not None and hit_y is None:
        return cur_y - (cur_x - hit_x) * math.tan(math.radians(dir))
    elif hit_x is None and hit_y is not None:
        return cur_x - (cur_y - hit_y) / math.tan(math.radians(dir))
    else:
        raise ValueError("only one of hit_x and hit_y should be given.")

# game initiate window


def gameInit():
    pygame.mixer.music.play(-1)

    # check response
    gameStart = False
    while not gameStart:
        # display initiate window
        DISPLAY.blit(backgroundImg, [0, 0])
        displayMsg("Pong PvC", BLACK, -170, "large")
        displayMsg(
            "Move the pads to bouce the ball and guard the goal", BLACK, -70)
        displayMsg("hit while moving you pad to add spin.", BLACK, -40)
        displayMsg("First one to 10 wins!", BLACK, -10)
        displayMsg("Player defualt - W and S", BLACK, 20)

        # display bottons
        displayButton(
            "Play", [WIDTH/2-50-200, 2*HEIGHT/3-25, 100, 50], GREEN, DARK_GREEN, action=gameLoop)
        displayButton(
            "Settings",
            [WIDTH/2-50, 2*HEIGHT/3-25, 100, 50], YELLOW, DARK_YELLOW, action=gameSettings)
        displayButton(
            "Quit", [WIDTH/2-50+200, 2*HEIGHT/3-25, 100, 50], RED, DARK_RED, action=gameQuit)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break # gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                elif event.key == pygame.K_s:
                    gameSettings()
                elif event.key == pygame.K_q:
                    break # gameQuit()
        clock.tick(FPS)

# game initiate window


def gameSettings():
    g = data['crazy_spin_data']
    cdata = [int(line.replace('\n', '')) for line in g.split('\n')[:6]]
    del g
    # check response
    while True:
        # display title and instructions
        DISPLAY.blit(backgroundImg, [0, 0])
        displayMsg("Settings", DARK_GREEN, -230, "large")
        displayMsg(
            "Please do not modify settings with text editor!", DARK_YELLOW, -140)

        # display sound settings
        displayMsg("Game-time music", DARK_YELLOW, -110)
        if cdata[4]:
            displayMsg("On [press B]", DARK_YELLOW, -80)
        else:
            displayMsg("Off [Press B]", DARK_YELLOW, -80)
        displayMsg("Sound effects", DARK_YELLOW, -50)
        if cdata[5]:
            displayMsg("On [Press V]", DARK_YELLOW, -20)
        else:
            displayMsg("Off [Press V]", DARK_YELLOW, -20)

        # display key set settings
        cursor_x, cursor_y = pygame.mouse.get_pos()
        if cursor_y <= HEIGHT/2:
            setKeyName = "Pad moves Up"
            setKeyNo = 0
        else:
            setKeyName = "Pad moves Down"
            setKeyNo = 1
        displayMsg(
            "Move the cursor to upper or lower side to change key.", DARK_YELLOW, 10)
        displayMsg("You can not use key that are pre-defined!", DARK_YELLOW, 40)
        displayMsg("Set Key for: " + setKeyName, DARK_YELLOW, 70)
        displayMsg(
            "Current Key: " + pygame.key.name(cdata[setKeyNo]), DARK_YELLOW, 100)

        # back button
        click = pygame.mouse.get_pressed()
        if 350 + 100 > cursor_x > 350 and 480 + 50 > cursor_y > 480:
            pygame.draw.rect(DISPLAY, DARK_GREEN, [350, 480, 100, 50])
            if click[0]:
                data['crazy_spin_data'] = ('\n'.join(map(str, cdata)))
                return
        else:
            pygame.draw.rect(DISPLAY, GREEN, [350, 480, 100, 50])
        buttonText("Back", BLACK, [350, 480, 100, 50])

        # renew display
        pygame.display.flip()

        # check for key set
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data['crazy_spin_data'] = ('\n'.join(map(str, cdata)))
                break # gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                elif event.key == pygame.K_q:
                    data['crazy_spin_data'] = ('\n'.join(map(str, cdata)))
                    break # gameQuit()
                elif event.key == pygame.K_b:
                    cdata[4] = 0 if cdata[4] else 1
                elif event.key == pygame.K_v:
                    cdata[5] = 0 if cdata[5] else 1
                elif event.key not in cdata:
                    cdata[setKeyNo] = event.key
        clock.tick(FPS)

# game pausing window


def gamePause():
    # stop music and sound effects
    pygame.mixer.music.pause()
    pygame.mixer.stop()

    pygame.mouse.set_visible(True)
    displayMsg("Paused", RED, -100, "large")
    displayMsg("Don't want to have fun with your mates?", BLACK, 25, "medium")
    pygame.display.flip()
    # wait for response
    gamePaused = True
    while gamePaused:
        cursor = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if WIDTH/2-50-200 + 100 > cursor[0] > WIDTH/2-50-200 and 2*HEIGHT/3-25 + 50 > cursor[1] > 2*HEIGHT/3-25: # WHAT IS THIS SH*T
            pygame.draw.rect(DISPLAY, DARK_GREEN, [WIDTH/2-50-200, 2*HEIGHT/3-25, 100, 50])
            if click[0]:
                pygame.mixer.music.unpause()
                pygame.mouse.set_visible(False)
                return
        else:
            pygame.draw.rect(DISPLAY, GREEN, [WIDTH/2-50-200, 2*HEIGHT/3-25, 100, 50])
        buttonText("Continue", BLACK, [WIDTH/2-50-200, 2*HEIGHT/3-25, 100, 50])
        displayButton("Quit", [WIDTH/2-50+200, 2*HEIGHT/3-25, 100, 50], RED, DARK_RED, action=gameQuit)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break # gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    break # gameQuit()
                elif event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    pygame.mouse.set_visible(False)
                    gamePaused = False
        clock.tick(FPS)

# game over window


def gameOver(side):
    pygame.mixer.Sound.play(cheerSound)
    pygame.mouse.set_visible(True)
    displayMsg("Game Over", BLACK, -150, "large")
    displayMsg(side.title() + " won!", BLACK, -50)
    displayMsg("Do you want to play again with the computer?", BLACK, -20)
    # check response
    gameStart = False
    while not gameStart:
        # display bottons
        displayButton(
            "Rematch",
            [WIDTH/2-50-200, 2*HEIGHT/3-25, 100, 50], GREEN, DARK_GREEN, action=gameLoop)
        displayButton(
            "Quit", [WIDTH/2-50+200, 2*HEIGHT/3-25, 100, 50], RED, DARK_RED, action=gameQuit)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break # gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    gameLoop()
                elif event.key == pygame.K_q:
                    break # gameQuit()
        clock.tick(FPS)

# main loop of the game


def gameLoop():
    cdata = [int(line.replace('\n', '')) for line in data['crazy_spin_data'].split('\n')[:6]]

    # initiate using settings
    pygame.mouse.set_visible(False)
    DISPLAY.blit(backgroundImg, [0, 0])
    displayMsg("Initiating...", BLACK, -250, "large")
    displayMsg("Please wait for a while.", RED, -160)
    leftPadUp, leftPadDown, rightPadUp, rightPadDown = cdata[:4]
    backgroundMusicOn, soundEffectOn = cdata[4:]
    if not backgroundMusicOn:
        pygame.mixer.music.pause()

    # initiate loop condition variables
    gameExit = False
    leftScore = 0
    rightScore = 0
    edgeBounce = 0

    # initiate pad variables
    leftPadX = 0
    leftPadY = int((HEIGHT - pad_length) / 2)
    leftPadMove = 0
    leftPadLength = pad_length
    rightPadX = WIDTH - pad_width
    rightPadY = int((HEIGHT - pad_length) / 2)
    rightPadMove = 0
    rightPadLength = pad_length
    # leftPadLength = HEIGHT # test left side full-length pad

    # initiate ball variables
    serveSide = random.choice(["left", "right"])
    ballX, ballY, ballDir, ballSpeed, ballSpin = ballReset(serveSide)

    # play-time loop
    while not gameExit:
        # control the pads
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == leftPadUp:
                    leftPadMove -= pad_speed
                elif event.key == leftPadDown:
                    leftPadMove += pad_speed
                elif event.key == pygame.K_p:
                    gamePause()
            elif event.type == pygame.KEYUP:
                if event.key == leftPadUp:
                    leftPadMove += pad_speed
                elif event.key == leftPadDown:
                    leftPadMove -= pad_speed

        # computer intelligence
        if not dumb():
            if ballY - ball_size <= rightPadY:
                rightPadMove = -pad_speed
            elif ballY >= rightPadY + pad_length:
                rightPadMove = pad_speed
            else:
                rightPadMove = 0

        # ball right and left edge and pad bounce
        if ballX <= pad_width:
            ballSpin *= -1
            edgeBounce = 0
            if (ballY + ball_size < leftPadY or
                    ballY > leftPadY + leftPadLength):
                pygame.display.flip()
                if soundEffectOn:
                    pygame.mixer.Sound.play(whistleSound)
                serveSide = "left"
                ballX, ballY, ballDir, ballSpeed, ballSpin = ballReset(
                    serveSide)
                leftPadY, rightPadY = padReset()
                rightScore += 1
            else:
                if soundEffectOn:
                    pygame.mixer.Sound.play(padBounceSound)
                ballSpin += leftPadMove / pad_speed
                ballDir = y_reflect(ballDir)
                ballSpeed *= ball_speed_rate
        elif ballX >= WIDTH - pad_width - ball_size:
            ballSpin *= -1
            edgeBounce = 0
            if (ballY + ball_size < rightPadY or
                    ballY > rightPadY + rightPadLength):
                if soundEffectOn:
                    pygame.mixer.Sound.play(whistleSound)
                serveSide = "right"
                ballX, ballY, ballDir, ballSpeed, ballSpin = ballReset(
                    serveSide)
                leftPadY, rightPadY = padReset()
                leftScore += 1
            else:
                if soundEffectOn:
                    pygame.mixer.Sound.play(padBounceSound)
                ballSpin += rightPadMove / pad_speed
                ballDir = y_reflect(ballDir)
                ballSpeed *= ball_speed_rate

        # ball upper and lower edge bounce
        if ballY <= 0 or ballY >= HEIGHT - ball_size:
            if soundEffectOn:
                pygame.mixer.Sound.play(edgeBounceSound)
            edgeBounce += 1
            ballDir = x_reflect(ballDir)

        # ball spin and move ball
        ballDir += ballSpin * ball_spin_effect
        ballSpin *= 1 - ball_spin_fade
        ballX += int(math.cos(math.radians(ballDir)) * ballSpeed)
        ballY += int(math.sin(math.radians(ballDir)) * ballSpeed)

        # move pads
        leftPadY += leftPadMove
        rightPadY += rightPadMove

        # pad hit edge
        if leftPadY < 0:
            leftPadY = 0
        elif leftPadY > HEIGHT - leftPadLength:
            leftPadY = HEIGHT - leftPadLength
        if rightPadY < 0:
            rightPadY = 0
        elif rightPadY > HEIGHT - rightPadLength:
            rightPadY = HEIGHT - rightPadLength

        # ball over move rewind
        if ballY <= 0:
            ballX = hit_point(ballX, ballY, ballDir, hit_y=0)
            ballY = 0
        elif ballY >= HEIGHT - ball_size:
            ballX = hit_point(
                ballX, ballY, ballDir, hit_y=HEIGHT - ball_size)
            ballY = HEIGHT - ball_size
        if ballX <= pad_width:
            ballX = pad_width
            ballY = hit_point(ballX, ballY, ballDir, hit_x=pad_width)
        elif ballX >= WIDTH - pad_width - ball_size:
            ballX = WIDTH - pad_width - ball_size
            ballY = hit_point(
                ballX,
                ballY, ballDir, hit_x=WIDTH - pad_width - ball_size)

        # display game objects
        displayBackground()
        displayDetail(leftScore, rightScore, edgeBounce)
        displayPad(leftPadX, leftPadY, leftPadLength)
        displayPad(rightPadX, rightPadY, rightPadLength)
        displayBall(ballX, ballY)
        pygame.display.flip()

        # edge bounce limit check
        if edgeBounce >= edge_bounce_limit:
            edgeBounce = 0
            ballX, ballY, ballDir, ballSpeed, ballSpin = ballReset(serveSide)
            leftPadY, rightPadY = padReset()

        # win condition check
        if leftScore >= win_condition:
            gameOver("player")
        elif rightScore >= win_condition:
            gameOver("computer")

        # frames per second
        clock.tick(FPS)

    # out of loop quit game
    pass # gameQuit()

# combo quit

def gameQuit():
    raise KeyboardInterrupt
# def break # gameQuit():
#     pygame.mixer.music.pause()
#     pygame.mixer.stop()
#     pygame.quit()
#     quit()

# game exception page


def gameExcept():
    DISPLAY.fill(WHITE)
    displayMsg("Ops!", RED, -90, "large")
    displayMsg("An unexpected error occurs!", BLACK, -10)
    displayMsg("Press any key or close button to quit.", BLACK, 30)
    pygame.display.flip()
    # game over waiting response
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                break # gameQuit()
        clock.tick(FPS)


# if __name__ == "__main__":
#     try:
gameInit()
# except SystemExit:
#     pass
# except:
#     gameExcept()
