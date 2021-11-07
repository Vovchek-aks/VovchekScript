from text_to_program import ShitDeleter, TestToProgramConverter
from running_shit import Runner


# try:
runner = Runner(TestToProgramConverter.convert(ShitDeleter.del_shit(open('test.vs', encoding='utf-8').read())))
while not runner.execute():
    pass

# except Exception as ex:
#     print(f'{ex.__class__.__name__}: {ex}\n')
