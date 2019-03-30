from cge import *
from sge import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (204, 51, 0)
YELLOW = (255, 153, 0)
DARK_GREEN = (51, 204, 51)
GREEN = (0, 128, 0)
DARK_BLUE = (0, 102, 255)
GREY = (40, 40, 50)
BLUE = (0, 0, 128)

MUSIC = False

ground_height = 200

pygame.display.set_caption('Simple Shooter')

instruction_img = images['ss_instruction']
instruction_img = pygame.transform.scale(instruction_img, (WIDTH, HEIGHT))
rocket_img = images['rocket']
explosion_img = images['explosion']
shield_img = images['shield']
shield_img = pygame.transform.scale(shield_img, (80, 80))
init_img = images['ss_init']
init_img = pygame.transform.scale(init_img, (WIDTH, HEIGHT))
player_img = images['ss_robot']

laser_sound_1 = sounds['sfx_laser1']
laser_sound_2 = sounds['sfx_laser2']

pygame.mixer.music.stop()

if MUSIC:
    pygame.mixer.music.load(music['song_1.ogg'])
    pygame.mixer.music.queue(music['song_2.ogg'])
    pygame.mixer.music.queue(music['song_3.ogg'])
    pygame.mixer.music.play(-1)


class Bullet:
    width = 2
    length = 20
    speed = 8
    good = []
    bad = []

    def __init__(self, x, y, harmful=True):
        pygame.mixer.Sound.play(laser_sound_1) if random.randint(
            0, 1) == 0 else pygame.mixer.Sound.play(laser_sound_2)
        self.x = x
        self.y = y
        self.harmful = harmful
        if harmful:
            Bullet.bad.append(self)
            temp = -50
        else:
            Bullet.good.append(self)
            temp = 25
        sge_print(DISPLAY, 'Pew', x + temp, y, colour=WHITE)

    def move(self):
        self.x -= Bullet.speed if self.harmful else -Bullet.speed
        if self.x > WIDTH-25 or self.x < 0:
            self.despawn()

    def display(self):
        if self.harmful:
            sge_rect(
                DISPLAY, self.x, self.y, Bullet.length, Bullet.width, RED)
        else:
            sge_rect(
                DISPLAY,
                self.x, self.y, Bullet.length, Bullet.width, DARK_BLUE)

    def despawn(self):
        DISPLAY.blit(explosion_img, (self.x, self.y))
        if self.harmful:
            Bullet.bad.remove(self)
        else:
            Bullet.good.remove(self)


class Rocket:
    rockets = []
    speed = 6
    limit = 3

    def __init__(self):
        self.x = WIDTH
        if random.choice([True, False]):
            self.y = HEIGHT - ground_height + 1 - Player.height
        else:
            self.y = random.randint(0, HEIGHT - ground_height + 1 - Player.height)
        Rocket.rockets.append(self)

    def move(self):
        self.x -= Rocket.speed
        if self.x > WIDTH or self.x < 0:
            self.despawn()

    def display(self):
        DISPLAY.blit(rocket_img, (self.x, self.y))

    def despawn(self):
        DISPLAY.blit(explosion_img, (self.x, self.y))
        Rocket.rockets.remove(self)


