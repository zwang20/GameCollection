import math
import os
import pygame
import random
import time

os.chdir(os.path.join(os.path.abspath(os.path.curdir), u'assets'))

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (185, 185, 185)
olivedrab = (51, 51, 0)
green = (0, 204, 0)
yellow = (255, 204, 0)
red = (255, 0, 0)
light_green = (0, 255, 0)
light_yellow = (255, 219, 77)
light_red = (255, 102, 102)
brown = (153, 102, 51)
blue = (51, 102, 255)
light_blue = (77, 166, 255)

smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 40)
largeFont = pygame.font.SysFont("comicsansms", 80)

display_width = 800
display_height = 600

# create display surface
gameDisplay = pygame.display.set_mode([display_width, display_height])

# name the window
pygame.display.set_caption("Pong PvP")

# set icon
iconImg = pygame.image.load("icon.png")
pygame.display.set_icon(iconImg)

# load background image
backgroundImg = pygame.image.load("background_image.png")
pygame.transform.scale(backgroundImg, [display_width, display_height])

# load sounds
padBounceSound = pygame.mixer.Sound("pad_bounce.wav")
edgeBounceSound = pygame.mixer.Sound("edge_bounce.wav")
cheerSound = pygame.mixer.Sound("cheer.wav")
whistleSound = pygame.mixer.Sound("whistle.wav")
backgroundMusic = pygame.mixer.music.load("background_music.wav")

clock = pygame.time.Clock()

# game wide constants
pad_length = int(display_height / 6)  # 100
pad_width = int(display_width / 45)  # 17
ball_size = int(display_height / 40)  # 15
effect_size = 30
pad_speed = int(display_height / 45)  # 13
ball_speed_init = int(display_height / 50)  # 12
ball_speed_rate = 1.05
ball_spin_effect = 1.1
ball_spin_fade = 0.008
edge_bounce_limit = 10
win_condition = 10

FPS = 45

# ball reflection lambdas


def x_reflect(x): return 360 - x


def y_reflect(x): return 180 - x

# create text objects


def text_objects(msg, color, size):
    if size == "small":
        screen_text = smallFont.render(msg, True, color)
    elif size == "medium":
        screen_text = medFont.render(msg, True, color)
    elif size == "large":
        screen_text = largeFont.render(msg, True, color)
    return screen_text, screen_text.get_rect()

# display mmessage


def displayMsg(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2, display_height / 2 + y_displace)
    gameDisplay.blit(textSurf, textRect)

# display score of players


def displayDetail(left_score, right_score, edge_bounce):
    scoreSurf, scoreRect = text_objects(
        str(left_score)+" : "+str(right_score), black, "small")
    scoreRect.center = (display_width / 2, 30)
    gameDisplay.blit(scoreSurf, scoreRect)
    if right_score != win_condition and left_score != win_condition:
        if right_score == win_condition - 1:
            msg = "Game Point"
            bounceSurf, bounceRect = text_objects(msg, black, "small")
            bounceRect.center = (display_width / 2 + 100, 30)
            gameDisplay.blit(bounceSurf, bounceRect)
        if left_score == win_condition - 1:
            msg = "Game Point"
            bounceSurf, bounceRect = text_objects(msg, black, "small")
            bounceRect.center = (display_width / 2 - 100, 30)
            gameDisplay.blit(bounceSurf, bounceRect)
    if edge_bounce >= edge_bounce_limit - 3:
        msg = "Ball respawn after "+str(
            edge_bounce_limit-edge_bounce)+" edge bounce"
        bounceSurf, bounceRect = text_objects(msg, black, "small")
        bounceRect.center = (display_width / 2, 60)
        gameDisplay.blit(bounceSurf, bounceRect)

# display text for buttons


def buttonText(msg, color, location, size="small"):
    button_x, button_y, button_width, button_height = location
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (
        (button_x + button_width/2), (button_y + button_height/2))
    gameDisplay.blit(textSurf, textRect)

# display responsive button


def displayButton(
        text,
        location, unfocus_color, focus_color, text_color=black, action=None):
    bX, bY, bWidth, bHeight = location
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if bX + bWidth > cursor[0] > bX and bY + bHeight > cursor[1] > bY:
        pygame.draw.rect(gameDisplay, focus_color, location)
        if click[0]:
            action()
    else:
        pygame.draw.rect(gameDisplay, unfocus_color, location)
    buttonText(text, text_color, location)


def displayBackground():
    gameDisplay.fill(white)
    gameDisplay.blit(backgroundImg, [0, 0])
    pygame.draw.rect(
        gameDisplay, light_blue, [0, 0, pad_width, display_height])
    pygame.draw.rect(
        gameDisplay,
        light_blue, [display_width - pad_width, 0, pad_width, display_height])

# display player pads


def displayPad(x, y, length):
    pygame.draw.rect(gameDisplay, black, [x, y, pad_width, length])

# display ball


def displayBall(x, y):
    pygame.draw.rect(gameDisplay, red, [x, y, ball_size, ball_size])

