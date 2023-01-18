import pygame.sprite

from setting import *


class Fire(pygame.sprite.Sprite):
    def __init__(self, all_sprites, fire_sprites, left, top):
        super().__init__(fire_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image("texture/fire.png"), (window.tile_size, window.tile_size))
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.time = 0
        self.rect.left = left
        self.left = True

    def update(self, miner, ground, chests, miner_x, miner_y):
        if self.rect.top < 0:
            self.kill()
        if miner_x == self.rect[0] and miner_y - 11 == self.rect[1]:
            miner.health -= 1
            self.kill()
        if pygame.sprite.spritecollide(self, chests, pygame.sprite.collide_mask):
            for elem in pygame.sprite.spritecollide(self, chests, pygame.sprite.collide_mask):
                elem.kill()
        if self.time == 50:
            collided = self.collide_with_ground(ground)
            if not collided:
                self.rect = self.rect.move(0, window.tile_size)
            if miner_x > self.rect[0] and collided and not self.collide_with_left_walls(ground):
                if self.left:
                    self.left = False
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.rect.move(window.tile_size, 0)
            if miner_x < self.rect[0] and collided and not self.collide_with_right_walls(ground):
                if not self.left:
                    self.left = True
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.rect.move(-window.tile_size, 0)
            self.time = 0
        else:
            self.time += 1

    def collide_with_ground(self, ground):
        flag = False
        for elem in ground:
            if self.rect[0] == elem.rect[0] and self.rect[1] == elem.rect[1] - window.tile_size:
                flag = True
        return flag

    def collide_with_right_walls(self, ground):
        for elem in ground:
            if self.rect[0] == elem.rect[0] + window.tile_size and self.rect[1] == elem.rect[1]:
                return True
        return False

    def collide_with_left_walls(self, ground):
        for elem in ground:
            if self.rect[0] == elem.rect[0] - window.tile_size and self.rect[1] == elem.rect[1]:
                print(True)
                return True
        return False
