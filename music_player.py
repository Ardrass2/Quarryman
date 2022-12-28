import random

import pygame

from setting import MUSIC_VOLUME


class Music:
    def __init__(self):
        self.value = MUSIC_VOLUME
        self.rand_music()
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(self.value)

    def rand_music(self):
        pygame.mixer.music.load(f"data/music/{random.randint(1, 2)}.mp3")

    def change_volume(self, volume):
        self.value = volume
        pygame.mixer.music.set_volume(self.value)
