from engine.main import *

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
