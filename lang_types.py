class BaseType:
    MY_TYPE = None

    @classmethod
    def convert_to(cls, text: str) -> type(MY_TYPE):
        return cls.MY_TYPE(text)

    @staticmethod
    def to_str(val: MY_TYPE) -> str:
        return str(val)


class TypeType(BaseType):
    MY_TYPE = BaseType

    @classmethod
    def convert_to(cls, text: str) -> type(MY_TYPE):
        return eval(text.capitalize() + 'Type')

    @staticmethod
    def to_str(val: MY_TYPE) -> str:
        return val.__name__[:-4]


class IntType(BaseType):
    MY_TYPE = int


class FloatType(BaseType):
    MY_TYPE = float


class StrType(BaseType):
    MY_TYPE = str


class BoolType(BaseType):
    MY_TYPE = bool

    @classmethod
    def convert_to(cls, text: str) -> type(MY_TYPE):
        if text not in '01':
            raise ValueError(f'BoolType must be "0" or "1", not "{text}"')

        return text == '1'

    @staticmethod
    def to_str(val: MY_TYPE) -> str:
        return '1' if val else '0'


class ListType(BaseType):
    MY_TYPE = list

    @classmethod
    def convert_to(cls, text: str) -> type(MY_TYPE):
        raise NotImplementedError('to make a list use ".list_start" and ".list_end"')

    @staticmethod
    def to_str(val: MY_TYPE) -> str:
        return 'list_start\n\t' + '\n\t'.join(map(BaseType.to_str, map(lambda x: x.val, val))) + '\nlist_end'
