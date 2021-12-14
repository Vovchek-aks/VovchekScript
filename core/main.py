from text_to_program import Converter
from running_shit import Runner
from errors_shit import ErrorHandler


def run(fname: str) -> None:
    runner = Runner(Converter.real_convert(open('../test.vs', encoding='utf-8').read()))

    try:
        while not runner.execute():
            pass
    except Exception as ex:
        ErrorHandler.handle(ex, runner)


if __name__ == '__main__':
    run(input('Project name:\n'))
