import os

import pygame
import pygame_gui

from setting import width, height, FPS
from function import *


class Start_Window:
    def __init__(self, clock):

        self.window_surface = pygame.display.set_mode((width, height))
        self.background = pygame.transform.scale(load_image("texture/cave.jpg"), (width, height))
        self.manager = pygame_gui.UIManager((width, height))
        self.manager.get_theme().load_theme('theme.json')
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 - (width * 0.25), height // 2 - (height * 0.05)),
                                      (width * 0.5, height * 0.1)),
            text="Начать игру", manager=self.manager)
        self.setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (width // 2 - (width * 0.25), height // 2 - (height * 0.05) + height * 0.1),
                (width * 0.5, height * 0.1)),
            text="Настройки", manager=self.manager)
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width // 2 - (width * 0.25), height // 2 - (height * 0.05) - height * 0.1),
                                      (width * 0.5, height * 0.1)), text="КОПАТЕЛЬ", manager=self.manager)
        self.next_window = self.main_cycle(clock)

    def main_cycle(self, clock):
        while True:
            time_delta = clock.tick(FPS) / 1000.0
            try_exit = ""
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        return "game"
                    if event.ui_element == self.setting_button:
                        return "setting"
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()
