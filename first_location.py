import pygame

from setting import *
from function import *


class Grass(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/трава.png"), (width, height * 2 // 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = height * 2 // 3


class Mine(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/mine.png"), (width * 0.3, height * 0.3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = height * 2 // 3 - height * 0.3
