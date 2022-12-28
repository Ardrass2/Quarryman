import pygame_gui

from function import *
from setting import *


class Settings_Window:
    def __init__(self, clock, music):

        self.music = music
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg = pygame.transform.scale(load_image("texture/sett_bg.jpg"), (WIDTH, HEIGHT))
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.manager.get_theme().load_theme('theme.json')

        self.selection_volume = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH * 0.35, HEIGHT * 0.4),
                                      (WIDTH * 0.5, HEIGHT * 0.081)),
            start_value=50, value_range=(0, 100), manager=self.manager)

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH * 0.25, HEIGHT * 0.075),
                                      (WIDTH * 0.5, HEIGHT * 0.1)), text="Настройки", manager=self.manager)

        self.label_window = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.541), HEIGHT - (HEIGHT * 0.71)),
                                      (WIDTH * 0.5, HEIGHT * 0.1)), text="Тип окна", manager=self.manager)

        self.label_volume = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.58), HEIGHT - (HEIGHT * 0.61)),
                                      (WIDTH * 0.5, HEIGHT * 0.1)), text="Звуки", manager=self.manager)

        self.label_music = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.56), HEIGHT - (HEIGHT * 0.51)),
                                      (WIDTH * 0.5, HEIGHT * 0.1)), text="Музыка", manager=self.manager)

        self.selection_resolution = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.15), HEIGHT - (HEIGHT * 0.7)),
                                      (WIDTH * 0.5, HEIGHT * 0.081)), options_list=['В окне', 'Полный экран'],
            starting_option='Полный экран', manager=self.manager)

        self.selection_volume_music = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH // 2 - (WIDTH * 0.15), HEIGHT - (HEIGHT * 0.5)),
                                      (WIDTH * 0.5, HEIGHT * 0.081)),
            start_value=(self.music.value * 100), value_range=(0, 100), manager=self.manager)
        self.back = self.main_cycle(clock)

    def main_cycle(self, clock):
        while True:
            time_delta = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.selection_volume_music:
                        self.music.change_volume(event.value / 100)
                        print(MUSIC_VOLUME)
                    if event.ui_element == self.selection_volume:
                        pass
                if event.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
                    if event.ui_element == self.selection_resolution:
                        pygame.display.set_mode()
            self.manager.update(time_delta=time_delta)
            self.screen.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()
            pygame.display.flip()
