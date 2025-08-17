class _OperationsMeta(type):
    def __contains__(cls, symbol) -> bool:
        return any(symbol in operation for operation in cls.get_symbols())  # type: ignore


class Operations(metaclass=_OperationsMeta):
    """
    Operations to convert to Tokens
    """

    PLUS: str = "+"
    MINUS: str = "-"
    TIMES: str = "*"
    DIVIDE: str = "/"
    POWER: str = "^"
    LOG: tuple[str] = ("log",)
    LEFT_PARENTHESES: str = "("
    RIGHT_PARENTHESES: str = ")"

    @classmethod
    def get_symbols(cls) -> list:
        return [
            cls.PLUS,
            cls.MINUS,
            cls.TIMES,
            cls.DIVIDE,
            cls.POWER,
            cls.LOG,
            cls.RIGHT_PARENTHESES,
            cls.LEFT_PARENTHESES,
        ]


class _AlphabetMeta(type):
    def __contains__(cls, character: str) -> bool:
        return any(character in symbol for symbol in cls.get_symbols())  # type: ignore


class Alphabet(metaclass=_AlphabetMeta):
    """
    Alphabet to convert to Tokens
    """

    # useless tokens
    WHITESPACE: str = " \n\t"

    # digits tokens
    DIGITS: str = "0123456789"

    # float point tokens
    FLOAT_POINTS: str = "."

    @classmethod
    def get_symbols(cls) -> set[str]:
        symbols: set = set(
            [
                cls.WHITESPACE,
                cls.DIGITS,
                cls.FLOAT_POINTS,
            ]
        )

        return symbols
