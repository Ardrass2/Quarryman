import pygame.sprite

from mining_location import TILE_SIZE
from music_player import Sound
from setting import *


class Miner(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows, level_map):
        super().__init__(all_sprites)
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
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (TILE_SIZE, TILE_SIZE - 10))
        self.rect.top = level_map[0][len(level_map[0]) // 2][1] + 11
        self.rect.left = level_map[0][len(level_map[0]) // 2][0]
        self.level_map[0][len(level_map[0]) // 2] = (0, 0)
        self.cell_x, self.cell_y = len(level_map[0]) // 2, 0
        self.right_corner = False
        self.key = str()
        self.act = False

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

    def update(self, ground):
        if self.time == 1:
            if self.cur_frame == len(self.frames) - 1:
                self.act = False
                self.change_action("stay")
                if self.key == "s":
                    self.key = ""
                    for elem in ground:
                        print(elem.rect[1], self.rect[1] - 11 + width * 0.1)
                        if self.right_corner:
                            if elem.rect[0] == self.rect[0] + TILE_SIZE and elem.rect[1] == self.rect[1] - 11:
                                elem.kill()
                            if elem.rect[0] == self.rect[0] + TILE_SIZE and \
                                    elem.rect[1] == self.rect[1] - 11 + TILE_SIZE:
                                elem.kill()
                        else:
                            if elem.rect[0] == self.rect[0] - TILE_SIZE and \
                                    elem.rect[1] == self.rect[1] - 11 + TILE_SIZE:
                                elem.kill()
                            if elem.rect[0] == self.rect[0] - TILE_SIZE and elem.rect[1] == self.rect[1] - 11:
                                elem.kill()

                if self.key == "d":
                    self.key = ""
                    no_blocks = True
                    for elem in ground:
                        if elem.rect[0] == self.rect[0] + TILE_SIZE and elem.rect[1] == self.rect[1] - 11:
                            elem.kill()
                            no_blocks = False
                            break
                    if no_blocks:
                        self.rect = self.rect.move(TILE_SIZE, 0)
                        self.cell_x = self.cell_x + 1
                        while len(self.collide_with(ground)) == 0:
                            self.rect = self.rect.move(0, TILE_SIZE)
                            self.cell_y = self.cell_y + 1

                if self.key == "a":
                    self.key = ""
                    no_blocks = True
                    for elem in ground:
                        if elem.rect[0] == self.rect[0] - TILE_SIZE and elem.rect[1] == self.rect[1] - 11:
                            elem.kill()
                            no_blocks = False
                            break
                    if no_blocks:
                        self.rect = self.rect.move(-TILE_SIZE, 0)
                        self.cell_x = self.cell_x - 1
                        while len(self.collide_with(ground)) == 0:
                            self.rect = self.rect.move(0, TILE_SIZE)
                            self.cell_y = self.cell_y + 1

                pygame.mixer.music.stop()

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (TILE_SIZE, TILE_SIZE - 10))
            if self.right_corner:
                self.right_corner = False
                self.change_view_side()
            self.time = 0
        else:
            self.time += 1

    def move(self, key_down):

        if key_down == pygame.K_s:
            if not self.act:
                if self.cell_x + 1 != len(self.level_map[self.cell_y]) and self.cell_x - 1 >= 0:
                    self.act = True
                    self.key = "s"
                    if self.right_corner and self.level_map[self.cell_y + 1][self.cell_x + 1] != (0, 0):
                        Sound("stone_destroy", 1)
                        self.cur_frame = 0
                        self.level_map[self.cell_y + 1][self.cell_x + 1] = (0, 0)
                        self.level_map[self.cell_y][self.cell_x + 1] = (0, 0)
                        self.change_action("d_under_person")
                    if not self.right_corner and self.level_map[self.cell_y + 1][self.cell_x - 1] != (0, 0):
                        Sound("stone_destroy", 1)
                        self.cur_frame = 0
                        self.level_map[self.cell_y + 1][self.cell_x - 1] = (0, 0)
                        self.level_map[self.cell_y][self.cell_x - 1] = (0, 0)
                        self.change_action("d_under_person")

        elif key_down == pygame.K_d:
            if not self.act:
                if self.cell_x + 1 != len(self.level_map[self.cell_y]):
                    self.act = True
                    self.key = "d"
                    if self.level_map[self.cell_y][self.cell_x + 1] != (0, 0) and \
                            self.level_map[self.cell_y][self.cell_x + 1] != (-1, -1):
                        Sound("stone_destroy", 2)
                        self.cur_frame = 0
                        self.level_map[self.cell_y][self.cell_x + 1] = (0, 0)
                        self.change_action("d_on_corner")
                    else:
                        self.change_action("run")
                        self.cur_frame = 8
                        Sound("steps", 1)
                if not self.right_corner:
                    self.change_view_side()

        elif key_down == pygame.K_a:
            if not self.act:
                if self.cell_x - 1 != -1:
                    self.act = True
                    self.key = "a"
                    if self.level_map[self.cell_y][self.cell_x - 1] != (0, 0) and \
                            self.level_map[self.cell_y][self.cell_x - 1] != (-1, -1):
                        Sound("stone_destroy", 2)
                        self.cur_frame = 0
                        self.level_map[self.cell_y][self.cell_x - 1] = (0, 0)
                        self.change_action("d_on_corner")
                    else:
                        self.change_action("run")
                        self.cur_frame = 8
                        Sound("steps", 1)
                if self.right_corner:
                    self.change_view_side()
        elif key_down == pygame.K_RIGHT:
            if not self.right_corner:
                self.change_view_side()
        elif key_down == pygame.K_LEFT:
            if self.right_corner:
                self.change_view_side()
        return self.cell_y

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
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.frames = []
        self.now_action = ""
        self.cut_sheet("stay")
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (width * 0.1, height * 0.2))
        self.rect.top = height * 2 // 3 - height * 0.2
        self.rect.left = width // 2
        self.some = False
        self.left_or_right = 0
        self.speed = 7
        self.time = 0
        self.sound = None

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
            pygame.mixer.music.stop()

        if self.time == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (width * 0.1, height * 0.2))
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
            self.sound = Sound("steps")

        elif args[0] == pygame.K_a:
            if self.now_action != "run":
                own_rect = self.rect[0], self.rect[1]
                self.cut_sheet("run")
                self.rect[0], self.rect[1] = own_rect[0], own_rect[1]
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = -1
            self.sound = Sound("steps")

        if not self.rect[0] >= width * 0.9 and not self.rect[0] <= -(width * 0.01):
            self.rect = self.rect.move(self.left_or_right * self.speed, 0)
        else:
            if self.rect[0] > width * 0.5:
                self.rect[0] = width * 0.87
            else:
                self.rect[0] = 0

    def check_collide(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            return True
