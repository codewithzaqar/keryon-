# Kryon

**Version:** v0.0.1  
**Status:** Pre-Alpha  

Kryon is a modern, high-performance systems programming language focused on safety, concurrency, and zero-cost abstractions. It aims to provide memory safety without garbage collection through a strict ownership model, with syntax inspired by Python and Go for readability.

## Features (Current)

- **Static Typing**: Type inference and explicit type annotations.
- **Memory Safety**: Ownership-based memory management (planned).
- **Concurrency**: Native `async`/`await` and `spawn` primitives (planned).
- **Zero-Cost Abstractions**: Compile-time generics (planned).
- **Control Flow**: `if`, `else`, `while`, `for` loops.
- **Data Structures**: Arrays, Structs.
- **Functions**: First-class functions, closures (planned).

## Syntax Examples

### Hello World
```kryon
fn main() {
print("Hello, Kryon!");
}
```

### Variables and Control Flow

```kryon
let x = 10;
mut y = 20;

if (x > 5) {
    print("x is big");
} else {
    print("x is small");
}

for (let i = 0; i < 5; i = i + 1) {
    print(i);
}
```

### Structs
```kryon
struct Person {
    name: str,
    age: i32
};

fn main() {
    let p = Person { name: "Alice", age: 30 };
    print(p.name);
}
```
## Getting Started
### Prerequisites
- Python 3.10+
### Installation
1. Clone the repository:
```bash
git clone https://github.com/codewithzaqar/kryon-.git
cd kryon
```
2. Install in development mode:
```bash
pip install -e .
```
### Running Kryon Code
You can run `.kry` files using the CLI:
```bash
python -m kryon.cli run examples/hello.kry
```
Or tokenize a file to see the lexer output:
```bash
python -m kryon.cli lex examples/hello.kry
```
## Project Structure
```text
kryon/
├── kryon/
│   ├── ast/          # Abstract Syntax Tree definitions
│   ├── lexer/        # Lexer implementation
│   ├── parser/       # Parser implementation
│   ├── interpreter/  # Tree-walking interpreter
│   └── cli.py        # Command-line interface
├── examples/         # Example Kryon programs
└── tests/            # Unit tests
```
## Roadmap
- **Parser:** Complete implementation for all language features.
- **Interpreter:** Full execution support for structs, methods, and modules.
- **Compiler:** Generate bytecode or machine code.
- **Standard Library:** Robust I/O, math, and collections.
- **Concurrency:** Implement `async`/`await` and `spawn`.

## License
MIT License. See `LICENSE` for details.