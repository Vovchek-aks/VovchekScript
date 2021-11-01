class BaseCommand:
    def __init__(self, com):
        if self.__class__ == BaseCommand:
            raise NotImplementedError('Word "Base" is nothing to u?!')

        self.com = com

    def execute(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self.com})'

    @staticmethod
    def command_from_str(line: str):
        if line[0] == '.':
            return ExecutedCommand(line)
        return DataCommand(line)


class DataCommand(BaseCommand):
    pass


class ExecutedCommand(BaseCommand):
    pass



