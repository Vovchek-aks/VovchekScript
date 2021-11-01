class BaseType:
    myType = None

    def __str__(self):
        return self.__class__.__name__


class TypeType(BaseType):
    myType = BaseType


class IntType(BaseType):
    myType = int


class FloatType(BaseType):
    myType = float


class StrType(BaseType):
    myType = str


class BoolType(BaseType):
    myType = bool


class ListType(BaseType):
    myType = list



