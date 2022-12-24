# Quarryman GAME
import os
import sys

import pygame

from setting import *
from start_window import Start_Window


class Grass(pygame.sprite.Sprite):
    def __init__(self, grass_img):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(grass_img, (WIDTH, HEIGHT * 2 // 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = HEIGHT
        self.rect.top = HEIGHT * 2 // 3


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
        grass = Grass(load_image("texture/трава.png"))
        bg = pygame.transform.scale(load_image("texture/sky.png"), (WIDTH, HEIGHT * 2 // 3))
        screen.blit(bg, (0, 0))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(FPS)

    elif start.next_window == "setting":
        Setting()
