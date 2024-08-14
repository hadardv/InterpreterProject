from lexer import TokenType, Token

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class FunctionDef(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Boolean(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class FunctionCall(AST):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class Lambda(AST):
    def __init__(self, params, body):
        self.params = params
        self.body = body

class Identifier(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class IfThenElse(AST):
    def __init__(self, condition, then_body, else_body):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class LetIn(AST):
    def __init__(self, var_name, var_value, body):
        self.var_name = var_name
        self.var_value = var_value
        self.body = body

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.BOOLEAN:
            self.eat(TokenType.BOOLEAN)
            return Boolean(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            if self.current_token.type == TokenType.LAMBDA:
                node = self.lambda_expression()
                self.eat(TokenType.RPAREN)
                if self.current_token.type == TokenType.LPAREN:
                    return self.function_call(node)
                return node
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.NOT:
            self.eat(TokenType.NOT)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.FUNCTION:
            return self.function_definition()
        elif token.type == TokenType.LAMBDA:
            return self.lambda_expression()
        elif token.type == TokenType.IDENTIFIER:
            return self.function_call_or_variable()
        elif token.type == TokenType.IF:
            return self.if_statement()
        elif token.type == TokenType.LET:
            return self.let_in_statement()
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE,TokenType.MODULO):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            elif token.type == TokenType.MODULO:
                self.eat(TokenType.MODULO)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def arithmetic_expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def comparison_expr(self):
        node = self.arithmetic_expr()

        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL,
                                          TokenType.LESS_THAN, TokenType.GREATER_THAN,
                                          TokenType.LESS_THAN_OR_EQUAL, TokenType.GREATER_THAN_OR_EQUAL):
            token = self.current_token
            self.eat(self.current_token.type)
            node = BinOp(left=node, op=token, right=self.arithmetic_expr())

        return node

    def and_expr(self):
        node = self.comparison_expr()

        while self.current_token.type == TokenType.AND:
            token = self.current_token
            self.eat(TokenType.AND)
            node = BinOp(left=node, op=token, right=self.comparison_expr())

        return node

    def or_expr(self):
        node = self.and_expr()

        while self.current_token.type == TokenType.OR:
            token = self.current_token
            self.eat(TokenType.OR)
            node = BinOp(left=node, op=token, right=self.and_expr())

        return node

    # def expr(self):
    #     node = self.arithmetic_expr()
    #
    #     while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL,
    #                                       TokenType.LESS_THAN, TokenType.GREATER_THAN,
    #                                       TokenType.LESS_THAN_OR_EQUAL, TokenType.GREATER_THAN_OR_EQUAL):
    #         token = self.current_token
    #         self.eat(self.current_token.type)
    #         node = BinOp(left=node, op=token, right=self.arithmetic_expr())
    #
    #     return node

    def expr(self):
        return self.or_expr()

    def function_definition(self):
        self.eat(TokenType.FUNCTION)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        params = []
        if self.current_token.type == TokenType.IDENTIFIER:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.ARROW)
        body = self.expr()
        return FunctionDef(name, params, body)

    def lambda_expression(self):
        self.eat(TokenType.LAMBDA)
        param = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ARROW)
        body = self.expr()
        lambda_node = Lambda([param], body)

        # Check if the lambda is immediately called
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            argument = self.expr()
            self.eat(TokenType.RPAREN)
            return FunctionCall(lambda_node, [argument])

        return lambda_node

    def function_call(self, callable_expr):
        self.eat(TokenType.LPAREN)
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.expr())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expr())
        self.eat(TokenType.RPAREN)
        return FunctionCall(callable_expr, arguments)

    def function_call_or_variable(self):
        token = self.current_token
        name = token.value
        self.eat(TokenType.IDENTIFIER)
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            arguments = []
            if self.current_token.type != TokenType.RPAREN:
                arguments.append(self.expr())
            self.eat(TokenType.RPAREN)
            return FunctionCall(name, arguments)
        return Identifier(token)

    def if_statement(self):
        self.eat(TokenType.IF)
        condition = self.expr()
        self.eat(TokenType.THEN)
        then_body = self.expr()
        self.eat(TokenType.ELSE)
        else_body = self.expr()
        return IfThenElse(condition, then_body, else_body)

    def let_in_statement(self):
        self.eat(TokenType.LET)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ARROW)
        var_value = self.expr()
        self.eat(TokenType.IN)
        body = self.expr()
        return LetIn(var_name, var_value, body)

    def parse(self):
        if self.current_token.type == TokenType.FUNCTION:
            return self.function_definition()
        return self.expr()