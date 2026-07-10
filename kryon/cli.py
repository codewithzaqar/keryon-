import sys
import os
from .lexer import Lexer

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m kryon <command> <file>")
        print("Commands:")
        print("  lex     Tokenize the file and print tokens")
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
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

def run_lexer(source: str, filename: str):
    print(f"--- Lexing {filename} ---")
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()
    
    for token in tokens:
        if token.type.name == "EOF":
            continue
        print(token)
    
    print("--- Lexing Complete ---")

if __name__ == "__main__":
    main()
