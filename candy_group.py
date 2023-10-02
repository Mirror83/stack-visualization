from pygame.sprite import Group

from candy import Candy


class CandyGroup(Group):
    def __init__(self):
        super().__init__()

    def shift_after_removal(self):
        for sprite in self.spritedict.keys():
            if isinstance(sprite, Candy):
                print("Will shift")
