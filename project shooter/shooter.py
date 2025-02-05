import pygame
import os
import sys
import random

from pygame.constants import K_DOWN, K_LEFT, K_UP, K_RIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, sh, x, y, direction):
        super().__init__(sh.bullets_group, sh.all_sprites)
        self.sh = sh
        self.image = pygame.transform.scale(sh.load_image('bullet.png'), (15, 15))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.direction = direction

    def update(self):
        if self.direction == 0:  # Вправо
            self.rect.x += self.speed
        elif self.direction == 1:  # Вверх
            self.rect.y -= self.speed
        elif self.direction == 2:  # Влево
            self.rect.x -= self.speed
        elif self.direction == 3:  # Вниз
            self.rect.y += self.speed

        # Удаляем пулю, если она выходит за границы экрана
        if not self.sh.screen.get_rect().colliderect(self.rect):
            self.kill()
        if pygame.sprite.spritecollide(self, self.sh.tiles_group, False):
            self.kill()

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
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
        self.type = tile_type
        tile_images = {
            'fin': sh.load_image('fin.png'),
            'wall': sh.load_image('preg.png'),
            'empty': sh.load_image('grass.jpg'),
            'base': sh.load_image('basement.jpg'),
            'wl': sh.load_image('wall_left.jpg'),
            'wu': sh.load_image('wall_up.jpg'),
            'wd': sh.load_image('wall_down.jpg'),
            'wr': sh.load_image('wall_right.jpg'),
            'stair': sh.load_image('stair.jpg'),
            'pit': sh.load_image('pit.jpg'),
            'hatch': sh.load_image('hatch.jpg'),
            'pol': sh.load_image('pol.jpg'),
            'black': sh.load_image('black.jpg'),
            'rd': sh.load_image('wall_colliderd.jpg'),
            'ru': sh.load_image('wall_collideru.jpg'),
            'lu': sh.load_image('wall_collidelu.jpg'),
            'ld': sh.load_image('wall_collideld.jpg'),
            'ch': sh.load_image('chest.jpg'),
            'sv': sh.load_image('svecha.jpg')

        }
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            sh.tile_width * pos_x, sh.tile_height * pos_y)


class Hero(pygame.sprite.Sprite):
    hero_images = {'up': 'pistol1_up.png',
                   'down': 'pistol1_down.png',
                   'r': 'pistol1.png',
                   'l': 'pistol1_left.png'}

    def shoot(self):
        bullet_x, bullet_y = self.rect.center
        Bullet(self.sh, bullet_x, bullet_y, self.sh.dir)

    def __init__(self, sh, pos):
        super().__init__(sh.player_group, sh.all_sprites)
        self.sh = sh
        self.image = pygame.transform.scale(sh.load_image(Hero.hero_images['r']),
                                            (self.sh.tile_width, self.sh.tile_height))

        self.rect = self.image.get_rect()

        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            self.sh.tile_width * pos[0], self.sh.tile_height * pos[1])

    def rotate(self):
        if self.sh.dir == 0:
            self.image = pygame.transform.scale(sh.load_image(Hero.hero_images['r']),
                                                (self.sh.tile_width, self.sh.tile_height))
        if self.sh.dir == 1:
            self.image = pygame.transform.scale(sh.load_image(Hero.hero_images['up']),
                                                (self.sh.tile_width, self.sh.tile_height))
        if self.sh.dir == 2:
            self.image = pygame.transform.scale(sh.load_image(Hero.hero_images['l']),
                                                (self.sh.tile_width, self.sh.tile_height))
        if self.sh.dir == 3:
            self.image = pygame.transform.scale(sh.load_image(Hero.hero_images['down']),
                                                (self.sh.tile_width, self.sh.tile_height))
        pygame.display.flip()

    def move(self, pos):
        self.rotate()
        self.rect.x += pos[0]
        self.rect.y += pos[1]
        if pygame.sprite.spritecollide(self, self.sh.tiles_group, False):
            print("hi")
            self.rect.x -= pos[0]
            self.rect.y -= pos[1]
        if pygame.sprite.spritecollide(self, self.sh.F, False):
            print("yes")
            sh.end_screen()
        if pygame.sprite.spritecollide(self, self.sh.L, False):
            print(pygame.sprite.spritecollide(self, self.sh.L, False)[0].type)
            if pygame.sprite.spritecollide(self, self.sh.L, False)[0].type == "stair":
                self.sh.dir = int()
                self.sh.b = int()
                self.sh.m = 'map1.txt'
                self.sh.all_sprites = pygame.sprite.Group()
                self.sh.tiles_group = pygame.sprite.Group()
                self.sh.bullets_group = pygame.sprite.Group()
                self.sh.til = pygame.sprite.Group()
                self.sh.F = pygame.sprite.Group()
                self.sh.L = pygame.sprite.Group()
                self.sh.player_group = pygame.sprite.Group()
                self.sh.camera = Camera()
                self.sh.hero, level_x, level_y = self.sh.generate_level(self.sh.load_level(self.sh.m))
                sh.run_game()

            if pygame.sprite.spritecollide(self, self.sh.L, False)[0].type == "pit":
                print("yes")
                sh.endall()
    def test(self):
        if pygame.sprite.spritecollide(self, self.sh.L, False):
            print("y")
            self.sh.m = "map3.txt"
            self.sh.all_sprites = pygame.sprite.Group()
            self.sh.tiles_group = pygame.sprite.Group()
            self.sh.bullets_group = pygame.sprite.Group()
            self.sh.til = pygame.sprite.Group()
            self.sh.F = pygame.sprite.Group()
            self.sh.L = pygame.sprite.Group()
            self.sh.player_group = pygame.sprite.Group()
            self.sh.screen.fill((17, 11, 25))
            self.sh.hero, level_x, level_y = self.sh.generate_level(self.sh.load_level(self.sh.m))


