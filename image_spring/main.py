import sys

import pygame as pg
from pygame import Vector2, Rect

from image_spring.candy_dispenser import Spring
from menu.menu import Menu


def on_push():
    print("pushed")
    spring.shrink()


def on_pop():
    print("popped")
    spring.grow()


def on_peek():
    print("peeked")


def on_is_empty():
    print("is empty checked")


def on_len():
    print("len checked")


pg.init()
SCREEN_SIZE = Vector2(800, 600)
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Stack visualization")

clock = pg.time.Clock()
MAX_FPS = 60

spring = Spring(mid_bottom=Vector2(SCREEN_SIZE.x / 4, SCREEN_SIZE.y - 10))

container_rect = Rect(Vector2(0, 0), Vector2(250, spring.rect.height + 20))
container_rect.midbottom = Vector2(SCREEN_SIZE.x / 4, SCREEN_SIZE.y)

buttons = [
    Menu.TextButton("S.push()", Vector2(20, 420), on_push, 35),
    Menu.TextButton("S.pop()", Vector2(20, 500), on_pop, 35),
    Menu.TextButton("S.peek()", Vector2(150, 420), on_peek, 35),
    Menu.TextButton("S.isEmpty()", Vector2(150, 500), on_is_empty, 35),
    Menu.TextButton("len(S)", Vector2(280, 420), on_len, 35)
]
menu = Menu(buttons, Vector2(SCREEN_SIZE.x / 2, SCREEN_SIZE.y), 35, SCREEN_SIZE.x / 2)

while True:
    for event in pg.event.get(exclude=pg.MOUSEBUTTONUP):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    screen.fill("yellow")
    pg.draw.rect(screen, "White", container_rect, 10)

    menu.render(screen)

    spring.render(screen)

    pg.display.flip()

    clock.tick(MAX_FPS)
