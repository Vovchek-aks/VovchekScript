import data_shit as ds
import types_shit as ts
import program_shit as ps


class Runner:
    def __init__(self, program: list):
        self.program = program
        self.cursor = 0

    def next(self) -> bool:
        self.cursor += 1
        return self.cursor >= len(self.program)

    def back(self) -> bool:
        self.cursor -= 1
        return self.cursor < 0

    def execute(self) -> bool:
        self.program[self.cursor].execute(self)
        return self.next()

    def find_com_down(self, com: str) -> None:
        c = self.program[self.cursor].com
        while self.program[self.cursor].com != com:
            if self.next():
                raise NameError(f'No "{com}" command after "{c}"')

    def find_com_up(self, com: str) -> None:
        c = self.program[self.cursor].com
        while self.program[self.cursor].com != com:
            if self.back():
                raise NameError(f'No "{com}" command before "{c}"')

    def goto(self, line):
        self.cursor = line
        if self.cursor >= len(self.program):
            raise ValueError(f'Attempt to go to line which doesnt exists')