class ShooterGame(pygame.sprite.Sprite):
    def __init__(self, *group):
        pygame.init()
        self.dir = int()
        self.l = 1
        self.b = int()
        self.m = 'map1.txt'
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.til = pygame.sprite.Group()
        self.F = pygame.sprite.Group()
        self.L = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.width, self.height = 600, 600
        self.tile_width = self.tile_height = 50
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.camera = Camera()
        pygame.display.set_caption('ShooterGame')
        self.hero, level_x, level_y = self.generate_level(self.load_level(self.m))
        self.fps = 30

    def run_game(self):
        run = True
        live = 3

        while run:
            if self.l == 1:
                self.start_screen()
                self.l = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.hero.test()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    live -= 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.dir = 3
                    self.hero.move((0, self.tile_height))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.dir = 1
                    self.hero.move((0, -self.tile_height))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.dir = 2
                    self.hero.move((-self.tile_width, 0))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.dir = 0
                    self.hero.move((self.tile_width, 0))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.hero.shoot()
                if event.type == pygame.KEYDOWN:
                    print(event.key)
                self.camera.update(self.hero)
                for sprite in self.all_sprites:
                    self.camera.apply(sprite)

            self.bullets_group.update()
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

    def endall(self):
        print("ye")
        self.m = "map31.txt"
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.til = pygame.sprite.Group()
        self.F = pygame.sprite.Group()
        self.L = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.screen.fill((17, 11, 25))
        self.hero, level_x, level_y = self.generate_level(self.load_level(self.m))

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
        k = ""
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    k = "empty"
                    Tile(self, 'empty', x, y)
                elif level[y][x] == 'H':
                    Tile(self, 'hatch', x, y)
                elif level[y][x] == 'V':
                    Tile(self, 'sv', x, y)
                elif level[y][x] == 'J':
                    Tile(self, 'ch', x, y)
                elif level[y][x] == '(':
                    Tile(self, 'ld', x, y)
                elif level[y][x] == ')':
                    Tile(self, 'ru', x, y)
                elif level[y][x] == '[':
                    Tile(self, 'lu', x, y)
                elif level[y][x] == ']':
                    Tile(self, 'rd', x, y)
                elif level[y][x] == ',':
                    self.tiles_group.add(Tile(self, 'black', x, y))
                elif level[y][x] == '*':
                    k = "pol"
                    Tile(self, 'pol', x, y)
                elif level[y][x] == '#':
                    self.tiles_group.add(Tile(self, 'wall', x, y))
                elif level[y][x] == 'D':
                    self.tiles_group.add(Tile(self, 'wd', x, y))
                elif level[y][x] == 'L':
                    self.tiles_group.add(Tile(self, 'wl', x, y))
                elif level[y][x] == 'U':
                    self.tiles_group.add(Tile(self, 'wu', x, y))
                elif level[y][x] == 'R':
                    self.tiles_group.add(Tile(self, 'wr', x, y))
                elif level[y][x] == 'F':
                    self.F.add(Tile(self, 'fin', x, y))
                elif level[y][x] == 'B':
                    self.L.add(Tile(self, 'base', x, y))
                elif level[y][x] == 'S':
                    self.L.add(Tile(self, 'stair', x, y))
                elif level[y][x] == 'P':
                    self.L.add(Tile(self, 'pit', x, y))
                elif level[y][x] == '@':
                    Tile(self, k, x, y)
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
        intro_text = ["                            ShootOGEym", "",
                      "                 Это игра с повторением заданий экзаменов",
                      "                 Побеждайте монстров,",
                      "                 Переходите на локации,",
                      "                 Открывайте сундуки,",
                      "                 Выполняйте задания", "",
                      "                         Нажмите G, чтобы начать игру"]
        fon = pygame.transform.scale(self.load_image('startscreen.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('Brown'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    return event.key
            pygame.display.flip()
            self.clock.tick(self.fps)

    def end_screen(self, time=1, timez=7):

        intro_text = [f"Общее время: {time}",
                      f"Время потраченное на задания: {timez}"]

        fon = pygame.transform.scale(self.load_image('fie.webp'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)
        fon = pygame.transform.scale(self.load_image('fie.webp'), (self.width, self.height - 200))
        self.screen.blit(fon, (-20, 150))

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
    sh.start_screen()
    sh.run_game()