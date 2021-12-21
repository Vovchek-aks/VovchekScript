from core.text_to_program import Converter
from core.running_shit import Runner
from core.errors_shit import ErrorHandler
import os


def run(fname: str, absolute=False) -> None:
    path = fname if absolute else f'../projects/{fname}/main.vs'
    if not os.path.exists(path):
        input(f'No project on path "core/{path}"')
        exit(0)

    runner = Runner(Converter.real_convert(open(path, encoding='utf-8').read()))

    try:
        while not runner.execute():
            pass
    except Exception as ex:
        ErrorHandler.handle(ex, runner)


if __name__ == '__main__':
    run(input('Project name:\n'))
