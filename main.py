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
    digger = Miner(all_sprites, load_image("texture/miner.png"), 10, 5, level_map)
    bg = pygame.transform.scale(load_image("texture/cave_mining.jpg"), (width, height))
    manager = pygame_gui.UIManager((width, height))
    manager.get_theme().load_theme('theme.json')
    scores = 10
    score = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((width * 0.45, height * 0.005),
                                  (width * 0.9, height * 0.08)), text="score - " + str(scores) + ' ', manager=manager)
    screen.blit(bg, (0, 0))
    camera = Camera()
    while True:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    digger.kill()
                    for elem in tiles_group:
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
    bg = pygame.transform.scale(load_image("texture/sky.png"), (width, height * 2 // 3))
    press_e = None
    manager = pygame_gui.UIManager((width, height))
    manager.get_theme().load_theme('game_theme.json')

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        if (digger.check_collide(mine) or digger.check_collide(shop)) and press_e is None:
            press_e = pygame_gui.elements.UILabel(manager=manager, text="Нажмите E, чтобы войти",
                                                  relative_rect=pygame.Rect((width * 0.5, 0),
                                                                            (width * 0.5, height * 0.1)),
                                                  object_id=pygame_gui.core.ObjectID(class_id='@game_text',
                                                                                     object_id='#help_text'))
        elif not (digger.check_collide(mine) or digger.check_collide(shop)) and press_e is not None:
            press_e = None
            manager.clear_and_reset()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                start.next_window = start.main_cycle(clock)
    if start.next_window == "game":
        upper_world_cycle()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Копатель')
    size = width, height
    music = Music()
    chests_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_borders = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    first_step()
    sys.excepthook = except_hook
