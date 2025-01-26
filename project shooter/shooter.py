import pygame
import os
import sys
import random

from pygame.constants import K_DOWN, K_LEFT, K_UP, K_RIGHT


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sh, sheet, columns, rows, x, y):
        super().__init__(sh.all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.shend(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def update(self):
        self.flag += 1
        if self.flag == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.flag = 0


class Camera:
    # зададим начальный сдвиг камеры
    def init(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - sh.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - sh.height // 2)


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


class Tile(pygame.sprite.Sprite):
    def __init__(self, sh, tile_type, pos_x, pos_y):
        super().__init__(sh.all_sprites)
        tile_images = {
            'fin': sh.load_image('fin.png'),
            'wall': sh.load_image('preg.png'),
            'empty': sh.load_image('grass.jpg')
        }

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            sh.tile_width * pos_x, sh.tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    def __init__(self, sh, pos):
        super().__init__(sh.player_group)
        self.choose = "pistol1.png"  # choose
        self.image = sh.load_image(self.choose)
        self.rect = self.image.get_rect()
        self.sh = sh
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            self.sh.tile_width * pos[0] + 15, self.sh.tile_height * pos[1] + 5)

    def update(self):
        print(sh.dir)
        self.rect.x += sh.dir[0]
        self.rect.y += sh.dir[1]
        if pygame.sprite.spritecollideany(self, self.sh.tiles_group):
            self.rect.x -= sh.dir[0]
            self.rect.y -= sh.dir[1]


class ShooterGame(pygame.sprite.Sprite):
    def __init__(self, *group):
        pygame.init()
        self.dir = (0, 0)
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.width, self.height = 600, 600
        self.tile_width = self.tile_height = 50
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.camera = Camera()
        pygame.display.set_caption('ShooterGame')
        self.hero, level_x, level_y = self.generate_level(self.load_level('map.txt'))
        self.fps = 30

    def run_game(self):
        run = True
        live = 3
        l = 1

        while run:
            if l == 1:
                self.start_screen()
                l = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    live -= 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.dir = (0, self.tile_height)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.dir = (0, -self.tile_height)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.dir = (-self.tile_width, 0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.dir = (self.tile_width, 0)
                self.camera.update(self.hero)
                for sprite in self.player_group:
                    self.camera.apply(sprite)

                self.all_sprites.draw(self.screen)
                self.tiles_group.draw(self.screen)
                self.player_group.update()
                self.player_group.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(self.fps)

                # обновляем положение всех спрайтов



            if live == 0:
                self.end_screen()
                live = 3
                l = 1




    def terminate(self):
        pygame.quit()
        sys.exit()





    def die_screen(self):
        self.image = load_image('fie.webp')


    def load_level(self, filename):
        filename = "photo/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '#':
                    self.tiles_group.add(Tile(self, 'wall', x, y))
                elif level[y][x] == 'F':
                    self.tiles_group.add(Tile(self, 'fin', x, y))
                elif level[y][x] == '@':
                    Tile(self, 'empty', x, y)
                    new_player = Hero(self, (x, y))
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


    def load_image(self, name, colorkey=None):
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
        """else:
            image = image.convert_alpha()"""
        return image


    def start_screen(self):
        self.screen.fill(pygame.Color('red'))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)


    def end_screen(self):
        self.screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(self.load_image('fie.webp'), (self.width, self.height - 200))
        self.screen.blit(fon, (-40, 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)





if __name__ == '__main__':
    sh = ShooterGame()
    #sh.start_screen()
    sh.run_game()
    sh.player_group()
    sh.end_screen()