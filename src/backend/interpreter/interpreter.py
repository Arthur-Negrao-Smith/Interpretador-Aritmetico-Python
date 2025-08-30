from src.backend.interpreter.values import Number
from src.backend.parser.nodes import *

from typing import Callable

import math
import logging

log = logging.getLogger(__name__)


class Interpreter:
    """
    Interpreter to evaluate syntax trees and manage variable storage.
    """
    def __init__(self):
        """
        Constructor for Interpreter.

        Initializes an empty dictionary to store variables.

        Attributes:
            variables (dict[str, Number]): Dictionary to store variable names and their values.
        """
        self.variables: dict[str, Number] = {}

    def visit(self, node: Node) -> Number:
        """
        Visit a syntax tree node and send to the appropriate visit method.

        Args:
            node (Node): The syntax tree node to visit.
        
        Returns:
            Number: The result of evaluating the node.
        """
        method_name: str = f"visit_{type(node).__name__}"
        method: Callable = getattr(self, method_name)
        return method(node)

    def visit_NumberNode(self, node: NumberNode) -> Number:
        """
        Process a NumberNode by returning its numeric value and putting it inside a Number object.

        Args:
            node (NumberNode): The NumberNode containing the numeric value.
        
        Returns:
            Number: The Number object representing the node's value.
        """
        return Number(node.value)

    def visit_BinOperationNode(self, node: BinOperationNode) -> Number:
        """
        Process a BinOperationNode by evaluating the left and right nodes and applying the binary operation.

        Supported operations:
            + : Addition
            - : Subtraction
            * : Multiplication
            / : Division (raises ZeroDivisionError if divisor is zero)
            ^ : Exponentiation
        
        Args:
            node (BinOperationNode): The binary operation node to evaluate.
        
        Returns:
            Number: The result of the binary operation.
        
        Raises:
            ZeroDivisionError: If the operation is division and the right node is zero.
            RuntimeError: If the operation is not supported.
        """
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
        """
        Process a UnaryOperationNode by evaluating the operand and applying the unary operation.

        Supported operations:
            + : Unary plus (returns the operand)
            - : Unary minus (negates the operand)
        
        Args: 
            node (UnaryOperationNode): The unary operation node to evaluate.
        
        Returns:
            Number: The result of the unary operation.
        
        Raises:
            RuntimeError: If the operation is not recognized.
        """
        value: Number = self.visit(node.operand)
        if node.operation == "+":
            return Number(+value.Value)
        elif node.operation == "-":
            return Number(-value.Value)

        raise RuntimeError(f"Unrecognized operation: '{node.operation}'.")

    def visit_FunctionNode(self, node: FunctionNode) -> Number:
        """
        Process a FunctionNode by evaluating its expression and applying the corresponding mathematical function.

        Supported functions:
            sqrt : Square root
            log  : Natural logarithm
            sin  : Sine (radians)
            cos  : Cosine (radians)
            exp  : Exponential function (e^x)

        Args:
            node (FunctionNode): The function node to evaluate.

        Returns:
            Number: The result of the function applied to the evaluated expression.

        Raises:
            RuntimeError: If the function is not supported.    
        """
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
        """
        Process an AssignmentNode by evaluating the value and storing it in the variable dictionary.

        Args:
            node (AssignmentNode): The assignment node containing the variable name and value.
        
        Returns:
            Number: The evaluated value assigned to the variable.
        """
        value: Number = self.visit(node.value)
        self.variables[node.variable_name] = value
        return value

    def visit_VariableNode(self, node):
        """
        Process a VariableNode by looking up its value in the variable dictionary.

        Args:
            node (VariableNode): The variable node containing the variable name.
        
        Returns:
                Number: The value assigned to the variable.
        
        Raises:
            ValueError: If the variable has not been assigned a value.
        """
        if node.name in self.variables:
            return self.variables[node.name]

        raise ValueError(f"No value assigned to variable: '{node.name}'.")
