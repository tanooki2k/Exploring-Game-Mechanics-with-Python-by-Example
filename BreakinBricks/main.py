import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("BreakinBricks")

# Bat
bat = pygame.image.load('images/paddle.png')
bat = bat.convert_alpha()
bat_rect = bat.get_rect()
bat_rect[0] = (screen.get_width() - bat_rect[2]) / 2
bat_rect[1] = screen.get_height() - 100
player_speed = 0.3

# Ball
ball = pygame.image.load('images/football.png')
ball = ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start = (bat_rect[0] + (bat_rect[2] - ball_rect[2]) / 2, bat_rect[1] - ball_rect[3])
ball_speed = (0.2, 0.2)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start
acceleration_ball = 1.01

# Bricks
brick = pygame.image.load('images/brick.png')
brick = brick.convert_alpha()
brick_rect = brick.get_rect()
bricks = []
brick_gap = 10
brick_rows = 5
bricks_cols = screen.get_width() // (brick_rect[2] + brick_gap)
side_gap = (brick_gap + screen.get_width() - (brick_rect[2] + brick_gap) * bricks_cols) / 2

for y in range(brick_rows):
    brickY = y * (brick_rect[3] + 5)
    for x in range(bricks_cols):
        brickX = x * (brick_rect[2] + brick_gap) + side_gap
        bricks.append((brickX, brickY))

clock = pygame.time.Clock()
x = bat_rect[0]
game_over = False

while not game_over:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            game_over = True

    dt = clock.tick(50)
    screen.fill((0, 0, 0))

    # Showing the brick
    for b in bricks:
        screen.blit(brick, b)

    # Player
    screen.blit(bat, bat_rect)
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        x -= player_speed * dt
        if x < 0:
            x = 0
    if keys[K_RIGHT]:
        x += player_speed * dt
        if x > screen.get_width() - bat_rect[2]:
            x = screen.get_width() - bat_rect[2]
    bat_rect[0] = x
    if keys[K_SPACE]:
        ball_served = True

    # Ball
    screen.blit(ball, ball_rect)
    if ball_served:
        ball_rect[0] += sx * dt
        ball_rect[1] += sy * dt
    else:
        ball_rect[0] = bat_rect[0] + (bat_rect[2] - ball_rect[2]) / 2
    # Ball's Hits
    # To bat
    if (bat_rect[0] - ball_rect[2] <= ball_rect[0] <= bat_rect[0] + bat_rect[2] and ball_rect[1] +
            ball_rect[3] >= bat_rect[1] and sy > 0):
        sy *= -1
        sx, sy = sx * acceleration_ball, sy * acceleration_ball  # Increase the difficult
        continue
    # Bricks
    delete_brick = None
    for b in bricks:
        bx, by = b
        if (bx + brick.get_width() >= ball_rect[0] >= bx - ball_rect[2] and by <= ball_rect[1]
                <= by + brick.get_height()):
            delete_brick = b
            # Calculating where ball will bounce
            if ball_rect[0] >= bx + 2:
                sx *= -1
            elif ball_rect[0] >= bx + brick.get_width() - 2:
                sx *= -1
            if ball_rect[1] <= by + 2:
                sy *= -1
            elif ball_rect[1] >= by + brick.get_height() - 2:
                sy *= -1
            break

    if delete_brick is not None:
        bricks.remove(delete_brick)

    # Top
    if ball_rect[1] <= 0:
        ball_rect[1] = 0
        sy *= -1
    # Down
    if ball_rect[1] >= screen.get_height() - ball_rect[3]:
        ball_rect.topleft = ball_start
        ball_served = False
        sx, sy = ball_speed
    # Left
    if ball_rect[0] <= 0:
        ball_rect[0] = 0
        sx *= -1
    # Right
    if ball_rect[0] >= screen.get_width() - ball_rect[2]:
        ball_rect[0] = screen.get_width() - ball_rect[2]
        sx *= -1
    pygame.display.update()
pygame.quit()