# reset ball position and variables


def ballReset(side):
    if side == "left":
        ball_dir = random.randint(130, 230)
        x_adjust = 0.3
        ball_x = int((display_width - ball_size) / 2 + display_width * 0.3)
        ball_y = int((display_height - ball_size) / 2)
        ball_speed = ball_speed_init
        ball_spin = 0
    elif side == "right":
        ball_dir = random.randint(-50, 50)
        ball_x = int((display_width - ball_size) / 2 - display_width * 0.3)
        ball_y = int((display_height - ball_size) / 2)
        ball_speed = ball_speed_init
        ball_spin = 0
    time.sleep(2)
    return ball_x, ball_y, ball_dir, ball_speed, ball_spin

# reset pad position and variables


def padReset():
    temp = int((display_height - pad_length) / 2)
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
        gameDisplay.blit(backgroundImg, [0, 0])
        displayMsg("Pong PvP", olivedrab, -170, "large")
        displayMsg(
            "Move the pads to bouce the ball and guard the goal", brown, -70)
        displayMsg("hit while moving you pad to add spin.", brown, -40)
        displayMsg("First one to 10 wins!", brown, -10)
        displayMsg("Player left defualt - W and S", brown, 20)
        displayMsg("Player right default - QUOTE and SLASH", brown, 50)

        # display bottons
        displayButton(
            "Play", [150, 400, 100, 50], green, light_green, action=gameLoop)
        displayButton(
            "Settings",
            [350, 400, 100, 50], yellow, light_yellow, action=gameSettings)
        displayButton(
            "Quit", [550, 400, 100, 50], red, light_red, action=gameQuit)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                elif event.key == pygame.K_s:
                    gameSettings()
                elif event.key == pygame.K_q:
                    gameQuit()
        clock.tick(FPS)

# game initiate window


def gameSettings():
    with open("settings.qgd", 'r') as f:
        data = [int(line.replace('\n', '')) for line in f.readlines()]
    # check response
    while True:
        # display title and instructions
        gameDisplay.blit(backgroundImg, [0, 0])
        displayMsg("Settings", olivedrab, -230, "large")
        displayMsg(
            "Please do not modify settings with text editor!", brown, -140)

        # display sound settings
        displayMsg("Game-time music", brown, -110)
        if data[4]:
            displayMsg("On [press B]", brown, -80)
        else:
            displayMsg("Off [Press B]", brown, -80)
        displayMsg("Sound effects", brown, -50)
        if data[5]:
            displayMsg("On [Press V]", brown, -20)
        else:
            displayMsg("Off [Press V]", brown, -20)

        # display key set settings
        cursor_x, cursor_y = pygame.mouse.get_pos()
        if cursor_x <= display_width/2:
            if cursor_y <= display_height/2:
                setKeyName = "Left Pad Up"
                setKeyNo = 0
            else:
                setKeyName = "Left Pad Down"
                setKeyNo = 1
        else:
            if cursor_y <= display_height/2:
                setKeyName = "Right Pad Up"
                setKeyNo = 2
            else:
                setKeyName = "Right Pad Down"
                setKeyNo = 3
        displayMsg(
            "Move\
             the cursor to quarters to change the pad or direction of key.",
            brown, 10)
        displayMsg("You can not use key that are pre-defined!", brown, 40)
        displayMsg("Set Key for: " + setKeyName, brown, 70)
        displayMsg(
            "Current Key: " + pygame.key.name(data[setKeyNo]), brown, 100)

        # back button
        click = pygame.mouse.get_pressed()
        if 350 + 100 > cursor_x > 350 and 480 + 50 > cursor_y > 480:
            pygame.draw.rect(gameDisplay, light_green, [350, 480, 100, 50])
            if click[0]:
                with open('settings.qgd', 'w') as f:
                    f.write('\n'.join(map(str, data)))
                return
        else:
            pygame.draw.rect(gameDisplay, green, [350, 480, 100, 50])
        buttonText("Back", black, [350, 480, 100, 50])

        # renew display
        pygame.display.flip()

        # check for key set
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('settings.qgd', 'w') as f:
                    f.write('\n'.join(map(str, data)))
                gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
                elif event.key == pygame.K_q:
                    with open('settings.qgd', 'w') as f:
                        f.write('\n'.join(map(str, data)))
                    gameQuit()
                elif event.key == pygame.K_b:
                    data[4] = 0 if data[4] else 1
                elif event.key == pygame.K_v:
                    data[5] = 0 if data[5] else 1
                elif event.key not in data:
                    data[setKeyNo] = event.key
        clock.tick(FPS)

# game pausing window


