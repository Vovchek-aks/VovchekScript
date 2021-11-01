from text_to_program import ShitDeleter, TestToProgramConverter


print(*TestToProgramConverter.convert(ShitDeleter.del_shit(open('test.vs', encoding='utf-8').read())), sep='\n')




