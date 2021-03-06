import pygame
import sys
import random

width = 300
height = 300
screen = pygame.display.set_mode([width, height])

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
ORANGE_RED = (255, 69, 0)
SNAKE_GREEN = (127, 255, 0)

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


# -----------------------------------------------------------------------------------------------------------------------
#  Parameters which will initialize the game#
move_x_change = 0
move_y_change = 0
head = pygame.Rect(100, 100, 10, 10)
# initialize default direction
direction = 0
f = Fruit()

prevX = 0
prevY = 0  # previous position of tongue
tail_length = 0

previousX = 0
previousY = 0

# initializing score
score = 0

body_list = []  # list of objects, type body -  using to draw body parts

# game over variable initialization
game_over = False
# starting game logic
pygame.init()
# declaring game font and its size
font = pygame.font.Font(None, 36)

# create background/surface where whole game is printed
background = pygame.Surface(screen.get_size())

# Caption
pygame.display.set_caption('Snake game by JK')

# Initialize Clock to limit speed
clock = pygame.time.Clock()

# using to check what to show game/menu
game_on = True

# initializing variable which will be used to end the game
exit_game = False

# whole game basing on the endless while loop
while not exit_game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    if game_on:
        # setting background
        screen.fill(WHITE)
        # slowing down loop and so goes snake
        pygame.time.wait(60)

        # setting fps , 60 fps refresh rate
        clock.tick(60)

        key = pygame.key.get_pressed()
        # managing action for pressing the key
        if key[pygame.K_LEFT]:
            # if before pressed key was right dont turn back
            if direction == 4:
                pass
            # variable which will help recognize the actual direction of snake
            else:
                direction = 1
                move_x_change = 0  # snake can't speed up
                move_x_change -= 10
                move_y_change = 0
        elif key[pygame.K_DOWN]:
            # if key up before key down ->if player wants to turn back
            if direction == 3:
                pass
            else:
                direction = 2
                move_y_change = 0  # snake can't speed up
                move_y_change += 10
                move_x_change = 0
        elif key[pygame.K_UP]:
            if direction == 2:
                pass
            else:
                direction = 3
                move_y_change = 0
                move_y_change -= 10
                move_x_change = 0
        elif key[pygame.K_RIGHT]:
            if direction == 1:
                pass
            else:
                direction = 4
                move_x_change = 0
                move_x_change += 10
                move_y_change = 0

        # keeping snake going forward
        head.x += move_x_change
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

        # 'head' contains x and y of head and its size
        pygame.draw.rect(screen, RED, head)

        # first part of body
        b = Body(prevX, prevY)
        if tail_length >= 1:
            # using previousX and Y to print other parts of snake body
            previousX = b.bodyX
            previousY = b.bodyY
            pygame.draw.rect(screen, SNAKE_GREEN, b.bod)

        # Here is first fruit which appears at the start of the game
        pygame.draw.rect(screen, GREEN, f.fru)

        # if snake eats food
        if f.positionX == head.x and f.positionY == head.y:
            del f
            f = Fruit()
            pygame.draw.rect(screen, GREEN, f.fru)  # drawing actual fruit position
            tail_length += 1  # counting how much body elements to print

            if not game_over:
                score += 5

        if tail_length >= 2:
            body_list.append(Body(previousX, previousY))  # first time he will get prev and prevy
            if len(body_list) > tail_length:
                del body_list[0]  # without this, snake would leave a path behind

        body_list_length = len(body_list)

        # printing the rest of the body
        for i in range(0, body_list_length):
            pygame.draw.rect(screen, SNAKE_GREEN, body_list[i].bod)
            if head.x == body_list[i].bodyX and head.y == body_list[i].bodyY:
                game_over = True

        # checking if head didnt crash into first part of the body of snake (only if snake is moving -> direction!=0)
        if head.x == b.bodyX and head.y == b.bodyY and direction != 0:
            print(head.x, head.y, b.bodyX, b.bodyY)
            game_over = True

    if game_over:
        game_on = False
        screen.fill(GREEN)

        text = font.render("Game Over!", True, BLACK)
        text_position = text.get_rect(centerx=background.get_width() / 2)
        text_position.top = 200
        screen.blit(text, text_position)
        score_show = font.render("Score:" + str(score), True, WHITE)
        score_position = score_show.get_rect(centerx =background.get_width()/2)
        score_position.top = background.get_height()/2
        screen.blit(score_show, score_position)

    if not game_over:
        score_show = font.render("Score:" + str(score), True, ORANGE_RED)
        score_position = score_show.get_rect(topleft=(0, 0))
        screen.blit(score_show, score_position)

    pygame.display.flip()
    prevX = head.x
    prevY = head.y
