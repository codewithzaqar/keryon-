import unittest
import sys
import os

# Add parent directory to path to import kryon
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kryon.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    
    def test_basic_arithmetic(self):
        source = "let x = 10 + 20;"
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        # Filter out EOF for easier testing
        tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        # There are 7 tokens: let, x, =, 10, +, 20, ;
        self.assertEqual(len(tokens), 7)
        
        self.assertEqual(tokens[0].type, TokenType.LET)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, "x")
        self.assertEqual(tokens[2].type, TokenType.EQUAL)
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].literal, 10.0)
        self.assertEqual(tokens[4].type, TokenType.PLUS)
        self.assertEqual(tokens[5].type, TokenType.NUMBER)
        self.assertEqual(tokens[5].literal, 20.0)
        self.assertEqual(tokens[6].type, TokenType.SEMICOLON)

    def test_function_definition(self):
        source = """
        fn add(a: i32, b: i32) -> i32 {
            return a + b
        }
        """
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        token_types = [t.type for t in tokens if t.type != TokenType.EOF]
        
        # Check for key structural tokens
        self.assertIn(TokenType.FN, token_types)
        self.assertIn(TokenType.RETURN, token_types)
        self.assertIn(TokenType.LEFT_BRACE, token_types)
        self.assertIn(TokenType.RIGHT_BRACE, token_types)

    def test_string_literal(self):
        source = 'let s = "Hello";'
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        tokens = [t for t in tokens if t.type != TokenType.EOF]
        
        string_token = next(t for t in tokens if t.type == TokenType.STRING)
        self.assertEqual(string_token.literal, "Hello")

if __name__ == '__main__':
    unittest.main()