class Player:
    width = 20
    height = 40
    score = 0
    speedx = 4
    speedy = 4

    def __init__(self):
        self.x = 0
        self.y = 0
        self.cooldown = 0
        self.health = 100

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y
        if self.x < 0:
            self.x = 0
        elif self.x > 300:
            self.x = 300
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - ground_height - Player.height:
            self.y = HEIGHT - ground_height - Player.height

    def chdir(self):
        self.movement = random.randint(50, 120)
        self.dir = random.choice(("left", "right", "up", "down"))

    def aimove(self):  # this now contains enemy ai
        if self.dir == "left":
            self.x -= self.speedx
        elif self.dir == "right":
            self.x += self.speedx
        elif self.dir == "up":
            self.y -= self.speedy
        elif self.dir == "down":
            self.y += self.speedy
        if self.x < 0:
            self.x = 0
            self.chdir()
        elif self.x > 300:
            self.x = 300
            self.chdir()
        if self.y < 0:
            self.y = 0
            self.chdir()
        elif self.y > HEIGHT - ground_height - Player.height:
            self.y = HEIGHT - ground_height - Player.height
            self.chdir()
        if self.dir in ("up", "down"):
            self.movement -= self.speedy
        elif self.dir in ("left", "right"):
            self.movement -= self.speedx
        if self.movement <= 0:
            self.chdir()

    def fire(self):
        if self.cooldown % 10 == 0:
            if self.cooldown < 90:

                Bullet(self.x + 20, self.y + 5, False)
                self.cooldown += 20

                Bullet(self.x + 20, self.y + 33, False)
                self.cooldown += 20

    def get_hit(self):  # checks if an enemy gets hit and respond accordingly
        for bullet in Bullet.bad:
            if self.x <= bullet.x <= self.x + Player.width:
                if self.y <= bullet.y <= self.y + Player.height:
                    bullet.despawn()
                    Player.score -= 10
                    self.health -= 10
        for rocket in Rocket.rockets:
            if self.x <= rocket.x <= self.x + Player.width:
                if self.y <= rocket.y <= self.y + Player.height:
                    rocket.despawn()
                    Player.score -= 50
                    self.health -= 50

    def renew(self):
        # cooldown recover
        if self.cooldown > 0:
            self.cooldown -= 1
        # gravity
        if self.y < HEIGHT - ground_height - Player.height:
            self.y += 1
        # score below 0
        if Player.score < 0:
            Player.score = 0

        if self.health <= 0:
            self.remove()

    def display(self):
        DISPLAY.blit(player_img, (self.x, self.y))
        # sge_rect(
        #     DISPLAY, self.x, self.y, Player.width, Player.height, WHITE)
        # sge_rect(
        #     DISPLAY, self.x + Player.width, self.y + 10, 5, 5, WHITE)


class Enemy:
    spawn_range = 500
    limit = 2
    width = 20
    height = 40
    family = []
    _difficulty = ("easy", "normal", "hard", 'hell')
    available = ("easy", "normal", "hard", 'hell')
    # available = Enemy._difficulty

    def __init__(self, difficulty=None):
        self.spawn()
        if difficulty is None:
            difficulty = random.choice(Enemy.available)
        if difficulty == "easy":
            self.speedx = 1
            self.speedy = random.randint(1, 2)
            self.fire_cooldown = 1
        elif difficulty == "normal":
            self.speedx = random.randint(2, 3)
            self.speedy = random.randint(2, 4)
            self.fire_cooldown = 0.5
        elif difficulty == "hard":
            self.speedx = random.randint(3, 4)
            self.speedy = random.randint(4, 7)
            self.fire_cooldown = 0.3
        elif difficulty == 'hell':
            self.speedx = random.randint(4, 5)
            self.speedy = random.randint(7, 10)
            self.fire_cooldown = 0.2
        elif difficulty == "dummy":
            self.speed = 0
            self.fire_cooldown = 99999
        self.difficulty = difficulty
        self.dir = 'up'
        self.movement = 50
        self.fire_timer = time.time()
        self.spawn_protect = time.time()
        Enemy.family.append(self)

    def spawn(self):
        self.x = random.randint(
            Enemy.spawn_range, WIDTH - Enemy.width - Bullet.length)
        self.y = random.randint(0, HEIGHT - ground_height - Enemy.height)

    def display(self):
        if self.difficulty == "easy":
            colour = DARK_GREEN
        elif self.difficulty == "normal":
            colour = YELLOW
        elif self.difficulty == "hard":
            colour = RED
        elif self.difficulty == 'hell':
            colour = BLACK
        elif self.difficulty == "dummy":
            colour = WHITE
        sge_rect(
            DISPLAY, self.x, self.y, Enemy.width, Enemy.height, colour)
        sge_rect(DISPLAY, self.x - 5, self.y + 10, 5, 5, colour)

    def chdir(self):
        self.movement = random.randint(50, 120)
        self.dir = random.choice(("left", "right", "up", "down"))

    def move(self):  # this now contains enemy ai
        if self.dir == "left":
            self.x -= self.speedx
        elif self.dir == "right":
            self.x += self.speedx
        elif self.dir == "up":
            self.y -= self.speedy
        elif self.dir == "down":
            self.y += self.speedy
        if self.x > WIDTH - Enemy.width:
            self.x = WIDTH - Enemy.width
            self.chdir()
        elif self.x < 500:
            self.x = 500
            self.chdir()
        if self.y < 0:
            self.y = 0
            self.chdir()
        elif self.y > HEIGHT - ground_height - Enemy.height:
            self.y = HEIGHT - ground_height - Enemy.height
            self.chdir()
        if self.dir in ("up", "down"):
            self.movement -= self.speedy
        elif self.dir in ("left", "right"):
            self.movement -= self.speedx
        if self.movement <= 0:
            self.chdir()

    def fire(self):
        if time.time() - self.fire_timer >= self.fire_cooldown:
            self.fire_timer = time.time()
            Bullet(self.x - 5, self.y + 7, True)

    def get_hit(self):  # checks if an enemy gets hit and respond accordingly
        for bullet in Bullet.good:
            if (self.x <= bullet.x <= self.x + Enemy.width and
                    self.y <= bullet.y <= self.y + Enemy.height):
                if time.time() - self.spawn_protect > 1:
                    self.despawn()
                    bullet.despawn()
                    if self.difficulty == "easy":
                        Player.score += 10
                    elif self.difficulty == "normal":
                        Player.score += 15
                    elif self.difficulty == "hard":
                        Player.score += 20
                    elif self.difficulty == 'hell':
                        Player.score += 30
                    player.health += 1
                    if player.health > 100:
                        player.health = 100
                else:
                    DISPLAY.blit(shield_img, (self.x - 30, self.y - 20))
                    bullet.despawn()

    def despawn(self):
        Enemy.family.remove(self)


