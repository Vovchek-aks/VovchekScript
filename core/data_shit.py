import core.types_shit as t
import core.running_shit as rs


class Value:
    TYPE_TO_SYMBOL = {
        t.TypeType: '~',
        t.IntType: '!',
        t.FloatType: '%',
        t.StrType: '$',
        t.BoolType: '?',
        t.ListType: ''
    }

    def __init__(self, type_: t.BaseType, val):
        type_ = type_.__class__

        if type_.MY_TYPE not in val.__class__.__bases__ + (val.__class__,):
            raise TypeError(f'"{val.__repr__()}" cant be {type_.__name__}')

        self.type = type_
        self.val = val

    def to_str(self):
        return self.type.to_str(self.val)

    def to_err(self):
        return f'{self.TYPE_TO_SYMBOL[self.type]}{self.val}'

    def to_list(self):
        return self.TYPE_TO_SYMBOL[self.type] + self.type.to_str(self.val)


    # def __repr__(self):
    #     return f'{t.TypeType.to_str(self.type)}: {self.type.to_str(self.val)}'


class Variable:
    def __init__(self, name: str, value: Value):
        self.name = name
        self.value = value

    def to_err(self):
        return f'{self.name} = {self.value.to_err()}'

    # def __repr__(self):
    #     return f'{self.name} = {self.value.__repr__()}'


class BufferManager:
    buffer = Value(t.ListType(), [])
    depth_of_lists = 0

    @staticmethod
    def add(val: Value) -> None:
        if val.__class__ != Value:
            raise TypeError(f'U can add to buffer only Value class, not "{val.__class__.__name__}"')

        BufferManager.get().val += [val]

    @staticmethod
    def clear() -> None:
        BufferManager.buffer.val = []

    @staticmethod
    def get() -> Value:
        return eval('BufferManager.buffer' + '.val[-1]' * BufferManager.depth_of_lists)

    @staticmethod
    def to_err():
        return BufferManager.buffer.to_str()


class VariablesManager:
    variables = set()

    @staticmethod
    def add(var: Variable) -> None:
        f = True
        try:
            VariablesManager.get(var.name)
        except NameError:
            f = False

        if f:
            VariablesManager.delete(var.name)

        VariablesManager.variables.add(var)

    @staticmethod
    def get(name: str) -> Variable:
        for st_el in FuncsManager.stack[::-1]:
            ret = st_el.get_var(name)
            if ret is not None:
                return ret

        ret = tuple(filter(lambda x: x.name == name, VariablesManager.variables))
        if len(ret) == 1:
            return ret[0]

        raise NameError(f'No variable with name "{name}"')

    @staticmethod
    def delete(name: str) -> None:
        for st_el in FuncsManager.stack[::-1]:
            if st_el.del_var(name):
                return

        n = len(VariablesManager.variables)
        VariablesManager.variables = set(filter(lambda x: x.name != name, VariablesManager.variables))

        if len(VariablesManager.variables) == n:
            raise NameError(f'To be deleted variable "{name}" must exists')

    @staticmethod
    def to_err():
        return '\n'.join(map(Variable.to_err, VariablesManager.variables))


class StackElement:
    def __init__(self, line: int, fname: str):
        self.line = line
        self.fname = fname
        self.vars = set()

    def get_var(self, name: str) -> Variable:
        ret = tuple(filter(lambda x: x.name == name, self.vars))

        if len(ret):
            return ret[0]

    def add_var(self, var: Variable) -> None:
        f = True
        try:
            self.get_var(var.name)
        except NameError:
            f = False

        if f:
            self.del_var(var.name)

        self.vars.add(var)

    def del_var(self, name: str) -> bool:
        n = len(self.vars)
        self.vars = set(filter(lambda x: x.name != name, self.vars))

        return n < len(self.vars)

    def to_err(self):
        return f'enter in {self.fname}:\n' + '\n'.join(map(Variable.to_err, self.vars)) + '\n'


class FuncsManager:
    funcs = set()
    stack = []

    @staticmethod
    def add(name: str, line: int) -> None:
        f = True
        try:
            FuncsManager.get_line(name)
        except NameError:
            f = False

        if f:
            raise NameError(f'Command with name ".{name}" already exists')

        FuncsManager.funcs.add((name, line))

    @staticmethod
    def get_line(name: str) -> int:
        f = tuple(filter(lambda x: x[0] == name, FuncsManager.funcs))
        if not len(f):
            raise NameError(f'No command with name "{name}"')

        return f[0][1]

    @staticmethod
    def delete(name: str) -> None:
        FuncsManager.funcs = set(filter(lambda x: x[0] != name, FuncsManager.funcs))

    @staticmethod
    def fun_execute(name: str, runner: rs.Runner) -> None:
        f_line = FuncsManager.get_line(name)
        FuncsManager.stack += [StackElement(runner.cursor, name)]

        runner.goto(f_line)

    @staticmethod
    def fun_return(runner: rs.Runner) -> None:
        runner.goto(FuncsManager.stack.pop(-1).line)

    @staticmethod
    def to_err():
        return 'Funcs:\n' + '\n'.join(map(lambda x: f'{x[0]} at line {x[1]}', FuncsManager.funcs)) + '\n\nStack:\n' + \
               '\n'.join(map(StackElement.to_err, FuncsManager.stack))
