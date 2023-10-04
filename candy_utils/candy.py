from typing import Any

import pygame
from pygame import Vector2

from candy_utils.motion_state import MotionState


class Candy(pygame.sprite.Sprite):
    SIZE = Vector2(150, 50)
    VERTICAL_START = 600
    HEIGHT_CHANGE = 30
    INTERPOLATION_SPEED = 0.05
    VERTICAL_START_CHANGE = 40

    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = pygame.Surface(Candy.SIZE)
        self.image.fill("Red")
        self.rect = self.image.get_rect(midbottom=(600, Candy.VERTICAL_START))

        self.motion_state: MotionState = MotionState.REST
        self.current_position: Vector2 = Vector2(self.rect.midbottom)
        self.next_position: Vector2 | None = None
        self.t = 0

        print(f"{Candy.VERTICAL_START=}")

    def move_up(self):
        self.motion_state = MotionState.UP
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] - Candy.HEIGHT_CHANGE)

    def move_down(self):
        self.motion_state = MotionState.DOWN
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] + Candy.HEIGHT_CHANGE)

    def move(self):
        if self.motion_state is not MotionState.REST:
            self.t += Candy.INTERPOLATION_SPEED
            self.t = pygame.math.clamp(self.t, 0, 1)
            self.rect.midbottom = self.current_position.lerp(self.next_position, self.t)

            if self.rect.midbottom == self.next_position:
                self.current_position = self.next_position
                self.t = 0

                # if self.motion_state is MotionState.UP:
                #     Candy.increment_vertical_start()
                # elif self.motion_state is MotionState.DOWN:
                #     Candy.decrement_vertical_start()

                self.motion_state = MotionState.REST

    @classmethod
    def decrement_vertical_start(cls):
        Candy.VERTICAL_START -= Candy.VERTICAL_START_CHANGE

    @classmethod
    def increment_vertical_start(cls):
        Candy.VERTICAL_START += Candy.VERTICAL_START_CHANGE

    def update(self, *args: Any, **kwargs: Any):
        self.move()