# Weapons


def smart_spawn():
    # difficulty renew
    if Player.score <= 50:
        Enemy.limit = 2
        Enemy.available = Enemy._difficulty[:1]
    elif Player.score <= 100:
        Enemy.limit = 3
        Enemy.available = Enemy._difficulty[:2]
    elif Player.score <= 135:
        Enemy.limit = 4
        Enemy.available = Enemy._difficulty[:2]
    elif Player.score <= 150:
        Enemy.limit = 5
        Enemy.available = Enemy._difficulty[:3]
    else:
        Enemy.limit = 6
        Enemy.available = Enemy._difficulty[1:]

    while len(Enemy.family) < Enemy.limit:
        Enemy()
    if len(Rocket.rockets) < Rocket.limit:
        if random.randint(0, 60) == 0:
            Rocket()


def ss_init():
    timer = 0
    global player
    # TODO: complete this description
    ss_initial = True
    player = Player()
    player.chdir()
    while ss_initial:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_exit()
                elif event.key == pygame.K_SPACE:
                    ss_initial = False

        DISPLAY.fill(GREY)
        sge_rect(x=600, y=250, width=200, height=100, colour=YELLOW)
        start_but = sge_rect(x=200, y=250, width=200, height=100, colour=DARK_GREEN)
        sge_print(string='Start', x=200, y=250)
        sge_print(string='Help', x=600, y=250)

        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        ss_game_help_2 = False
        if 600 < mouse_pos[0] < 800 and 250 < mouse_pos[1] < 350:
            sge_rect(x=600, y=250, width=200, height=100, colour=DARK_YELLOW)
            sge_print(string='Help', x=600, y=250)
            if mouse_press[0] == True:
                ss_game_help_2 = True
        while ss_game_help_2:
            mouse_pos = pygame.mouse.get_pos()
            DISPLAY.blit(init_img, (0, 0))
            pygame.draw.rect(DISPLAY, DARK_GREEN, (WIDTH - 100, HEIGHT - 100 - 30, 100, 100))
            sge_print(string='Back', x=WIDTH - 100, y=HEIGHT - 100 - 30)
            mouse_press = pygame.mouse.get_pressed()
            if WIDTH - 100 < mouse_pos[0] < WIDTH and HEIGHT - 100 - 30 < mouse_pos[1] < HEIGHT - 30:
                pygame.draw.rect(DISPLAY, GREEN, (WIDTH - 100, HEIGHT - 100 - 30, 100, 100))
                sge_print(string='Back', x=WIDTH - 100, y=HEIGHT - 100 - 30)
                if mouse_press[0] == True:
                    ss_game_help_2 = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit()
                    elif event.key == pygame.K_SPACE:
                        ss_initial = False
            pygame.display.update()
        if start_but.collidepoint(mouse_pos) and mouse_press[0]:
            ss_initial = False
        sge_rect(
            DISPLAY,
            0,
            HEIGHT - ground_height,
            WIDTH, ground_height, BLACK)
        smart_spawn()
        for enemy in Enemy.family:
            enemy.move()
            enemy.get_hit()
            enemy.fire()
            enemy.display()
        for bullet in Bullet.good + Bullet.bad:
            bullet.display()
        for bullet in Bullet.good + Bullet.bad:
            bullet.move()
        if timer >= 20:
            sge_print(
                string='A 2D shooting game consists of basic geometric shapes.',
                colour=WHITE)
            sge_print(
                string='Made by Michael with assistance form Edward',
                y=30, colour=WHITE)
            sge_print(
                string='To Quit Press Q',
                y=60, colour=WHITE)
        player.display()
        player.aimove()

        if 200 < mouse_pos[0] < 400 and 250 < mouse_pos[1] < 350:
            sge_rect(x=200, y=250, width=200, height=100, colour=GREEN)
            sge_print(string='Start', x=200, y=250)

        pygame.display.update()
        timer += 1


