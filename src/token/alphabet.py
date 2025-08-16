from tokens import Token, TokenType
from utils.raises import InvalideOperationError


class Operations:
    # operations signals
    PLUS: str = "+"
    MINUS: str = "-"
    MULTIPLY: str = "*"
    DIVIDE: str = "/"
    POWER: str = "^"
    LOG: str = "log"
    LEFT_PARENTHESES: str = "("
    RIGHT_PARENTHESES: str = ")"

    @classmethod
    def get_operation(cls) -> set:
        return set([cls.PLUS, cls.MINUS, cls.MULTIPLY, cls.DIVIDE, cls.POWER, cls.LOG])

    @classmethod
    def __contains__(cls, symbol: str) -> bool:
        contains: bool = False
        for operation in cls.get_operation():
            if symbol in operation:
                contains = True
                break

        return contains

    @classmethod
    def convert_operation(cls, operation: str) -> Token:
        if operation in cls.PLUS:
            return Token(TokenType.PLUS)
        if operation in cls.MINUS:
            return Token(TokenType.MINUS)
        if operation in cls.MULTIPLY:
            return Token(TokenType.MULTIPLY)
        if operation in cls.DIVIDE:
            return Token(TokenType.DIVIDE)
        if operation in cls.POWER:
            return Token(TokenType.POWER)
        if operation in cls.LOG:
            return Token(TokenType.LOG)

        raise InvalideOperationError


class Alphabet:
    # useless tokens
    WHITESPACE: str = " \n\t"

    # digits tokens
    DIGITS: str = "0123456789"

    # float point tokens
    FLOAT_POINTS: str = "."

    @classmethod
    def get_symbols(cls) -> set:
        symbols: set = set(
            [
                cls.WHITESPACE,
                cls.DIGITS,
                cls.FLOAT_POINTS,
            ]
        )

        return symbols

    @classmethod
    def __contains__(cls, character: str) -> bool:
        contains: bool = False
        for symbol in cls.get_symbols():
            if character in symbol:
                contains = True
                break

        return contains
