# Quarryman GAME
import os
import sys

import pygame

from setting import *
from start_window import Start_Window


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
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start = Start_Window(load_image("texture/cave.jpg"), clock)
    while start.next_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start.next_window = 0
        screen.fill((0, 0, 0))
        pygame.display.flip()
    pygame.quit()
