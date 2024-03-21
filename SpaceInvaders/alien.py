import pygame
import settings


class Alien(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, alien_type):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.type = alien_type
        self.frame = 0
        self.image = pygame.image.load('images/aliens_sm.png')
        self.sprite_size = 32
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x * self.sprite_size + settings.x_offset,
                             self.pos_y * self.sprite_size + settings.y_offset)

    def draw(self, screen):
        self.rect.topleft = (self.pos_x * self.sprite_size + settings.x_offset,
                             self.pos_y * self.sprite_size + settings.y_offset)
        if (settings.x_offset // 10) % 2 == 0:
            self.frame = 1
        else:
            self.frame = 0
        screen.blit(self.image,
                    [self.pos_x * self.sprite_size + settings.x_offset,
                     self.pos_y * self.sprite_size + settings.y_offset,
                     self.sprite_size, self.sprite_size],
                    (self.frame * self.sprite_size, self.sprite_size * self.type, self.sprite_size, self.sprite_size))
        if self.pos_y * self.sprite_size + settings.y_offset >= 458:
            settings.lose = 1
