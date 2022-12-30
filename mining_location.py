import pygame

from setting import *
from function import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles_group, all_spritez)
        self.block = pygame.transform.scale(load_image("texture/dirth.png"), (50, 50))
        self.block_depth = pygame.transform.scale(load_image("texture/rock.png"), (50, 50))
        if y < 4:
            self.rect = self.block.get_rect().move(x * 50 - 50, (height * 2 // 3) - (y * 50))
        else:
            self.rect = self.block_depth.get_rect().move(x * 50 - 50, (height * 2 // 3) - (y * 50))


all_spritez = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def generate_mine():
    for y in range(13):
        for x in range(28):
            Tile(x, y)
