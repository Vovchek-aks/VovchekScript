class Runner:
    def __init__(self, program: list):
        if not len(program):
            exit(0)

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

    def find_com_down(self, com: str, com2=None) -> None:
        c = self.program[self.cursor].com
        n = 0 if com2 else 1
        while True:
            if self.program[self.cursor].com == com:
                n -= 1
                if not n:
                    break
            elif self.program[self.cursor].com == com2:
                n += 1

            if self.next():
                raise NameError(f'No "{com}" command after "{c}"')

    def find_com_up(self, com: str, com2=None) -> None:
        c = self.program[self.cursor].com
        n = 0 if com2 else 1
        while True:
            if self.program[self.cursor].com == com:
                n -= 1
                if not n:
                    break
            elif self.program[self.cursor].com == com2:
                n += 1

            if self.back():
                raise NameError(f'No "{com}" command before "{c}"')

    def goto(self, line):
        self.cursor = line
        if self.cursor >= len(self.program):
            raise ValueError(f'Attempt to go to line which doesnt exists')