def ss_end():
    while True:
        if pygame.event.peek(pygame.QUIT):
            pygame.mixer.music.pause()
            pygame.mixer.stop()
            raise KeyboardInterrupt


def ss_settings():
    pass


def ss_pause():
    ss_pause = True
    while ss_pause:
        # sge_clear(DISPLAY)
        DISPLAY.blit(instruction_img, (0, 0))
        sge_print(string='Paused', colour=WHITE)
        sge_print(string='To unpause press keyboard "X"', y=30, colour=WHITE)
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            ss_pause = False
        for event in pygame.event.get():  # Input
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT:
                game_exit()


def ss():
    while True:

        ss_init()
        ss_run = True

        # player = Player()

        while ss_run:
            DISPLAY.fill(GREY)
            clock.tick(60)

            sge_rect(DISPLAY, 0, HEIGHT - ground_height,
                     WIDTH, ground_height, BLACK)  # Ground

            for event in pygame.event.get():  # Input
                if event.type == pygame.QUIT:
                    game_exit()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:  # Quit
                game_exit()
            if keys[pygame.K_w]:  # Up
                player.move(0, -6)
            if keys[pygame.K_d]:  # Right
                player.move(4, 0)
            if keys[pygame.K_a]:  # Left
                player.move(-4, 0)
            if keys[pygame.K_s]:  # Down
                player.move(0, 3)
            if keys[pygame.K_SPACE]:  # Fire
                player.fire()
            if keys[pygame.K_p]:  # Pause
                ss_pause()

            # CALCULATIONS
            for enemy in Enemy.family:
                enemy.move()
                enemy.get_hit()
                enemy.fire()

            for bullet in Bullet.good + Bullet.bad:
                bullet.move()

            player.get_hit()
            player.renew()

            smart_spawn()

            for enemy in Enemy.family:
                enemy.display()
            for bullet in Bullet.good + Bullet.bad:
                bullet.display()

            player.display()

            for rocket in Rocket.rockets:
                rocket.display()
                rocket.move()

            sge_rect(DISPLAY, WIDTH-100, HEIGHT-10, 100, 10, WHITE)
            sge_rect(DISPLAY, WIDTH-100, HEIGHT-10, player.cooldown, 10, RED)
            sge_print(DISPLAY, Player.score, colour=WHITE)

            sge_rect(DISPLAY, WIDTH-200, HEIGHT-10, 100, 10, WHITE)
            sge_rect(DISPLAY, WIDTH-200, HEIGHT-10, player.health, 10, DARK_BLUE)

            pygame.display.update()


def game_exit():
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    raise KeyboardInterrupt


while True:
    try:
        ss()
    except KeyboardInterrupt:
        pygame.mixer.music.pause()
        pygame.mixer.stop()
        raise KeyboardInterrupt
