from function import *
from setting import *

TILE_SIZE = height * 0.2


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, tiles_group):
        super().__init__(tiles_group, all_sprites)
        if y < 1:
            self.image = pygame.transform.scale(load_image("texture/grass.png"), (TILE_SIZE, TILE_SIZE))
            self.rect = self.image.get_rect().move(x * TILE_SIZE - TILE_SIZE, (height * 2 // 3) + (y * TILE_SIZE))
        else:
            self.image = pygame.transform.scale(load_image("texture/dirt.png"), (TILE_SIZE, TILE_SIZE))
            self.rect = self.image.get_rect().move(x * TILE_SIZE - TILE_SIZE, (height * 2 // 3) + (y * TILE_SIZE))


def generate_mine(all_sprites, tiles_group):
    for y in range(5):
        for x in range(16):
            Tile(x, y, all_sprites, tiles_group)
