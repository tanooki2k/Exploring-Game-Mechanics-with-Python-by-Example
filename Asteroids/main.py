import pygame
import random
from pygame import Vector2
from pygame.transform import rotozoom
from pygame.mixer import Sound


asteroid_images = ['images/asteroid1.png', 'images/asteroid2.png', 'images/asteroid3.png']


def asteroids_respawn():
    ast = []
    while len(ast) < 10:
        pos_x, pos_y = (random.randint(0, screen.get_width()),
                        random.randint(0, screen.get_height()))
        if abs(screen.get_width() / 2 - pos_x) >= 150 and abs(screen.get_height() / 2 - pos_y) >= 150:
            asteroid_position = (pos_x, pos_y)
            ast.append(Asteroid((asteroid_position[0], asteroid_position[1]), 0))
    return ast


def wrap_position(position):
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)


def blit_rotated(position, velocity, image):
    angle = velocity.angle_to(Vector2(0, -((velocity.x ** 2) + (velocity.y ** 2)) ** 0.5))
    rotated_surface = rotozoom(image, angle, 1.0)
    rotated_surface_size = Vector2(rotated_surface.get_size())
    blit_position = position - rotated_surface_size / 2
    screen.blit(rotated_surface, blit_position)


class Ship:
    def __init__(self, position):
        self.position = Vector2(position)
        self.image = pygame.image.load('images/ship.png')
        self.forward = Vector2(0, -1)
        self.can_shoot = 0
        self.bullets = []
        self.drift = Vector2(0, 0)
        self.shoot = Sound('sounds/shoot.wav')

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            self.position += self.forward
            self.drift = (self.drift + self.forward) / 1.75
        if key_pressed[pygame.K_LEFT]:
            self.forward = self.forward.rotate(-1)
        if key_pressed[pygame.K_RIGHT]:
            self.forward = self.forward.rotate(1)
        if key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            self.bullets.append(Bullet(self.position, self.forward * 10))
            self.can_shoot = 500
            self.shoot.play()

        self.position += self.drift

        if self.can_shoot > 0:
            self.can_shoot -= clock.get_time()
        else:
            self.can_shoot = 0

    def draw(self):
        self.position = wrap_position(self.position)
        blit_rotated(self.position, self.forward, self.image)


class Bullet:
    def __init__(self, position, velocity):
        self.position = Vector2(position)
        self.forward = Vector2(velocity)

    def update(self):
        self.position += self.forward

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), [self.position.x, self.position.y, 5, 5])


class Asteroid:
    def __init__(self, position, size):
        self.position = Vector2(position)
        self.velocity = Vector2(0, 0)
        while self.velocity == (0, 0):
            self.velocity = Vector2(random.randint(-3, 3), random.randint(-3, 3))
        self.image = pygame.image.load(asteroid_images[size])
        self.size = size
        self.radius = self.image.get_width() / 2
        self.explode = Sound('./sounds/explode.ogg')

    def update(self):
        self.position += self.velocity

    def draw(self):
        self.position = wrap_position(self.position)
        blit_rotated(self.position, self.velocity, self.image)

    def hit(self, position):
        if self.position.distance_to(position) <= self.radius:
            self.explode.play()
            return True
        return False


pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Asteroids")
ship = Ship((screen.get_width() / 2, screen.get_height() / 2))
asteroids = asteroids_respawn()
background = pygame.image.load('images/space.png')
out_of_bounds = [-150, -150, screen.get_width() + 150, screen.get_height() + 150]
clock = pygame.time.Clock()
game_over = False

font = pygame.font.Font('fonts/Alien.ttf', 80)
text_gap = 100
text_loser = font.render("You Lost!", True, (255, 255, 255))
text_winner = font.render("You Won!", True, (255, 255, 255))
text_restart = font.render('Press "Enter"', True, (255, 255, 255))
text_loser_position = ((screen.get_width() - text_loser.get_width()) / 2,
                       (screen.get_height() - (text_loser.get_height() + text_restart.get_height() + text_gap)) / 2)
text_winner_position = ((screen.get_width() - text_winner.get_width()) / 2,
                        (screen.get_height() - (
                                text_winner.get_height() + text_restart.get_height() + text_gap)) / 2)
text_restart_position = ((screen.get_width() - text_restart.get_width()) / 2,
                         (screen.get_height() + text_loser.get_height() + text_gap - text_restart.get_height()) / 2)

while not game_over:
    clock.tick(55)
    dead_bullets = []
    dead_asteroids = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(background, (0, 0))

    if ship is None:
        key = pygame.key.get_pressed()
        screen.blit(text_loser, text_loser_position)
        screen.blit(text_restart, text_restart_position)
        if key[pygame.K_RETURN]:
            ship = Ship((screen.get_width() / 2, screen.get_height() / 2))
            asteroids = asteroids_respawn()
        pygame.display.update()
        continue

    for a in asteroids:
        a.update()
        a.draw()

        if a.hit(ship.position):
            if not dead_asteroids.__contains__(a):
                dead_asteroids.append(a)
            ship = None
            break

    if ship is None:
        continue

    for b in ship.bullets:
        b.update()
        b.draw()

        if (b.position.x < out_of_bounds[0]) or (b.position.x > out_of_bounds[2]) or (
                b.position.y < out_of_bounds[1]) or (b.position.y > out_of_bounds[3]):
            if not dead_bullets.__contains__(b):
                dead_bullets.append(b)

        for a in asteroids:
            if a.hit(b.position):
                if not dead_asteroids.__contains__(a):
                    dead_asteroids.append(a)
                if not dead_bullets.__contains__(b):
                    dead_bullets.append(b)

    for a in dead_asteroids:
        if a.size != 2:
            for i in range(2):
                asteroids.append(Asteroid(a.position, a.size + 1))
        asteroids.remove(a)

    for b in dead_bullets:
        ship.bullets.remove(b)

    if len(asteroids) == 0:
        screen.blit(text_winner, text_winner_position)
        pygame.display.update()
        continue

    ship.update()
    ship.draw()

    pygame.display.update()

pygame.quit()
