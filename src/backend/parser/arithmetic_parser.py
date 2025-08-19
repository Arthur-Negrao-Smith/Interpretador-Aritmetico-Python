from types import FunctionType
from src.backend.parser.nodes import *
from src.backend.token.tokens import Token, TokenType

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

    @staticmethod
    def left_bind_power(token: Token) -> int:
        """
        Function to return bind power of the operator

        Args:
            token (Token): Token to return the bind power

        Returns:
            int: Bind power fo the operation

        Raises:
            RuntimeError: If the Token not in simple operations
        """
        match token.type:
            case TokenType.EQUAL:
                return 1
            case TokenType.PLUS:
                return 10
            case TokenType.MINUS:
                return 10
            case TokenType.MULTIPLY:
                return 20
            case TokenType.DIVIDE:
                return 20
            case TokenType.POWER:
                return 30
            case _:
                raise RuntimeError(f"Bad token: '{token}'")


    def nud(self, token: Token) -> Node:
        """
        Parse Literal values and Function calls

        Args:
            token (Token): Token to parse and create Node
        """
        if token.type == TokenType.NUMBER:
            return NumberNode(token.value)

        if token.type in (TokenType.VARIABLE, TokenType.COS, TokenType.LOG, TokenType.EXP, TokenType.SIN):

            if token.type == TokenType.LEFT_PARENTHESES:
                pass



        raise SyntaxError(f"Bad token: '{token}'")

    def led(self, token: Token, left_node: Node) -> Token:
        """
        Parse Operations like: +, -, /, *, ^ and =

        Args:
            token (Token): Token to parse and create Node
            left_node (Node): Left node in syntax tree
        """
        pass

    def expression(self) -> Node:
        pass

    def parse(self) -> None:
        pass
