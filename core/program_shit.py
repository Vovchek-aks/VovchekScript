import data_shit as ds
import types_shit as ts
import running_shit as rs


class BaseCommand:
    def __init__(self, com, line: int):
        if self.__class__ == BaseCommand:
            raise NotImplementedError('Word "Base" is nothing to u?!')

        self.com = com
        self.line = line

    def execute(self, runner):
        pass

    def __repr__(self):
        return f'{self.__class__.__name__}({self.com})'

    @staticmethod
    def command_from_str(line: int, com: str):
        if com[0] == '.':
            return ExecutedCommand(com, line)
        return DataCommand(com, line)


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
            ds.FuncsManager.fun_execute(self.com[1:], runner)


class ImplementedFuncs:
    @staticmethod
    def buf_len_check(fname: str, n: int) -> None:
        buf = ds.BufferManager.buffer.val
        if len(buf) != n:
            raise ValueError(f'"{fname}" can be used only with {n} value in the buffer, not {len(buf)}')

    @staticmethod
    def type_check(fname: str, val: ds.Value, *types_: ts.BaseType) -> None:
        types_ = set(map(lambda x: x.__class__, types_))

        if val.type not in types_:
            raise TypeError(
                f'"{fname}" can be used only with ({", ".join(ts.TypeType.to_str(i) for i in types_)}) types, not {ts.TypeType.to_str(val.type)}')

    def f_pass(self, runner: rs.Runner) -> None:
        gorodishko = 'nastya lox <3'
        pass

    def f_var(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.var', 2)
        ImplementedFuncs.type_check('.var', buf[1], ts.StrType())

        ds.VariablesManager.add(ds.Variable(buf[1].val, buf[0]))
        ds.BufferManager.clear()

    def f_fvar(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.fvar', 2)
        ImplementedFuncs.type_check('.fvar', buf[1], ts.StrType())

        ds.FuncsManager.stack[-1].add_var(ds.Variable(buf[1].val, buf[0]))
        ds.BufferManager.clear()

    def f_del(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.del', 1)
        ImplementedFuncs.type_check('.del', buf[0], ts.StrType())

        ds.VariablesManager.delete(buf[0].val)
        ds.BufferManager.clear()

    def f_print(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        if len(buf) == 0:
            print()
        elif len(buf) == 1:
            print(buf[0].to_str(), end='')
        else:
            print(ds.BufferManager.buffer.to_str(), end='')

    def f_input(self, runner: rs.Runner) -> None:
        ds.BufferManager.add(ds.Value(ts.StrType(), input()))

    def f_int(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('int', 1)

        n = int(buf[0].val)
        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.IntType(), n))

    def f_sum(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('sum', 2)

        if buf[0].type != buf[1].type:
            raise TypeError(f'".sum" can be used only with same types, not {buf[0].type} and {buf[1].type}')

        tp = buf[0].type
        v = buf[0].val + buf[1].val

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(tp(), v))

    def f_space(self, runner: rs.Runner) -> None:
        ds.BufferManager.add(ds.Value(ts.StrType(), ' '))

    def f_list(self, runner: rs.Runner) -> None:
        ds.BufferManager.add(ds.Value(ts.ListType(), []))

    def f_list_start(self, runner: rs.Runner) -> None:
        ds.BufferManager.add(ds.Value(ts.ListType(), []))
        ds.BufferManager.depth_of_lists += 1

    def f_list_end(self, runner: rs.Runner) -> None:
        if not ds.BufferManager.depth_of_lists:
            raise ValueError('command ".list_end" must be after ".list_start"')
        ds.BufferManager.depth_of_lists -= 1

    def f_cb(self, runner: rs.Runner) -> None:
        ds.BufferManager.clear()

    def f_compile_str(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('compile_str', 1)

        if buf[0].type != ts.StrType:
            raise TypeError(f'".str_compile" can be used only with str, not {buf[0].type}')

        v = buf[0].val.replace('\\n', '\n').replace('\\t', '\t')

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.StrType(), v))

    def f_rep_start(self, runner: rs.Runner) -> None:
        pass

    def f_rep_end(self, runner: rs.Runner) -> None:
        runner.find_com_up('.rep_start', '.rep_end')

    def f_rep_stop(self, runner: rs.Runner) -> None:
        runner.find_com_down('.rep_end')

    def f_fun_start(self, runner: rs.Runner) -> None:
        ImplementedFuncs.buf_len_check('.fun_start', 1)
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.type_check('.fun_start', buf[0], ts.StrType())

        ds.FuncsManager.add(buf[0].val, runner.cursor)
        ds.BufferManager.clear()

        runner.find_com_down('.fun_end')

    def f_fun_end(self, runner: rs.Runner) -> None:
        ds.FuncsManager.fun_return(runner)

    def f_fun_stop(self, runner: rs.Runner) -> None:
        ImplementedFuncs.f_fun_end(None, runner)

    def f_if_start(self, runner: rs.Runner) -> None:
        ImplementedFuncs.buf_len_check('.if_start', 1)
        val = ds.BufferManager.buffer.val[0]
        ImplementedFuncs.type_check('.if_start', val, ts.BoolType())

        if not val.val:
            runner.find_com_down('.if_end', '.if_start')

    def f_if_end(self, runner: rs.Runner) -> None:
        pass

    def f_bool(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer

        ImplementedFuncs.buf_len_check('.bool', 1)

        f = False
        if buf.val[0].type in (ts.StrType, ts.ListType) and len(buf.val[0].val) > 0:
            f = True
        elif buf.val[0].type in (ts.IntType, ts.FloatType) and buf.val[0].val != 0:
            f = True

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.BoolType(), f))

    def f_eq(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.eq', 2)

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.BoolType(), buf[0].val == buf[1].val))

    def f_gt(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.gt', 2)

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.BoolType(), buf[0].val > buf[1].val))

    def f_not(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.not', 1)
        ImplementedFuncs.type_check('.not', buf[0], ts.BoolType())

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.BoolType(), not buf[0].val))

    def f_get_item(self, runner: rs.Runner) -> None:
        buf = ds.BufferManager.buffer.val
        ImplementedFuncs.buf_len_check('.get_item', 2)
        ImplementedFuncs.type_check('.get_item', buf[0], ts.ListType(), ts.StrType())
        ImplementedFuncs.type_check('.get_item', buf[1], ts.IntType())

        if len(buf[0].val) - 1 < buf[1].val:
            raise ValueError(
                f'To get item from {ts.TypeType.to_str(buf[0].type)} its length must be >= {buf[1].val} + 1, not {len(buf[0].val)}')

        val = buf[0].val[buf[1].val]

        ds.BufferManager.clear()
        ds.BufferManager.add(ds.Value(ts.StrType() if val.__class__ == str else val.__class__(), val))
