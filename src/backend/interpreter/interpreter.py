from src.backend.parser import *
from src.backend.interpreter.values import Number
import math

class Interpreter: 
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_NumberNode(self, node):
        return Number(node.value)

    def visit_BinOperationNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operation_ = node.operation

        if operation_ == '+':
            return Number(left.Value + right.Value)
        
        elif operation_ == '-':
            return Number(left.Value - right.Value)
        
        elif operation_ == '*':
            return Number(left.Value * right.Value)
        
        elif operation_ == '/':
            if right.Value == 0:
                raise ZeroDivisionError("Divisão por zero.")
            return Number(left.Value / right.Value)
        elif operation_ == '^':
            return Number(left.Value ** right.Value)
        
        else:
            raise Exception(f"Operação desconhecida: {operation_}")
    
    def visit_UnaryOperationNode(self, node):
        value = self.visit(node.operand)
        if node.operation == '+':
            return Number(+value.Value)
        elif node.operation =='-':
            return Number(-value.Value)
        else: Exception(f"Operação desconhecida: {node.operaation}")
    
    def visit_FunctionNode(self, node):
        arg = self.visit(node.expression)
        funct_name = node.function_name.lower()

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
        else:
            raise Exception(f"Função desconhecida: {funct_name}")