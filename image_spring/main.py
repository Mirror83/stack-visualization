import sys

import pygame as pg
from pygame import Vector2

from image_spring.candy_dispenser import CandyDispenser
from menu.menu import Menu


def on_push():
    print("pushed")
    output, is_error = candy_dispenser.push_candy()
    menu.update_command_output(output, is_error)


def on_pop():
    print("popped")
    output, is_error = candy_dispenser.pop_candy()
    menu.update_command_output(output, is_error)


def on_peek():
    print("peeked")
    output, is_error = candy_dispenser.peek()
    menu.update_command_output(output, is_error)


def on_is_empty():
    print("is empty checked")
    output = candy_dispenser.is_empty()
    menu.update_command_output(output)


def on_len():
    print("len checked")
    output = candy_dispenser.len()
    menu.update_command_output(output)


pg.init()
SCREEN_SIZE = Vector2(800, 600)
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Stack visualization")

clock = pg.time.Clock()
MAX_FPS = 60

candy_dispenser = (
    CandyDispenser(Vector2(SCREEN_SIZE.x / 4, SCREEN_SIZE.y)))

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

    screen.fill("Lightblue")

    menu.render(screen)

    candy_dispenser.render(screen)

    pg.display.flip()

    clock.tick(MAX_FPS)
