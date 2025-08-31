from src.backend.lexer.lexer import Lexer
from src.backend.parser.arithmetic_parser import Parser
from src.backend.parser.nodes import Node
from src.backend.interpreter.interpreter import Interpreter

from typing import Generator
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import logging
import os

LOG_FILENAME: str = "app.log"


def active_log(level, log_filename: str) -> None:
    """
    Will active current logs

    Args:
        level (int): Constant of logging to see logs with loglevel selected
        log_filename (str): Name of the file to keep logs
    """
    try:
        os.remove(log_filename)
    except:
        pass

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=level, format=log_format, filename=log_filename, filemode="a"
    )


active_log(logging.INFO, LOG_FILENAME)

logger = logging.getLogger(__name__)

app = FastAPI()


# cors to allow access
origins: list[str] = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Model
class ExpressionRequest(BaseModel):
    """
    Request model to receive an arithmetic expression string.

    Attributes:
        expression (str): The arithmetic expression to be evaluated.
    """

    expression: str


class InterpreterResponse(BaseModel):
    """
    Response model for evaluated expressions.

    Attributes:
        expression (str): The original expression sent by the user.
        result (str | None): The evaluated result of the expression if don't have a error, otherwise "None".
        type_error (str | None): Type of error if one occurred, otherwise "None".
        error (str | None): Error message if one occurred, otherwise "None".
    """

    expression: str
    result: str | None = None
    type_error: str | None = None
    error: str | None = None


class HTTPResponse(BaseModel):
    """
    HTTP response model for status messages.

    Attributes:
        message (str): Readable message.
        status (int): HTTP status code.
    """

    message: str
    status: int


global interpreter
interpreter = Interpreter()


@app.get("/")
async def root() -> HTTPResponse:
    """
    Root endpoint of the API.

    Returns:
        HTTPResponse: Welcome message and status code.
    """
    return HTTPResponse(
        message="Bem-vindo ao Validador de Expressões Aritméticas",
        status=200,
    )


@app.post("/expressions")
async def calculate_expression(req: ExpressionRequest) -> InterpreterResponse:
    """
    Parse, evaluate, and interpret an arithmetic expression.

    Args:
        req (ExpressionRequest): The request body containing the expression.
    Returns:
        InterpreterResponse: Result of the evaluated expression, or error details.
    """
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
        )

    except Exception as error:
        logger.error(f"Error in expression '{req.expression}': {error}")
        return InterpreterResponse(
            expression=req.expression,
            type_error=type(error).__name__,
            error=str(error),
        )


@app.post("/interpreter/reset")
async def reset_interpreter() -> HTTPResponse:
    """
    Reset the interpreter instance and clear stored variables.

    Returns:
        HTTPResponse: confirmation message and status code.

    Raises:
        HTTPException: If the interpreter cannot be restarted.
    """
    try:
        global interpreter
        interpreter = Interpreter()
        logger.info("Interpreter was restarted.")
        return HTTPResponse(
            message="The interpreter was restarted",
            status=200,
        )

    except Exception as error:
        logger.error(f"Error to restart interpreter: {error}")
        raise HTTPException(
            status_code=500,
            detail="Internal error when restarting the interpreter",
            headers={"X-Error-Type": "ResetError"},
        )


@app.get("/logs")
async def get_logs() -> dict:
    """
    Get the contents of the log file.

    Returns:
        dict: Log lines and status code.

    Raises:
        HTTPException: If the log file is not found or an unexpected error occurs.
    """
    try:
        with open("app.log", "r") as f:
            logs: list[str] = f.read().splitlines()
            return {"logs": logs, "status": 200}

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
        logger.error(f"Unexpected error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while reading the log file",
            headers={
                "X-Error-Type": "InternalServerError",
                "X-Error-Code": "UNEXPECTED_ERROR",
                "Cache-Control": "no-cache, no-store, must-revalidate",
            },
        )
