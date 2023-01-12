import os
import sys

from setting import *
import pygame
import pygame_gui


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    # Оагрузка изображения
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def change_window_size(size):
    settings_in = open("setting.txt", "r")
    settings_out = open("sett.txt", "w")
    for elem in settings_in.readlines():
        if elem.startswith("width="):
            settings_out.write("width=" + str(size[0]) + "\n")
        elif elem.startswith("height="):
            settings_out.write("height=" + str(size[1]) + "\n")
        else:
            settings_out.write(elem)
    settings_in.close()
    settings_out.close()
    os.remove("setting.txt")
    os.rename("sett.txt", "setting.txt")


def update_window_size():
    with open("setting.txt") as setting:
        for elem in setting:
            if elem.startswith("width="):
                width = elem.rstrip()[6:]
            if elem.startswith("height="):
                height = elem.rstrip()[7:]

    return int(width), int(height)


def update_sound_value():
    sound_value = 0
    with open("setting.txt") as setting:
        for elem in setting:
            if elem.startswith("sound_value="):
                sound_value = elem.rstrip()[12:]

    return int(sound_value) / 100


def update_music_value():
    music_value = 0
    with open("setting.txt") as setting:
        for elem in setting:
            if elem.startswith("music_value="):
                music_value = elem.rstrip()[12:]

    return int(music_value) / 100


def change_music_value(new_value):
    settings_in = open("setting.txt", "r")
    settings_out = open("sett.txt", "w")
    for elem in settings_in.readlines():
        if elem.startswith("music_value="):
            settings_out.write("music_value=" + str(new_value) + "\n")
        else:
            settings_out.write(elem)
    settings_in.close()
    settings_out.close()
    os.remove("setting.txt")
    os.rename("sett.txt", "setting.txt")


def change_sound_value(new_value):
    settings_in = open("setting.txt", "r")
    settings_out = open("sett.txt", "w")
    for elem in settings_in.readlines():
        if elem.startswith("sound_value="):
            settings_out.write("sound_value=" + str(new_value) + "\n")
        else:
            settings_out.write(elem)
    settings_in.close()
    settings_out.close()
    os.remove("setting.txt")
    os.rename("sett.txt", "setting.txt")


def dead(score, manager, wind_w, wind_h):
    label = pygame_gui.elements.UILabel(text=f"ВЫ ПОГИБЛИ И ПОТЕРЯЛИ {score}$", manager=manager,
                                        relative_rect=pygame.Rect(wind_w // 4, wind_h / 2 - 100,
                                                                  wind_w * 2 // 3, 200))
    ok_button = pygame_gui.elements.UIButton(text="Вернуться", manager=manager,
                                             relative_rect=pygame.Rect(wind_w // 2 - 100, wind_h - 200,
                                                                       wind_w // 4, 200))
    return ok_button

def except_hook(cls, exception, traceback):
    # Отлов ошибок
    sys.__excepthook__(cls, exception, traceback)
