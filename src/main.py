from src.lexer.lexer import Lexer
from typing import Generator

import logging
import sys

if "debug" in sys.argv:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

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
        print(list(tokens))

    except Exception as error:
        print(error)
        continue

