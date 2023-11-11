from sys import exit

import pygame
from pygame import Vector2, QUIT, MOUSEBUTTONUP, BUTTON_LEFT

from piston_spring.sprite_candy import SpriteCandy
from piston_spring.candy_group import CandyGroup
from menu.menu import Menu
from piston_spring.spring import Spring
from stack import Stack

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stack Visualization")

candy_stack = Stack()

spring = Spring()
candy_group = CandyGroup()


# Click handlers for the TextButtons

def on_push():
    global candy_group, candy_stack, spring, menu
    is_done_shifting = candy_group.is_done_shifting()
    if SpriteCandy.VERTICAL_START > 0 and is_done_shifting:
        candy = SpriteCandy()
        candy_stack.push(candy)
        candy_group.add(candy)
        candy_group.shift_after_addition()
        spring.move_down()
        menu.update_command_output("")
        print(len(candy_stack))
    elif not is_done_shifting:
        print("push: Still shifting")
        menu.update_command_output("")
    else:
        menu.update_command_output("Stack full")
        print("push: Stack full")


def on_pop():
    global candy_group, candy_stack, spring, menu
    is_done_shifting = candy_group.is_done_shifting()
    if not candy_stack.is_empty() and is_done_shifting:
        popped_candy = candy_stack.pop()
        candy_group.remove(popped_candy)
        candy_group.shift_after_removal()
        spring.move_up()
        menu.update_command_output(str(popped_candy))
        print(f"pop: len = {len(candy_stack)}")
    elif not is_done_shifting:
        print("pop: Still shifting")
    else:
        menu.update_command_output("Nothing to remove")
        print("pop: Nothing to remove")


def on_top():
    global candy_stack, menu
    if not candy_stack.is_empty():
        menu.update_command_output(str(candy_stack.peek()))
        print(f"top: {candy_stack.peek()}")
    else:
        menu.update_command_output("SpriteCandy stack is empty")
        print("top: Candy stack is empty")


def on_is_empty():
    menu.update_command_output(str(candy_stack.is_empty()))
    print(f"is_empty: {candy_stack.is_empty()}")


def on_len():
    menu.update_command_output(str(len(candy_stack)))
    print(f"len: {len(candy_stack)}")


buttons = [
    Menu.TextButton("S.push()", Vector2(20, 450), on_push, 50),
    Menu.TextButton("S.pop()", Vector2(20, 550), on_pop, 50),
    Menu.TextButton("S.top()", Vector2(200, 450), on_top, 50),
    Menu.TextButton("S.isEmpty()", Vector2(200, 550), on_is_empty, 50),
    Menu.TextButton("len(S)", Vector2(380, 450), on_len, 50)
]
menu = Menu(buttons, size=Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT), font_size=60)

SpriteCandy.VERTICAL_START = SpriteCandy.BASE_VERTICAL_START = SCREEN_HEIGHT - Spring.SIZE.y - 120

clock = pygame.time.Clock()
MAX_FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
            for button in buttons:
                if button.is_hover():
                    button.click()

    screen.fill("Black")  # Erase the screen so that trails of objects at previous positions are not seen

    spring.render(screen)

    candy_group.draw(screen)
    candy_group.update()

    menu.render(screen)

    pygame.display.flip()
    clock.tick(MAX_FPS)
