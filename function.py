import pygame
import pygame_gui

import sqlite3
import os
import sys
from setting import *

con = sqlite3.connect("data/Game_data")
cur = con.cursor()


def change_current_level(level):
    cur.execute(f"""UPDATE Level
                    SET current_level = {level}
                    WHERE level = (SELECT MAX(level) FROM Level)""")
    con.commit()


def get_level_look():
    result = cur.execute("""SELECT MAX(current_level) FROM Level""").fetchall()
    return result[0][0]


def next_level():
    cur.execute(f"""INSERT INTO Level(money_need, current_level) 
                VALUES ((SELECT MAX(money_need) FROM Level) * 1.1 + 100, (SELECT MAX(current_level) FROM Level))""")
    con.commit()


def money_need():
    result = cur.execute("SELECT MAX(money_need) FROM Level").fetchall()
    return result[0][0]


def get_current_level():
    result = cur.execute("SELECT MAX(current_level) FROM Level").fetchall()
    return result[0][0]


def get_level():
    result = cur.execute("SELECT MAX(level) FROM Level").fetchall()
    return result[0][0]


def get_health():
    result = cur.execute("""SELECT miner_health FROM Miner
                         WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)""").fetchall()
    return result[0][0]


def get_digger_speed():
    result = cur.execute("""SELECT dig_speed FROM Miner
                         WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)""").fetchall()
    return result[0][0]


def get_digger_luck():
    result = cur.execute("""SELECT dig_luck FROM Miner
                         WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)""").fetchall()
    return result[0][0]


def get_score():
    result = cur.execute("""SELECT total_money FROM Score
                         WHERE id = (SELECT MAX(id) FROM Score)""").fetchall()
    return result[0][0]


def change_score(value):
    cur.execute(f"""INSERT INTO Score (change_money, total_money) VALUES ({value}, (SELECT total_money FROM Score
                    WHERE id = (SELECT MAX(id) FROM Score)) + {value})""")
    con.commit()


def change_speed(value):
    cur.execute(f"""INSERT INTO Miner (dig_speed, dig_luck, miner_health) VALUES ((SELECT dig_speed FROM Miner
                    WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)) + {value}, {get_digger_luck()}, {get_health()})""")
    con.commit()


def change_luck(value):
    cur.execute(f"""INSERT INTO Miner (dig_speed, dig_luck, miner_health) VALUES 
    ({get_digger_speed()}, (SELECT dig_luck FROM Miner
                            WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)) + {value}, {get_health()})""")
    con.commit()


def change_health(value):
    cur.execute(f"""INSERT INTO Miner (dig_speed, dig_luck, miner_health) VALUES 
    ({get_digger_speed()}, {get_digger_luck()}, (SELECT miner_health FROM Miner
                            WHERE buys_id = (SELECT MAX(buys_id) FROM Miner)) + {value})""")
    con.commit()


def terminate():
    con.close()
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


def win(score, manager, wind_w, wind_h):
    label = pygame_gui.elements.UILabel(text=f"Вы заработали {score}$ и прошли уровень", manager=manager,
                                        relative_rect=pygame.Rect(wind_w // 8, wind_h / 2 - 100,
                                                                  wind_w * 4 // 5, 200))
    ok_button = pygame_gui.elements.UIButton(text="Вернуться", manager=manager,
                                             relative_rect=pygame.Rect(wind_w // 2 - 100, wind_h - 200,
                                                                       wind_w // 4, 200))
    return ok_button


def except_hook(cls, exception, traceback):
    # Отлов ошибок
    sys.__excepthook__(cls, exception, traceback)
