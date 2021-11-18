from text_to_program import Converter
from running_shit import Runner
from errors_shit import ErrorHandler


# try:
runner = Runner(Converter.real_convert(open('test.vs', encoding='utf-8').read()))

try:
    while not runner.execute():
        pass
except Exception as ex:
    ErrorHandler.handle(ex, runner)

