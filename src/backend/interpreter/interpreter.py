from src.backend.interpreter.values import Number
from src.backend.parser.nodes import *

from typing import Callable

import math
import logging

log = logging.getLogger(__name__)


class Interpreter:
    def __init__(self):
        self.variables: dict[str, Number] = {}

    def visit(self, node: Node) -> Number:
        method_name: str = f"visit_{type(node).__name__}"
        method: Callable = getattr(self, method_name)
        return method(node)

    def visit_NumberNode(self, node: NumberNode) -> Number:
        return Number(node.value)

    def visit_BinOperationNode(self, node: BinOperationNode) -> Number:
        left: Number = self.visit(node.left_node)
        right: Number = self.visit(node.right_node)
        operation_: str = node.operation

        if operation_ == "+":
            return Number(left.Value + right.Value)

        elif operation_ == "-":
            return Number(left.Value - right.Value)

        elif operation_ == "*":
            return Number(left.Value * right.Value)

        elif operation_ == "/":
            if right.Value == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return Number(left.Value / right.Value)

        elif operation_ == "^":
            return Number(left.Value**right.Value)

        else:
            raise RuntimeError(f"Unsuported operation: '{operation_}'.")

    def visit_UnaryOperationNode(self, node: UnaryOperationNode) -> Number:
        value: Number = self.visit(node.operand)
        if node.operation == "+":
            return Number(+value.Value)
        elif node.operation == "-":
            return Number(-value.Value)

        raise RuntimeError(f"Unrecognized operation: '{node.operation}'.")

    def visit_FunctionNode(self, node: FunctionNode) -> Number:
        arg: Number = self.visit(node.expression)
        funct_name: str = node.function_name.lower()

        if funct_name == "sqrt":
            return Number(math.sqrt(arg.Value))
        elif funct_name == "log":
            return Number(math.log(arg.Value))
        elif funct_name == "sin":
            return Number(math.sin(arg.Value))
        elif funct_name == "cos":
            return Number(math.cos(arg.Value))
        elif funct_name == "exp":
            return Number(math.exp(arg.Value))

        raise RuntimeError(f"Unsuported function: '{funct_name}'.")

    def visit_AssignmentNode(self, node: AssignmentNode) -> Number:
        value: Number = self.visit(node.value)
        self.variables[node.variable_name] = value
        return value

    def visit_VariableNode(self, node):
        if node.name in self.variables:
            return self.variables[node.name]

        raise ValueError(f"No value assigned to variable: '{node.name}'.")
