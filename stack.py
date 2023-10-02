from typing import Any


class Stack:
    def __init__(self):
        self.elements = []

    def __len__(self) -> int:
        return len(self.elements)

    def is_empty(self):
        return len(self) == 0

    def push(self, element: Any) -> None:
        self.elements.append(element)

    def pop(self) -> Any:
        return self.elements.pop()

    def peek(self) -> Any:
        print(self.elements[len(self) - 1])
