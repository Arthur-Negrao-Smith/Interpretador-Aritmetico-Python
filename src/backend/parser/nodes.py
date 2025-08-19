from typing import Literal
from dataclasses import dataclass


class Node:
    """
    Node to use with Parser
    """

    pass


# Literal nodes
@dataclass
class VariableNode(Node):
    """
    Node to use with variables

    Attributes:
        name (str): Name of variable
    """

    name: str

    def __repr__(self) -> str:
        return f"{self.name}"


@dataclass
class NumberNode(Node):
    """
    Node to represent literal numbers

    Attributes:
    value (int): Literal value of the node
    """

    value: int | float

    def __repr__(self) -> str:
        return f"{self.value}"


# Operations
@dataclass
class BinOperationNode(Node):
    """
    Binary node operations like: +, -, *, ^, ...

    Attributes:
        left_node (type[Node]): Node to use operation
        operation (str): Operation to use with left and right node
        right_node (type[Node]): Node to use operation
    """

    left_node: Node
    operation: str
    right_node: Node

    def __repr__(self) -> str:
        return f"({self.left_node}{self.operation}{self.right_node})"


@dataclass
class UnaryOperationNode(Node):
    """
    Unary node to operations like: -x or +x

    Attributes:
        operation (Literal["+", "-"]): Operation to use with node
        node (type[Node]): Node to use operator
    """

    operation: Literal["+", "-"]
    operand: Node

    def __repr__(self) -> str:
        return f"({self.operation}{self.operand})"


# Assignment
@dataclass
class AssignmentNode(Node):
    """
    Node to represent "="

    Attributes:
        variable_name (str): Name of variable
        expression (Node): Node to represent the expression to assign
    """

    variable_name: str
    value: Node

    def __repr__(self) -> str:
        return f"{self.variable_name}={self.value}"


# Functions Node
@dataclass
class FunctionNode(Node):
    """
    Node to represent functions like: sqrt, log, sin, cos, ...

    Attributes:
        function_name (str): Name of used function
        expression (Node): Expression to use in function args
    """

    function_name: str
    expression: Node

    def __repr__(self) -> str:
        return f"{self.function_name}({self.expression})"
