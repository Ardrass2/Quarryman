import pygame_gui

from function import *
from setting import *


class Inside_Shop:
    def __init__(self, clock):
        self.window_surface = pygame.display.set_mode((width, height))
        self.bg = pygame.transform.scale(load_image("texture/in_shop.png"), (width, height))
        self.manager = pygame_gui.UIManager((width, height))
        self.manager.get_theme().load_theme('theme.json')
        self.mine_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width // 2 - (width * 0.25), height // 2 - (height * 0.05)),
                                      (width * 0.5, height * 0.1)),
            text="Шахты", manager=self.manager)
        self.upgrade_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (width // 2 - (width * 0.25), height // 2 - (height * 0.05) + height * 0.1),
                (width * 0.5, height * 0.1)),
            text="Улучшения", manager=self.manager)
        self.cycle(clock)

    def cycle(self, clock):
        while True:
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.mine_button:
                        self.mine_button.kill()
                    if event.ui_element == self.upgrade_button:
                        self.upgrade_button.kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
            time_delta = clock.tick(FPS) / 1000.0
            self.manager.update(time_delta=time_delta)
            self.window_surface.blit(self.bg, (0, 0))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
            pygame.display.flip()