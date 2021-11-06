import data_shit as ds
import lang_types as t


class BaseCommand:
    def __init__(self, com):
        if self.__class__ == BaseCommand:
            raise NotImplementedError('Word "Base" is nothing to u?!')

        self.com = com

    def execute(self):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self.com})'

    @staticmethod
    def command_from_str(line: str):
        if line[0] == '.':
            return ExecutedCommand(line)
        return DataCommand(line)


class DataCommand(BaseCommand):
    SYMBOL_TO_TYPE = {
        '~': t.TypeType,
        '!': t.IntType,
        '%': t.FloatType,
        '$': t.StrType,
        '?': t.BoolType
    }

    def execute(self):
        val = None

        if self.com[0] == '@':
            val = ds.VariablesManager.get(self.com[1:]).value
        else:
            tp = self.SYMBOL_TO_TYPE[self.com[0]]
            val = ds.Value(tp(), tp.convert_to(self.com[1:]))

        ds.BufferManager.add(val)


class ExecutedCommand(BaseCommand):
    def execute(self):
        f = ImplementedFuncs.__dict__.get(f'f_{self.com[1:]}', None)
        if f is not None:
            f(None)
        else:
            raise NotImplementedError(f'No command with name {self.com[1:]}')


class ImplementedFuncs:
    def f_var(self):
        buf = ds.BufferManager.buffer.val
        if len(buf) != 2:
            raise ValueError('To make a variable u need exactly 2 values in the buffer')

        if buf[1].type != t.StrType:
            raise ValueError('Variable name must be str')

        ds.VariablesManager.add(ds.Variable(buf[1].val, buf[0]))
        ds.BufferManager.clear()

    def f_print(self):
        buf = ds.BufferManager.buffer.val
        if len(buf) == 0:
            print(end='')
        elif len(buf) == 1:
            print(buf[0].to_str(), end='')
        else:
            print(ds.BufferManager.buffer.to_str(), end='')

    def f_input(self):
        ds.BufferManager.add(ds.Value(t.StrType(), input()))

    def f_int(self):
        buf = ds.BufferManager.buffer.val
        if len(buf) != 1:
            raise ValueError(f'".int" can be used only with 1 value in the buffer, not {len(buf)}')

        n = int(buf[0].val)
        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(t.IntType(), n))

    def f_sum(self):
        buf = ds.BufferManager.buffer.val
        if len(buf) != 2:
            raise ValueError(f'".sum" can be used only with 2 value in the buffer, not {len(buf)}')

        if buf[0].type != buf[1].type:
            raise TypeError(f'".sum" can be used only with same types, not {buf[0].type} and {buf[1].type}')

        tp = buf[0].type
        v = buf[0].val + buf[1].val

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(tp(), v))

    def f_space(self):
        ds.BufferManager.add(ds.Value(t.StrType(), ' '))

    def f_cb(self):
        ds.BufferManager.clear()

    def f_compile_str(self):
        buf = ds.BufferManager.buffer.val
        if len(buf) != 1:
            raise ValueError(f'".str_compile" can be used only with 1 value in the buffer, not {len(buf)}')

        if buf[0].type != t.StrType:
            raise ValueError(f'".str_compile" can be used only with str, not {buf[0].type}')

        v = buf[0].val.replace('\\n', '\n').replace('\\t', '\t')

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(t.StrType(), v))




