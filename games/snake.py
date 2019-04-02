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

    snake_head = [340, 0]
    snake_pos = numpy.array([[40, 0], [140, 0], [240, 0], [340, 0]])
    direction = 'right'

    while True:
        clock.tick(2)
        get_input()

        if direction == 'right':
            snake_head[0] += 100

        snake_pos = numpy.append(snake_pos, [snake_head], axis=0)
        print(snake_pos)


        GameObj.family.draw(DISPLAY) # draw sprites
        pygame.display.update()  # update
        # This should be the last thing in the loop

main()
