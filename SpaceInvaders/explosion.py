import pygame
import settings


class Explosion:
    def __init__(self, pos_x, pos_y):
        self.image = pygame.image.load('images/explode.png')
        self.pos_x, self.pos_y = pos_x, pos_y
        self.frame_x, self.frame_y = 3, 3
        self.sprite_size = 32

    def draw(self, screen):
        screen.blit(self.image,
                    [self.pos_x * self.sprite_size + settings.x_offset,
                     self.pos_y * self.sprite_size + settings.y_offset,
                     self.sprite_size, self.sprite_size],
                    (self.frame_x * self.sprite_size, self.frame_y * self.sprite_size, self.sprite_size, self.sprite_size))
        self.frame_x -= 1
        if self.frame_x < 0:
            self.frame_x = 3
            self.frame_y -= 1
