import core.program_shit as ps


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
    def real_convert(text: str) -> list:
        return Converter.convert(Converter.del_shit(Converter.enumerate_lines(text)))
