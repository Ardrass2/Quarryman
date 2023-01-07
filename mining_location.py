from function import *
from setting import *

TILE_SIZE = width * 0.1


class Border(pygame.sprite.Sprite):
    def __init__(self, all_sprites, borders, y, left=False):
        super().__init__(borders, all_sprites)
        self.image = pygame.transform.scale(load_image("texture/side_border.png"),  (TILE_SIZE * 5, TILE_SIZE))
        if not left:
            self.rect = self.image.get_rect().move(-6 * TILE_SIZE, (height * 2 // 3) + (y * TILE_SIZE))
        else:
            self.rect = self.image.get_rect().move(15 * TILE_SIZE, (height * 2 // 3) + (y * TILE_SIZE))


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, y, all_sprites, tiles_group):
        super().__init__(tiles_group, all_sprites)
        if y < 1:
            self.image = pygame.transform.scale(load_image("texture/grass.png"), (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.transform.scale(load_image("texture/dirt.png"), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect().move(size)


def generate_mine(all_sprites, tiles_group):
    tile_map = []
    for y in range(5):
        tile_map.append([])
        for x in range(16):
            size = x * TILE_SIZE - TILE_SIZE, (height * 2 // 3) + (y * TILE_SIZE)
            if x != 8 or y != 0:
                Tile(size, y, all_sprites, tiles_group)
            tile_map[y].append(size)
    return tile_map


def generate_borders(all_sprites, all_borders):
    for y in range(5):
        Border(all_sprites, all_borders, y)
        Border(all_sprites, all_borders, y, True)
