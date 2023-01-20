import pygame

from data.moduls.function import *

# Кадры в секунду
FPS = 75
# Громкость музыки
music_volume = update_music_value()
# Громкость звуков
sound_volume = update_sound_value()


class Window_Size:
    def __init__(self):
        self.width, self.height = 0, 0
        self.update_window_size()
        self.tile_size = self.width * 0.1
        self.fullscreen = 0
        self.update_display_mode()

    def update_display_mode(self):
        with open("setting.txt") as setting:
            for elem in setting:
                if elem.startswith("fullscreen="):
                    f = elem.rstrip()[11:]
        if int(f) == 1:
            self.fullscreen = pygame.FULLSCREEN
        else:
            self.fullscreen = pygame.SCALED

    def update_window_size(self):
        with open("setting.txt") as setting:
            for elem in setting:
                if elem.startswith("width="):
                    w = elem.rstrip()[6:]
                if elem.startswith("height="):
                    h = elem.rstrip()[7:]

        self.width, self.height = int(w), int(h)

    def update_tile_size(self):
        self.tile_size = self.width * 0.1
        return self.tile_size


# Экземпляр класса, содержащий размер экрана
window = Window_Size()
