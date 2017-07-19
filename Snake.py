import pygame
import sys
import random

width = 500
height = 500
screen = pygame.display.set_mode([width, height])

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

rows = height / 10  # using for making food only in y=10,20 ,...
cols = width / 10


class Fruit:
    fruX = 0
    fruY = 0

    def __init__(self):
        self.fruX = random.randint(1, rows - 1)
        self.fruY = random.randint(1, cols - 1)
        self.positionX = self.fruX * 10
        self.positionY = self.fruY * 10
        self.fru = pygame.Rect(self.positionX, self.positionY, 10, 10)


class Body:
    bodyX = 0
    bodyY = 0

    def __init__(self, x, y):
        self.bodyX = x
        self.bodyY = y
        self.bod = pygame.Rect(self.bodyX, self.bodyY, 10, 10)


pygame.init()

width = 500
height = 500

move_x_change = 0
move_y_change = 0
head = pygame.Rect(100, 100, 10, 10)

f = Fruit()

prevX = 0
prevY = 0  # previous position of tongue
tail_length = 0

previousX = 0
previousY = 0

body_list = []  # list of objects, type body -  using to draw body parts
list_ofX = []
list_ofy = []  # lists of coords x and y afterwards will compare them with x and y of existing snake parts

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill(WHITE)

    pygame.time.wait(60)
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        move_x_change = 0  # we dont want snake to speed up
        move_x_change -= 10
        move_y_change = 0
    elif key[pygame.K_DOWN]:
        move_y_change = 0  # we dont want snake to speed up
        move_y_change += 10
        move_x_change = 0
    elif key[pygame.K_UP]:
        move_y_change = 0
        move_y_change -= 10
        move_x_change = 0
    elif key[pygame.K_RIGHT]:
        move_x_change = 0
        move_x_change += 10
        move_y_change = 0
    head.x += move_x_change  # thanks to it our snake is keeping going forward
    head.y += move_y_change
    pygame.time.wait(5)
    if head.x >= width:
        head.x = 10
    if head.y >= height:
        head.y = 10
    if head.x <= 0:
        head.x = width
    if head.y <= 0:
        head.y = height

        # here should be a loop drawing body of snake!!!!!!!!!!!!

    pygame.draw.rect(screen, BLUE, head)  # 'head' contains x and y of head and size
    if tail_length >= 1:
        b = Body(prevX, prevY)  # first part of body
        previousX = b.bodyX
        previousY = b.bodyY
        pygame.draw.rect(screen, BLUE, b.bod)

    print(prevX, prevY)
    pygame.draw.rect(screen, GREEN, f.fru)

    if f.positionX == head.x and f.positionY == head.y:
        del f
        f = Fruit()
        pygame.draw.rect(screen, GREEN, f.fru)  # drawing actual fruit position
        tail_length += 1  # counting how much body elements to print

    if tail_length >= 2:
        body_list.append(Body(previousX, previousY))  # first time he will get prev and prevy
        if len(body_list) > tail_length:
            del body_list[0]    # without this, snake would leave a path behind

            # now we cant use prevY and prevX cause it only contains xy of head

    list_length = len(body_list)

    for i in range(0, list_length):
        pygame.draw.rect(screen, BLUE, body_list[i].bod)

    pygame.display.flip()
    prevX = head.x
    prevY = head.y
