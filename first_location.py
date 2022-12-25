import pygame

from setting import *


class Grass(pygame.sprite.Sprite):
    def __init__(self, grass_img, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(grass_img, (WIDTH, HEIGHT * 2 // 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = HEIGHT * 2 // 3


class Mine(pygame.sprite.Sprite):
    def __init__(self, mine_img, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(mine_img, (WIDTH * 0.3, HEIGHT * 0.2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = HEIGHT - HEIGHT // 2
