from src.backend.parser import *
from values import Number

class Interpreter: 
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    def visit_NumberNode(self, node):
        return Number(node.value)

    def visit_BinOperantionsNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)
        operation_ = node.operation

        if operation_ == '+':
            return Number(left.Value + right.Value)
        
        if operation_ == '-':
            return Number(left.Value - right.Value)
        
        if operation_ == '*':
            return Number(left.Value * right.Value)
        
        if operation_ == '/':
            if right.Value == 0:
                raise ZeroDivisionError("Divisão por zero.")
            return Number(left.Value - right.Value)
        if operation_ == '^':
            return Number(left.Value ** right.Value)
        
        else:
            raise Exception(f"Operação desconhecida: {operation_}")
        