import pygame
import os
import sys
import random
import PIL

from pygame.constants import K_DOWN, K_LEFT, K_UP, K_RIGHT


def load_image(name, colorkey=None):
    fullname = os.path.join('photo', name)
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


class ShooterGame(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('1location.jpg')
        self.image = load_image('pistol1.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


    def update(self, pos):
        self.rect.x += pos[0]
        self.rect.y += pos[1]