from src.backend.lexer.lexer import Lexer
from src.backend.parser.arithmetic_parser import Parser
from src.backend.parser.nodes import Node
from src.backend.interpreter.interpreter import Interpreter
from typing import Generator

import logging
import sys

interpreter = Interpreter()
def active_log(level) -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=level, format=log_format)


if "debug" in sys.argv:
    active_log(logging.DEBUG)

elif "info" in sys.argv:
    active_log(logging.INFO)

msg: str = """
============================
        Calculator
============================
"""

print(msg)
while True:
    text: str = input("Caculate >> ")
    if text == "exit":
        break

    try:
        lexer: Lexer = Lexer(text)
        tokens: Generator = lexer.generate_tokens()
        parser: Parser = Parser(list(tokens))
        expression: Node | None = parser.parse()

        if expression is None:
            print("")
        else:
            result = interpreter.visit(expression)
            print(result)

    except Exception as error:
        print(f"Syntax Error: {error}")
        continue
