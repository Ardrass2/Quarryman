# Quarryman GAME
import os
import sys

import pygame

from character import Digger
from first_location import Grass, Mine
from setting import *
from start_window import Start_Window
from settings_window import Settings_Window


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Копатель')
    size = WIDTH, HEIGHT
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    start = Start_Window(load_image("texture/cave.jpg"), clock)
    if start.next_window == "game":
        grass = Grass(load_image("texture/трава.png"), all_sprites)
        digger = Digger(load_image("texture/character.png"), all_sprites)
        mine = Mine(load_image("texture/mine.png"), all_sprites)
        print(all_sprites)
        bg = pygame.transform.scale(load_image("texture/sky.png"), (WIDTH, HEIGHT * 2 // 3))
        screen.blit(bg, (0, 0))
        while running:
            speed = 20
            flag = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    flag = True
                    digger.update(event.key, speed, flag)
                if event.type == pygame.KEYUP:
                    flag = False
                    digger.update(event.key, speed, flag)
            screen.blit(bg, (0, 0))
            all_sprites.update(grass, flag)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    elif start.next_window == "setting":
        start = Settings_Window(load_image("texture/sett_bg.jpg"), clock)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()