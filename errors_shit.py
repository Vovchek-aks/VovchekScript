from running_shit import Runner
from termcolor import cprint


class ErrorHandler:
    @staticmethod
    def handle(ex: Exception, runner: Runner):
        com = runner.program[runner.cursor]
        while True:
            cprint(f'{"-" * 10}\n\nOops, u have an error at line {com.line} ({com.com})\nError: {ex}\n\n{"-" * 10}', 'red')
            input()
