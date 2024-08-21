from parser import BinOp, Num, FunctionDef, FunctionCall, Identifier, IfThenElse, LetIn, Boolean, Lambda, UnaryOp
from lexer import TokenType


#Represents a function in the interpreter's environment.
class Function:
    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.env = env

    def __str__(self):
        if self.name:
            return f"<function {self.name}>"
        else:
            return f"<lambda function>"


#Main class responsible for executing the AST.
class Interpreter:

    #Initializes the interpreter with an empty global environment.
    def __init__(self):
        self.global_env = {}

    #A generic method that dispatches to the appropriate visit_*
    # method based on the node type.
    def visit(self, node, env):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node, env)

    #Raises an exception for unsupported node types.
    def generic_visit(self, node, env):
        raise Exception(f'No visit_{type(node).__name__} method')

    #Handles binary operations.
    #Recursively evaluates left and right operands before performing the operation.
    def visit_BinOp(self, node, env):
        left = self.visit(node.left, env)
        right = self.visit(node.right, env)

        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.MULTIPLY:
            return left * right
        elif node.op.type == TokenType.DIVIDE:
            return left // right
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

    #Handles unary operations.
    def visit_UnaryOp(self, node, env):
        expr = self.visit(node.expr, env)
        if node.op.type == TokenType.PLUS:
            return +expr
        elif node.op.type == TokenType.MINUS:
            return -expr
        elif node.op.type == TokenType.NOT:
            return not expr

    #Returns the value of numeric literals.
    def visit_Num(self, node, env):
        return node.value

    #Returns the value of boolean literals.
    def visit_Boolean(self, node, env):
        return node.value

    #Defines a new function in the global environment.
    #Also used for the recursion
    def visit_FunctionDef(self, node, env):
        function = Function(node.name, node.params, node.body, env.copy())
        self.global_env[node.name] = function
        return f"Function '{node.name}' defined"


    #Creates and returns a lambda function.
    def visit_Lambda(self, node, env):
        def lambda_func(*args):
            local_env = env.copy()
            for param, arg in zip(node.params, args):
                local_env[param] = arg
            return self.visit(node.body, local_env)

        return lambda_func

    #Handles function calls, including lambda function calls.
    #Creates a new environment for the function call, evaluates arguments,
    # and executes the function body.
    def visit_FunctionCall(self, node, env):
        if isinstance(node.name, Lambda):
            # It's a lambda function call
            lambda_func = self.visit_Lambda(node.name, env)
            arguments = [self.visit(arg, env) for arg in node.arguments]
            return lambda_func(*arguments)
        else:
            # Regular function call
            function = self.global_env.get(node.name)
            if function is None:
                raise Exception(f"Function '{node.name}' is not defined")
            if len(function.params) != len(node.arguments):
                raise Exception(f"Expected {len(function.params)} arguments, got {len(node.arguments)}")

            # Create a new environment for this function call
            call_env = function.env.copy()

            # Evaluate arguments in the current environment
            evaluated_args = [self.visit(arg, env) for arg in node.arguments]

            # Bind parameters to arguments in the new environment
            for param, arg in zip(function.params, evaluated_args):
                call_env[param] = arg

            # Execute the function body in the new environment
            return self.visit(function.body, call_env)

    #Looks up the value of an identifier in the current environment or global environment.
    def visit_Identifier(self, node, env):
        if node.value in env:
            return env[node.value]
        elif node.value in self.global_env:
            return self.global_env[node.value]
        else:
            raise Exception(f"Variable '{node.value}' is not defined")

    #Evaluates the condition and executes either the 'then' or 'else' branch.
    def visit_IfThenElse(self, node, env):
        if self.visit(node.condition, env):
            return self.visit(node.then_body, env)
        else:
            return self.visit(node.else_body, env)

    #Creates a new environment with the bound variable and evaluates the body in this new environment.
    def visit_LetIn(self, node, env):
        var_value = self.visit(node.var_value, env)
        new_env = env.copy()
        new_env[node.var_name] = var_value
        return self.visit(node.body, new_env)

    #The main entry point for interpretation.
    # Starts the interpretation process with the global environment.
    def interpret(self, tree):
        return self.visit(tree, self.global_env)
