from setting import *
import pygame_gui
import pygame
import os
import sys


class Grass(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/трава.png"), (window.width, window.height * 2 // 3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = window.height * 2 // 3


class Mine(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/mine.png"), (window.width * 0.3, window.height * 0.3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = window.height * 2 // 3 - window.height * 0.3


class Shop(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/shop.png"), (window.width * 0.2, window.height * 0.6))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.right = window.width
        self.rect.top = window.height * 2 // 3 - window.height * 0.6
