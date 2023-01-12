import pygame_gui

from setting import *


mine_sprites = 0
mine_sprite = None


class Mines:
    def __init__(self, clock):
        self.exit_dialog = None
        self.confirm_dialog = None
        self.window_surface = pygame.display.set_mode((window.width, window.height))
        self.bg = pygame.transform.scale(load_image("texture/in_shop.png"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')

        self.buy_button_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24), window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)

        self.buy_button_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.28,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)

        self.buy_button_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.56,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)

        self.mine_1 = pygame.transform.scale(load_image("texture/dirt1.png"),
                                             (window.width * 0.15, window.width * 0.15))

        self.mine_2 = pygame.transform.scale(load_image("texture/rock.png"),
                                             (window.width * 0.15, window.width * 0.15))

        self.mine_3 = pygame.transform.scale(load_image("texture/rock_2.jpg"),
                                             (window.width * 0.15, window.width * 0.15))

        size = window.width, window.height
        self.screen = pygame.display.set_mode(size)
        self.cycle(clock)

    def cycle(self, clock):
        while True:
            global mine_sprites
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((window.width * 0.4, window.height * 0.3),
                                         (window.width // 2, window.height // 2)),
                        manager=self.manager,
                        window_title="Подтверждение",
                        action_long_desc="Вы уверены, что хотите выйти?",
                        action_short_name="Да",
                        blocking=True)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.buy_button_1:
                        self.buy_button_1.disable()
                    if event.ui_element == self.buy_button_2:
                        self.buy_button_2.disable()
                        mine_sprites = 1
                    if event.ui_element == self.buy_button_3:
                        self.buy_button_3.disable()
                        mine_sprites = 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((window.width // 2, window.height // 2),
                                             (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Вы точно все купили?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.exit_dialog:
                        terminate()
                    if event.ui_element == self.confirm_dialog:
                        return mine_sprites
            time_delta = clock.tick(FPS) / 1000.0
            self.window_surface.blit(self.bg, (0, 0))
            self.screen.blit(self.mine_1, (window.width // 11, window.height // 3))
            self.screen.blit(self.mine_2, (window.width // 2.68, window.height // 3))
            self.screen.blit(self.mine_3, (window.width // 1.53, window.height // 3))
            self.manager.update(time_delta=time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()


class Inside_Shop:
    def __init__(self, clock):
        self.confirm_dialog = None
        self.exit_dialog = None
        self.window_surface = pygame.display.set_mode((window.width, window.height))
        self.bg = pygame.transform.scale(load_image("texture/in_shop.png"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')
        self.mine_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.25), window.height // 2 - (window.height * 0.05)),
                (window.width * 0.5, window.height * 0.1)),
            text="Шахты", manager=self.manager)
        self.upgrade_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.25),
                 window.height // 2 - (window.height * 0.05) + window.height * 0.1),
                (window.width * 0.5, window.height * 0.1)),
            text="Улучшения", manager=self.manager)
        self.cycle(clock)

    def cycle(self, clock):
        global mine_sprite
        while True:
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((window.width * 0.4, window.height * 0.3),
                                         (window.width // 2, window.height // 2)),
                        manager=self.manager,
                        window_title="Подтверждение",
                        action_long_desc="Вы уверены, что хотите выйти?",
                        action_short_name="Да",
                        blocking=True)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.mine_button:
                        self.mine_button.kill()
                        self.upgrade_button.kill()
                        mine_sprite = Mines(clock).cycle(clock)
                    if event.ui_element == self.upgrade_button:
                        self.upgrade_button.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((window.width // 2, window.height // 2),
                                             (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Вы точно все купили?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.exit_dialog:
                        terminate()
                    if event.ui_element == self.confirm_dialog:
                        return mine_sprite
            time_delta = clock.tick(FPS) / 1000.0
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()
