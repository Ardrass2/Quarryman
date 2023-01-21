import pygame_gui

from data.moduls.function import *
from data.moduls.setting import window, FPS


class Start_Window:
    def __init__(self, clock):
        self.window_surface = pygame.display.set_mode((window.width, window.height), window.fullscreen)
        self.background = pygame.transform.scale(load_image("texture/cave.jpg"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.25), window.height // 2 - (window.height * 0.05)),
                (window.width * 0.5, window.height * 0.1)),
            text="Начать игру", manager=self.manager)
        self.setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.25),
                 window.height // 2 - (window.height * 0.05) + window.height * 0.1),
                (window.width * 0.5, window.height * 0.1)),
            text="Настройки", manager=self.manager)
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width // 2 - (window.width * 0.25),
                                       window.height // 2 - (window.height * 0.05) - window.height * 0.1),
                                      (window.width * 0.5, window.height * 0.1)), text="КОПАТЕЛЬ", manager=self.manager)
        self.next_window = self.main_cycle(clock)

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
                        self.confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((250, 250), (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Вы уверены, что хотите выйти?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        return "game"
                    if event.ui_element == self.setting_button:
                        return "setting"
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.confirm_dialog:
                        terminate()
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()