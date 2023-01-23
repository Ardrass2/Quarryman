from data.moduls.function import *
from data.moduls.setting import window, FPS


class Start_Window:
    def __init__(self, clock):
        self.confirm_dialog = None
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
        self.instruct_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (window.width // 2 - (window.width * 0.25),
                 window.height // 2 - (window.height * 0.05) + window.height * 0.2),
                (window.width * 0.5, window.height * 0.1)),
            text="Инструкция", manager=self.manager)
        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((window.width // 2 - (window.width * 0.25),
                                       window.height // 2 - (window.height * 0.05) - window.height * 0.1),
                                      (window.width * 0.5, window.height * 0.1)), text="КОПАТЕЛЬ", manager=self.manager)
        self.corp = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, window.height * 0.05), (window.width * 0.4, window.height * 0.05)),
            text="by Eugene Bychkov and Vladimir Vasilchenko", manager=self.manager,
            object_id=pygame_gui.core.ObjectID(object_id='#team_text'))
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
                    if event.ui_element == self.instruct_button:
                        pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((0, 0), (window.width, window.height)),
                            manager=self.manager,
                            window_title="Инструкция",
                            action_long_desc="Данная игра создана Евгением Бычковым и Владимиром Васильченко\n"
                                             " Управление:\n"
                                             "'A' - Идти влево/ломать блок слева\n"
                                             "'S' - Копать вниз\n"
                                             "'D' - Идти вправо/ломать блок справа\n"
                                             " В меню настроек вы можете поменять основные параметры игры:\n"
                                             "1. Тип экрана - меняет отображение экрана\n"
                                             "2. Разрешение - меняет разрешенение экрана\n"
                                             "3. Громкость музыки/звуков - меняет громкость музыки/звуков\n"
                                             " Для входа в шахту или в магазин нужно подойти к спрайту того или другого"
                                             " и нажать 'E'\n"
                                             " Покупки в магазине осуществляются кнопками.\n В разделе 'Шахты' можно"
                                             " приобрести стилистическое оформление вашей шахты. За каждую шахту игрок"
                                             " получает бонус ввиде удвоенной награды за сундук.\n "
                                             "В разделе 'Улучшения' Вы приобритаете улучшения на своего персонажа:\n"
                                             "1. Скорость - ускоряет персонажа (максимальный уровень - 4)\n"
                                             "2. Удача - позволяет минимизировать шанс появления огня \n"
                                             "3. Жизнь - за каждый дополнительный уровень добавляется 1 сердечко\n"
                                             " В шахте ваша цель состоит в добыче конкретной награды. При входе в шахту"
                                             " Вам открывается диалоговое окно с Вашей целью. При достижение цели Вы "
                                             "завершаете уровень и на Ваш игровой счет начисляется сумма равная"
                                             " добытой. При ломании блоков из них с шансом "
                                             f"{round(1 / get_digger_luck(), 3) * 100}% появляется огонь, который при"
                                             f" соприкосновение с персонажем снимает 1 единицу жизни.",
                            action_short_name="Ок",
                            blocking=True)
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == self.confirm_dialog:
                        terminate()
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()
