import pygame as pg
from pygame.math import Vector2

import sys

pg.init()

MAX_FPS = 60
clock = pg.time.Clock()

SCREEN_SIZE = Vector2(1000, 800)
screen = pg.display.set_mode(SCREEN_SIZE)

start = Vector2(100, 100)
stop = Vector2(500, 500)


PLAYER_SIZE = Vector2(50, 50)

player = pg.Rect(start, PLAYER_SIZE)
t = 0


def move_player():
    global player, start, stop, t
    t += 0.005
    t = pg.math.clamp(t, 0, 1)

    player.topleft = start.lerp(stop, t)

    if player.topleft == stop:
        t = 0
        start, stop = stop, start


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    screen.fill("White")
    pg.draw.circle(screen, "Red", start, 10)
    pg.draw.circle(screen, "Blue", stop, 10)

    move_player()
    pg.draw.rect(screen, "Pink", player)

    pg.display.update()
    clock.tick(MAX_FPS)
