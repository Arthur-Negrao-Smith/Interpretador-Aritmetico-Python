from typing import Generator, Iterator

from src.utils.raises import (
    InvalidCharacterInLexerError,
    InvalideOperationError,
    InvalideTypeInLexerError,
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
            raise InvalideTypeInLexerError(
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
        """
        decimal_points_count: int = 0
        number_buffer: str | None = self.current_character

        if number_buffer is None:
            raise RuntimeError("It was passed a None object to generate_number().")

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
            number_buffer = "0" + number_buffer

        if number_buffer[-1] in Alphabet.FLOAT_POINTS:
            number_buffer += "0"

        number_token: Token = Token(
            TokenType.NUMBER,
            (float(number_buffer) if decimal_points_count > 0 else int(number_buffer)),
        )
        log.debug(f"The number generated is: {number_token.value}")

        self.next_character()
        return number_token

    def generate_tokens(self) -> Generator:
        """
        Generator to tokens

        Returns:
            Generator: Generator of Tokens
        """
        self.next_character()
        while self.current_character is not None:
            if self.current_character in Alphabet.WHITESPACE:
                log.debug("The current character is Blank Space")
                self.next_character()
                continue

            elif self.current_character in Alphabet:
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

                    case Operations.PLUS:
                        log.debug("Current character is Plus")
                        self.next_character()
                        yield Token(TokenType.PLUS)

                    case Operations.MINUS:
                        log.debug("Current character is Minus")
                        self.next_character()
                        yield Token(TokenType.MINUS)

                    case Operations.MULTIPLY:
                        log.debug("Current character is Multiply")
                        self.next_character()
                        yield Token(TokenType.MULTIPLY)

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
