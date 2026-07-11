import sys
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .ast import nodes as ast  # <-- ADDED IMPORT

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m kryon <command> <file>")
        print("Commands:")
        print("  lex     Tokenize the file and print tokens")
        print("  run     Parse and execute the file")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    with open(filename, 'r') as f:
        source = f.read()

    if command == "lex":
        run_lexer(source, filename)
    elif command == "run":
        run_interpreter(source, filename)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

def run_lexer(source: str, filename: str):
    print(f"--- Lexing {filename} ---")
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    for token in tokens:
        if token.type.name == "EOF": continue
        print(token)
    print("--- Lexing Complete ---")

def run_interpreter(source: str, filename: str):
    print(f"--- Running {filename} ---")
    
    # 1. Lex
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    # 2. Parse
    parser = Parser(tokens)
    statements = parser.parse()
    
    if parser.errors:
        print("--- Parse Errors ---")
        for error in parser.errors:
            print(error)
        return

    # 3. Interpret
    try:
        interpreter = Interpreter()
        interpreter.interpret(statements)
        
        # 4. Auto-run main() if it exists
        if "main" in interpreter.environment.values:
            main_func = interpreter.environment.get("main")
            if isinstance(main_func, ast.FunctionDecl):
                interpreter.execute_function(main_func, [])
                
        print("--- Execution Complete ---")
    except Exception as e:
        print(f"Interpreter Error: {e}")

if __name__ == "__main__":
    main()
