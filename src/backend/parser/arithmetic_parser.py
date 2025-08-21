from src.backend.parser.nodes import *
from src.backend.token.tokens import Token, TokenType

from typing import Iterator
import logging

log = logging.getLogger(__name__)


class Parser:
    """
    Parser to analyze syntax and organize operations maintaining the order of precedence
    """

    def __init__(self, tokens: list[Token]) -> None:
        """
        Constructor from Parser

        Args:
            tokens (Generator[Token]): All tokens to parser in a Generator
        """
        self.tokens: Iterator = iter(tokens)
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

        log.info(f"Next Token: '{self.current_token}'")

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
                return 10
            case TokenType.PLUS:
                return 20
            case TokenType.MINUS:
                return 20
            case TokenType.MULTIPLY:
                return 30
            case TokenType.DIVIDE:
                return 30
            case TokenType.POWER:
                return 40
            case _:
                # parenthesis
                return 0

    @staticmethod
    def convert_operation_to_string(token: Token) -> str:
        match token.type:
            case TokenType.PLUS:
                return "+"
            case TokenType.MINUS:
                return "-"
            case TokenType.MULTIPLY:
                return "*"
            case TokenType.DIVIDE:
                return "/"
            case TokenType.POWER:
                return "^"
            case _:
                raise RuntimeError(f"Unsuported operation: '{token}'.")

    @staticmethod
    def convert_function_to_string(token: Token) -> str:
        match token.type:
            case TokenType.LOG:
                return "log"
            case TokenType.EXP:
                return "exp"
            case TokenType.COS:
                return "cos"
            case TokenType.SIN:
                return "sin"
            case TokenType.SQRT:
                return "sqrt"
            case _:
                raise RuntimeError(f"Unsuported function: '{token}'.")

    def expression(self, right_bind_power: int) -> Node:
        """
        Create a node to represent a expression

        Args:
            right_bind_power (int): Bind power of the operation
        """
        token: Token | None = self.current_token
        if token is None:
            raise RuntimeError(f"None passed to function call: Parser.expression().")

        self.next_token()
        left_node: Node = self.nud(token)

        # while current node isn't None and right_bind_power is less than left_bind_power
        while self.current_token and right_bind_power < self.left_bind_power(
            self.current_token
        ):
            token = self.current_token
            self.next_token()
            left_node = self.led(token, left_node)

        # if the current token is a Ned Node again
        if self.current_token and self.current_token.type in (
            TokenType.LEFT_PARENTHESES,
            TokenType.COS,
            TokenType.SIN,
            TokenType.SQRT,
            TokenType.LOG,
            TokenType.EXP,
            TokenType.EQUAL,
            TokenType.NUMBER,
            TokenType.VARIABLE,
        ):
            raise SyntaxError(
                f"Unexpected Token after expression '{left_node}': '{self.current_token}'."
            )

        return left_node

    def nud(self, token: Token) -> Node:
        """
        Parse Literal values and Function calls

        Args:
            token (Token): Token to parse and create Node

        Returns:
            Node: Node to represent function call
        """
        if token.type == TokenType.NUMBER:
            log.info(f"Number Node created: '{token.value}'")
            return NumberNode(token.value)

        elif token.type == TokenType.VARIABLE:
            log.info(f"Variable Node created: '{token.value}'")
            return VariableNode(token.value)

        elif token.type in (TokenType.PLUS, TokenType.MINUS):
            expression: Node = self.expression(100)
            operation: Literal["-", "+"] = "+" if token.type == TokenType.PLUS else "-"
            log.info(f"Unary Node created: '{operation}'")
            return UnaryOperationNode(operation, expression)

        elif token.type in (
            TokenType.COS,
            TokenType.LOG,
            TokenType.EXP,
            TokenType.SIN,
            TokenType.SQRT,
        ):

            # if don't have parenthesis
            if (
                self.current_token is None
                or self.current_token.type != TokenType.LEFT_PARENTHESES
            ):
                raise SyntaxError(
                    f"Must have parenthesis after the function: '{self.convert_function_to_string(token)}'."
                )

            function_name: str = self.convert_function_to_string(token)

            self.next_token()
            expression: Node = self.expression(0)

            # if don't have right parenthesis
            if (
                self.current_token is None
                or self.current_token.type != TokenType.RIGHT_PARENTHESES
            ):
                raise SyntaxError(
                    f"Miss right parenthesis to close expression in function: '{function_name}'."
                )

            # consume the parenthesis ")"
            self.next_token()
            log.info(f"Function Node created: '{function_name}'.")
            return FunctionNode(function_name, expression)

        elif token.type == TokenType.LEFT_PARENTHESES:
            expression: Node = self.expression(0)
            if (
                self.current_token is None
                or self.current_token.type != TokenType.RIGHT_PARENTHESES
            ):
                raise SyntaxError(
                    f"Expect a right parenthesis. passed token: '{self.current_token}'."
                )
            self.next_token()
            return expression

        raise SyntaxError(f"No value token: '{token}'.")

    def led(self, token: Token, left_node: Node) -> Node:
        """
        Parse Operations like: +, -, /, *, ^ and =

        Args:
            token (Token): Token to parse and create Node
            left_node (Node): Left node in syntax tree
        """

        # if don't have any literal value to use operations
        if self.current_token is None:
            raise SyntaxError(
                f"Binary operator '{self.convert_operation_to_string(token)}' requires a right-hand side expression."
            )

        if token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            right_node: Node = self.expression(self.left_bind_power(token))
            operation: str = self.convert_operation_to_string(token)
            log.info(f"Binary Operation Node created: '{operation}'")
            return BinOperationNode(left_node, operation, right_node)

        if token.type == TokenType.POWER:
            right_node = self.expression(self.left_bind_power(token) - 1)
            log.info(f"Binary Operation Node created: '^'")
            return BinOperationNode(left_node, "^", right_node)

        if token.type == TokenType.EQUAL:
            if not isinstance(left_node, VariableNode):
                raise SyntaxError(f"Just variables can be assigned: '{left_node}'")
            right_node = self.expression(self.left_bind_power(token) - 1)
            log.info(f"Assigment Node created: '='")
            return AssignmentNode(left_node.name, right_node)

        raise SyntaxError(f"This operation doesn' exists: '{token}'.")

    def parse(self) -> Node | None:
        """
        Parse the expression

        Returns:
            Node: First node of syntatic tree
            None: If the expression is empty
        """
        if not self.current_token:
            return None

        return self.expression(0)
