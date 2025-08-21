from src.backend.interpreter.values import Number
from src.backend.lexer.lexer import Lexer
from src.backend.parser.arithmetic_parser import Parser
from src.backend.parser.nodes import Node
from src.backend.interpreter.interpreter import Interpreter

from typing import Generator
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import logging
import sys


def active_log(level) -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level, format=log_format, filename="app.log", filemode="a"
    )


if "debug" in sys.argv:
    active_log(logging.DEBUG)

else:
    active_log(logging.INFO)

logger = logging.getLogger(__name__)

interpreter = Interpreter()

app = FastAPI()


# Request Model
class ExpressionRequest(BaseModel):
    expression: str


class InterpreterResponse(BaseModel):
    expression: str
    result: str
    type_error: str
    error: str


@app.get("/")
def root():
    return {"message": "Bem-vindo ao Validador de Expressões Aritméticas"}


@app.post("/expressions")
def calculate_expression(req: ExpressionRequest):
    try:
        lexer: Lexer = Lexer(req.expression)
        tokens: Generator = lexer.generate_tokens()
        parser: Parser = Parser(list(tokens))
        expression: Node | None = parser.parse()

        if expression is None:
            return InterpreterResponse(
                expression=req.expression, result="", type_error="None", error="None"
            )

        else:
            result = interpreter.visit(expression)

        logger.info(f"Expression: {req.expression} = {result}")
        return InterpreterResponse(
            expression=req.expression,
            result=str(result),
            type_error="None",
            error="None",
        )

    except Exception as error:
        logger.error(f"Error in expression '{req.expression}': {error}")
        return InterpreterResponse(
            expression=req.expression,
            result="",
            type_error=type(error).__name__,
            error=str(error),
        )


@app.get("/logs")
def get_logs() -> dict[str, list[str]]:
    try:
        with open("app.log", "r") as f:
            logs: list[str] = f.read().splitlines()
            return {"logs": logs}

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="The log file wasn't found",
            headers={
                "X-Error-Type": "FileNotFound",
                "X-File-Name": "app.log",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "X-Retry-After": "30",
            },
        )

    except Exception as error:
        print(f"Unexpected error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while reading the log file",
            headers={
                "X-Error-Type": "InternalServerError",
                "X-Error-Code": "UNEXPECTED_ERROR",
                "Cache-Control": "no-cache, no-store, must-revalidate",
            },
        )
