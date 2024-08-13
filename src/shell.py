from lexer import Lexer, TokenType
from parser import Parser, BinOp, UnaryOp, Num, Boolean, FunctionDef, Lambda, FunctionCall, Identifier
from interpreter import Interpreter


def print_ast(node, level=0):
    indent = '  ' * level
    if isinstance(node, BinOp):
        print(f"{indent}BinOp:")
        print(f"{indent}  Left:")
        print_ast(node.left, level + 2)
        print(f"{indent}  Op: {node.op.type.name}")
        print(f"{indent}  Right:")
        print_ast(node.right, level + 2)
    elif isinstance(node, UnaryOp):
        print(f"{indent}UnaryOp:")
        print(f"{indent}  Op: {node.op.type.name}")
        print(f"{indent}  Expr:")
        print_ast(node.expr, level + 2)
    elif isinstance(node, Num):
        print(f"{indent}Num: {node.value}")
    elif isinstance(node, Boolean):
        print(f"{indent}Boolean: {node.value}")
    elif isinstance(node, FunctionDef):
        print(f"{indent}FunctionDef:")
        print(f"{indent}  Name: {node.name}")
        print(f"{indent}  Params: {', '.join(node.params)}")
        print(f"{indent}  Body:")
        print_ast(node.body, level + 2)
    elif isinstance(node, Lambda):
        print(f"{indent}Lambda:")
        print(f"{indent}  Params: {', '.join(node.params)}")
        print(f"{indent}  Body:")
        print_ast(node.body, level + 2)
    elif isinstance(node, FunctionCall):
        print(f"{indent}FunctionCall:")
        print(f"{indent}  Name: {node.name}")
        print(f"{indent}  Arguments:")
        for arg in node.arguments:
            print_ast(arg, level + 2)
    elif isinstance(node, Identifier):
        print(f"{indent}Identifier: {node.value}")
    else:
        print(f"{indent}Unknown node type: {type(node)}")


def main():
    print("Simple Interpreter")
    print("Type 'exit' to quit")

    interpreter = Interpreter()

    while True:
        try:
            text = input('> ')
            if text.lower() == 'exit':
                print("Goodbye!")
                break

            lexer = Lexer(text)
            parser = Parser(lexer)

            print("Tokens:")
            lexer_copy = Lexer(text)  # Create a new lexer instance for token printing
            while True:
                token = lexer_copy.get_next_token()
                print(token)
                if token.type == TokenType.EOF:
                    break

            print("\nAbstract Syntax Tree:")
            ast = parser.parse()
            print_ast(ast)

            print("\nResult:")
            result = interpreter.interpret(ast)
            print(result)
            print()

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()