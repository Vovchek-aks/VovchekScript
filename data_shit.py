import lang_types as t


class Value:
    def __init__(self, type_: t.BaseType, val):
        type_ = type_.__class__

        if type_.MY_TYPE not in val.__class__.__bases__ + (val.__class__,):
            raise TypeError(f'"{val.__repr__()}" cant be {type_.__name__}')

        self.type = type_
        self.val = val

    def to_str(self):
        return self.type.to_str(self.val)


class Variable:
    def __init__(self, name: str, value: Value):
        self.name = name
        self.value = value


class BufferManager:
    buffer = Value(t.ListType(), [])

    @staticmethod
    def add(val: Value) -> None:
        BufferManager.buffer.val += [val]

    @staticmethod
    def clear() -> None:
        BufferManager.buffer.val = []


class VariablesManager:
    variables = []

    @staticmethod
    def add(var: Variable) -> None:
        VariablesManager.variables += [var]

    @staticmethod
    def get(name: str) -> Variable:
        ret = tuple(filter(lambda x: x.name == name, VariablesManager.variables))
        if len(ret) == 1:
            return ret[0]

        raise NameError(f'No variable with name {name}')

    @staticmethod
    def delete(name: str) -> None:
        VariablesManager.variables = list(filter(lambda x: x.name != name, VariablesManager.variables))


class FuncsManager:
    funcs = {}
    stack = []

    @staticmethod
    def add(name: str, line: int) -> None:
        FuncsManager.funcs[name] = line

    @staticmethod
    def get(name: str) -> int:
        return tuple(filter(lambda x: x.name == name, FuncsManager.funcs))[0]

    @staticmethod
    def delete(name: str) -> None:
        FuncsManager.funcs = list(filter(lambda x: x.name != name, FuncsManager.funcs))

    @staticmethod
    def fun_execute(name: str, cur_line: int) -> None:
        f_line = FuncsManager.get(name)
        FuncsManager.stack += [cur_line]

        raise NotImplementedError()

    @staticmethod
    def fun_return(name: str) -> None:
        ret_line = FuncsManager.stack.pop(-1)

        raise NotImplementedError()




