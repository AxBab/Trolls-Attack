import pygame as pg
from random import choice

import towers


class Troll(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(*groups)
        self.group = groups

        self.road_map = road_map.sprites()
        self.screen = screen
        self.max_health = 0
        self.health = 0
        self.images = (
            pg.image.load('images/обычный тролль сверху.png'),
            pg.image.load('images/быстрый тролль сверху.png'),
            pg.image.load('images/тролль в лёгкой броне сверху.png'),
            pg.image.load('images/тролль в средней броне сверху.png'),
            pg.image.load('images/тролль в тяжёлой броне сверху.png'),
        )

        self.image = choice(self.images)
        self.rect = self.image.get_rect(centerx=road_map.sprites()[0].rect.centerx,
                                        centery=road_map.sprites()[0].rect.centery)
        self.speed = 1
        self.points = 0

    def move(self):
        self.rect.x += self.speed

    def get_hit(self, towers: pg.sprite.Group):
        for tower in towers.sprites():
            for bullet in tower.ammo:
                if bullet.rect.colliderect(self.rect):
                    self.health -= tower.damage

    def is_out(self):
        return self.rect.centerx >= 700


    def is_death(self):
        return self.health <= 0

    def update(self, towers):
        self.screen.blit(self.image, self.rect)
        self.move()
        self.get_hit(towers)


class CommonTroll(Troll):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(screen, road_map, *groups)
        self.points = 50
        self.health = 150
        self.max_health = 150
        self.speed = 1
        self.image = pg.image.load('images/обычный тролль сверху.png')


class FastTroll(Troll):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(screen, road_map, *groups)
        self.points = 75
        self.health = 200
        self.max_health = 200
        self.speed = 2
        self.image = pg.image.load('images/быстрый тролль сверху.png')


class LowArmoredTroll(Troll):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(screen, road_map, *groups)
        self.points = 100
        self.health = 600
        self.max_health = 600
        self.speed = 1
        self.rect.size = (80, 100)
        self.image = pg.image.load('images/тролль в лёгкой броне сверху.png')


class MediumArmoredTroll(Troll):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(screen, road_map, *groups)
        self.points = 150
        self.health = 1500
        self.max_health = 1500
        self.speed = 1
        self.rect.size = (80, 100)
        self.image = pg.image.load('images/тролль в средней броне сверху.png')


class HardArmoredTroll(Troll):
    def __init__(self, screen: pg.Surface, road_map: pg.sprite.Group, *groups):
        super().__init__(screen, road_map, *groups)
        self.points = 250
        self.health = 4000
        self.max_health = 4000
        self.speed = 1
        self.rect.size = (80, 100)
        self.image = pg.image.load('images/тролль в тяжёлой броне сверху.png')
