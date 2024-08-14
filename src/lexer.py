from enum import Enum


class TokenType(Enum):
    FUNCTION = 'FUNCTION'
    LAMBDA = 'LAMBDA'
    ARROW = 'ARROW'
    IDENTIFIER = 'IDENTIFIER'
    COMMA = 'COMMA'
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    LET = 'LET'
    IN = 'IN'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        if result == 'function':
            return Token(TokenType.FUNCTION, result)
        elif result == 'if':
            return Token(TokenType.IF, result)
        elif result == 'then':
            return Token(TokenType.THEN, result)
        elif result == 'else':
            return Token(TokenType.ELSE, result)
        elif result == 'let':
            return Token(TokenType.LET, result)
        elif result == 'in':
            return Token(TokenType.IN, result)
        elif result == 'lambda':
            return Token(TokenType.LAMBDA, result)
        elif result.lower() == 'true':
            return Token(TokenType.BOOLEAN, True)
        elif result.lower() == 'false':
            return Token(TokenType.BOOLEAN, False)
        else:
            return Token(TokenType.IDENTIFIER, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')

            if self.current_char == '%':
                self.advance()
                return Token(TokenType.MODULO, '%')

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            if self.current_char == '=' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '>':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '=>')

            if self.current_char == '<' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LESS_THAN_OR_EQUAL, '<=')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GREATER_THAN_OR_EQUAL, '>=')
                return Token(TokenType.GREATER_THAN, '>')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LESS_THAN_OR_EQUAL, '<=')
                return Token(TokenType.LESS_THAN, '<')

            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(TokenType.AND, '&&')

            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(TokenType.OR, '||')

            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, '!=')
                self.advance()
                return Token(TokenType.NOT, '!')

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQUAL, '==')

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')
            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None)