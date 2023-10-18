from pygame.sprite import Group

from candy_utils.candy import Candy
from candy_utils.motion_state import MotionState


class CandyGroup(Group):
    def __init__(self):
        super().__init__()
        self.motion_state: MotionState = MotionState.REST

    def is_done_shifting(self) -> bool:
        for sprite in self.spritedict.keys():
            if isinstance(sprite, Candy) and sprite.motion_state is not MotionState.REST:
                return False

        if self.motion_state is MotionState.UP:
            Candy.increment_vertical_start()
        elif self.motion_state is MotionState.DOWN:
            Candy.decrement_vertical_start()
        self.motion_state = MotionState.REST

        return True

    def shift_after_removal(self):
        self.motion_state = MotionState.UP
        for sprite in self.spritedict.keys():
            if isinstance(sprite, Candy):
                sprite.move_up()

    def shift_after_addition(self):
        self.motion_state = MotionState.DOWN
        for sprite in self.spritedict.keys():
            if isinstance(sprite, Candy):
                sprite.move_down()
