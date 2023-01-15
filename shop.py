from setting import *


class Upgrades:
    def __init__(self, clock):
        self.exit_dialog = None
        self.conf_dialog = None
        self.window_surface = pygame.display.set_mode((window.width, window.height))
        self.bg = pygame.transform.scale(load_image("texture/in_shop.png"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')
        self.score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width * 0.45, 5),
                                      (window.width * 0.9, window.height * 0.08)), text=f"СЧЕТ - {str(get_score())}$ ",
            manager=self.manager)

        self.label_1 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24), window.height // 2 * 1.1 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Скорость - " + str(get_digger_speed()), manager=self.manager)

        self.label_2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 1.64 - (window.width * 0.24), window.height // 2 * 1.1 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Удача - " + str(get_digger_luck()), manager=self.manager)

        self.label_3 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (window.width // 1.12 - (window.width * 0.24), window.height // 2 * 1.1 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Жизни - " + str(get_health()), manager=self.manager)

        self.buy_button_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24), window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_digger_speed() <= 3:
            self.buy_button_1.set_text("Максимум")
            self.buy_button_1.disable()

        self.buy_button_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.28,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_digger_luck() > 14:
            self.buy_button_2.set_text("Максимум")
            self.buy_button_2.disable()

        self.buy_button_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.56,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_health() > 6:
            self.buy_button_3.set_text("Максимум")
            self.buy_button_3.disable()

        self.speed = pygame.transform.scale(load_image("texture/heart.png"),
                                            (window.width * 0.12, window.width * 0.12))

        self.luck = pygame.transform.scale(load_image("texture/heart.png"),
                                           (window.width * 0.12, window.width * 0.12))

        self.health = pygame.transform.scale(load_image("texture/heart.png"),
                                             (window.width * 0.12, window.width * 0.12))

        size = window.width, window.height
        self.screen = pygame.display.set_mode(size)

    def cycle(self, clock):
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
                    if event.ui_element == self.buy_button_1:
                        if int(get_score()) < 14000:
                            self.buy_button_1.set_text("Не хватает средств")
                            self.buy_button_1.disable()
                        else:
                            if int(get_digger_speed()) >= 3:
                                change_speed(-1)
                                change_score(-14000)
                                self.score.set_text("СЧЕТ - " + str(get_score()) + "$")
                                self.label_1.set_text("Скорость - " + str(get_digger_speed()))
                            else:
                                self.buy_button_1.set_text("Максимум")
                                self.buy_button_1.disable()
                    if event.ui_element == self.buy_button_2:
                        if int(get_score()) < 2000:
                            self.buy_button_2.set_text("Не хватает средств")
                            self.buy_button_2.disable()
                        else:
                            if int(get_digger_luck()) < 15:
                                change_luck(1)
                                change_score(-2000)
                                self.score.set_text("СЧЕТ - " + str(get_score()) + "$")
                                self.label_2.set_text("Удача - " + str(get_digger_luck()))
                            else:
                                self.buy_button_2.set_text("Максимум")
                                self.buy_button_2.disable()
                    if event.ui_element == self.buy_button_3:
                        if int(get_score()) < 8000:
                            self.buy_button_1.set_text("Не хватает средств")
                            self.buy_button_1.disable()
                        else:
                            if int(get_health()) < 7:
                                change_health(1)
                                change_score(-8000)
                                self.score.set_text("СЧЕТ - " + str(get_score()) + "$")
                                self.label_3.set_text("Жизни - " + str(get_health()))
                            else:
                                self.buy_button_3.set_text("Максимум")
                                self.buy_button_3.disable()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((window.width // 2, window.height // 2),
                                             (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Вернуться назад?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.exit_dialog:
                        terminate()
                    if event.ui_element == self.conf_dialog:
                        return 1
            time_delta = clock.tick(FPS) / 1000.0
            self.window_surface.blit(self.bg, (0, 0))
            self.screen.blit(self.speed, (window.width // 6.44, window.height // 3 * 0.8))
            self.screen.blit(self.luck, (window.width // 2.3, window.height // 3 * 0.8))
            self.screen.blit(self.health, (window.width // 1.4, window.height // 3 * 0.8))
            self.manager.update(time_delta=time_delta)
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()


class Mines:
    def __init__(self, clock):
        self.exit_dialog = None
        self.conf_dialog = None
        self.window_surface = pygame.display.set_mode((window.width, window.height))
        self.bg = pygame.transform.scale(load_image("texture/in_shop.png"), (window.width, window.height))
        self.manager = pygame_gui.UIManager((window.width, window.height))
        self.manager.get_theme().load_theme('theme.json')
        self.score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width * 0.45, 5),
                                      (window.width * 0.9, window.height * 0.08)), text=f"СЧЕТ - {str(get_score())}$ ",
            manager=self.manager)

        self.buy_button_1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24), window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_current_level() >= 1 or get_score():
            self.buy_button_1.disable()

        self.buy_button_2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.28,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_current_level() >= 2:
            self.buy_button_2.disable()

        self.buy_button_3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 3 - (window.width * 0.24) + window.width * 0.56,
                 window.height * 2 // 3 - (window.height * 0.05)),
                (window.width * 0.25, window.height * 0.1)),
            text="Купить", manager=self.manager)
        if get_current_level() == 3:
            self.buy_button_3.disable()

        self.mine_1 = pygame.transform.scale(load_image("texture/dirt1.png"),
                                             (window.width * 0.15, window.width * 0.15))

        self.mine_2 = pygame.transform.scale(load_image("texture/rock.png"),
                                             (window.width * 0.15, window.width * 0.15))

        self.mine_3 = pygame.transform.scale(load_image("texture/rock_2.jpg"),
                                             (window.width * 0.15, window.width * 0.15))

        size = window.width, window.height
        self.screen = pygame.display.set_mode(size)

    def cycle(self, clock):
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
                    if event.ui_element == self.buy_button_1:
                        self.buy_button_1.disable()
                    if event.ui_element == self.buy_button_2:
                        self.buy_button_2.disable()
                    if event.ui_element == self.buy_button_3:
                        self.buy_button_3.disable()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((window.width // 2, window.height // 2),
                                             (300, 300)),
                            manager=self.manager,
                            window_title="Подтверждение",
                            action_long_desc="Вернуться назад?",
                            action_short_name="Да",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.exit_dialog:
                        terminate()
                    if event.ui_element == self.conf_dialog:
                        return 1
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
        self.score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width * 0.45, 5),
                                      (window.width * 0.9, window.height * 0.08)), text=f"СЧЕТ - {str(get_score())}$ ",
            manager=self.manager)

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
        while True:
            for event in pygame.event.get():
                self.manager.process_events(event)
                self.score.set_text("СЧЕТ - " + str(get_score()) + "$")
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
                        self.mine_button.visible = False
                        self.upgrade_button.visible = False
                        Mines(clock).cycle(clock)
                        self.mine_button.visible = True
                        self.upgrade_button.visible = True
                    if event.ui_element == self.upgrade_button:
                        Upgrades(clock).cycle(clock)
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
                        return "back"
            time_delta = clock.tick(FPS) / 1000.0
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()
