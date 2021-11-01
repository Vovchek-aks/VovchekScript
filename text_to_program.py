import program_shit as ps


class ShitDeleter:
    @staticmethod
    def del_shit(text: str) -> str:
        return '\n'.join(i.strip() for i in text.split('\n') if i.strip() and
                         i.strip()[0] in '.@%$~?&' and
                         ''.join(i.strip().split()) == i.strip())


class TestToProgramConverter:
    @staticmethod
    def convert(text: str):
        prog = []
        for line in text.split('\n'):
            prog += [ps.BaseCommand.command_from_str(line)]
        return prog



