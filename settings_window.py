import pygame_gui

from setting import *


class Settings_Window:
    def __init__(self, clock, music):

        self.music = music
        self.screen = pygame.display.set_mode((width, height))
        self.bg = pygame.transform.scale(load_image("texture/sett_bg.jpg"), (width, height))
        self.manager = pygame_gui.UIManager((width, height))
        self.manager.get_theme().load_theme('theme.json')
        self.sound_value = int(sound_volume * 100)
        self.music_value = int(music_volume * 100)

        self.selection_volume = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((width * 0.35, height * 0.4),
                                      (width * 0.5, height * 0.081)),
            start_value=sound_volume * 100, value_range=(0, 100), manager=self.manager)

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width * 0.25, height * 0.075),
                                      (width * 0.5, height * 0.1)), text="Настройки", manager=self.manager)

        self.label_window = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width // 2 - (width * 0.541), height - (height * 0.71)),
                                      (width * 0.5, height * 0.1)), text="Тип окна", manager=self.manager)

        self.label_volume = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width // 2 - (width * 0.58), height - (height * 0.61)),
                                      (width * 0.5, height * 0.1)), text="Звуки", manager=self.manager)

        self.label_music = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((width // 2 - (width * 0.56), height - (height * 0.51)),
                                      (width * 0.5, height * 0.1)), text="Музыка", manager=self.manager)

        self.selection_resolution = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((width // 2 - (width * 0.15), height - (height * 0.7)),
                                      (width * 0.5, height * 0.081)), options_list=['В окне', 'Полный экран'],
            starting_option='Полный экран', manager=self.manager)

        self.selection_volume_music = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((width // 2 - (width * 0.15), height - (height * 0.5)),
                                      (width * 0.5, height * 0.081)),
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
                        change_music_value(self.music_value)
                        change_sound_value(self.sound_value)
                        return "back"
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.selection_volume_music:
                        self.music_value = int(event.value)
                        self.music.change_volume(event.value / 100)
                    if event.ui_element == self.selection_volume:
                        self.sound_value = int(event.value)
                    if event.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
                        if event.ui_element == self.selection_resolution:
                            pygame.display.set_mode()
            self.manager.update(time_delta=time_delta)
            self.screen.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()
            pygame.display.flip()
