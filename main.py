# Quarryman GAME

from character import Digger
from first_location import Grass, Mine
from function import *
from music_player import *
from setting import *
from settings_window import Settings_Window
from start_window import Start_Window

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Копатель')
    size = width, height
    music = Music()
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    start = Start_Window(clock)
    if start.next_window == "setting":
        while start.next_window == "setting":
            setting_window = Settings_Window(clock, music)
            if setting_window.back == "back":
                start.next_window = start.main_cycle(clock)
    if start.next_window == "game":
        grass = Grass(all_sprites)
        digger = Digger(all_sprites)
        mine = Mine(all_sprites)
        bg = pygame.transform.scale(load_image("texture/sky.png"), (width, height * 2 // 3))
        screen.blit(bg, (0, 0))
        while True:
            flag = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    flag = True
                    digger.update(event.key, flag)
                if event.type == pygame.KEYUP:
                    flag = False
                    digger.update(event.key, flag)
            screen.blit(bg, (0, 0))
            all_sprites.update(grass, mine)
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
