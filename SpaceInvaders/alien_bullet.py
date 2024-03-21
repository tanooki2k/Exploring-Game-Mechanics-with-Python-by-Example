import pygame
import settings


class Alien_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/abullet.png')
        self.pos_x, self.pos_y = pos[0] + (enemy_size - self.image.get_width()) / 2, pos[1] + enemy_size
        self.dy = settings.alien_bullet_speed
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, screen):
        self.pos_y += self.dy
        self.rect.topleft = (self.pos_x, self.pos_y)
        screen.blit(self.image, [self.pos_x, self.pos_y, self.image.get_width(), self.image.get_height()])
        if self.pos_y > screen.get_height():
            del self
