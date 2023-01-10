# Quarryman GAME

import pygame.sprite
import pygame_gui

from camera import *
from fire import *
from character import *
from first_location import *
from mining_location import *
from music_player import *
from setting import *
from settings_window import Settings_Window
from shop import Inside_Shop
from start_window import Start_Window

level_map = []


def mine_update():
    tiles_group.update()
    tiles_group.draw(screen)
    all_sprites.update(tiles_group)
    all_sprites.draw(screen)
    all_borders.update()
    all_borders.draw(screen)


def start_mine():
    exit_dialog = None
    digger = Miner(all_sprites, load_image("texture/miner.png"), 10, 5, level_map)
    bg = pygame.transform.scale(load_image("texture/cave_mining.jpg"), (window.width, window.height))
    manager = pygame_gui.UIManager((window.width, window.height))
    manager.get_theme().load_theme('theme.json')
    scores = 10
    score = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((window.width * 0.45, window.height * 0.005),
                                  (window.width * 0.9, window.height * 0.08)), text="score - " + str(scores) + ' ',
        manager=manager)
    screen.blit(bg, (0, 0))
    camera = Camera()
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 250), (300, 300)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name="Да",
                    blocking=True)
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == exit_dialog:
                    terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    digger.kill()
                    for elem in all_sprites:
                        elem.kill()
                    return upper_world_cycle()
                digger.move(event.key)
        screen.blit(bg, (0, 0))
        camera.update(digger)
        for sprite in all_sprites:
            camera.apply(sprite)
        mine_update()
        manager.update(time_delta=time_delta)
        manager.draw_ui(screen)
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
                    rect=pygame.Rect((250, 250), (300, 300)),
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
                    level_map = generate_mine(all_sprites, tiles_group, chests_group)
                    # for elem in level_map:
                    #     print(len(elem))
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
    chests_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_borders = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    first_step()
    sys.excepthook = except_hook
