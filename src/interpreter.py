from parser import BinOp, UnaryOp, Num, Boolean
from lexer import TokenType

class Function:
    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.env = env
class Interpreter:
    def __init__(self):
        self.global_env = {}

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.MULTIPLY:
            return left * right
        elif node.op.type == TokenType.DIVIDE:
            return left // right  # Integer division
        elif node.op.type == TokenType.MODULO:
            return left % right
        elif node.op.type == TokenType.AND:
            return left and right
        elif node.op.type == TokenType.OR:
            return left or right
        elif node.op.type == TokenType.EQUAL:
            return left == right
        elif node.op.type == TokenType.NOT_EQUAL:
            return left != right
        elif node.op.type == TokenType.LESS_THAN:
            return left < right
        elif node.op.type == TokenType.GREATER_THAN:
            return left > right
        elif node.op.type == TokenType.LESS_THAN_OR_EQUAL:
            return left <= right
        elif node.op.type == TokenType.GREATER_THAN_OR_EQUAL:
            return left >= right

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        if node.op.type == TokenType.PLUS:
            return +expr
        elif node.op.type == TokenType.MINUS:
            return -expr
        elif node.op.type == TokenType.NOT:
            return not expr

    def visit_Num(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_FunctionDef(self, node):
        function = Function(node.name, node.params, node.body, self.global_env.copy())
        self.global_env[node.name] = function
        return f"Function '{node.name}' defined"

    def visit_Lambda(self, node):
        return Function(None, node.params, node.body, self.global_env.copy())

    def visit_FunctionCall(self, node):
        function = self.global_env.get(node.name)
        if function is None:
            raise NameError(f"Function '{node.name}' is not defined")

        if len(function.params) != len(node.arguments):
            raise ValueError(f"Expected {len(function.params)} arguments, got {len(node.arguments)}")

        local_env = function.env.copy()
        for param, arg in zip(function.params, node.arguments):
            local_env[param] = self.visit(arg)

        previous_env = self.global_env
        self.global_env = local_env
        result = self.visit(function.body)
        self.global_env = previous_env
        return result

    def visit_Identifier(self, node):
        value = self.global_env.get(node.value)
        if value is None:
            raise NameError(f"Name '{node.value}' is not defined")
        return value
    def interpret(self, tree):
        return self.visit(tree)

