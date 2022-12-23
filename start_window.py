import os

import pygame
import pygame_gui

from setting import WIDTH, HEIGHT, FPS


class Start_Window:
    def __init__(self, background, clock):

        self.window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.manager.get_theme().load_theme('theme.json')
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.25), HEIGHT // 2 - (HEIGHT * 0.05)),
                                      (WIDTH * 0.5, HEIGHT * 0.1)),
            text="Начать игру", manager=self.manager)
        self.setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (WIDTH // 2 - (WIDTH * 0.25), HEIGHT // 2 - (HEIGHT * 0.05) + HEIGHT * 0.1),
                (WIDTH * 0.5, HEIGHT * 0.1)),
            text="Настройки", manager=self.manager)
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.25), HEIGHT // 2 - (HEIGHT * 0.05) - HEIGHT * 0.1),
                                      (WIDTH * 0.5, HEIGHT * 0.1)), text="КОПАТЕЛЬ", manager=self.manager)
        self.next_window = self.main_cycle(clock)

    def main_cycle(self, clock):
        while True:
            time_delta = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.USEREVENT:
                    time_delta = clock.tick(60) / 1000.0
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.start_button:
                            return 1
                        if event.ui_element == self.setting_button:
                            return 2
                        self.manager.process_events(event)
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()
