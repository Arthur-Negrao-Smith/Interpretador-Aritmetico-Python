from src.backend.interpreter.values import Number
from src.backend.lexer.lexer import Lexer
from src.backend.parser.arithmetic_parser import Parser
from src.backend.parser.nodes import Node
from src.backend.interpreter.interpreter import Interpreter
from typing import Generator
from fastapi import FastAPI
from pydantic import BaseModel

import logging
import sys


def active_log(level) -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=level, format=log_format, filename="app.log", filemode="a")


if "debug" in sys.argv:
    active_log(logging.DEBUG)

else:
    active_log(logging.INFO)

logger = logging.getLogger(__name__)

interpreter = Interpreter()

app = FastAPI()

# Modelo de request
class ExpressionRequest(BaseModel):
    expression: str

@app.get("/")
def root():
    return{"message": "Bem-vindo ao Validador de Expressões Aritméticas"}

@app.post("/expressions")
def calculate_expression(req: ExpressionRequest):
    try:
        lexer: Lexer = Lexer(req.expression)
        tokens: Generator = lexer.generate_tokens()
        parser: Parser = Parser(list(tokens))
        expression: Node | None = parser.parse()

        if expression is None:
            result = None
        else:
            result = interpreter.visit(expression)
        
        logger.info(f"Expressão: {req.expression} = {result}")
        return {"expression": req.expression, "result": result}
    
    except Exception as error:
        logger.error(f"Erro na expressão '{req.expression}': {error}")
        return {"error": str(error)}

@app.get("/logs")
def get_logs():
    try:
        with open("app.log", "r") as f:
            logs = f.read().splitlines()
            return {"logs": logs}
    except FileNotFoundError:
        return {"logs": []}
