from lexer import Lexer, TokenType
from parser import Parser, BinOp, Num, FunctionDef, FunctionCall, Identifier, IfThenElse, LetIn, Boolean, Lambda, \
    UnaryOp
from interpreter import Interpreter
import sys


#This function recursively prints the Abstract Syntax Tree (AST).
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
        if isinstance(node.name, Lambda):
            print(f"{indent}  Name (Lambda):")
            print_ast(node.name, level + 2)
        elif isinstance(node.name, Identifier):
            print(f"{indent}  Name: {node.name.value}")
        else:
            print(f"{indent}  Name: {node.name}")
        print(f"{indent}  Arguments:")
        for arg in node.arguments:
            print_ast(arg, level + 2)
    elif isinstance(node, Identifier):
        print(f"{indent}Identifier: {node.value}")
    elif isinstance(node, IfThenElse):
        print(f"{indent}IfThenElse:")
        print(f"{indent}  Condition:")
        print_ast(node.condition, level + 2)
        print(f"{indent}  Then:")
        print_ast(node.then_body, level + 2)
        print(f"{indent}  Else:")
        print_ast(node.else_body, level + 2)
    elif isinstance(node, LetIn):
        print(f"{indent}LetIn:")
        print(f"{indent}  Variable: {node.var_name}")
        print(f"{indent}  Value:")
        print_ast(node.var_value, level + 2)
        print(f"{indent}  In:")
        print_ast(node.body, level + 2)
    else:
        print(f"{indent}Unknown node type: {type(node)}")


#This function tokenizes the input text and prints each token.
def print_tokens(text):
    lexer = Lexer(text)
    while True:
        token = lexer.get_next_token()
        print(token)
        if token.type == TokenType.EOF:
            break


#This is the core function that processes user input.
#It tokenizes the input, parses it into an AST, and interprets the result.
#If debug is True, it prints the tokens and AST before interpreting.
def execute_command(interpreter, text, debug=False):
    try:
        if debug:
            print("Tokens:")
            print_tokens(text)

        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()

        if debug:
            print("\nAbstract Syntax Tree:")
            print_ast(tree)

        result = interpreter.interpret(tree)
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


#This function implements an interactive Read-Eval-Print Loop (REPL).
def interactive_mode(interpreter):
    while True:
        try:
            text = input('Functastic> ')
            if text.lower() == 'exit':
                break
            if text.lower() == 'debug':
                debug_text = input('debug> ')
                execute_command(interpreter, debug_text, debug=True)
            else:
                execute_command(interpreter, text)
            print()
        except EOFError:
            break


#This function reads a program from a file and executes it.
#It splits the program into commands (separated by semicolons) and executes each command.
def program_mode(interpreter, filename):
    with open(filename, 'r') as file:
        program = file.read()

    commands = program.split(';')
    for command in commands:
        command = command.strip()  #method used to remove leading and trailing whitespace from a string.
        if command:
            print(f"Executing: {command}")
            execute_command(interpreter, command)
            print()


#This is the entry point of the script.
def main():
    interpreter = Interpreter()

    if len(sys.argv) > 1:
        # Program mode
        program_mode(interpreter, sys.argv[1])
    else:
        # Interactive mode
        print("Interactive mode. Type 'exit' to quit. Type 'debug' to enter debug mode.")
        interactive_mode(interpreter)


if __name__ == '__main__':
    main()
