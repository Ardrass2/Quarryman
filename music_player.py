import random

import pygame

from setting import music_volume


class Music:
    def __init__(self):
        self.value = music_volume
        self.rand_music()
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(self.value)

    def rand_music(self):
        pygame.mixer.music.load(f"data/music/{random.randint(1, 2)}.mp3")

    def change_volume(self, volume):
        self.value = volume
        pygame.mixer.music.set_volume(self.value)
