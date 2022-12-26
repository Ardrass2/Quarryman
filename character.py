import pygame

from setting import *


class Digger(pygame.sprite.Sprite):
    def __init__(self, character_image, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(character_image, (WIDTH * 0.2, HEIGHT * 0.3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = 0
        self.rect.left = WIDTH // 2
        self.some = False

    def update(self, *args):
        if type(args[0]) != int:
            if not pygame.sprite.collide_mask(self, args[0]):
                self.rect = self.rect.move(0, 1)
                x, y = self.rect[0], self.rect[1]
        if args[0] == pygame.K_d:
            if not self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
            if not self.rect[0] >= WIDTH * 0.87:
                self.rect = self.rect.move(args[1], 0)
        elif args[0] == pygame.K_a:
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)
            if not self.rect[0] <= -(WIDTH * 0.06):
                self.rect = self.rect.move(-args[1], 0)
