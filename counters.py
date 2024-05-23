import pygame as pg

pg.init()


class Counter(pg.sprite.Sprite):
    def __init__(self, text: str, pos: tuple, start_count):
        super().__init__()
        self.points = start_count
        self.text = text

        self.font = pg.font.SysFont('Arial', 30, True, True)
        self.image = self.font.render(f'{self.text}: {self.points}', True, 'red', 'black')
        self.rect = self.image.get_rect(centerx=pos[0], centery=pos[1])

    def add_points(self, points: int):
        self.points += points

    def update(self):
        self.image = self.font.render(f'{self.text}: {self.points}', True, 'red', 'black')


