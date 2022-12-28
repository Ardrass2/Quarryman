from function import *
from setting import *


class Digger(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image("texture/character.png"), (width * 0.2, height * 0.3))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.top = height * 2 // 3 - height * 0.25
        self.rect.left = width // 2
        self.some = False
        self.left_or_right = 0
        self.speed = 7

    def update(self, *args):
        if type(args[0]) != int and type(args[1]) != int:
            if not pygame.sprite.collide_mask(self, args[0]):
                self.rect = self.rect.move(0, 1)
                x, y = self.rect[0], self.rect[1]
            if pygame.sprite.collide_mask(self, args[1]):
                self.speed = 0
        if not args[1]:
            self.left_or_right = 0
            print(self.left_or_right)
        elif args[0] == pygame.K_d:
            if not self.some:
                self.some = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = 1
        elif args[0] == pygame.K_a:
            if self.some:
                self.some = False
                self.image = pygame.transform.flip(self.image, True, False)
            self.left_or_right = -1
        if not self.rect[0] >= width * 0.87 and not self.rect[0] <= -(width * 0.06):
            self.rect = self.rect.move(self.left_or_right * self.speed, 0)
