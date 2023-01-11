import random

import pygame

from setting import music_volume, sound_volume


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


class Sound:
    def __init__(self, sound, repeat_time=-1):
        self.repeat_time = repeat_time
        self.value = sound_volume
        self.sound = pygame.mixer.Sound(f"data/music/{sound}.wav")
        self.sound.set_volume(self.value)

    def change_repeat_time(self, repeat_time):
        self.repeat_time = repeat_time

    def start(self):
        self.sound.play(self.repeat_time)

    def stop(self):
        self.sound.stop()
