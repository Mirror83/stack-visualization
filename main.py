import pygame
from sys import exit

from candy import Candy
from candy_group import CandyGroup
from stack import Stack

pygame.init()

screen = pygame.display.set_mode(size=(1000, 600))
pygame.display.set_caption("Stack Visualization")

candy_group = CandyGroup()
candy_stack = Stack()

clock = pygame.time.Clock()
MAX_FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            candy = Candy()
            candy_stack.push(candy)
            candy_group.add(candy)
            Candy.decrement_vertical_start()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not candy_stack.is_empty():
                    candy_group.remove(candy_stack.pop())
                    candy_group.shift_after_removal()
                    Candy.increment_vertical_start()
                else:
                    print("Nothing to remove")

    screen.fill("Black")  # Erase the screen so that trails of objects at previous positions are not seen
    candy_group.draw(screen)
    candy_group.update()

    pygame.display.update()
    clock.tick(MAX_FPS)
