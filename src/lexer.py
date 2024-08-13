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
    LPAREN = 'LPAREN'  # New token type for left parenthesis
    RPAREN = 'RPAREN'  # New token type for right parenthesis
    EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return (f'Token({self.type}, {self.value})')

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result.lower() == 'function':  # Change this line
            return Token(TokenType.FUNCTION, result)
        elif result.lower() == 'lambda':  # Add this line for consistency
            return Token(TokenType.LAMBDA, result)
        else:
            return Token(TokenType.IDENTIFIER, result)

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
        if self.current_char == '-':
            result += self.current_char
            self.advance()
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '-':
                return Token(TokenType.INTEGER, self.integer())

            if self.current_char.lower() == 't':
                self.advance()
                if self.text[self.pos:self.pos+3].lower() == 'rue':
                    self.pos += 3
                    self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
                    return Token(TokenType.BOOLEAN, True)

            if self.current_char.lower() == 'f':
                self.advance()
                if self.text[self.pos:self.pos+4].lower() == 'alse':
                    self.pos += 4
                    self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
                    return Token(TokenType.BOOLEAN, False)

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

            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.GREATER_THAN_OR_EQUAL, '>=')
                self.advance()
                return Token(TokenType.GREATER_THAN, '>')

            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LESS_THAN_OR_EQUAL, '<=')
                self.advance()
                return Token(TokenType.LESS_THAN, '<')

            if self.current_char == '(':  # New condition for left parenthesis
                self.advance()
                return Token(TokenType.LPAREN, '(')

            if self.current_char == ')':  # New condition for right parenthesis
                self.advance()
                return Token(TokenType.RPAREN, ')')
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')

            if self.current_char == '=' and self.peek() == '>':
                self.advance()
                self.advance()
                return Token(TokenType.ARROW, '=>')

            raise Exception(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None)