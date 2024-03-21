import pygame
import random

blocks = [
    [[1, 4, 7], [3, 4, 5]],  # Straight
    [[1, 3, 4, 5, 7]],  # Cross
    [[0, 1, 4, 5], [1, 3, 4, 6]],  # Two on two 1
    [[1, 2, 3, 4], [0, 3, 4, 7]],  # Two on two 3
    [[0, 1, 3, 6], [0, 1, 2, 5], [2, 5, 7, 8], [3, 6, 7, 8]],  # L1
    [[1, 2, 5, 8], [5, 6, 7, 8], [0, 3, 6, 7], [0, 1, 2, 3]],  # L2
    [[4, 6, 7, 8], [0, 3, 4, 6], [0, 1, 2, 4], [2, 4, 5, 8]],  # One on three
    [[0, 1, 3, 4]]  # Square
]

colours = [
    (0, 119, 211),
    (254, 72, 25),
    (254, 251, 52),
    (83, 218, 63),
    (1, 237, 250),
    (221, 10, 178),
    (234, 20, 28)
]


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(blocks) - 1)
        self.rotation = 0
        self.colour = colours[random.randint(0, len(colours) - 1)]

    def shape(self):
        return blocks[self.type][self.rotation]


def rotate():
    last_rotation = block.rotation
    block.rotation = (block.rotation + 1) % len(blocks[block.type])
    can_rotate = True
    for y in range(3):
        for x in range(3):
            if 3 * y + x in block.shape():
                if collides():
                    can_rotate = False

    if not can_rotate:
        block.rotation = last_rotation


def draw_block():
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                pygame.draw.rect(screen, block.colour,
                                 [(x + block.x) * grid_size + x_gap + 1,
                                  (y + block.y) * grid_size + y_gap + 1,
                                  grid_size - 2, grid_size - 2])


def draw_grid(rows, cols, size, gap):
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(screen, (100, 100, 100),
                             [x * size + gap[0], y * size + gap[1], size, size], 1)
            if game_board[y][x] != (0, 0, 0):
                pygame.draw.rect(screen, game_board[y][x],
                                 [x * grid_size + gap[0] + 1, y * grid_size + gap[1] + 1, grid_size - 2, grid_size - 2])


def collides(nx=0, ny=0):
    collision = False
    for y in range(3):
        for x in range(3):
            if 3 * y + x in block.shape():
                # Axis Y:
                if (block.y + y + ny < 0) or (block.y + y + ny > grid_rows - 1):
                    collision = True
                    break
                if (block.x + x + nx < 0) or (block.x + x + nx > grid_cols - 1):
                    collision = True
                    break
                elif game_board[block.y + y + ny][block.x + x + nx] != (0, 0, 0):
                    collision = True
                    break
    return collision


def drop_block():
    can_drop = True
    for y in range(3):
        for x in range(3):
            if 3 * y + x in block.shape():
                if collides(0, 1):
                    can_drop = False
    if can_drop:
        block.y += 1
    else:
        for y in range(3):
            for x in range(3):
                if 3 * y + x in block.shape():
                    game_board[block.y + y][block.x + x] = block.colour
    return can_drop


def side_move(dx):
    can_move = True
    for y in range(3):
        for x in range(3):
            if 3 * y + x in block.shape():
                if collides(dx):
                    can_move = False
    if can_move:
        block.x += dx
    else:
        drop_block()


def find_lines():
    lines = 0
    for y in range(grid_rows):
        empty = 0
        for x in range(grid_cols):
            if game_board[y][x] != (0, 0, 0):
                empty += 1
        if empty == grid_cols:
            lines += 1
            for y2 in range(y, 1, -1):
                for x2 in range(grid_cols):
                    game_board[y2][x2] = game_board[y2 - 1][x2]
    return lines


pygame.init()
screen = pygame.display.set_mode((320, 600))
pygame.display.set_caption("Tetris")
grid_size = 30
grid_rows, grid_cols = screen.get_height() // grid_size, screen.get_width() // grid_size
x_gap, y_gap = (screen.get_width() - grid_cols * grid_size) / 2, (screen.get_height() - grid_rows * grid_size) / 2
block = Block(grid_cols // 2 - 1, 0)
clock = pygame.time.Clock()
fps_0, dfps = 2, 12
fps = fps_0
game_over = False
score = 0
font = pygame.font.SysFont('Arial', 25, True, False)
font2 = pygame.font.SysFont('Arial', 50, True, False)
finished_text = font2.render("Game Over", True, (255, 255, 255))
ftpos = [(screen.get_width() - finished_text.get_width()) / 2, (screen.get_height() - finished_text.get_height()) / 2]
game_finished = False

# Initialize game board
game_board = []
for i in range(grid_rows):
    new_col = []
    for j in range(grid_cols):
        new_col.append((0, 0, 0))
    game_board.append(new_col)

while not game_over:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN and not game_finished:
            if event.key == pygame.K_UP:
                rotate()
    fps = fps_0
    if event.type == pygame.KEYDOWN and not game_finished:
        if event.key == pygame.K_LEFT:
            side_move(-1)
            fps = dfps / 2
        if event.key == pygame.K_RIGHT:
            side_move(1)
            fps = dfps / 2
        if event.key == pygame.K_DOWN:
            fps = dfps
    screen.fill((0, 0, 0))
    draw_grid(grid_rows, grid_cols, grid_size, [x_gap, y_gap])
    if not game_finished:
        if block is not None:
            draw_block()
            if event.type != pygame.KEYDOWN or event.key == pygame.K_DOWN:
                if not drop_block():
                    score += find_lines()
                    block = Block(random.randint(4, grid_cols - 4), 0)
                    if collides():
                        game_finished = True
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, [0, 0])
    if game_finished:
        screen.blit(finished_text, ftpos)
    pygame.display.update()
pygame.quit()
