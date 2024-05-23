import pygame as pg
cells = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0]]


class Cell(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, pos: tuple):
        super().__init__()

        self.busy = False
        sc_size = screen.get_size()
        self.image = pg.Surface((sc_size[0] // 7 - 10, sc_size[1] // 7 - 10))
        self.image.fill("white")
        self.rect = self.image.get_rect(x=pos[0] + 5, y=pos[1] + 5)


    def clicked(self):
        click = pg.mouse.get_pressed()[0]
        m_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(m_pos) and click:
            return True


class RoadCell(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface, pos: tuple):
        super().__init__()
        sc_size = screen.get_size()
        self.image = pg.Surface((sc_size[0] // 7, sc_size[1] // 7))
        self.image.fill("brown")
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])


