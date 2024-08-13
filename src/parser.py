from lexer import Lexer, TokenType, Token


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Boolean(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class FunctionDef(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


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

    def function_definition(self):
        self.eat(TokenType.FUNCTION)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        params = []
        if self.current_token.type != TokenType.RPAREN:
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
        params = []
        if self.current_token.type != TokenType.ARROW:
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ARROW)
        body = self.expr()
        return Lambda(params, body)

    def function_call(self):
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LPAREN)
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            arguments.append(self.expr())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                arguments.append(self.expr())
        self.eat(TokenType.RPAREN)
        return FunctionCall(name, arguments)

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
            if self.lexer.current_char == '(':
                return self.function_call()
            else:
                self.eat(TokenType.IDENTIFIER)
                return Identifier(token)

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
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

    def expr(self):
        return self.or_expr()

    def parse(self):
        return self.expr()


# Example usage
if __name__ == '__main__':
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.parse()
        print(result)
