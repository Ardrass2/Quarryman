from random import randint

import pygame.sprite

from fire import Fire
from music_player import Sound
from setting import *


class Miner(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, level_map):
        super().__init__(all_sprites)
        self.destroy_sound = Sound("stone_destroy", 1)
        self.walk_sound = Sound("steps", 1)
        self.money = Sound("money", 0)
        self.level_map = level_map
        self.action = {"stay": 2,
                       "run": 1,
                       "d_under_person": 0,
                       "d_on_corner": 4}
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.frames = []
        self.need_destroy = False
        self.now_action = ""
        self.time = 0
        self.cut_sheet("stay")
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (window.tile_size, window.tile_size - 10))
        self.rect.top = level_map[0][len(level_map[0]) // 2][1] + 11
        self.rect.left = level_map[0][len(level_map[0]) // 2][0]
        self.level_map[0][len(level_map[0]) // 2] = (0, 0)
        self.cell_x, self.cell_y = len(level_map[0]) // 2, 0
        self.right_corner = False
        self.key = str()
        self.chance = get_digger_luck()
        self.d_score = 0
        self.health = get_health()
        self.act = False
        self.dig_speed = get_digger_speed()

    def cut_sheet(self, action):
        self.frames = []
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // self.columns,
                                self.sheet.get_height() // self.rows)
        for i in range(self.columns):
            frame_location = (self.rect.w * i, self.rect.h * self.action[action])
            self.frames.append(self.sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        self.now_action = action
        self.frames = self.frames[::-1]

    def change_action(self, action):
        self.cur_frame = 0
        own_rect = self.rect[0], self.rect[1]
        self.cut_sheet(action)
        self.rect[0], self.rect[1] = own_rect[0], own_rect[1]

    def update_lines(self, new_line):
        self.level_map = [*self.level_map, *new_line]

    def go_down(self, ground, chests):
        if len(self.collide_with(ground)) == 0:
            if self.cell_y > 5:
                for elem in ground:
                    if elem.rect[1] == self.rect[1] - 11 - 4 * window.tile_size:
                        elem.kill()
            self.rect = self.rect.move(0, window.tile_size)
            self.get_chest(chests)
            self.cell_y = self.cell_y + 1
        else:
            self.key = ""
            self.act = ""

    def update(self, ground, chests, fire, all_spr):
        if self.d_score != 0:
            self.d_score = 0
        if self.key == "go under" and self.time == self.dig_speed // 2:
            self.go_down(ground, chests)
            return self.d_score
        elif self.time == self.dig_speed:
            if self.cur_frame == 0:
                if self.now_action != "d_under_person":
                    if self.act:
                        self.destroy_sound.start()
            if self.cur_frame == 6:
                if self.act:
                    self.destroy_sound.stop()
                    self.destroy_sound.start()
            if self.cur_frame == len(self.frames) - 1:
                self.act = False
                self.change_action("stay")
                if self.key == "s":
                    self.key = ""
                    for elem in ground:
                        if self.right_corner:
                            if elem.rect[0] == self.rect[0] + window.tile_size and elem.rect[1] == self.rect[1] - 11:
                                elem.kill()
                                if randint(1, self.chance) == 5:
                                    Fire(all_spr, fire, self.rect[0] + window.tile_size, self.rect[1] - 11)

                            if elem.rect[0] == self.rect[0] + window.tile_size and \
                                    elem.rect[1] == self.rect[1] - 11 + window.tile_size:
                                elem.kill()
                                if randint(1, self.chance) == 5:
                                    Fire(all_spr, fire, self.rect[0] + window.tile_size,
                                         self.rect[1] - 11 + window.tile_size)
                        else:
                            if elem.rect[0] == self.rect[0] - window.tile_size and \
                                    elem.rect[1] == self.rect[1] - 11 + window.tile_size:
                                elem.kill()
                                if randint(1, self.chance) == 5:
                                    Fire(all_spr, fire, self.rect[0] - window.tile_size,
                                         self.rect[1] - 11 + window.tile_size)

                            if elem.rect[0] == self.rect[0] - window.tile_size and elem.rect[1] == self.rect[1] - 11:
                                elem.kill()
                                if randint(1, self.chance) == 5:
                                    Fire(all_spr, fire, self.rect[0] - window.tile_size, self.rect[1] - 11)

                if self.key == "d":
                    self.key = ""
                    no_blocks = True
                    for elem in ground:
                        if elem.rect[0] == self.rect[0] + window.tile_size and elem.rect[1] == self.rect[1] - 11:
                            elem.kill()
                            no_blocks = False
                            if randint(1, self.chance) == 5:
                                Fire(all_spr, fire, self.rect[0] + window.tile_size, self.rect[1] - 11)
                            break
                    if no_blocks:
                        self.rect = self.rect.move(window.tile_size, 0)
                        self.cell_x = self.cell_x + 1
                        self.get_chest(chests)
                        if len(self.collide_with(ground)) == 0:
                            self.key = "go under"
                            self.act = "go down"

                if self.key == "a":
                    self.key = ""
                    no_blocks = True
                    for elem in ground:
                        if elem.rect[0] == self.rect[0] - window.tile_size and elem.rect[1] == self.rect[1] - 11:
                            elem.kill()
                            no_blocks = False
                            if randint(1, self.chance) == 5:
                                Fire(all_spr, fire, self.rect[0] - window.tile_size, self.rect[1] - 11)
                            break
                    if no_blocks:
                        self.rect = self.rect.move(-window.tile_size, 0)
                        self.get_chest(chests)
                        self.cell_x = self.cell_x - 1
                        if len(self.collide_with(ground)) == 0:
                            self.key = "go under"
                            self.act = "go down"

                self.destroy_sound.stop()
                self.walk_sound.stop()

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (window.tile_size, window.tile_size - 10))
            if self.right_corner:
                self.right_corner = False
                self.change_view_side()
            self.time = 0
            return self.d_score
        else:
            self.time += 1
            return 0

    def is_miner_dead(self):
        if self.health == 0:
            return 1
        else:
            return 0

    def get_chest(self, chests):
        for elem in chests:
            if elem.rect[1] == self.rect[1] - 11 and elem.rect[0] == self.rect[0]:
                elem.kill()
                self.d_score += randint(9999, 99999)
                self.money.start()
                break

    def move(self, key_down):
        if key_down == pygame.K_s:
            if not self.act:
                if self.cell_x + 1 != len(self.level_map[self.cell_y]) and self.cell_x - 1 >= 0:
                    self.act = True
                    self.key = "s"
                    if self.right_corner and self.level_map[self.cell_y + 1][self.cell_x + 1] != (0, 0):
                        self.cur_frame = 0
                        self.level_map[self.cell_y + 1][self.cell_x + 1] = (0, 0)
                        self.level_map[self.cell_y][self.cell_x + 1] = (0, 0)
                        self.change_action("d_under_person")
                        return "under"
                    if not self.right_corner and self.level_map[self.cell_y + 1][self.cell_x - 1] != (0, 0):
                        self.cur_frame = 0
                        self.level_map[self.cell_y + 1][self.cell_x - 1] = (0, 0)
                        self.level_map[self.cell_y][self.cell_x - 1] = (0, 0)
                        self.change_action("d_under_person")
                        return "under"

        elif key_down == pygame.K_d:
            if not self.act:
                if self.cell_x + 1 != len(self.level_map[self.cell_y]):
                    self.act = True
                    self.key = "d"
                    if self.level_map[self.cell_y][self.cell_x + 1] != (0, 0) and \
                            self.level_map[self.cell_y][self.cell_x + 1] != (-1, -1):
                        self.cur_frame = 0
                        self.level_map[self.cell_y][self.cell_x + 1] = (0, 0)
                        self.change_action("d_on_corner")
                    else:
                        self.change_action("run")
                        self.cur_frame = 8
                        self.walk_sound.start()
                if not self.right_corner:
                    self.change_view_side()

        elif key_down == pygame.K_a:
            if not self.act:
                if self.cell_x - 1 != -1:
                    self.act = True
                    self.key = "a"
                    if self.level_map[self.cell_y][self.cell_x - 1] != (0, 0) and \
                            self.level_map[self.cell_y][self.cell_x - 1] != (-1, -1):
                        self.cur_frame = 0
                        self.level_map[self.cell_y][self.cell_x - 1] = (0, 0)
                        self.change_action("d_on_corner")
                    else:
                        self.change_action("run")
                        self.cur_frame = 8
                        self.walk_sound.start()
                if self.right_corner:
                    self.change_view_side()
        elif key_down == pygame.K_RIGHT and not self.act:
            if not self.right_corner:
                self.change_view_side()
        elif key_down == pygame.K_LEFT and not self.act:
            if self.right_corner:
                self.change_view_side()

    def change_view_side(self):
        self.right_corner = not self.right_corner
        self.image = pygame.transform.flip(self.image, True, False)

    def collide_with(self, sprites):
        return pygame.sprite.spritecollide(self, sprites, False, collided=pygame.sprite.collide_mask)


class Digger(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows):
        super().__init__(all_sprites)
        self.action = {"stay": 2,
                       "run": 3}
        self.sound = Sound("steps")
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.frames = []
        self.now_action = ""
        self.cut_sheet("stay")
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (window.width * 0.1, window.height * 0.2))
        self.rect.top = window.height * 2 // 3 - window.height * 0.2
        self.rect.left = window.width // 2
        self.some = False
        self.left_or_right = 0
        self.speed = 7
        self.time = 0

    def cut_sheet(self, action):
        self.frames = []
        self.rect = pygame.Rect(0, 0, self.sheet.get_width() // self.columns,
                                self.sheet.get_height() // self.rows)
        for i in range(self.columns):
            frame_location = (self.rect.w * i, self.rect.h * self.action[action])
            self.frames.append(self.sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        self.now_action = action
        self.frames = self.frames[::-1]

    def update(self, *args):
        if self.left_or_right == 0:
            if self.sound is not None:
                self.sound.stop()
        if self.time == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (window.width * 0.1, window.height * 0.2))
            if self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.time = 0
        else:
            self.time += 1

        if type(args[0]) != int and type(args[1]) != int:
            if not self.check_collide(args[0]):
                self.rect = self.rect.move(0, 1)

        if not args[1]:
            if self.now_action != "stay":
                own_rect = self.rect[0], self.rect[1]
                self.cut_sheet("stay")
                self.rect[0], self.rect[1] = own_rect[0], own_rect[1]
            self.left_or_right = 0

        elif args[0] == pygame.K_d:
            if self.now_action != "run":
                own_rect = self.rect[0], self.rect[1]
                self.cut_sheet("run")
                self.rect[0], self.rect[1] = own_rect[0], own_rect[1]
            if not self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = 1
            self.sound.start()

        elif args[0] == pygame.K_a:
            if self.now_action != "run":
                own_rect = self.rect[0], self.rect[1]
                self.cut_sheet("run")
                self.rect[0], self.rect[1] = own_rect[0], own_rect[1]
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = -1
            self.sound.start()

        if not self.rect[0] >= window.width * 0.9 and not self.rect[0] <= -(window.width * 0.01):
            self.rect = self.rect.move(self.left_or_right * self.speed, 0)
        else:
            if self.rect[0] > window.width * 0.5:
                self.rect[0] = window.width * 0.87
            else:
                self.rect[0] = 0

    def check_collide(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            return True
