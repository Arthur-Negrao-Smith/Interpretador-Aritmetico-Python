from typing import Literal


class Node:
    """
    Node to use with Parser
    """

    pass


# Literal nodes
class VariableNode(Node):
    """
    Node to use with variables
    """

    def __init__(self, name: str) -> None:
        """
        Constructor from VariableNode

        Args:
            name (str): Name of variable
        """
        super().__init__()
        self.name: str = name

    def __repr__(self) -> str:
        return f"{self.name}"


class NumberNode(Node):
    """
    Node to represent literal numbers
    """

    def __init__(self, value: int | float) -> None:
        """
        Constructor from NumberNode

        Args:
            value (int): Literal value of the node
        """
        super().__init__()
        self.value: int | float = value

    def __repr__(self) -> str:
        return f"{self.value}"


# Operations
class BinOperationsNode(Node):
    """
    Binary node operations like: +, -, *, ^, ...
    """

    def __init__(
        self, operation: str, left_node: type[Node], right_node: type[Node]
    ) -> None:
        """
        Contructor from BinOperationsNode

        Args:
            operation (str): Operation to use with left and right node
            left_node (type[Node]): Node to use operation
            right_node (type[Node]): Node to use operation
        """
        super().__init__()
        self.operation: str = operation
        self.left_node: type[Node] = left_node
        self.right_node: type[Node] = right_node

    def __repr__(self) -> str:
        return f"({self.left_node}{self.operation}{self.right_node})"


class UnaryOperationNode(Node):
    """
    Unary node to operations like: -x or +x
    """

    def __init__(self, operation: Literal["+", "-"], node: type[Node]) -> None:
        """
        Contructor from UnaryOperationNode

        Args:
            operation (str): Operation to use with node
            node (type[Node]): Node to use operator
        """
        super().__init__()
        self.operation: Literal["+", "-"] = operation
        self.operand: type[Node] = node

    def __repr__(self) -> str:
        return f"({self.operand}{self.operation})"


# Assignment
class AssignmentNode(Node):
    """
    Node to represent "="
    """

    def __init__(self, variable_name: str, expression: type[Node]) -> None:
        """
        Constructor from AsssignmentNode

        Args:
            variable_name (str): Name of variable
            expression (type[Node]): Node to represent the expression to assign
        """
        super().__init__()
        self.variable_name: str = variable_name
        self.value: type[Node] = expression

    def __repr__(self) -> str:
        return f"{self.variable_name}={self.value}"


# Functions Node
class FunctionNode(Node):
    """
    Node to represent functions like: sqrt, log, sin, cos, ...
    """

    def __init__(self, function_name: str, expression: type[Node]) -> None:
        """
        Constructor from FunctionNode

        Args:
            function_name (str): Name of used function
            expression (type[Node]): Expression to use in function args
        """
        super().__init__()
        self.function_name: str = function_name
        self.args: type[Node] = expression
