import core.program_shit as ps
import os


class Converter:
    @staticmethod
    def enumerate_lines(text: str) -> list:
        return list(map(lambda x: (x[0] + 1, x[1]), enumerate(text.split('\n'))))

    @staticmethod
    def del_shit(text: list) -> list:
        text = map(lambda x: (x[0], x[1].split()[0] if x[1].split() else ''), text)
        return list(filter(lambda x: x[1] and x[1][0] in '.!$%?~@', text))

    @staticmethod
    def convert(text: list) -> list:
        program = []
        for line in text:
            program += [ps.BaseCommand.command_from_str(*line)]
        return program

    @staticmethod
    def add_libs(libs: str, path: str) -> list:
        vscode = []
        for i in libs.strip().split():
            cp = '\\'.join(path.split('\\')[:-1]) + f'\\{i}'
            if not os.path.exists(cp):
                raise NameError(f'There is no file "{i}"')
            if i[-3:] != '.vs':
                raise NameError(f'Only VovchekScrypt in this house, not "{i}"')

            vscode += Converter.real_convert(cp)

        return vscode

    @staticmethod
    def real_convert(path: str) -> list:
        text = open(path, encoding='utf-8').read()

        x = text.count('##---##')

        if x > 1:
            raise ValueError('"##---##" can be only once in code')

        if x == 1:
            libs, text = text.split('##---##')
            return Converter.add_libs(libs, path) + Converter.convert(Converter.del_shit(Converter.enumerate_lines(text)))

        return Converter.convert(Converter.del_shit(Converter.enumerate_lines(text)))
