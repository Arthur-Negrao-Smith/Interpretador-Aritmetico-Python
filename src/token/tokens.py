from enum import Enum
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    """
    Type of tokens
    """

    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    POWER = 5
    LOG = 6
    LEFT_PARENTHESES = 7
    RIGHT_PARENTHESES = 8


@dataclass
class Token:
    """
    Minimal package of information to use in Lexer
    """

    type: TokenType
    value: Any = None

    def __repr__(self) -> str:
        return self.type.name + (f": {self.value}" if self.value is not None else "")
