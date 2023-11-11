from typing import Any

import pygame
from pygame import Vector2
from pygame.font import Font

from piston_spring.motion_state import MotionState


class SpriteCandy(pygame.sprite.Sprite):
    CANDY_COLORS = ["Red", "Purple", "Pink", "Yellow"]
    TOTAL_CANDIES = 0
    SIZE = Vector2(150, 50)
    BASE_VERTICAL_START = 600
    VERTICAL_START = 600
    HEIGHT_CHANGE = 30
    INTERPOLATION_SPEED = 0.05
    VERTICAL_START_CHANGE = 40
    TEXT_POSITION = Vector2(10, 10)

    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.number = SpriteCandy.TOTAL_CANDIES
        self.color = SpriteCandy.CANDY_COLORS[self.number % len(SpriteCandy.CANDY_COLORS)]
        self.image = pygame.Surface(SpriteCandy.SIZE)
        self.image.fill(self.color)
        print(f"candy: SpriteCandy.VERTICAL_START = {SpriteCandy.VERTICAL_START}")
        self.rect = self.image.get_rect(midbottom=(300, SpriteCandy.VERTICAL_START))

        self.label_surface = Font(None, 50). \
            render(str(self.number), True, "Black"). \
            convert_alpha()

        self.motion_state: MotionState = MotionState.REST
        self.current_position: Vector2 = Vector2(self.rect.midbottom)
        self.next_position: Vector2 | None = None
        self.t = 0

    def move_up(self):
        self.motion_state = MotionState.UP
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] - SpriteCandy.HEIGHT_CHANGE)

    def move_down(self):
        self.motion_state = MotionState.DOWN
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] + SpriteCandy.HEIGHT_CHANGE)

    def move(self):
        if self.motion_state is not MotionState.REST:
            self.t += SpriteCandy.INTERPOLATION_SPEED
            self.t = pygame.math.clamp(self.t, 0, 1)
            self.rect.midbottom = self.current_position.lerp(self.next_position, self.t)

            if self.rect.midbottom == self.next_position:
                self.current_position = self.next_position
                self.t = 0

                # if self.motion_state is MotionState.UP:
                #     SpriteCandy.increment_vertical_start()
                # elif self.motion_state is MotionState.DOWN:
                #     SpriteCandy.decrement_vertical_start()

                self.motion_state = MotionState.REST

    @classmethod
    def decrement_vertical_start(cls):
        SpriteCandy.VERTICAL_START -= SpriteCandy.VERTICAL_START_CHANGE
        SpriteCandy.TOTAL_CANDIES += 1

    @classmethod
    def increment_vertical_start(cls):
        SpriteCandy.VERTICAL_START = min(SpriteCandy.BASE_VERTICAL_START,
                                         SpriteCandy.VERTICAL_START + SpriteCandy.VERTICAL_START_CHANGE)
        SpriteCandy.TOTAL_CANDIES = max(0, SpriteCandy.TOTAL_CANDIES - 1)

    def update(self, *args: Any, **kwargs: Any):
        self.move()
        self.image.blit(self.label_surface, SpriteCandy.TEXT_POSITION)

    def __str__(self) -> str:
        return f"SpriteCandy(Color={self.color}, Number={self.number})"
