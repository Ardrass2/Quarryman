import pygame.sprite

from function import *
from mining_location import TILE_SIZE
from setting import *


class Miner(pygame.sprite.Sprite):
    def __init__(self, all_sprites, sheet, columns, rows):
        super().__init__(all_sprites)
        self.action = {"stay": 2,
                       "run": 1,
                       "d_under_person": 0,
                       "d_on_corner": 4}
        self.sheet = sheet
        self.columns, self.rows = columns, rows
        self.frames = []
        self.now_action = ""
        self.time = 0
        self.cut_sheet("stay")
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (width * 0.1, height * 0.2))
        self.rect.center = width // 2 - 15, height // 2 + 25
        self.some = False
        self.act = [0, 0]

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

    def update(self, ground, key_down=0):
        if len(pygame.sprite.spritecollide(self, ground, False, collided=pygame.sprite.collide_mask)) == 0:
            self.rect = self.rect.move(0, 1)
        if self.time == 5:
            if self.cur_frame == len(self.frames) - 1:
                self.change_action("stay")
                self.rect = self.rect.move(self.act[0], self.act[1])
                if self.act != [0, 0]:
                    self.collide_with(ground)
                    self.act = [0, 0]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (width * 0.1, height * 0.2))
            if self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.time = 0
        else:
            self.time += 1
        if key_down == pygame.K_s:
            self.act = [0, TILE_SIZE - 10]
            self.cur_frame = 0
            self.change_action("d_under_person")
        if key_down == pygame.K_d:
            self.act = [TILE_SIZE - 2, -10]
            self.cur_frame = 0
            self.change_action("d_on_corner")
            if not self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
        if key_down == pygame.K_a:
            self.act = [-TILE_SIZE + 2, -10]
            self.change_action("d_on_corner")
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)

    def collide_with(self, sprites):
        if not pygame.sprite.spritecollide(self, sprites, True, collided=pygame.sprite.collide_mask):
            return False
        return True


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
        elif args[0] == pygame.K_a:
            if self.now_action != "run":
                own_rect = self.rect[0], self.rect[1]
                self.cut_sheet("run")
                self.rect[0], self.rect[1] = own_rect[0], own_rect[1]
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = -1
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
