import pygame
from pygame import Vector2, Rect, Surface

from candy_utils.motion_state import MotionState


class Spring:
    """
    Represents a spring but for now is actually just a solid rectangle
    """
    SIZE = Vector2(200, 300)
    MID_BOTTOM = Vector2(600, 700)
    HEIGHT_CHANGE = 30
    INTERPOLATION_SPEED = 0.05

    def __init__(self):
        # The rectangle here is given an arbitrary left and right since
        # the midbottom property (assigned on the next line) will take care of its positioning
        self.rect = Rect((10, 10), Spring.SIZE)
        self.rect.midbottom = Spring.MID_BOTTOM

        self.t: float = 0
        self.motion_state: MotionState = MotionState.REST
        self.current_position: Vector2 = Vector2(self.rect.midbottom)
        self.next_position: Vector2 | None = None

        self.color: str = "Blue"

    def move_up(self):
        self.motion_state = MotionState.UP
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] - Spring.HEIGHT_CHANGE)

    def move_down(self):
        self.motion_state = MotionState.DOWN
        self.next_position = Vector2(self.rect.midbottom[0], self.rect.midbottom[1] + Spring.HEIGHT_CHANGE)

    def move(self):
        if self.motion_state is not MotionState.REST:
            self.t += Spring.INTERPOLATION_SPEED
            self.t = pygame.math.clamp(self.t, 0, 1)
            self.rect.midbottom = self.current_position.lerp(self.next_position, self.t)

            if self.rect.midbottom == self.next_position:
                self.current_position = self.next_position
                self.t = 0

                self.motion_state = MotionState.REST

    def render(self, screen: Surface):
        self.move()
        pygame.draw.rect(screen, self.color, self.rect)


