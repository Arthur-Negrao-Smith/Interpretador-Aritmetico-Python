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
    LEFT_PARENTHESES: str = "("
    RIGHT_PARENTHESES: str = ")"
    EQUAL: str = "="

    # Named operations
    LOG: str = "log"
    SQRT: str = "sqrt"
    SIN: str = "sin"
    COS: str = "cos"

    @classmethod
    def get_symbols(cls) -> list:
        return [
            cls.PLUS,
            cls.MINUS,
            cls.TIMES,
            cls.DIVIDE,
            cls.POWER,
            cls.RIGHT_PARENTHESES,
            cls.LEFT_PARENTHESES,
            cls.EQUAL,
        ]

    @classmethod
    def get_named_operations(cls) -> tuple:
        return (
            cls.LOG,
            cls.SQRT,
            cls.SIN,
            cls.COS
        )

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

    # letters
    LETTERS: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

    @classmethod
    def get_symbols(cls) -> set[str]:
        symbols: set = set(
            [
                cls.WHITESPACE,
                cls.DIGITS,
                cls.FLOAT_POINTS,
                cls.LETTERS,
            ]
        )

        return symbols
