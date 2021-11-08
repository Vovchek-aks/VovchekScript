import data_shit as ds
import types_shit as ts


class BaseCommand:
    def __init__(self, com):
        if self.__class__ == BaseCommand:
            raise NotImplementedError('Word "Base" is nothing to u?!')

        self.com = com

    def execute(self, runner):
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
        '~': ts.TypeType,
        '!': ts.IntType,
        '%': ts.FloatType,
        '$': ts.StrType,
        '?': ts.BoolType
    }

    def execute(self, runner):
        val = None

        if self.com[0] == '@':
            val = ds.VariablesManager.get(self.com[1:]).value
        else:
            tp = self.SYMBOL_TO_TYPE[self.com[0]]
            val = ds.Value(tp(), tp.convert_to(self.com[1:]))

        ds.BufferManager.add(val)


class ExecutedCommand(BaseCommand):
    def execute(self, runner):
        f = ImplementedFuncs.__dict__.get(f'f_{self.com[1:]}', None)
        if f is not None:
            f(None, runner)
        else:
            raise NameError(f'No command with name "{self.com[1:]}"')


class ImplementedFuncs:
    @staticmethod
    def buf_len_check(fname: str, n: int):
        buf = ds.BufferManager.buffer.val
        if len(buf) != n:
            raise ValueError(f'"{fname}" can be used only with {n} value in the buffer, not {len(buf)}')

    @staticmethod
    def type_check(fname: str, type_: ts.BaseType, val: ds.Value):
        type_ = type_.__class__

        if val.type != type_:
            raise TypeError(
                f'"{fname}" can be used only with {ts.TypeType.to_str(type_)} type, not {ts.TypeType.to_str(val.type)}')

    def f_pass(self, runner):
        pass

    def f_var(self, runner):
        buf = ds.BufferManager.buffer.val
        if len(buf) != 2:
            raise ValueError('To make a variable u need exactly 2 values in the buffer')

        if buf[1].type != ts.StrType:
            raise TypeError('Variable name must be str type')

        ds.VariablesManager.add(ds.Variable(buf[1].val, buf[0]))
        ds.BufferManager.clear()

    def f_print(self, runner):
        buf = ds.BufferManager.buffer.val
        if len(buf) == 0:
            print()
        elif len(buf) == 1:
            print(buf[0].to_str(), end='')
        else:
            print(ds.BufferManager.buffer.to_str(), end='')

    def f_input(self, runner):
        ds.BufferManager.add(ds.Value(ts.StrType(), input()))

    def f_int(self, runner):
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('int', 1)

        n = int(buf[0].val)
        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.IntType(), n))

    def f_sum(self, runner):
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('sum', 2)

        if buf[0].type != buf[1].type:
            raise TypeError(f'".sum" can be used only with same types, not {buf[0].type} and {buf[1].type}')

        tp = buf[0].type
        v = buf[0].val + buf[1].val

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(tp(), v))

    def f_space(self, runner):
        ds.BufferManager.add(ds.Value(ts.StrType(), ' '))

    def f_cb(self, runner):
        ds.BufferManager.clear()

    def f_compile_str(self, runner):
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('compile_str', 1)

        if buf[0].type != ts.StrType:
            raise TypeError(f'".str_compile" can be used only with str, not {buf[0].type}')

        v = buf[0].val.replace('\\n', '\n').replace('\\t', '\t')

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.StrType(), v))

    def f_rep_start(self, runner):
        pass

    def f_rep_end(self, runner):
        runner.find_com_up('.rep_start', '.rep_end')

    def f_rep_stop(self, runner):
        runner.find_com_down('.rep_end')

    def f_if_start(self, runner):
        ImplementedFuncs.buf_len_check('.if_start', 1)
        val = ds.BufferManager.buffer.val[0]
        ImplementedFuncs.type_check('.if_start', ts.BoolType(), val)

        if not val.val:
            runner.find_com_down('.if_end', '.if_start')

    def f_if_end(self, runner):
        pass

    # def f_sum_to(self, runner):
    #     buf = ds.BufferManager.buffer.val
    #     ImplementedFuncs.buf_len_check('sum_to', 2)
    #
    #     var = ds.VariablesManager.get(buf[1].val)
    #
    #     if buf[0].type != var.value.type:
    #         raise TypeError(f'".sum_to" can be used only with same types, not {buf[0].type} and {var.value.type}')
    #
    #     var.value.val += buf[0].val

    def f_bool(self, runner):
        buf = ds.BufferManager.buffer
        ds.BufferManager.clear()
        f = False
        if len(buf.val) > 1:
            f = True
        elif len(buf.val) == 1:
            if buf.val[0].type == ts.StrType and len(buf.val[0].val) > 0:
                f = True
            elif buf.val[0].type in (ts.IntType, ts.FloatType) and buf.val[0].val != 0:
                f = True

        ds.BufferManager.add(ds.Value(ts.BoolType(), f))

    def f_eq(self, runner):
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.eq', 2)

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.BoolType(), buf[0].val == buf[1].val))







