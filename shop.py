import pygame as pg


class Shop(pg.sprite.Sprite):
    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.selected_tower = None
        self.activated = False
        self.screen = screen
        sc_size = screen.get_size()
        self.image = pg.Surface((sc_size[0], sc_size[1] // 8))
        self.rect = self.image.get_rect(centerx=sc_size[0] // 2, bottom=sc_size[1] - 10)

        self.towers_images = (
            pg.image.load('images/башня лучников 1 уровня сверху.png'),
            pg.image.load('images/башня лучников 2 уровня сверху.png'),
            pg.image.load('images/башня лучников 3 уровня сверху.png'),
            pg.image.load('images/башня магов 1 уровня сверху.png'),
            pg.image.load('images/башня магов 2 уровня сверху.png'),
            pg.image.load('images/башня магов 3 уровня сверху.png'),
            pg.image.load('images/башня пушек 1 уровня сверху.png'),
            pg.image.load('images/башня пушек 2 уровня сверху.png'),
            pg.image.load('images/башня пушек 3 уровня сверху.png')
        )

        self.towers_pos = tuple((self.towers_images[i].get_rect(
                           centerx=self.rect.x + self.rect.width // 10 + self.rect.width // 10 * i,
                           centery=self.rect.y + self.rect.height // 2)
                           for i in range(len(self.towers_images))))

        self.tower_types = {1: "Arrow", 2: "Magic", 3: "Cannon"}
        self.tower_level = None
        self.tower_type = None

    def __new_draw(self):
        image_size = self.towers_images[0].get_size()
        if self.activated:
            self.screen.blit(self.selected_tower, (pg.mouse.get_pos()[0] - image_size[0] // 2,
                                                   pg.mouse.get_pos()[1] - image_size[1] // 2))

        pg.draw.rect(self.screen, "white", self.rect, 5, 90)
        for i in range(len(self.towers_images)):
            self.screen.blit(self.towers_images[i], self.towers_pos[i])

    def __choise(self):
        m_pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()[0]
        for i in range(len(self.towers_pos)):
            if self.towers_pos[i].collidepoint(m_pos) and click:
                self.activated = True
                self.selected_tower = self.towers_images[i]

                self.tower_level = i % 3 + 1
                self.tower_type = self.tower_types[i // 3 + 1]

    def update(self):
        self.__choise()
        self.__new_draw()