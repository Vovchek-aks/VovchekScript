from text_to_program import ShitDeleter, TestToProgramConverter


for command in TestToProgramConverter.convert(ShitDeleter.del_shit(open('test.vs', encoding='utf-8').read())):
    command.execute()




