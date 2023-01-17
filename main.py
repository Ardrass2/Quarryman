# Quarryman GAME
import pygame.sprite

from camera import *
from character import *
from fire import *
from first_location import *
from mining_location import *
from music_player import *
from setting import *
from settings_window import Settings_Window
from shop import Inside_Shop
from start_window import Start_Window

level_map = []


def start_mine():
    exit_dialog = None
    confirm_dialog = None
    ok_but = None
    level_look = get_level_look()
    digger = Miner(all_sprites, load_image("texture/miner.png"), 10, 5, level_map)
    bg = pygame.transform.scale(load_image("texture/cave_mining.jpg"), (window.width, window.height))
    hearts = [pygame.transform.scale(load_image("texture/heart.png"),
                                     (window.width * 0.04, window.height * 0.066)) for _ in range(get_health())]
    manager = pygame_gui.UIManager((window.width, window.height))
    manager.get_theme().load_theme('theme.json')
    scores = 0
    need_money = int(money_need())
    level = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((window.width * 0.35, 5), (window.width * 0.3, window.height * 0.08)),
        text=f"Уровень - {int(get_level())}", manager=manager)
    score = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((window.width * 0.45, 5),
                                  (window.width * 0.9, window.height * 0.08)), text=f"СЧЕТ - {str(scores)}$ ",
        manager=manager)
    s = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((window.width // 2, window.height // 2),
                         (300, 300)),
        manager=manager,
        window_title="БулюмБулюм",
        action_long_desc=f"Вы попали в шахту, ваша задача на сегодня накопать сокровищ на {need_money} $.",
        action_short_name="Ок",
        blocking=True)
    n_lines = number_of_line + 1
    camera = Camera()
    tiles_group.update()
    tiles_group.draw(screen)
    all_borders.update()
    all_borders.draw(screen)
    pygame.event.set_allowed(
        [pygame.KEYDOWN, pygame.QUIT, pygame_gui.UI_BUTTON_PRESSED, pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED])
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((window.width // 2, window.height // 2),
                                     (300, 300)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name="Да",
                    blocking=True)
            if ok_but is not None:
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ok_but:
                        change_score(scores)
                        if scores != 0:
                            next_level()
                        for elem in all_sprites:
                            elem.kill()
                        return upper_world_cycle()
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == exit_dialog:
                    terminate()
                if event.ui_element == confirm_dialog:
                    digger.kill()
                    for elem in all_sprites:
                        elem.kill()
                    return upper_world_cycle()
            if event.type == pygame.KEYDOWN and ok_but is None:
                if event.key == pygame.K_ESCAPE:
                    confirm_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((window.width // 2, window.height // 2),
                                         (300, 300)),
                        manager=manager,
                        window_title="Предупреждение",
                        action_long_desc="Если вы выйдите весь ваш прогресс будет утерен.",
                        action_short_name="Ок",
                        blocking=True)
                if digger.move(event.key) == "under":
                    digger.update_lines(new_line(all_sprites, tiles_group, chests_group, n_lines - 1,
                                                 camera.all_diff_x, camera.all_diff_y, level_look))
                    generate_borders(all_sprites, all_borders, n_lines - 1, camera.all_diff_x, camera.all_diff_y)
                    n_lines += 2
                all_borders.update()
                all_borders.draw(screen)
                tiles_group.update()
                tiles_group.draw(screen)
        screen.blit(bg, (0, 0))
        fire_group.update(digger, tiles_group, chests_group, digger.rect[0], digger.rect[1])
        if scores >= 0:
            scores += digger.update(tiles_group, chests_group, fire_group, all_sprites)
        if scores >= need_money and ok_but is None:
            ok_but = win(scores, manager, window.width, window.height)
            digger.kill()
        if ok_but is None:
            camera.update(digger)
            camera.all_diff_update()
        for sprite in all_sprites:
            camera.apply(sprite)
        score.set_text(f"СЧЕТ - {str(scores)}$ ")
        all_sprites.draw(screen)
        manager.update(time_delta=time_delta)
        manager.draw_ui(screen)
        for i in range(digger.health):
            screen.blit(hearts[i], (window.width * 0.04 * i, 5))
        if digger.is_miner_dead() and ok_but is None:
            ok_but = dead(scores, manager, window.width, window.height)
            digger.kill()
            scores = 0
        pygame.display.flip()
        clock.tick(FPS)


def upper_world_cycle():
    grass = Grass(all_sprites)
    mine = Mine(all_sprites)
    shop = Shop(all_sprites)
    digger = Digger(all_sprites, load_image("texture/miner.png"), 10, 5)
    bg = pygame.transform.scale(load_image("texture/sky.png"), (window.width, window.height * 2 // 3))
    press_e = None
    exit_dialog = None
    manager = pygame_gui.UIManager((window.width, window.height))
    manager.get_theme().load_theme('game_theme.json')

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        if (digger.check_collide(mine) or digger.check_collide(shop)) and press_e is None:
            press_e = pygame_gui.elements.UILabel(manager=manager, text="Нажмите E, чтобы войти",
                                                  relative_rect=pygame.Rect((window.width * 0.5, 0),
                                                                            (window.width * 0.5, window.height * 0.1)),
                                                  object_id=pygame_gui.core.ObjectID(class_id='@game_text',
                                                                                     object_id='#help_text'))
        elif not (digger.check_collide(mine) or digger.check_collide(shop)) and press_e is not None:
            press_e = None
            manager.clear_and_reset()
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((window.width // 2, window.height // 2),
                                     (300, 300)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name="Да",
                    blocking=True)
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == exit_dialog:
                    terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and digger.check_collide(mine):
                    for elem in all_sprites:
                        elem.kill()
                    manager.clear_and_reset()
                    global level_map
                    level_map = generate_mine(all_sprites, tiles_group, chests_group, int(get_level_look()))
                    # for elem in level_map:
                    #     print(len(elem))
                    print(get_score())
                    generate_borders(all_sprites, all_borders)
                    start_mine()
                if event.key == pygame.K_e and digger.check_collide(shop):
                    Inside_Shop(clock)
                flag = True
                digger.update(event.key, flag)
            if event.type == pygame.KEYUP:
                flag = False
                digger.update(event.key, flag)
        screen.blit(bg, (0, 0))
        all_sprites.update(grass, mine)
        all_sprites.draw(screen)
        manager.update(time_delta=time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def first_step():
    start = Start_Window(clock)
    if start.next_window == "setting":
        while start.next_window == "setting":
            setting_window = Settings_Window(clock, music)
            if setting_window.back == "back":
                start.__init__(clock)
                start.next_window = start.main_cycle(clock)
    if start.next_window == "game":
        upper_world_cycle()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Копатель')
    size = window.width, window.height
    music = Music()
    fire_group = pygame.sprite.Group()
    chests_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_borders = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    first_step()
    sys.excepthook = except_hook
