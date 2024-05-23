import pygame as pg
from map import Cell, RoadCell, cells
from shop import Shop
from towers import Tower, ArrowTower, MagicTower, CannonTower
from troll import CommonTroll, FastTroll, LowArmoredTroll, MediumArmoredTroll, HardArmoredTroll
from random import choice
from counters import Counter

pg.init()
main_music = pg.mixer.Sound('music/MainMusic.mp3')
victory_sound = pg.mixer.Sound('music/Victory.mp3')

screen = pg.display.set_mode((700, 700), pg.RESIZABLE)
fps = pg.time.Clock()

main_map = pg.sprite.Group(
    *(Cell(screen, (i, j))
      for i in range(0, 700, 100)
      for j in range(0, 600, 100)
      if not cells[j // 100][i // 100])
)

road_map = pg.sprite.Group(
    *(RoadCell(screen, (i, j))
      for i in range(0, 700, 100)
      for j in range(0, 600, 100)
      if cells[j // 100][i // 100])
)

trolls = pg.sprite.Group()

shop = Shop(screen)

towers = pg.sprite.Group()

counters = pg.sprite.Group(
    Counter('Тролли', (screen.get_size()[0] // 2, 15), 0),
    Counter('Монеты', (screen.get_size()[0] // 2, 45), 500),
    Counter('Жизни', (screen.get_size()[0] - 100, 15), 5)
)


def new_troll(troll_out_counter, troll_spawn_timer):
    if troll_spawn_timer >= 2:
        if 0 <= troll_out_counter < 30:
            return CommonTroll(screen, road_map, trolls)
        elif troll_out_counter < 60:
            return choice([CommonTroll(screen, road_map, trolls), FastTroll(screen, road_map, trolls)])
        elif troll_out_counter < 100:
            return FastTroll(screen, road_map, trolls)
        elif troll_out_counter < 180:
            return LowArmoredTroll(screen, road_map, trolls)
        elif troll_out_counter < 280:
            return MediumArmoredTroll(screen, road_map, trolls)
        elif troll_out_counter < 400:
            return HardArmoredTroll(screen, road_map, trolls)


def run_game():
    troll_spawn_timer = 1
    troll_out_counter = 0
    main_music.play(-1)
    while True:
        if troll_out_counter % 100 == 0 and troll_out_counter != 0:
            victory_sound.play(1)
        troll_spawn_timer += counters.sprites()[0].points / 5000 + 1 / 120  # Исправить
        screen.fill("black")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        if shop.activated:
            for cell in main_map.sprites():
                if cell.clicked() and not cell.busy:
                    if shop.tower_type == "Arrow" and\
                       Tower.prices['Arrow'][shop.tower_level - 1] <= counters.sprites()[1].points:
                        ArrowTower(cell.rect.center, shop.tower_level, towers)
                        counters.sprites()[1].points -= Tower.prices['Arrow'][shop.tower_level - 1]
                        cell.busy = True
                    elif shop.tower_type == "Magic" and\
                       Tower.prices['Magic'][shop.tower_level - 1] <= counters.sprites()[1].points:
                        MagicTower(cell.rect.center, shop.tower_level, towers)
                        counters.sprites()[1].points -= Tower.prices['Magic'][shop.tower_level - 1]
                        cell.busy = True
                    elif shop.tower_type == "Cannon" and\
                       Tower.prices['Cannon'][shop.tower_level - 1] <= counters.sprites()[1].points:
                        CannonTower(cell.rect.center, shop.tower_level, towers)
                        counters.sprites()[1].points -= Tower.prices['Cannon'][shop.tower_level - 1]
                        CannonTower(cell.rect.center, shop.tower_level, towers)
                        cell.busy = True

        main_map.draw(screen)
        road_map.draw(screen)
        shop.update()
        trolls.update(towers)
        towers.update(trolls)

        for troll in trolls.sprites():
            if troll.is_death():
                trolls.remove(troll)
                troll_out_counter += 1
                counters.sprites()[1].add_points(troll.points)
                counters.sprites()[0].add_points(1)
                print(troll_out_counter)
            elif troll.is_out():
                trolls.remove(troll)
                counters.sprites()[2].add_points(-1)

        if not counters.sprites()[2].points:
            break

        new_troll(troll_out_counter, troll_spawn_timer)
        if troll_spawn_timer >= 2:
            troll_spawn_timer = 0


        counters.update()
        counters.draw(screen)
        fps.tick(120)
        pg.display.update()


run_game()
