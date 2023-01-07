import pygame

from setting import *
from function import *
from mining_location import TILE_SIZE


class Fire:
    def __init__(self, all_sprites, spawn_chance):
        super().__init__(all_sprites)
        self.fire_dx = 0
        self.fire_dy = 0
        if not spawn_chance == 5:
            pass
        else:
            self.image = pygame.transform.scale(load_image("texture/fire.jpg"), (TILE_SIZE, TILE_SIZE))
            # тут нужно сделать так, чтобы он встал на место сломанного блока,    (self.rect)
            # по идеи блок выдает цифру когда ломается и свои координаты, если 5, то огонь появляется на месте блока.

    def update_fire(self, miner, block, miner_x, miner_y, fire_x, fire_y):
        if miner_x == fire_x and miner_y == fire_y:  # если огонь в майнере
            for elem in self.collide_with(miner):
                elem.kill()
        elif miner_y < fire_y:  # и снизу не пустота.    (если майнер ниже)
            if miner_x < fire_x:
                self.fire_dx = -50
            elif miner_x > fire_x:
                self.fire_dx = 50
            else:
                self.fire_dx = 0
        elif miner_y == fire_y:  # если на одном уровне
            if miner_x < fire_x:
                self.fire_dx = -50
            else:
                self.fire_dx = 50
        elif miner_y > fire_y:  # если майнер выше
            if miner_x > fire_x:
                self.fire_dx = 50
            elif miner_x < fire_x:
                self.fire_dx = -50
            else:
                self.fire_dx = 0
        else:
            self.fire_dx = 0
        #  self.rect.move(self.fire_dx, self.fire_dy) обновляем местоположение огня.

    def collide_with(self, sprites):
        return pygame.sprite.spritecollide(self, sprites, False, collided=pygame.sprite.collide_mask)
