from random import randint

from data.moduls.function import *
from data.moduls.setting import *
import pygame

number_of_chests = 5
number_of_line = 10


class Chest(pygame.sprite.Sprite):
    def __init__(self, size, all_sprites, tiles_group):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(load_image("texture/chest.png"), (window.tile_size, window.tile_size))
        self.rect = self.image.get_rect().move(size)


class Border(pygame.sprite.Sprite):
    def __init__(self, all_sprites, borders, y, left, dx, dy):
        super().__init__(borders, all_sprites)
        self.image = pygame.transform.scale(load_image("texture/side_border.png"),
                                            (window.tile_size * 5, window.tile_size))
        if not left:
            self.rect = self.image.get_rect().move(-6 * window.tile_size + dx,
                                                   (window.height * 2 // 3) + (y * window.tile_size) + dy)
        else:
            self.rect = self.image.get_rect().move(15 * window.tile_size + dx,
                                                   (window.height * 2 // 3) + (y * window.tile_size) + dy)


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, y, all_sprites, tiles_group, mine_level):
        super().__init__(tiles_group, all_sprites)
        if mine_level == 0:
            if y < 1:
                self.image = pygame.transform.scale(load_image("texture/grass.png"),
                                                    (window.tile_size, window.tile_size))
            else:
                self.image = pygame.transform.scale(load_image("texture/dirt.png"),
                                                    (window.tile_size, window.tile_size))
            self.rect = self.image.get_rect().move(size)
        if mine_level == 1:
            self.image = pygame.transform.scale(load_image("texture/dirt1.png"), (window.tile_size, window.tile_size))
            self.rect = self.image.get_rect().move(size)
        elif mine_level == 2:
            self.image = pygame.transform.scale(load_image("texture/rock.png"), (window.tile_size, window.tile_size))
            self.rect = self.image.get_rect().move(size)
        elif mine_level == 3:
            self.image = pygame.transform.scale(load_image("texture/rock_2.png"), (window.tile_size, window.tile_size))
            self.rect = self.image.get_rect().move(size)


def generate_mine(all_sprites, tiles_group, chests_group, mine_sprites):
    tile_map = []
    chest_number = [2]
    for y in range(number_of_line):
        tile_map.append([])
        for x in range(16):
            size = x * window.tile_size - window.tile_size, (window.height * 2 // 3) + (y * window.tile_size)
            if x != 8 or y != 0:
                if randint(0, 15) in chest_number and number_of_chests > 0 and y > 1:
                    Chest(size, all_sprites, chests_group)
                    tile_map[y].append((-1, -1))
                else:
                    Tile(size, y, all_sprites, tiles_group, mine_sprites)
                    tile_map[y].append(size)
            else:
                tile_map[y].append(size)
    return tile_map


def new_line(all_sprites, tiles_group, chests_group, line_n, d_x, d_y, level_look):
    line_coords = []
    chest_number = [1, 2]
    for y in range(2):
        line_coords.append([])
        for x in range(16):
            size = x * window.tile_size - window.tile_size + d_x,\
                   (window.height * 2 // 3) + ((line_n + y) * window.tile_size) + d_y
            if randint(0, 30) in chest_number and number_of_chests > 0:
                Chest(size, all_sprites, chests_group)
                line_coords[y].append((-1, -1))
            else:
                Tile(size, line_n, all_sprites, tiles_group, level_look)
                line_coords[y].append(size)
    return line_coords


def generate_borders(all_sprites, all_borders, line_n=0, dx=0, dy=0):
    if len(all_borders) == 0:
        for y in range(number_of_line):
            Border(all_sprites, all_borders, y, False, dx, dy)
            Border(all_sprites, all_borders, y, True, dx, dy)
    else:
        for y in range(2):
            Border(all_sprites, all_borders, line_n + y, True, dx, dy)
            Border(all_sprites, all_borders, line_n + y, False, dx, dy)
