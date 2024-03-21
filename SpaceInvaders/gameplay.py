import pygame
import random
import settings
from player import Player
from alien import Alien
from alien_bullet import Alien_Bullet
from explosion import Explosion
from wall import Wall


class Gameplay:
    def __init__(self, screen):
        self.font = pygame.font.Font('fonts/Alien.ttf', 80)
        self.title = self.font.render('Game Over', True, (255, 255, 255))
        self.title_position = ((screen.get_width() - self.title.get_width()) / 2,
                               (screen.get_height() - self.title.get_height()) / 2)
        self.title_won = self.font.render('You Won!', True, (255, 255, 255))
        self.title_won_position = ((screen.get_width() - self.title_won.get_width()) / 2,
                                   (screen.get_height() - self.title_won.get_height()) / 2)

        self.button_text_colour = (255, 255, 255)
        self.button_font = pygame.font.SysFont('Arial', 20)
        self.button_text = self.button_font.render('Back', True, self.button_text_colour)

        self.button_colour = (0, 0, 175)
        self.button_over_colour = (255, 50, 50)
        self.button_width = self.button_text.get_width() + 10
        self.button_height = self.button_text.get_height() + 15
        self.button_x, self.back_button_y = screen.get_width() - (self.button_width + 10), 0
        self.button_rect = [self.button_x, self.back_button_y, self.button_width, self.button_height]

        self.mouse_x, self.mouse_y = (0, 0)
        self.main_menu = None
        self.player = Player(screen.get_height() - 100, screen)
        self.explosions = []

        self.aliens = []
        self.aliens_rows = 5
        self.aliens_cols = 15
        for x in range(self.aliens_cols):
            self.list = []
            for y in range(self.aliens_rows):
                self.list.append(Alien(x, y, random.randint(0, 1)))
            self.aliens.append(self.list)
        self.left_border = 50
        self.right_border = screen.get_width() - self.left_border
        self.dx = 1.03
        self.dy = 20
        self.direction = self.dx
        self.dv_x = 1.03
        self.alien_can_shoot = random.randint(0, len(self.aliens))
        self.alien_cooldown = 0
        self.bullet_wait_time = 40

        wall_pos_x = (self.right_border - settings.wall_size * len(settings.wall_sprite[0]) - self.left_border) / 3
        self.wall_position = [(self.left_border + n * wall_pos_x, screen.get_height() - 200) for n in range(4)]
        for pos in self.wall_position:
            for y in range(len(settings.wall_sprite)):
                for x in range(len(settings.wall_sprite[y])):
                    if settings.wall_sprite[y][x] == 1:
                        settings.wall.append(Wall(pos, (x, y)))

        self.screen = screen

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.pos
                if (self.button_x <= self.mouse_x <= self.button_x + self.button_width and
                        self.back_button_y <= self.mouse_y <= self.back_button_y + self.button_height):
                    self.reset()
                    return self.main_menu
            if event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            if event.type == pygame.KEYDOWN:
                if (settings.lose == 1 or settings.win == 1) and event.key == pygame.K_RETURN:
                    self.reset()

        self.player.update()

        dead_player_bullets = []
        if self.player.bullets != [] and self.aliens != []:
            for b in self.player.bullets:
                found = False
                for x in self.aliens:
                    for a in pygame.sprite.spritecollide(b, x, False):
                        self.explosions.append(Explosion(a.pos_x, a.pos_y))
                        x.remove(a)
                        a.kill()
                        self.dx *= self.dv_x
                        found = True
                if found or b.pos_y + b.image.get_height() < 0:
                    dead_player_bullets.append(b)
        for b in dead_player_bullets:
            self.player.bullets.remove(b)
            b.kill()

        dead_alien_bullets = []
        for b in settings.alien_bullets:
            found = False
            for w in pygame.sprite.spritecollide(b, settings.wall, False):
                settings.wall.remove(w)
                w.kill()
                found = True
            if found:
                dead_alien_bullets.append(b)

        for b in dead_alien_bullets:
            settings.alien_bullets.remove(b)
            b.kill()

        return self

    def draw(self, screen):
        if (self.button_x <= self.mouse_x <= self.button_x + self.button_width and
                self.back_button_y <= self.mouse_y <= self.back_button_y + self.button_height):
            pygame.draw.rect(screen, self.button_over_colour, self.button_rect)
        else:
            pygame.draw.rect(screen, self.button_colour, self.button_rect)
        screen.blit(self.button_text, (
            self.button_x + (self.button_width - self.button_text.get_width()) / 2,
            self.back_button_y + (self.button_height - self.button_text.get_height()) / 2))

        if settings.lives <= 0 or settings.lose == 1:
            screen.blit(self.title, self.title_position)
            settings.lose = 1
            return self
        elif len(self.aliens) <= 0:
            screen.blit(self.title_won, self.title_won_position)
            settings.win = 1
            return self

        for x in self.aliens:
            for y in x:
                y.draw(screen)
        self.aliens = [col for col in self.aliens if len(col) != 0]

        for w in settings.wall:
            w.draw(screen)

        self.player.draw(screen)

        self.alien_cooldown += 1
        if self.alien_cooldown >= self.bullet_wait_time and self.alien_can_shoot < len(self.aliens):
            settings.alien_bullets.append(Alien_Bullet(
                (self.aliens[self.alien_can_shoot][-1].pos_x * self.aliens[0][0].sprite_size + settings.x_offset,
                 self.aliens[self.alien_can_shoot][-1].pos_y * self.aliens[0][0].sprite_size + settings.y_offset),
                self.aliens[0][0].sprite_size))
            self.alien_cooldown = 0
        self.alien_can_shoot = random.randint(0, len(self.aliens))

        dead_bullets = []
        if settings.alien_bullets:
            for b in settings.alien_bullets:
                if b.pos_y > screen.get_height():
                    dead_bullets.append(b)
                b.draw(screen)

        for b in dead_bullets:
            settings.alien_bullets.remove(b)

        if self.direction > 0:
            self.direction = self.dx
        elif self.direction < 0:
            self.direction = -self.dx

        update_y = False
        if len(self.aliens) > 0 and (settings.x_offset + self.aliens[-1][-1].pos_x * 32) > self.right_border:
            self.direction *= -1
            update_y = True
            settings.x_offset = self.right_border - self.aliens[-1][-1].pos_x * 32
        if 0 < len(self.aliens) and (settings.x_offset + self.aliens[0][0].pos_x * 32) < self.left_border:
            self.direction *= -1
            update_y = True
            settings.x_offset = self.left_border - self.aliens[0][0].pos_x * 32

        settings.x_offset += self.direction
        if update_y:
            settings.y_offset += self.dy

        dead_explosions = []
        for e in self.explosions:
            e.draw(screen)
            if e.frame_y < 0:
                dead_explosions.append(e)

        for e in dead_explosions:
            self.explosions.remove(e)

    def reset(self):
        if settings.win == 1:
            self.bullet_wait_time *= 9/10
            self.dx = self.dv_x
            self.dv_x += 0.0005
            settings.alien_bullet_speed *= 1.04
        if settings.lose == 1:
            self.bullet_wait_time = 40
            self.dx = 1.03
            self.dv_x = 1.03
            settings.alien_bullet_speed = 8
        self.player = Player(self.screen.get_height() - 100, self.screen)
        self.aliens = []
        self.aliens_rows = 5
        self.aliens_cols = 15
        self.alien_can_shoot = random.randint(0, len(self.aliens))
        self.alien_cooldown = 0
        settings.win = 0
        settings.lose = 0
        settings.lives = 3
        settings.x_offset = 50
        settings.y_offset = 50
        settings.alien_bullets = []
        self.explosions = []
        for x in range(self.aliens_cols):
            self.list = []
            for y in range(self.aliens_rows):
                self.list.append(Alien(x, y, random.randint(0, 1)))
            self.aliens.append(self.list)
        settings.wall = []
        for pos in self.wall_position:
            for y in range(len(settings.wall_sprite)):
                for x in range(len(settings.wall_sprite[y])):
                    if settings.wall_sprite[y][x] == 1:
                        settings.wall.append(Wall(pos, (x, y)))
