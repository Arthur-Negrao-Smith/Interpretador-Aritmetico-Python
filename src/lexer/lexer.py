from typing import Generator, Iterator

from src.utils.raises import (
    FloatPointSyntaxError,
    InvalidCharacterInLexerError,
    InvalidTypeInLexerError,
)
from src.token.tokens import Token, TokenType
from src.token.alphabet import Alphabet, Operations

import logging

log = logging.getLogger(__name__)


class Lexer:
    """
    Lexer to convert a string to tokens
    """

    def __init__(self, text: str) -> None:
        """
        Constructor from Lexer

        Args:
            text (str): Text to convert to Tokens
        """
        log.debug(f"The text in lexes is: '{text}'")
        self.text: Iterator = iter(text)
        self._current_character: str | None = None

    @property
    def current_character(self) -> str | None:
        """
        Current Lexer character

        raises:
            InvalidTypeInLexerError: If the Lexer don't have a valid current character to convert
        """
        if self._current_character is not None and not isinstance(
            self._current_character, str
        ):
            raise InvalidTypeInLexerError(
                f"Illegal type in Lexer: {self._current_character}: {type(self._current_character)}"
            )

        return self._current_character

    @current_character.setter
    def current_character(self, new_caracter: str | None) -> None:
        """
        The current Lexer character

        Args:
            new_caracter (str | None): New character to substitute the old character
        """
        self._current_character = new_caracter

    def next_character(self) -> None:
        """
        Advance to next character
        """
        try:
            self.current_character = next(self.text)
            log.debug(f"Next character is '{self.current_character}'")
        except StopIteration:
            self.current_character = None

    def generate_number(self) -> Token:
        """
        Create a number token

        Returns:
            Token: Minimal information of Lexer
        """
        decimal_points_count: int = 0
        number_buffer: str | None = self.current_character

        if number_buffer is None:
            raise RuntimeError("It was passed a None object to generate_number().")

        if number_buffer in Alphabet.FLOAT_POINTS:
            decimal_points_count += 1

        self.next_character()
        while self.current_character is not None and (
            self.current_character in Alphabet.DIGITS
            or self.current_character in Alphabet.FLOAT_POINTS
        ):
            if self.current_character in Alphabet.FLOAT_POINTS:
                decimal_points_count += 1
                if decimal_points_count > 1:
                    break

            number_buffer += self.current_character
            self.next_character()

        if number_buffer[0] in Alphabet.FLOAT_POINTS:
            raise FloatPointSyntaxError(
                f"Float Point is in incorrect position: Expect a digit before '{number_buffer[0]}'."
            )

        if number_buffer[-1] in Alphabet.FLOAT_POINTS:
            raise FloatPointSyntaxError(
                f"Float Point is in incorrect position: Expect a digit after '{number_buffer[-1]}'."
            )

        number_token: Token = Token(
            TokenType.NUMBER,
            float(number_buffer) if decimal_points_count > 0 else int(number_buffer),
        )
        log.debug(f"The number generated is: {number_token.value}")

        return number_token

    def generate_variable(self) -> Token:
        """
        Generate variables

        Returns:
            Token: Minimal information of Lexer
        """
        name_buffer: str | None = self.current_character

        if name_buffer is None:
            raise RuntimeError("It was passed a None object to generate_number().")

        self.next_character()
        # while character is not None and is a letter or a digit
        while self.current_character is not None and (
            self.current_character in Alphabet.LETTERS
            or self.current_character in Alphabet.DIGITS
        ):
            name_buffer += self.current_character
            self.next_character()

        # if float point appear
        if (
            self.current_character is not None
            and self.current_character in Alphabet.FLOAT_POINTS
        ):
            raise SyntaxError(f"Variables don't have '{self.current_character}'")

        token: Token = Token(TokenType.VARIABLE, name_buffer)
        log.debug(f"The variable generated is: {token.value}")
        return token

    def generate_tokens(self) -> Generator:
        """
        Generator to tokens

        Returns:
            Generator: Generator of Tokens
        """
        self.next_character()
        while self.current_character is not None:
            if self.current_character in Alphabet.WHITESPACE:  # type: ignore
                log.debug("The current character is Blank Space")
                self.next_character()
                continue

            elif self.current_character in Alphabet:  # type: ignore
                if self.current_character in Alphabet.LETTERS:
                    yield self.generate_variable()
                else:
                    yield self.generate_number()

            elif self.current_character in Operations:
                match self.current_character:
                    case Operations.LEFT_PARENTHESES:
                        log.debug("Current character is Left Parentheses")
                        self.next_character()
                        yield Token(TokenType.LEFT_PARENTHESES)

                    case Operations.RIGHT_PARENTHESES:
                        log.debug("Current character is Right Parentheses")
                        self.next_character()
                        yield Token(TokenType.RIGHT_PARENTHESES)

                    case Operations.EQUAL:
                        log.debug("Current character is Equal")
                        self.next_character()
                        yield Token(TokenType.EQUAL)

                    case Operations.PLUS:
                        log.debug("Current character is Plus")
                        self.next_character()
                        yield Token(TokenType.PLUS)

                    case Operations.MINUS:
                        log.debug("Current character is Minus")
                        self.next_character()
                        yield Token(TokenType.MINUS)

                    case Operations.TIMES:
                        log.debug("Current character is Times")
                        self.next_character()
                        yield Token(TokenType.TIMES)

                    case Operations.DIVIDE:
                        log.debug("Current character is Divide")
                        self.next_character()
                        yield Token(TokenType.DIVIDE)

                    case Operations.POWER:
                        log.debug("Current character is Power")
                        self.next_character()
                        yield Token(TokenType.POWER)

                    case Operations.LOG:
                        log.debug("Current character is Log")
                        self.next_character()
                        yield Token(TokenType.LOG)
            else:
                raise InvalidCharacterInLexerError(
                    f"Illegal character: '{self.current_character}'"
                )
