from function import *

# Кадры в секунду
FPS = 60
# Громкость музыки
music_volume = update_music_value()
# Громкость звуков
sound_volume = update_sound_value()


class Window_Size:
    def __init__(self):
        self.width, self.height = 0, 0
        self.update_window_size()

    def update_window_size(self):
        with open("setting.txt") as setting:
            for elem in setting:
                if elem.startswith("width="):
                    w = elem.rstrip()[6:]
                if elem.startswith("height="):
                    h = elem.rstrip()[7:]

        self.width, self.height = int(w), int(h)


# Экземпляр класса, содержащий размер экрана
window = Window_Size()
