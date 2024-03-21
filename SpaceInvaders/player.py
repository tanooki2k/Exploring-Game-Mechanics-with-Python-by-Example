import pygame
from pygame.locals import *
from player_bullet import Player_Bullet
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/ship.png')
        self.pos_x, self.pos_y = ((screen.get_width() - self.image.get_width()) / 2, pos_y)
        self.bullets = []
        self.can_shoot = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

        self.lives_font = pygame.font.Font('fonts/Alien.ttf', 25)
        self.lives_text = self.lives_font.render("Lives: " + str(settings.lives), True, (255, 100, 100))
        self.lives_text_position = (10, 10)

    def update(self):
        self.lives_text = self.lives_font.render("Lives: " + str(settings.lives), True, (255, 100, 100))
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and self.pos_x + 3 < 750 - self.image.get_width() / 2:
            self.pos_x += 6
        elif keys[K_LEFT] and self.pos_x - 3 > 50 - self.image.get_width() / 2:
            self.pos_x -= 6
        self.rect.topleft = (self.pos_x, self.pos_y)
        if keys[K_SPACE] and self.can_shoot >= 0:
            self.bullets.append(
                Player_Bullet((self.pos_x, self.pos_y), (self.image.get_width(), self.image.get_height())))
            self.can_shoot = -15
        self.can_shoot += 1

        for a in pygame.sprite.spritecollide(self, settings.alien_bullets, False):
            settings.lives -= 1
            settings.alien_bullets.remove(a)
            a.kill()

        dead_player_bullets = []
        for b in self.bullets:
            found = False
            for w in pygame.sprite.spritecollide(b, settings.wall, False):
                settings.wall.remove(w)
                w.kill()
                found = True
            if found:
                dead_player_bullets.append(b)

        for b in dead_player_bullets:
            self.bullets.remove(b)
            b.kill()

    def draw(self, screen):
        screen.blit(self.lives_text, self.lives_text_position)
        for b in self.bullets:
            b.draw(screen)

        screen.blit(self.image, [self.pos_x, self.pos_y, self.image.get_width(), self.image.get_height()])
