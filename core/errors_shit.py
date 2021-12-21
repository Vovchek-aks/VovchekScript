from core.running_shit import Runner
from core.data_shit import VariablesManager, FuncsManager, BufferManager
from termcolor import cprint


class ErrorHandler:
    @staticmethod
    def handle(ex: Exception, runner: Runner):
        if ex.__class__ not in (ValueError, NameError, InCodeError):
            cprint(f'{"-" * 10}\n\nPythonError: {ex}\n\n{"-" * 10}', 'red')

        com = runner.program[runner.cursor]
        err_mes = f'\n\n{"-" * 10}\n\n' +\
                  f'Oops, u have an error at line {com.line} ({com.com})\n{ex.__class__.__name__}: ' + \
                  f'{ex}\n\n{"-" * 10}\n\nVariables:\n{VariablesManager.to_err()}\n\n{FuncsManager.to_err()}' + \
                  f'\nBuffer:\n{BufferManager.to_err()}'

        cprint(err_mes, 'green')

        while True:
            input()


class InCodeError(Exception):
    pass
