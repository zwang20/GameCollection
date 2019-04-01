from games.cge import *

pygame.display.set_caption('Snake')

DISPLAY.fill(WHITE)

# class Cell(GameObj):
#
#     family = pygame.sprite.Group()
#
#     WIDTH = 10
#     HEIGHT = 10
#
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.status = 0 # 0 = nothing, 1 = snake, 2 = food
#         self.image = pygame.Surface(WIDTH, HEIGHT)
#         self.image.fill(WHITE)
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (self.x, self.y)
#         Cell.family.add(self)
#
#     def change_status(self, new_status):
#         self.status = new_status
#
#     def update(self):
#         if self.status == 0:
#             self.image.fill(WHITE)
#         if self.status == 1:
#             self.image.fill(BLACK)
#         if self.status == 2:
#             self.image.fill(RED)

# WIDTH = 1280
# HEIGHT = 800

# [40, 140, 240, 340, 440, 540, 640, 740, 840, 940, 1040, 1140]

def main():
    while True:
        get_input()


        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop
