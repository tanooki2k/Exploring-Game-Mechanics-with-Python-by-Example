import pygame


class MainMenu:
    def __init__(self, screen):
        self.font = pygame.font.Font('fonts/Alien.ttf', 80)
        self.font2 = pygame.font.Font('fonts/Alien.ttf', 40)
        self.title = self.font.render("Alien Invasion!", True, (255, 255, 255))
        self.press_text = self.font2.render('Press "Enter"', True, (255, 255, 255))
        self.text_gap = 10
        self.title_position = ((screen.get_width() - self.title.get_width()) / 2,
                               (screen.get_height() - (self.title.get_height() + self.text_gap + self.press_text.get_height())) / 2)
        self.press_text_position = ((screen.get_width() - self.press_text.get_width()) / 2,
                                    self.title_position[1] + self.title.get_height() + self.text_gap)
        self.press_text_frames = 6
        self.press_text_wait = 0
        self.game_play_scene = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.game_play_scene
        return self

    def draw(self, screen):
        screen.blit(self.title, self.title_position)

        self.press_text_wait += 1
        if self.press_text_wait <= self.press_text_frames:
            screen.blit(self.press_text, self.press_text_position)
        elif self.press_text_wait == (self.press_text_frames - 1) * 2:
            self.press_text_wait = 0
