import types as t


class Value:
    def __init__(self, type_: t.BaseType, val):
        if type_.myType not in val.__bases__:
            raise TypeError()

        self.type = type_
        self.val = val


class Variable:
    def __init__(self, name: str, value: Value):
        self.name = name
        self.value = value


class Buffer:
    buffer = []

    @staticmethod
    def add(val: Value) -> None:
        Buffer.buffer += [val]

    @staticmethod
    def clear() -> None:
        Buffer.buffer = []


class VariablesManager:
    variables = []

    @staticmethod
    def add(var: Variable) -> None:
        VariablesManager.variables += [var]

    @staticmethod
    def get(name: str) -> Variable:
        return filter(lambda x: x.name == name, VariablesManager.variables)[0]