def gamePause():
    # stop music and sound effects
    pygame.mixer.music.pause()
    pygame.mixer.stop()

    pygame.mouse.set_visible(True)
    displayMsg("Paused", red, -100, "large")
    displayMsg("Don't want to have fun with your mates?", black, 25, "medium")
    pygame.display.flip()
    # wait for response
    gamePaused = True
    while gamePaused:
        cursor = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 200 + 100 > cursor[0] > 200 and 380 + 50 > cursor[1] > 380:
            pygame.draw.rect(gameDisplay, light_green, [200, 380, 100, 50])
            if click[0]:
                pygame.mouse.set_visible(False)
                return
        else:
            pygame.draw.rect(gameDisplay, green, [200, 380, 100, 50])
        buttonText("Continue", black, [200, 380, 100, 50])
        displayButton(
            "Quit", [500, 380, 100, 50], red, light_red, action=gameQuit)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameQuit()
                elif event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    pygame.mouse.set_visible(False)
                    gamePaused = False
        clock.tick(FPS)

# game over window


def gameOver(side):
    pygame.mixer.Sound.play(cheerSound)
    pygame.mouse.set_visible(True)
    displayMsg("Game Over", olivedrab, -150, "large")
    displayMsg(side.title() + " won!", brown, -50)
    displayMsg("Do you want to play again with your mate?", brown, -20)
    # check response
    gameStart = False
    while not gameStart:
        # display bottons
        displayButton(
            "Rematch",
            [250, 380, 100, 50], green, light_green, action=gameLoop)
        displayButton(
            "Quit", [450, 380, 100, 50], red, light_red, action=gameQuit)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    gameLoop()
                elif event.key == pygame.K_q:
                    gameQuit()
        clock.tick(FPS)

# main loop of the game


def gameLoop():
    with open("settings.qgd", 'r') as f:
        data = [int(line.replace('\n', '')) for line in f.readlines()]

    # initiate using settings
    pygame.mouse.set_visible(False)
    gameDisplay.blit(backgroundImg, [0, 0])
    displayMsg("Initiating...", black, -250, "large")
    displayMsg("Please wait for a while.", red, -160)
    leftPadUp, leftPadDown, rightPadUp, rightPadDown = data[:4]
    backgroundMusicOn, soundEffectOn = data[4:]
    if not backgroundMusicOn:
        pygame.mixer.music.pause()

    # initiate loop condition variables
    gameExit = False
    leftScore = 0
    rightScore = 0
    edgeBounce = 0

    # initiate pad variables
    leftPadX = 0
    leftPadY = int((display_height - pad_length) / 2)
    leftPadMove = 0
    leftPadLength = pad_length
    rightPadX = display_width - pad_width
    rightPadY = int((display_height - pad_length) / 2)
    rightPadMove = 0
    rightPadLength = pad_length
    # leftPadLength = display_height # test left side full-length pad

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
                elif event.key == rightPadUp:
                    rightPadMove -= pad_speed
                elif event.key == rightPadDown:
                    rightPadMove += pad_speed
                elif event.key == pygame.K_p:
                    gamePause()
            elif event.type == pygame.KEYUP:
                if event.key == leftPadUp:
                    leftPadMove += pad_speed
                elif event.key == leftPadDown:
                    leftPadMove -= pad_speed
                elif event.key == rightPadUp:
                    rightPadMove += pad_speed
                elif event.key == rightPadDown:
                    rightPadMove -= pad_speed

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
        elif ballX >= display_width - pad_width - ball_size:
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
        if ballY <= 0 or ballY >= display_height - ball_size:
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
        elif leftPadY > display_height - leftPadLength:
            leftPadY = display_height - leftPadLength
        if rightPadY < 0:
            rightPadY = 0
        elif rightPadY > display_height - rightPadLength:
            rightPadY = display_height - rightPadLength

        # ball over move rewind
        if ballY <= 0:
            ballX = hit_point(ballX, ballY, ballDir, hit_y=0)
            ballY = 0
        elif ballY >= display_height - ball_size:
            ballX = hit_point(
                ballX, ballY, ballDir, hit_y=display_height - ball_size)
            ballY = display_height - ball_size
        if ballX <= pad_width:
            ballX = pad_width
            ballY = hit_point(ballX, ballY, ballDir, hit_x=pad_width)
        elif ballX >= display_width - pad_width - ball_size:
            ballX = display_width - pad_width - ball_size
            ballY = hit_point(
                ballX,
                ballY, ballDir, hit_x=display_width - pad_width - ball_size)

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
            gameOver("left hand side")
        elif rightScore >= win_condition:
            gameOver("right hand side")

        # frames per second
        clock.tick(FPS)

    # out of loop quit game
    gameQuit()

# combo quit


def gameQuit():
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    pygame.quit()
    quit()

# game exception page


def gameExcept():
    gameDisplay.fill(white)
    displayMsg("Ops!", red, -90, "large")
    displayMsg("An unexpected error occurs!", black, -10)
    displayMsg("Press any key or close button to quit.", black, 30)
    pygame.display.flip()
    # game over waiting response
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                gameQuit()
        clock.tick(FPS)


if __name__ == "__main__":
    try:
        gameInit()
    except SystemExit:
        pass
    except:
        gameExcept()
