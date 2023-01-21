from data.moduls.setting import *


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.all_diff_x = 0
        self.all_diff_y = 0

    def all_diff_update(self):
        self.all_diff_x += self.dx
        self.all_diff_y += self.dy

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - window.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - window.height // 2)
