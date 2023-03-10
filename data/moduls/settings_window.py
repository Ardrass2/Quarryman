import pygame
import pygame_gui

from data.moduls.setting import *


class Settings_Window:
    def __init__(self, clock, music):
        self.back_dialog = None
        self.confirm_dialog = None
        self.music = music
        self.screen = pygame.display.set_mode((window.width, window.height), window.fullscreen)
        self.sound_value = int(sound_volume * 100)
        self.music_value = int(music_volume * 100)
        self.full_screen = ""
        self.__init_elements()
        self.back = self.main_cycle(clock)

    def __init_elements(self):
        self.bg = pygame.transform.scale(load_image("texture/sett_bg.jpg"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width * 0.25, window.height * 0.075),
                                      (window.width * 0.5, window.height * 0.1)), text="Настройки",
            manager=self.manager)

        self.mode_select_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.541), window.height - (window.height * 0.71)),
                (window.width * 0.5, window.height * 0.1)), text="Тип окна", manager=self.manager)

        self.size_select_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.58), window.height - (window.height * 0.61)),
                (window.width * 0.5, window.height * 0.1)), text="Разрешение", manager=self.manager)
        self.label_sound = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.56), window.height - (window.height * 0.51)),
                (window.width * 0.5, window.height * 0.1)), text="Звуки", manager=self.manager)

        self.label_music = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.56), window.height - (window.height * 0.41)),
                (window.width * 0.5, window.height * 0.1)), text="Музыка", manager=self.manager)
        if window.fullscreen == pygame.SCALED:
            self.full_screen = "В окне"
        elif window.fullscreen == pygame.FULLSCREEN:
            self.full_screen = "Полный экран"
        self.select_display_mode = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.15), window.height - (window.height * 0.7)),
                (window.width * 0.5, window.height * 0.081)), options_list=['В окне', 'Полный экран'],
            starting_option=self.full_screen, manager=self.manager)

        self.select_display_size = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.15), window.height - (window.height * 0.6)),
                (window.width * 0.5, window.height * 0.081)),
            options_list=['1280x720', "1280x1024", "1440x900", "1600x900", "1920x1080"],
            starting_option=f"{window.width}x{window.height}", manager=self.manager)

        self.selection_volume = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((window.width * 0.35, window.height - (window.height * 0.5)),
                                      (window.width * 0.5, window.height * 0.081)),
            start_value=sound_volume * 100, value_range=(0, 100), manager=self.manager)

        self.selection_volume_music = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.15), window.height - (window.height * 0.4)),
                (window.width * 0.5, window.height * 0.081)),
            start_value=(self.music.value * 100), value_range=(0, 100), manager=self.manager)

    def main_cycle(self, clock):
        while True:
            time_delta = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 250), (300, 300)),
                        manager=self.manager,
                        window_title="Подтверждение",
                        action_long_desc="Вы уверены, что хотите выйти?",
                        action_short_name="Да",
                        blocking=True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((250, 250), (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Перейти в главное меню?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.confirm_dialog:
                        terminate()
                    if event.ui_element == self.back_dialog:
                        change_music_value(self.music_value)
                        change_sound_value(self.sound_value)
                        return "back"
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.selection_volume_music:
                        self.music_value = int(event.value)
                        self.music.change_volume(event.value / 100)
                    if event.ui_element == self.selection_volume:
                        self.sound_value = int(event.value)
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.select_display_mode:
                        if event.text == "Полный экран":
                            self.full_screen = event.text
                            self.screen = pygame.display.set_mode(update_window_size(), pygame.FULLSCREEN)
                            change_display_mode(1)
                        else:
                            self.full_screen = event.text
                            self.screen = pygame.display.set_mode(update_window_size(), pygame.SCALED)
                            change_display_mode(0)
                        window.update_display_mode()
                    if event.ui_element == self.select_display_size:
                        change_window_size((int(event.text[:event.text.index("x")]),
                                            int(event.text[event.text.index("x") + 1:])))
                        if self.full_screen == "Полный экран":
                            self.screen = pygame.display.set_mode(update_window_size(), pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode(update_window_size(), pygame.SCALED)

                        window.update_window_size()
                        window.update_tile_size()
                        self.__init_elements()
            self.manager.update(time_delta=time_delta)
            self.screen.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()
            pygame.display.flip()
