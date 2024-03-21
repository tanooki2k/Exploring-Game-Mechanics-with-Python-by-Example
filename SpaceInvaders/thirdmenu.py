import pygame


class ThirdMenu:
    def __init__(self):
        self.font = pygame.font.Font('fonts/Alien.ttf', 80)
        self.start = self.font.render("Third Menu", True, (255, 255, 255))
        self.start_position = (20, 200)
        self.main_menu = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return self.main_menu
        return self

    def draw(self, screen):
        screen.blit(self.start, self.start_position)
