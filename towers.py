import pygame as pg

import troll


class Bullet(pg.sprite.Sprite):
    def __init__(self, start_pos, speed, damage, image_path):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(center=start_pos)
        self.dir = pg.Vector2()
        self.speed = speed
        self.damage = damage


    def move(self):
        self.rect.centerx += self.dir.x * self.speed
        self.rect.centery += self.dir.y * self.speed

    def change_dir(self, trolls: pg.sprite.Group):
        start_range = 1000
        if trolls.sprites():
            start_troll = trolls.sprites()[0]

        # Определение ближайшего тролля
        for troll in trolls.sprites():
            min_range = min(start_range, abs(troll.rect.x - self.rect.centerx) + abs(troll.rect.y - self.rect.centery))
            if min_range < start_range:
                start_range = min_range
                start_troll = troll

        # Изменение направления в сторону ближайшего тролля
        if trolls.sprites():
            self.dir.x = start_troll.rect.x - self.rect.centerx + 50
            self.dir.y = start_troll.rect.y - self.rect.centery + 50

            if self.dir.magnitude() != 0:
                self.dir = self.dir.normalize()

    def update(self, trolls):
        pg.display.get_surface().blit(self.image, self.rect)
        self.change_dir(trolls)
        self.move()


class Tower(pg.sprite.Sprite):
    prices = {
        'Arrow': (100, 250, 1000),
        'Magic': (100, 250, 1000),
        'Cannon': (100, 250, 1000)
    }

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = None
        self.rect = None
        self.pos = pos
        self.bullet_image = None

        self.price = 0
        self.timer = 0
        self.range = 0
        self.speed = 0
        self.damage = 0
        self.reload_time = 0

        self.ammo = pg.sprite.Group()

    def shoot(self, trolls: pg.sprite.Group):
        for troll in trolls.sprites():
            if abs(self.rect.centerx - troll.rect.centerx) <= self.range and\
                    abs(self.rect.centery - troll.rect.centery) <= self.range\
                    and self.timer >= self.reload_time:
                self.ammo.add(Bullet(self.rect.center, self.speed, self.damage, self.bullet_image))
                self.timer = 0
            if self.ammo and self.ammo.sprites()[0].rect.colliderect(troll.rect):
                self.ammo.sprites()[0].kill()
        if not trolls.sprites():
            self.ammo.empty()

    def draw(self):
        pg.display.get_surface().blit(self.image, self.rect)

    def reload(self):
        self.timer += 1

    def update(self, trolls):
        self.shoot(trolls)
        self.draw()
        self.reload()
        self.ammo.update(trolls)


class ArrowTower(Tower):
    def __init__(self, pos, level, *groups):
        super().__init__(pos, *groups)
        self.bullet_image = 'images/стрела.png'

        self.level = level
        self.characteristics = {
            1: (2, 3, 100, 400, 100, pg.image.load('images/башня лучников 1 уровня сверху.png')),
            2: (4, 2, 150, 450, 250, pg.image.load('images/башня лучников 2 уровня сверху.png')),
            3: (6, 1, 400, 500, 1000, pg.image.load('images/башня лучников 3 уровня сверху.png')),
        }

        self.speed = self.characteristics[level][0]
        self.reload_time = self.characteristics[level][1] * 120
        self.timer = 0
        self.damage = self.characteristics[level][2]
        self.range = self.characteristics[level][3]
        self.price = self.characteristics[level][4]

        self.image = self.characteristics[level][5]
        self.rect = self.image.get_rect(center=pos)


class MagicTower(Tower):
    def __init__(self, pos, level, *groups):
        super().__init__(pos, *groups)
        self.bullet_image = 'images/огонь.png'

        self.characteristics = {
            1: (1, 3, 100, 450, 100, pg.image.load('images/башня магов 1 уровня сверху.png')),
            2: (2, 3, 200, 500, 250, pg.image.load('images/башня магов 2 уровня сверху.png')),
            3: (3, 2, 500, 600, 1000, pg.image.load('images/башня магов 3 уровня сверху.png')),
        }

        self.speed = self.characteristics[level][0]
        self.reload_time = self.characteristics[level][1] * 120
        self.timer = 0
        self.damage = self.characteristics[level][2]
        self.range = self.characteristics[level][3]
        self.price = self.characteristics[level][4]

        self.image = self.characteristics[level][5]
        self.rect = self.image.get_rect(center=pos)


class CannonTower(Tower):
    def __init__(self, pos, level, *groups):
        super().__init__(pos, *groups)
        self.bullet_image = 'images/пушечное ядро.png'

        self.characteristics = {
            1: (3, 4,  500,  500,  100, pg.image.load('images/башня пушек 1 уровня сверху.png')),
            2: (5, 4,  1000, 650, 250, pg.image.load('images/башня пушек 2 уровня сверху.png')),
            3: (10, 3,  3000, 700, 1000, pg.image.load('images/башня пушек 3 уровня сверху.png')),
        }

        self.speed = self.characteristics[level][0]
        self.reload_time = self.characteristics[level][1] * 120
        self.timer = 0
        self.damage = self.characteristics[level][2]
        self.range = self.characteristics[level][3]
        self.price = self.characteristics[level][4]

        self.image = self.characteristics[level][5]
        self.rect = self.image.get_rect(center=pos)
