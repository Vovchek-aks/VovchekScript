from text_to_program import ShitDeleter, TestToProgramConverter


text = open('test.vs', encoding='utf-8').read()

print(*TestToProgramConverter.convert(ShitDeleter.del_shit(text)), sep='\n')




