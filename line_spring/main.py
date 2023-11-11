import sys

import pygame as pg
from pygame import Vector2

from candy_utils.menu import Menu
from line_spring.candy_dispenser import CandyDispenser

pg.init()
pg.display.set_caption("Stack visualisation")

MAX_FPS = 60
SCREEN_SIZE = Vector2(800, 600)
clock = pg.time.Clock()

screen = pg.display.set_mode(Vector2(SCREEN_SIZE))
candy_dispenser = CandyDispenser(Vector2(0, 0), Vector2(SCREEN_SIZE.x / 2, SCREEN_SIZE.y))


def on_push():
    global candy_dispenser, menu
    push_output = candy_dispenser.add_candy()
    menu.update_command_output(push_output)


def on_pop():
    global candy_dispenser, menu
    pop_output = candy_dispenser.remove_candy()
    menu.update_command_output(pop_output)


def on_peek():
    global candy_dispenser, menu
    top_output = candy_dispenser.peek()
    menu.update_command_output(top_output)


def on_is_empty():
    global candy_dispenser, menu
    is_empty_output = candy_dispenser.is_empty()
    menu.update_command_output(is_empty_output)


def on_len():
    number_of_candies = candy_dispenser.number_of_candies()
    menu.update_command_output(number_of_candies)


buttons = [
    Menu.TextButton("S.push()", Vector2(20, 420), on_push, 35),
    Menu.TextButton("S.pop()", Vector2(20, 500), on_pop, 35),
    Menu.TextButton("S.peek()", Vector2(150, 420), on_peek, 35),
    Menu.TextButton("S.isEmpty()", Vector2(150, 500), on_is_empty, 35),
    Menu.TextButton("len(S)", Vector2(280, 420), on_len, 35)
]
menu = Menu(buttons, Vector2(SCREEN_SIZE.x / 2, SCREEN_SIZE.y), 35, SCREEN_SIZE.x / 2)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
            for button in buttons:
                if button.is_hover():
                    button.click()

    screen.fill("Black")
    candy_dispenser.render(screen)
    menu.render(screen)

    pg.display.flip()
    clock.tick(MAX_FPS)
