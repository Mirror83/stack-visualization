import pygame
from sys import exit

from candy_utils.candy import Candy
from candy_utils.candy_group import CandyGroup
from candy_utils.spring import Spring
from stack import Stack

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stack Visualization")

spring = Spring()

candy_group = CandyGroup()
candy_stack = Stack()

Candy.VERTICAL_START = SCREEN_HEIGHT - Spring.SIZE.y - 120

clock = pygame.time.Clock()
MAX_FPS = 60


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                is_done_shifting = candy_group.is_done_shifting()
                if Candy.VERTICAL_START > 0 and is_done_shifting:
                    candy = Candy()
                    candy_stack.push(candy)
                    candy_group.add(candy)
                    candy_group.shift_after_addition()
                    spring.move_down()
                    print(len(candy_stack))
                elif not is_done_shifting:
                    print("Still shifting")
                else:
                    print("Dispenser full")
            elif event.button == pygame.BUTTON_RIGHT:
                is_done_shifting = candy_group.is_done_shifting()
                if not candy_stack.is_empty() and is_done_shifting:
                    candy_group.remove(candy_stack.pop())
                    candy_group.shift_after_removal()
                    spring.move_up()
                    print(len(candy_stack))
                elif not is_done_shifting:
                    print("Still shifting")
                else:
                    print("Nothing to remove")

    screen.fill("Black")  # Erase the screen so that trails of objects at previous positions are not seen

    spring.render(screen)

    candy_group.draw(screen)
    candy_group.update()

    pygame.display.update()
    clock.tick(MAX_FPS)
