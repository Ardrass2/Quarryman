import pygame

from setting import *
from function import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, tiles_group):
        super().__init__(tiles_group, all_sprites)
        if y < 1:
            self.image = pygame.transform.scale(load_image("texture/grass.png"), (125, 125))
            self.rect = self.image.get_rect().move(x * 125 - 125, (height * 2 // 3) + (y * 125))
        else:
            self.image = pygame.transform.scale(load_image("texture/dirt.png"), (125, 125))
            self.rect = self.image.get_rect().move(x * 125 - 125, (height * 2 // 3) + (y * 125))


def generate_mine(all_sprites, tiles_group):
    for y in range(3):
        for x in range(15):
            Tile(x, y, all_sprites, tiles_group)
