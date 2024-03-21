import pygame
import settings


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, square):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/green_pixel.png')
        self.pos_x, self.pos_y = pos[0] + settings.wall_size * square[0], pos[1] + settings.wall_size * square[1]
        self.color = (0, 255, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.rect.topleft = (self.pos_x, self.pos_y)
