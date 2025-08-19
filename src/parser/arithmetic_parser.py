from src.parser.nodes import *
from src.token.tokens import Token

from typing import Generator


class Parser:
    """
    Parser to analyze syntax and organize operations maintaining the order of precedence
    """

    def __init__(self, tokens: Generator[Token]) -> None:
        """
        Constructor from Parser

        Args:
            tokens (Generator[Token]): All tokens to parser in a Generator
        """
        self.tokens = tokens
        self._current_token: Token | None = None
        self.next_token()

    @property
    def current_token(self) -> Token | None:
        """
        Current Parser Token

        Returns:
            Token | None: Current Token to parser or None
        """
        return self._current_token

    @current_token.setter
    def current_token(self, token: Token | None) -> None:
        """
        Current Parser Token

        Args:
            token (Token | None): New Token to substitute old Token
        """
        self._current_token = token

    def next_token(self) -> None:
        """
        Advance to next Token in Generator
        """
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def nud(self) -> Token:
        pass

    def led(self) -> Token:
        pass

    def parse(self) -> None:
        pass
