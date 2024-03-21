import pygame


class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, player_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.pos_x, self.pos_y = pos[0] + (player_size[0] - self.image.get_width()) / 2, pos[1]
        self.dy = 20
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, screen):
        self.pos_y -= self.dy
        self.rect.topleft = (self.pos_x, self.pos_y)
        screen.blit(self.image, [self.pos_x, self.pos_y, self.image.get_width(), self.image.get_height()])
