import pygame
from sys import exit

from candy import Candy
from candy_group import CandyGroup
from stack import Stack

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stack Visualization")

candy_group = CandyGroup()
candy_stack = Stack()

spring_rectangle_height = 300
Candy.VERTICAL_START = SCREEN_HEIGHT - spring_rectangle_height - 120

# The rectangle here is given an arbitrary left and right since
# the midbottom property (assigned on the next line) will take care of its positioning
spring_rectangle = pygame.rect.Rect((10, 10), (200, spring_rectangle_height))
spring_rectangle.midbottom = (600, 700)

clock = pygame.time.Clock()
MAX_FPS = 60


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                candy = Candy()
                candy_stack.push(candy)
                candy_group.add(candy)
                candy_group.shift_after_addition()
                Candy.decrement_vertical_start()
                spring_rectangle.inflate_ip(0, -10)
                spring_rectangle.midbottom = (600, 700)
            elif event.button == 3:
                if not candy_stack.is_empty():
                    candy_group.remove(candy_stack.pop())
                    Candy.increment_vertical_start()
                    candy_group.shift_after_removal()
                    spring_rectangle.inflate_ip(0, 10)
                    spring_rectangle.midbottom = (600, 700)
                else:
                    print("Nothing to remove")

    screen.fill("Black")  # Erase the screen so that trails of objects at previous positions are not seen
    candy_group.draw(screen)
    candy_group.update()
    pygame.draw.rect(surface=screen, color="Blue", rect=spring_rectangle, width=spring_rectangle.width)

    pygame.display.update()
    clock.tick(MAX_FPS)
